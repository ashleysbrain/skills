from __future__ import annotations

from datetime import datetime
from pathlib import Path
from string import Template
import argparse
import hashlib
import re

from weasyprint import HTML

"""Render the 8D Pattern Awareness user-facing report from editable markdown.

Usage:
  python render_user_facing_report.py \
    --source /path/to/user-facing-report-example.md \
    --output /tmp/report.pdf

The markdown format is intentionally simple:
- one top-level title line starting with '# '
- section headings starting with '## '
- regular paragraphs and '-' bullet lines under each section

This renderer preserves the editable source-of-truth and avoids flattened/raster-only PDFs.
"""

PAGE_SIZE = "letter"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def md_inline(text: str) -> str:
    text = esc(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text


def parse_markdown(source: Path):
    raw_lines = source.read_text(encoding="utf-8").splitlines()
    sections = []
    current = None
    title = None
    for line in raw_lines:
        if line.startswith("# ") and title is None:
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            current = {"title": line[3:].strip(), "items": []}
            sections.append(current)
        elif current is not None and line.strip():
            current["items"].append(line.rstrip())
    if title is None:
        title = source.stem.replace("-", " ").title()
    return title, sections


def section_lookup(sections, title: str) -> str:
    for sec in sections:
        if sec["title"].strip().lower() == title.strip().lower():
            return "\n".join(sec["items"])
    return ""


def mood_from_text(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["low", "deplet", "hard", "strain", "drag", "tired", "heavy", "stuck", "friction"]):
        return "recovery"
    if any(k in t for k in ["better", "improv", "up", "lighter", "steady", "clearer", "traction", "momentum"]):
        return "momentum"
    return "balanced"


def build_moment_quote(sections, stamp: str) -> dict[str, str]:
    overview = section_lookup(sections, "Overview")
    psych = section_lookup(sections, "Psychological read")
    seed = f"{overview}|{psych}|{stamp}".encode("utf-8")
    h = int(hashlib.sha256(seed).hexdigest(), 16)

    # Factual quote bank only: exact text with stable attribution.
    quote_bank = {
        "recovery": [
            {
                "text": "The impediment to action advances action. What stands in the way becomes the way.",
                "author": "Marcus Aurelius",
                "source": "Meditations 5.20",
            },
            {
                "text": "You have power over your mind — not outside events. Realize this, and you will find strength.",
                "author": "Marcus Aurelius",
                "source": "Meditations 7.8",
            },
        ],
        "momentum": [
            {
                "text": "Do what you can, with what you have, where you are.",
                "author": "Theodore Roosevelt",
                "source": "widely cited quotation",
            },
            {
                "text": "The best way out is always through.",
                "author": "Robert Frost",
                "source": "A Further Range",
            },
        ],
        "balanced": [
            {
                "text": "Waste no more time arguing about what a good man should be. Be one.",
                "author": "Marcus Aurelius",
                "source": "Meditations 10.16",
            },
            {
                "text": "If it is not right, do not do it; if it is not true, do not say it.",
                "author": "Marcus Aurelius",
                "source": "Meditations 12.17",
            },
        ],
    }

    mood = mood_from_text(overview + " " + psych)
    bank = quote_bank[mood]
    return bank[h % len(bank)]


DIMENSION_ORDER = ["PSY", "PHY", "ENV", "SOC", "SPI", "INT", "VOC", "FIN"]
DIMENSION_LABELS = {
    "PSY": "Psychology",
    "PHY": "Physical recovery",
    "ENV": "Environment",
    "SOC": "Social connection",
    "SPI": "Purpose / meaning",
    "INT": "Intellectual load",
    "VOC": "Momentum / follow-through",
    "FIN": "Financial load",
}


def extract_signal_map(sections) -> list[tuple[str, str]]:
    sec = find_section(sections, "8D signals")
    if not sec:
        return []

    signals = []
    for raw in sec["items"]:
        line = raw.lstrip("- ").strip()
        m = re.match(r"(?:\*\*)?([A-Z]{3})(?:\*\*)?:\s*(.+)$", line)
        if m:
            signals.append((m.group(1), m.group(2).strip()))
    return signals


def recommendation_mode(signal_text: str) -> str:
    t = signal_text.lower()
    recovery_markers = ["low", "harder", "drag", "strain", "depleted", "overload", "friction", "less available", "stuck", "heavy"]
    momentum_markers = ["easier", "returning", "usable again", "more settled", "better", "traction", "available", "cleanly", "steady"]
    if any(k in t for k in recovery_markers):
        return "recovery"
    if any(k in t for k in momentum_markers):
        return "momentum"
    return "steady"


def specialist_read_for_dimension(dim: str, signal_text: str) -> str:
    mode = recommendation_mode(signal_text)
    signal = signal_text.lower()

    if dim == "PSY":
        if "irrit" in signal or "strain" in signal or "frustr" in signal:
            return "The emotional lane is carrying strain, so the next move should lower pressure before it asks for more regulation."
        if mode == "momentum":
            return "The emotional lane is steady enough to protect; keep it calm and do not over-amplify the day."
        return "This is mostly a regulation problem, not a character problem, so keep the emotional ask small and clean."

    if dim == "PHY":
        if any(k in signal for k in ["sleep", "recover", "energy", "tired", "deplet", "heavy"]):
            return "Physical recovery looks like the limiter, so refill first and treat output as secondary."
        if mode == "momentum":
            return "The body has enough traction to keep moving, but the gains only stick if you pace the load."
        return "Treat the body like the base layer and keep it supported enough to avoid a later dip."

    if dim == "ENV":
        if any(k in signal for k in ["clutter", "interrupt", "friction", "drag", "setup"]):
            return "The setup itself is costing energy, so the specialist move is to remove friction before adding effort."
        if mode == "momentum":
            return "The environment is already helping, so preserve the clean path and do not let noise creep back in."
        return "The environment should be made easier to re-enter, not harder to maintain."

    if dim == "SOC":
        if any(k in signal for k in ["alone", "support", "people", "contact", "interaction"]):
            return "The social lane needs one precise connection, not a broad social fix."
        if mode == "momentum":
            return "Use the steadier social field to keep the right relationships warm without overcommitting."
        return "Keep social demands specific and bounded so they do not drain the rest of the day."

    if dim == "SPI":
        if any(k in signal for k in ["meaning", "purpose", "value", "why"]):
            return "Purpose is the stabilizer here, so one meaningful move should anchor the rest of the day."
        if mode == "momentum":
            return "The meaning layer is available, so let it guide the next action without turning into a philosophy project."
        return "Keep the purpose signal simple: one small action that still feels aligned."

    if dim == "INT":
        if any(k in signal for k in ["focus", "read", "analysis", "thinking", "overload", "mental"]):
            return "Cognitive load is the issue, so the specialist move is to reduce switches and narrow the thinking lane."
        if mode == "momentum":
            return "Focus is available enough to use well, so spend it on the hardest thinking first."
        return "The mind needs a single target and fewer open loops so it can stay organized."

    if dim == "VOC":
        if any(k in signal for k in ["initiat", "follow", "momentum", "completion", "procrast", "output"]):
            return "Execution is the lever here, so shrink the first step and protect the finish."
        if mode == "momentum":
            return "The work engine is already moving, so convert it into one clean completed win."
        return "The next move should be obvious to start and simple enough to finish cleanly."

    if dim == "FIN":
        if any(k in signal for k in ["money", "bill", "budget", "spend", "account"]):
            return "Money needs visibility, not drama, so make the financial lane legible and bounded."
        if mode == "momentum":
            return "Use the steadier day to keep financial choices intentional and quiet."
        return "A quick visibility check is enough; do not let the financial lane become a source of extra noise."

    return "Use the current signal as the guide and make the next step small enough to execute cleanly."


def recommendations_for_dimension(dim: str, signal_text: str) -> list[str]:
    mode = recommendation_mode(signal_text)
    signal = signal_text.lower()
    summary = specialist_read_for_dimension(dim, signal_text)

    if dim == "PSY":
        if mode == "recovery":
            return [
                summary,
                "Name the emotional weather in one sentence before the next task.",
                "Take a short reset that lowers pressure rather than adding more thought.",
            ]
        if mode == "momentum":
            return [
                summary,
                "Use the calmer state to make one clean decision instead of three.",
                "Protect the regulation you already have by avoiding unnecessary friction.",
            ]
        return [
            summary,
            "Check in with the emotional state before you switch tasks.",
            "Do one small regulating action before asking for more output.",
        ]

    if dim == "PHY":
        if mode == "recovery":
            return [
                summary,
                "Hydrate now and add a quick protein or mineral reset.",
                "Protect tonight’s sleep window as a hard recovery asset.",
            ]
        if mode == "momentum":
            return [
                summary,
                "Keep meals and hydration steady so the traction holds.",
                "Do not spend the better energy all at once; pace it across the day.",
            ]
        return [
            summary,
            "Keep hydration and food rhythm steady enough to avoid a dip later.",
            "Add a short movement break if the body starts to go flat.",
        ]

    if dim == "ENV":
        if mode == "recovery":
            return [
                summary,
                "Clear one visible surface or clutter point in under 3 minutes.",
                "Silence one alert, tab, or notification source that is adding drag.",
            ]
        if mode == "momentum":
            return [
                summary,
                "Keep distractions quiet so the better flow does not splinter.",
                "Pre-stage the next step and let the environment protect your pace.",
            ]
        return [
            summary,
            "Reduce one small source of visual or digital noise.",
            "Keep the next task visible so the environment does part of the work.",
        ]

    if dim == "SOC":
        if mode == "recovery":
            return [
                summary,
                "Send one honest check-in to the right person.",
                "Ask for one specific kind of support instead of a vague ask.",
            ]
        if mode == "momentum":
            return [
                summary,
                "Keep one supportive connection warm without overcommitting the day.",
                "Use the steadier state to make one clean social repair or update.",
            ]
        return [
            summary,
            "Choose the smallest useful human contact instead of letting isolation stack up.",
            "Ask directly for the kind of support that would actually help.",
        ]

    if dim == "SPI":
        if mode == "recovery":
            return [
                summary,
                "Reconnect with one value and let it set the tone for the next action.",
                "Do one small action that feels meaningful, not just productive.",
            ]
        if mode == "momentum":
            return [
                summary,
                "Use the clearer state to align the next action with a real value.",
                "Let one purposeful move anchor the rest of the day.",
            ]
        return [
            summary,
            "Pause long enough to check whether the day still points where you want it to point.",
            "Pick one action that would feel congruent even if nobody saw it.",
        ]

    if dim == "INT":
        if mode == "recovery":
            return [
                summary,
                "Single-task for 15 minutes; close the other loops first.",
                "Write the next three steps before you begin so the brain stops searching.",
            ]
        if mode == "momentum":
            return [
                summary,
                "Use the clearer focus on the hardest thinking first.",
                "Capture the next three moves and then execute without reopening the loop.",
            ]
        return [
            summary,
            "Give the mind one target at a time and keep the context switches low.",
            "Write the next move down so attention does not scatter.",
        ]

    if dim == "VOC":
        if mode == "recovery":
            return [
                summary,
                "Use a short timer so initiation does not become a negotiation.",
                "Finish one small thing completely before opening the next loop.",
            ]
        if mode == "momentum":
            return [
                summary,
                "Let the momentum carry a single important task across the finish line.",
                "Do not scatter the better start across too many open loops.",
            ]
        return [
            summary,
            "Use a timer to keep the first step small enough to execute.",
            "Close one loop before opening another so momentum stays visible.",
        ]

    if dim == "FIN":
        if mode == "recovery":
            return [
                summary,
                "Avoid one impulse spend or unplanned commitment today.",
                "Set one tiny financial guardrail for the next 24 hours.",
            ]
        if mode == "momentum":
            return [
                summary,
                "Review one account or budget line while your attention is still clear.",
                "Do not turn a good day into a new obligation by accident.",
            ]
        return [
            summary,
            "Avoid any purchase or promise that is driven by pressure rather than choice.",
            "Do one quick visibility check on the financial side of the day.",
        ]

    return [
        summary,
        "Use the specialist read to reduce friction rather than add more complexity.",
        "Protect the strongest part of the day and do not overbuild the rest.",
    ]


def build_quick_wins_html(sections) -> str:
    signals = extract_signal_map(sections)
    if not signals:
        signals = [("PSY", "no clear signal"), ("VOC", "no clear signal")]

    cards = []
    seen = set()
    for dim, signal_text in signals:
        if dim in seen:
            continue
        seen.add(dim)
        items = "".join(f"<li>{md_inline(item)}</li>" for item in recommendations_for_dimension(dim, signal_text))
        label = DIMENSION_LABELS.get(dim, dim)
        signal_html = f"<div class='dim-signal'>{md_inline(signal_text)}</div>"
        cards.append(f"""
          <section class='dim-card'>
            <div class='dim-head'>{dim} — {md_inline(label)}</div>
            {signal_html}
            <ul class='dim-list'>{items}</ul>
          </section>
        """)

    return """
      <section class='wide-section'>
        <div class='wide-title'>Recommended next moves by dimension</div>
        <div class='dim-grid'>
          %s
        </div>
      </section>
    """ % "".join(cards)


def build_section_html(sec) -> str:
    items_html = []
    for item in sec["items"]:
        if item.startswith("- "):
            items_html.append(f"<li>{md_inline(item[2:].strip())}</li>")
        else:
            items_html.append(f"<p>{md_inline(item)}</p>")

    return f"""
      <section class='card'>
        <div class='card-head'>
          <div class='eyebrow'>{md_inline(sec['title'])}</div>
        </div>
        <div class='card-body'>
          {''.join(items_html)}
        </div>
      </section>
    """


def build_sections_html(sections, *, exclude_titles=()) -> str:
    excluded = {t.strip().lower() for t in exclude_titles}
    return "".join(build_section_html(sec) for sec in sections if sec['title'].strip().lower() not in excluded)


def find_section(sections, title: str):
    for sec in sections:
        if sec['title'].strip().lower() == title.strip().lower():
            return sec
    return None


def build_html(title_text: str, sections, stamp: str) -> str:
    quote = build_moment_quote(sections, stamp)
    hero_subtitle = "Divinity Health AI"
    footer_text = (
        "Your 8D Summary brought to you by Divinity Health AI powered by Divinity Science Research Lab"
        f" • {stamp}"
    )
    sections_html = build_sections_html(sections, exclude_titles=("Confidence",))
    confidence_section = find_section(sections, "Confidence")
    confidence_html = build_section_html(confidence_section) if confidence_section else ""
    quick_wins_html = build_quick_wins_html(sections)

    return Template("""<!doctype html>
<html lang='en'>
<head>
<meta charset='utf-8'>
<style>
  @page {
    size: letter;
    margin: 0.38in 0.42in 0.34in 0.42in;
    @bottom-right {
      content: 'Page ' counter(page);
      color: #6B7280;
      font-size: 7.2pt;
      letter-spacing: 0.02em;
    }
  }
  html, body {
    margin: 0;
    padding: 0;
    background: #FAF3E0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    color: #16161D;
  }
  body {
    line-height: 1.12;
    font-size: 8.25pt;
  }
  .page { width: 100%; }
  .hero {
    background: linear-gradient(135deg, #0D1B2A 0%, #16213E 58%, #0D1B2A 100%);
    color: white;
    border-radius: 14px;
    padding: 11px 14px 11px 14px;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.05) inset;
    position: relative;
    overflow: hidden;
    margin-bottom: 7px;
  }
  .hero:before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    height: 3px;
    background: #FFD700;
  }
  .kicker {
    font-size: 6.8pt;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: rgba(255,255,255,.76);
    margin-bottom: 4px;
    font-weight: 700;
  }
  .hero h1 {
    margin: 0;
    font-size: 17.2pt;
    line-height: 1.0;
    letter-spacing: -0.02em;
    font-weight: 800;
  }
  .quote-wrap {
    margin-top: 6px;
  }
  .quote {
    margin: 0;
    font-size: 8.2pt;
    line-height: 1.24;
    color: rgba(255,255,255,.92);
    max-width: 96%;
    font-style: italic;
  }
  .quote-attrib {
    margin: 3px 0 0 0;
    font-size: 7.25pt;
    line-height: 1.1;
    color: rgba(255,255,255,.78);
    font-weight: 700;
    letter-spacing: .03em;
  }
  .card {
    background: rgba(255,255,255,.94);
    border: 1px solid #D7D2DB;
    border-left: 4px solid #0D1B2A;
    border-radius: 13px;
    padding: 8px 10px 7px 10px;
    margin: 0 0 5px 0;
    page-break-inside: auto;
    break-inside: auto;
    orphans: 2;
    widows: 2;
  }
  .card-head {
    display: flex;
    flex-direction: column;
    gap: 1px;
    margin-bottom: 4px;
  }
  .eyebrow {
    font-size: 6.9pt;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: #7B6A3A;
    font-weight: 800;
  }
  .card-body p {
    margin: 0 0 3px 0;
    color: #1D1D25;
  }
  .card-body p:last-child {
    margin-bottom: 0;
  }
  .card-body ul {
    margin: 0;
    padding: 0 0 0 13px;
  }
  .card-body li {
    margin: 0 0 2px 0;
    padding-left: 2px;
  }
  strong { color: #0D1B2A; }

  .wide-section {
    background: rgba(255,255,255,.92);
    border: 1px solid #D7D2DB;
    border-radius: 13px;
    padding: 8px 10px 9px 10px;
    margin: 0 0 6px 0;
    page-break-inside: auto;
    break-inside: auto;
    orphans: 2;
    widows: 2;
  }
  .wide-title {
    font-size: 7.6pt;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #0D1B2A;
    font-weight: 800;
    margin-bottom: 2px;
  }
  .dim-intro {
    margin: 0 0 6px 0;
    font-size: 7.25pt;
    line-height: 1.18;
    color: #5E6472;
  }
  .dim-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
  }
  .dim-card {
    border: 1px solid #D9D3DD;
    border-radius: 11px;
    background: linear-gradient(180deg, rgba(255,255,255,.98), rgba(250,243,224,.92));
    padding: 7px 8px 6px 8px;
    page-break-inside: auto;
    break-inside: auto;
    orphans: 2;
    widows: 2;
  }
  .dim-head {
    font-size: 7.3pt;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #7B6A3A;
    font-weight: 800;
    margin-bottom: 4px;
  }
  .dim-signal {
    font-size: 6.95pt;
    line-height: 1.16;
    color: #5E6472;
    margin: 0 0 4px 0;
    font-style: italic;
  }
  .dim-signal strong { color: #0D1B2A; }
  .dim-list {
    margin: 0;
    padding: 0 0 0 12px;
  }
  .dim-list li {
    margin: 0 0 2px 0;
    padding-left: 2px;
  }
  .footer-card {
    margin-top: 4px;
    border-top: 1px solid #E3DCCB;
    padding-top: 6px;
    color: #6B7280;
    font-size: 6.95pt;
    letter-spacing: .02em;
    text-align: left;
  }
  .footer-card strong {
    color: #0D1B2A;
  }
</style>
</head>
<body>
  <div class='page'>
    <div class='hero'>
      <div class='kicker'>$hero_subtitle</div>
      <h1>8D Pattern Awareness</h1>
      <div class='quote-wrap'>
        <p class='quote'>“$quote_text”</p>
        <p class='quote-attrib'>— $quote_author</p>
      </div>
    </div>

    $sections_html

    $quick_wins_html

    $confidence_html

    <div class='footer-card'>$footer_text</div>
  </div>
</body>
</html>""").substitute(
        hero_subtitle=hero_subtitle,
        quote_text=quote["text"],
        quote_author=quote["author"],
        sections_html=sections_html,
        quick_wins_html=quick_wins_html,
        confidence_html=confidence_html,
        footer_text=footer_text,
    )


def main():
    parser = argparse.ArgumentParser(description="Render the 8D report from editable markdown.")
    parser.add_argument("--source", required=True, type=Path, help="Editable markdown source")
    parser.add_argument("--output", required=True, type=Path, help="Output PDF path")
    parser.add_argument(
        "--timestamp",
        default=None,
        help="Optional explicit timestamp for the footer, e.g. '2026-05-31 19:04 CDT'",
    )
    args = parser.parse_args()

    title, sections = parse_markdown(args.source)
    stamp = args.timestamp or datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    html = build_html(title, sections, stamp)
    HTML(string=html, base_url='file:///tmp').write_pdf(str(args.output))
    print(args.output)


if __name__ == '__main__':
    main()
