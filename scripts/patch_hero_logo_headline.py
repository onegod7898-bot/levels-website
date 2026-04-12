"""Inject Levels wordmark into hero headline (Next + logo). Run: py scripts/patch_hero_logo_headline.py"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

OLD_CSS = """    .hero-services-headline__brand {
      display: block;
      margin-top: 0.06em;
      font-family: var(--font-logo);
      font-weight: 500;
      font-style: italic;
      font-size: clamp(2rem, 5.5vw, 3.35rem);
      letter-spacing: 0.03em;
      text-transform: none;
      line-height: 1.05;
      background: linear-gradient(95deg, #9dd9de 0%, #c9b896 42%, #e8c4b8 78%, #b8a5e0 100%);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
      filter: drop-shadow(0 2px 20px rgba(0, 0, 0, 0.45));
    }
    @supports not (background-clip: text) {
      .hero-services-headline__brand {
        color: var(--champagne);
        -webkit-text-fill-color: var(--champagne);
      }
    }"""

NEW_CSS = """    .hero-services-headline__brand {
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

OLD_HTML = """            <span class="hero-services-headline__brand">Next Level</span>"""

NEW_HTML = """            <span class="hero-services-headline__brand">
              <span class="hero-services-headline__next">Next</span>
              <img class="hero-services-headline__logo" src="https://images.squarespace-cdn.com/content/v1/65390bdc8b505402583f3d5b/707db16c-7f27-44f5-88ee-e5badc2a7ddd/LEVELS+LOGO.png?format=500w" width="315" height="60" alt="Levels" fetchpriority="high" decoding="async">
            </span>"""


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    if "hero-services-headline__logo" in text:
        print("Already patched.")
        return
    if OLD_CSS not in text:
        raise SystemExit("OLD_CSS not found")
    if OLD_HTML not in text:
        raise SystemExit("OLD_HTML not found")
    text = text.replace(OLD_CSS, NEW_CSS, 1)
    text = text.replace(OLD_HTML, NEW_HTML, 1)
    INDEX.write_text(text, encoding="utf-8")
    print("OK: hero headline uses Next + Levels logo.")


if __name__ == "__main__":
    main()
