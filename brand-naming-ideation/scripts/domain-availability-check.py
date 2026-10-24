#!/usr/bin/env python3
"""
Parallel domain-availability checker for brand name candidates.

USAGE (from execute_code or terminal):
    from hermes_tools import ...  # then paste this file, or:
    python3 scripts/domain-availability-check.py name1 name2 name3 ...

WHY THIS EXISTS:
  The default `whois <domain>` on macOS hits the IANA WHOIS server and returns
  the generic registry record (e.g. the COM registry itself), NOT the registrar
  record for the specific domain. Every domain — taken or free — looks identical
  ("refer: whois.verisign-grs.com / domain: COM"), so naive availability
  classification produces 100% false-TAKEN results.

  The fix: query the authoritative registry whois servers directly with
  `whois -h <server> <domain>`. Those servers return real availability markers
  ("No match for domain ...") or full registration records.

  This script does that, in parallel (ThreadPoolExecutor), because serial whois
  over 20+ domain*TLD combinations takes minutes and frequently times out.

WHAT IT CHECKS:
  .com  -> whois.verisign-grs.com   (marker: "no match for domain")
  .io   -> whois.nic.io             (marker: "domain not found" / "is free")
  .ai   -> whois.nic.ai             (marker: "domain not found" / "not found")

NOTE ON .labs.com AND OTHER SUBDOMAINS:
  whois CANNOT check arbitrary subdomains like `foo.labs.com` — those are not
  separately registered and whois returns the parent (labs.com) registry record.
  Use .com / .io / .ai as your variants, NOT `<name>.labs.com`.

NOTE ON FLAKINESS:
  .io and .ai whois occasionally return ambiguous output (no clear available
  marker, no registration data) = UNKNOWN. Re-query to resolve; do not assume
  UNKNOWN means available or taken.
"""
import subprocess, sys, concurrent.futures

SERVERS = {
    "com": "whois.verisign-grs.com",
    "io":  "whois.nic.io",
    "ai":  "whois.nic.ai",
}

AVAIL_MARKERS = {
    "com": ["no match for domain"],
    "io":  ["domain not found", "is free", "is available"],
    "ai":  ["domain not found", "not found", "no entries found",
            "status: available", "no data found"],
}
TAKEN_MARKERS = ["registry domain id", "domain name:", "creation date",
                 "registrar:", "registry expiry", "name server", "updated date"]

def whois_one(name_tld):
    name, tld = name_tld
    domain = f"{name}.{tld}"
    try:
        r = subprocess.run(
            ["whois", "-h", SERVERS[tld], domain],
            capture_output=True, text=True, timeout=12
        )
        return domain, (r.stdout + r.stderr).lower()
    except Exception as e:
        return domain, f"err {e}".lower()

def whois_one_retry(name_tld, max_attempts=3):
    """Query whois with retry on UNKNOWN (rate-limited / empty) responses.
    Verisign throttles under parallel load — a batch of 20+ lookups often
    returns short empty responses mid-batch that classify as UNKNOWN.
    Retry with a small backoff until we get a definitive answer or exhaust attempts.
    """
    import time
    domain, text = whois_one(name_tld)
    _, tld = name_tld
    for attempt in range(max_attempts - 1):
        if classify(text, tld) != "UNKNOWN":
            break
        time.sleep(1.5 * (attempt + 1))  # 1.5s, then 3s
        domain, text = whois_one(name_tld)
    return domain, text

def classify(text, tld):
    t = text.lower()
    if t.startswith("err"):
        return "ERROR"
    # RATE-LIMIT / EMPTY-RESPONSE GUARD (learned 2026-08-11):
    # Verisign and nic.io throttle under load, returning a short response with
    # NO registration data AND NO availability marker. Naive inline checks that
    # treat "not taken => available" FALSELY classify these as AVAILABLE.
    # The script already requires an explicit marker, but a very short response
    # is never a reliable signal either way — force it to UNKNOWN so the caller
    # retries instead of trusting it.
    if len(t.strip()) < 250:
        return "UNKNOWN"
    if any(m in t for m in AVAIL_MARKERS.get(tld, [])):
        return "AVAILABLE"
    if any(m in t for m in TAKEN_MARKERS):
        return "TAKEN"
    return "UNKNOWN"

def check(names, tlds=("com", "io", "ai"), max_workers=8):
    """Check domain availability. max_workers capped at 8 (not 24) because
    Verisign throttles aggressively under high parallelism, returning short
    empty responses that force retries and slow the whole batch down.
    8 workers + retry is faster end-to-end than 24 workers + constant retry.
    UNKNOWNs are retried inside whois_one_retry before being reported."""
    queries = [(n, tld) for n in names for tld in tlds]
    raw = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(whois_one_retry, q): q for q in queries}
        for fut in concurrent.futures.as_completed(futs):
            domain, text = fut.result()
            raw[domain] = text

    results = {}
    for name in names:
        row = {tld: classify(raw.get(f"{name}.{tld}", ""), tld) for tld in tlds}
        results[name] = row
        avails = [t for t, s in row.items() if s == "AVAILABLE"]
        unknowns = [t for t, s in row.items() if s == "UNKNOWN"]
        suffix = ""
        if avails:
            suffix += f"  <<< AVAILABLE: {avails}"
        if unknowns:
            suffix += f"  !!! UNVERIFIED (rate-limited): {unknowns} — re-run or check manually"
        print(f"{name:<14} " + "  ".join(f"{t}={row[t]:<9}" for t in tlds) + suffix)
    return results

if __name__ == "__main__":
    names = sys.argv[1:]
    if not names:
        print("usage: domain-availability-check.py name1 name2 ...")
        sys.exit(1)
    check(names)
