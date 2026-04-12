"""Apply serif hero layout: line 1 = TAKE YOUR EVENT TO THE NEXT, line 2 = logo only."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

OLD_HTML = """            <span class="hero-services-headline__line">Take Your Event To The</span>
            <span class="hero-services-headline__brand">
              <span class="hero-services-headline__next">Next</span>
              <img class="hero-services-headline__logo" src="https://images.squarespace-cdn.com/content/v1/65390bdc8b505402583f3d5b/707db16c-7f27-44f5-88ee-e5badc2a7ddd/LEVELS+LOGO.png?format=500w" width="315" height="60" alt="Levels" fetchpriority="high" decoding="async">
            </span>"""

NEW_HTML = """            <span class="hero-services-headline__line">Take Your Event To The Next</span>
            <span class="hero-services-headline__brand">
              <img class="hero-services-headline__logo" src="https://images.squarespace-cdn.com/content/v1/65390bdc8b505402583f3d5b/707db16c-7f27-44f5-88ee-e5badc2a7ddd/LEVELS+LOGO.png?format=500w" width="315" height="60" alt="Levels" fetchpriority="high" decoding="async">
            </span>"""

OLD_CSS = """    .hero-services-headline {
      font-family: var(--font-body);
      font-size: clamp(1.65rem, 4.2vw, 2.75rem);
      font-weight: 800;
      line-height: 1.08;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      margin: 0 0 14px;
      text-wrap: balance;
      color: #fff;
      text-shadow: 0 2px 24px rgba(0, 0, 0, 0.55);
    }
    .hero-services-headline__line {
      display: block;
    }
    .hero-services-headline__brand {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      align-items: center;
      gap: 0.35em 0.55em;
      margin-top: 0.06em;
      line-height: 1.05;
    }
    .hero-services-headline__next {
      font-family: var(--font-body);
      font-weight: 800;
      font-style: normal;
      font-size: clamp(1.65rem, 4.2vw, 2.75rem);
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: #fff;
      text-shadow: 0 2px 24px rgba(0, 0, 0, 0.55);
      background: none;
      -webkit-background-clip: unset;
      background-clip: unset;
      -webkit-text-fill-color: #fff;
      filter: none;
    }
    .hero-services-headline__logo {
      height: clamp(1.85rem, 5vw, 3rem);
      width: auto;
      max-width: min(70vw, 260px);
      object-fit: contain;
      object-position: center left;
      filter: drop-shadow(0 2px 16px rgba(0, 0, 0, 0.5));
    }"""

NEW_CSS = """    .hero-services-headline {
      margin: 0 0 14px;
      text-align: center;
      color: #fff;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: clamp(12px, 2.2vw, 22px);
      text-wrap: balance;
    }
    .hero-services-headline__line {
      display: block;
      max-width: 40rem;
      margin: 0 auto;
      font-family: var(--font-display);
      font-weight: 500;
      font-size: clamp(0.9rem, 2.15vw, 1.2rem);
      line-height: 1.45;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      text-shadow: 0 2px 22px rgba(0, 0, 0, 0.55);
    }
    .hero-services-headline__brand {
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 0;
      line-height: 0;
    }
    .hero-services-headline__logo {
      height: clamp(2.65rem, 9vw, 4.85rem);
      width: auto;
      max-width: min(88vw, 340px);
      object-fit: contain;
      object-position: center;
      filter: drop-shadow(0 4px 24px rgba(0, 0, 0, 0.55));
    }"""


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    if NEW_HTML.split("\n")[0].strip() in text and "hero-services-headline__next" not in text:
        print("Already applied.")
        return
    if OLD_HTML not in text:
        raise SystemExit("OLD_HTML not found")
    if OLD_CSS not in text:
        raise SystemExit("OLD_CSS not found")
    text = text.replace(OLD_HTML, NEW_HTML, 1)
    text = text.replace(OLD_CSS, NEW_CSS, 1)
    INDEX.write_text(text, encoding="utf-8")
    print("OK: serif two-line hero (Next in line 1, logo only line 2).")


if __name__ == "__main__":
    main()
