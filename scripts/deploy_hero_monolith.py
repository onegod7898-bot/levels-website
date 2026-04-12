"""
Apply 4-service hero to monolithic index.html (inline CSS + inline script).
Run: py scripts/deploy_hero_monolith.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
SITE_CSS = ROOT / "assets" / "site.css"

NEW_HERO = """<section id="home" class="hero hero--services">
      <div class="hero-services-bg" aria-hidden="true"></div>
      <div class="hero__inner">
        <header class="hero__intro fade-in">
          <h1 class="hero-services-headline">
            <span class="hero-services-headline__line">Take Your Event To The</span>
            <span class="hero-services-headline__brand">Next Level</span>
          </h1>
          <p class="hero-services-sub">All-in-one event experiences — from 360 Video Booth to catering setups.</p>
          <a class="btn-pill btn-pill--primary hero-services-cta" href="#booking">Book Your Date</a>
        </header>
        <div class="hero-services" data-hero-services>
          <div class="hero-services__grid" role="list">
            <article class="hero-service-card fade-in" role="listitem" data-service-index="0">
              <a href="#booth" class="hero-service-card__link">
                <div class="hero-service-card__media">
                  <img src="images/hero-360-video-booth.png" alt="360 Video Booth — professional platform, lighting, and branding" width="800" height="1000" loading="eager" fetchpriority="high" decoding="async">
                  <div class="hero-service-card__overlay"></div>
                  <h2 class="hero-service-card__title">360 Video Booth</h2>
                </div>
              </a>
            </article>
            <article class="hero-service-card fade-in" role="listitem" data-service-index="1">
              <a href="#services" class="hero-service-card__link">
                <div class="hero-service-card__media">
                  <img src="images/hero-selfie-booth.png" alt="Luxury selfie booth with ring light and backdrop" width="800" height="1000" loading="eager" decoding="async">
                  <div class="hero-service-card__overlay"></div>
                  <h2 class="hero-service-card__title">Selfie Booth</h2>
                </div>
              </a>
            </article>
            <article class="hero-service-card fade-in" role="listitem" data-service-index="2">
              <a href="#services" class="hero-service-card__link">
                <div class="hero-service-card__media">
                  <img src="images/hero-pancake-cart.png" alt="Pancake cart with mini pancakes, sauces, and toppings" width="1600" height="900" loading="eager" decoding="async">
                  <div class="hero-service-card__overlay"></div>
                  <h2 class="hero-service-card__title">Pancake Cart</h2>
                </div>
              </a>
            </article>
            <article class="hero-service-card fade-in" role="listitem" data-service-index="3">
              <a href="#services" class="hero-service-card__link">
                <div class="hero-service-card__media">
                  <img src="images/hero-chocolate-fountain.png" alt="Chocolate fountain with fruit and dipping treats" width="800" height="1000" loading="eager" decoding="async">
                  <div class="hero-service-card__overlay"></div>
                  <h2 class="hero-service-card__title">Chocolate Fountain</h2>
                </div>
              </a>
            </article>
          </div>
          <div class="hero-services__dots" data-hero-dots aria-label="Service slides"></div>
        </div>
      </div>
    </section>"""

INIT_JS = """
      function initHeroServices() {
        var wrap = document.querySelector('[data-hero-services]');
        if (!wrap) return;
        var grid = wrap.querySelector('.hero-services__grid');
        var dotsWrap = wrap.querySelector('[data-hero-dots]');
        if (!grid) return;
        var cards = grid.querySelectorAll('.hero-service-card');
        if (!cards.length) return;
        var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        var idx = 0;
        var timer = null;

        function setHighlight(i) {
          idx = (i + cards.length) % cards.length;
          cards.forEach(function (c, j) {
            c.classList.toggle('is-highlight', j === idx);
          });
          if (dotsWrap) {
            var dots = dotsWrap.querySelectorAll('.hero-services__dot');
            dots.forEach(function (d, j) {
              d.setAttribute('aria-current', j === idx ? 'true' : 'false');
            });
          }
        }

        function scrollCardIntoView(i) {
          if (window.innerWidth > 699) return;
          var card = cards[i];
          if (!card) return;
          var left = card.offsetLeft - grid.offsetLeft;
          try {
            grid.scrollTo({ left: left, behavior: reduced ? 'auto' : 'smooth' });
          } catch (e) {
            grid.scrollLeft = left;
          }
        }

        function isMobile() {
          return window.innerWidth <= 699;
        }

        if (dotsWrap && isMobile()) {
          for (var di = 0; di < cards.length; di++) {
            (function (n) {
              var b = document.createElement('button');
              b.type = 'button';
              b.className = 'hero-services__dot';
              b.setAttribute('aria-label', 'Go to service ' + (n + 1));
              b.addEventListener('click', function () {
                setHighlight(n);
                scrollCardIntoView(n);
              });
              dotsWrap.appendChild(b);
            })(di);
          }
        }

        setHighlight(0);

        if (!reduced) {
          timer = window.setInterval(function () {
            var next = (idx + 1) % cards.length;
            setHighlight(next);
            if (isMobile()) scrollCardIntoView(next);
          }, isMobile() ? 6200 : 4800);
        }

        if (isMobile()) {
          grid.addEventListener(
            'scroll',
            function () {
              var vp = grid.scrollLeft + grid.clientWidth * 0.5;
              var best = 0;
              var bestDist = Infinity;
              for (var si = 0; si < cards.length; si++) {
                var c = cards[si];
                var mid = c.offsetLeft + c.clientWidth * 0.5;
                var d = Math.abs(mid - vp);
                if (d < bestDist) {
                  bestDist = d;
                  best = si;
                }
              }
              setHighlight(best);
            },
            { passive: true }
          );
        }
      }
"""


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
        "document.querySelectorAll('.card-grid, .testimonial-grid, .premium-grid, .gallery-masonry, .process-steps, .hero-services__grid')",
        1,
    )

    INDEX.write_text(text, encoding="utf-8")
    print("OK: monolith index.html updated")


if __name__ == "__main__":
    main()
