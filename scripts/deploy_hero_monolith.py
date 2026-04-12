"""
Apply 4-service hero (slideshow + strip) to monolithic index.html (inline CSS + inline script).
Run: py scripts/deploy_hero_monolith.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from patch_hero_slideshow import INIT_JS, NEW_HERO

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SITE_CSS = ROOT / "assets" / "site.css"


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")

    if "hero.hero--services" not in text:
        css_lines = SITE_CSS.read_text(encoding="utf-8").splitlines()
        block = "\n".join(css_lines[768:989]) + "\n"
        text = text.replace("</style>", block + "</style>", 1)

    text = re.sub(
        r"<section id=\"home\" class=\"hero\">.*?</section>",
        NEW_HERO,
        text,
        count=1,
        flags=re.DOTALL,
    )

    text = text.replace(
        '  <link rel="preload" href="assets/hero-bg.mp4" as="video" type="video/mp4">\n',
        "",
    )

    if "function initHeroServices()" not in text:
        text = text.replace(
            "      function initAmbientVideos() {",
            INIT_JS + "\n      function initAmbientVideos() {",
            1,
        )
        text = text.replace(
            "      initHeroVideo();\n      initAmbientVideos();",
            "      initHeroVideo();\n      initAmbientVideos();\n      initHeroServices();",
            1,
        )

    text = text.replace(
        "document.querySelectorAll('.card-grid, .testimonial-grid, .premium-grid, .gallery-masonry, .process-steps')",
        "document.querySelectorAll('.card-grid, .testimonial-grid, .premium-grid, .gallery-masonry, .process-steps, .hero-services__strip')",
        1,
    )

    INDEX.write_text(text, encoding="utf-8")
    print("OK: monolith index.html updated")


if __name__ == "__main__":
    main()
