"""Remove Strategic paragraph, why blurb, footer levels-360.com links; retarget meta URLs to Vercel."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://levels-website.vercel.app"
OLD_SITE = "https://www.levels-360.com"

FOOTER_SNIPPETS = [
    ' · <a href="https://www.levels-360.com/">levels-360.com</a>',
    f' · <a href="{SITE_URL}/">levels-360.com</a>',
    f' · <a href="{SITE_URL}">levels-360.com</a>',
]


def clean_html(t: str) -> str:
    for s in FOOTER_SNIPPETS:
        t = t.replace(s, "")
    t = re.sub(
        r"\n\s*<p class=\"section-lead fade-in\"><strong>The Strategic</strong>.*?</p>\s*",
        "\n",
        t,
        flags=re.DOTALL,
    )
    t = re.sub(
        r"\n\s*<p class=\"section-lead fade-in\">What we bring to every booking.*?</p>\s*",
        "\n",
        t,
        flags=re.DOTALL,
    )
    t = t.replace(OLD_SITE, SITE_URL)
    return t


def main() -> None:
    for path in sorted(ROOT.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        new = clean_html(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("updated", path.name)

    bp = ROOT / "scripts" / "build_pages.py"
    if bp.is_file():
        t = bp.read_text(encoding="utf-8")
        nt = clean_html(t)
        if nt != t:
            bp.write_text(nt, encoding="utf-8")
            print("updated build_pages.py")

    print("done")


if __name__ == "__main__":
    main()
