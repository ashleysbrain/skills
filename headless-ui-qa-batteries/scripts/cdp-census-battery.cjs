// CDP census battery: page-by-page view + wiring sweep for a single-page app.
// Usage: NODE_PATH=/tmp/rs-qa/node_modules node rs-battery.cjs
// Expects chrome already running:
//   '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
//     --headless=new --remote-debugging-port=9333 --user-data-dir=/tmp/rs-qa-profile \
//     --disable-gpu about:blank
// Token (if app needs auth): read from env WS_TOKEN, inject via localStorage best-effort.

const CDP = require('chrome-remote-interface');
const fs = require('fs');

const APP_URL = process.env.APP_URL || 'http://127.0.0.1:port/';
const VIEWS = (process.env.VIEWS || 'dashboard,calendar,activity,research,discover,build,library,drafts,compose,brainstorm,courses,panel,revision,authorship,publish,connections,skeleton,focus').split(',');
const OUT = process.env.OUT || '/tmp/rs-census.json';

(async () => {
  const client = await CDP({port: 9333});
  const {Page, Runtime, Console, Network} = client;
  await Page.enable(); await Runtime.enable(); await Console.enable(); await Network.enable();
  const errors = [];
  Console.messageAdded(({type, text}) => { if (type === 'error') errors.push(text.slice(0, 160)); });
  const failedUrls = [];
  Network.responseReceived(({response}) => { if (response.status >= 400) failedUrls.push(response.status + ' ' + response.url.slice(0, 120)); });

  await Page.navigate({url: APP_URL});
  await Page.loadEventFired();
  await new Promise(r => setTimeout(r, 2500));

  const ev = async (e) => {
    const res = await Runtime.evaluate({expression: e, returnByValue: true, awaitPromise: true});
    if (res.exceptionDetails) return {probeErr: String(res.exceptionDetails).slice(0, 120)};
    return res.result.value;
  };

  const out = {ts: new Date().toISOString(), views: {}, errors, failedUrls};
  for (const v of VIEWS) {
    // RULE 6: eval('typeof '+name) in page scope — NEVER window[name] (const/let fns invisible)
    // RULE 7: split multi-statement onclick on ';' and take the LAST segment
    const r = await ev(`(() => { try {
      const el = document.getElementById('view-${v}') || document.querySelector('[data-view="${v}"]');
      if (!el) return {missing: true};
      const vis = el.offsetWidth > 0 || el.offsetHeight > 0;
      const btns = [...el.querySelectorAll('button')];
      let dead = -1;
      try {
        dead = btns.filter(b => {
          const h = b.getAttribute('onclick'); if (!h) return false;
          const last = h.split(';').map(s => s.trim()).filter(Boolean).pop() || '';
          const name = last.split('(')[0].replace(/['"\\s]/g, '');
          try { return name && eval('typeof ' + name) === 'undefined'; } catch (e) { return false; }
        }).length;
      } catch (e) {}
      return { present: true, visibleNow: vis, buttons: btns.length,
               visibleButtons: btns.filter(b => b.offsetWidth > 0).length,
               deadOnclick: dead,
               inputs: el.querySelectorAll('input,textarea,select').length,
               textSample: (el.innerText || '').replace(/\\s+/g, ' ').slice(0, 90) };
    } catch (e) { return {probeErr: String(e).slice(0, 120)}; } })()`);
    out.views[v] = r;
    if (r && r.present && !r.visibleNow) {
      await ev(`(() => { const b = document.querySelector('[onclick*="${v}"],[data-view="${v}"]'); if (b) b.click(); return 1; })()`);
      await new Promise(r2 => setTimeout(r2, 900));
      out.views[v].afterNav = await ev(`(() => { const el = document.getElementById('view-${v}'); return el ? el.offsetWidth > 0 : false; })()`);
    }
  }
  fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
  const summary = {};
  for (const [k, v] of Object.entries(out.views)) summary[k] = v.missing ? 'MISSING' : (v.visibleNow || v.afterNav ? `ok(btn:${v.visibleButtons ?? v.buttons},in:${v.inputs},dead:${v.deadOnclick})` : 'NOT-VISIBLE');
  console.log(JSON.stringify({summary, consoleErrors: errors.slice(0, 8), httpFails: failedUrls.slice(0, 8)}, null, 1));
  await client.close();
})().catch(e => { console.error('BATTERY-FAIL', e.message); process.exit(1); });
