"""One-off patch: hero slideshow + service strip. Run: py scripts/patch_hero_slideshow.py"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

NEW_CSS = r"""    .hero.hero--services {
      min-height: min(100vh, 1120px);
      padding: calc(96px + env(safe-area-inset-top, 0px)) clamp(16px, 4vw, 28px) clamp(28px, 4vw, 48px);
      align-items: flex-start;
      padding-top: calc(88px + env(safe-area-inset-top, 0px));
      position: relative;
      overflow: hidden;
    }
    .hero-services-slideshow {
      position: absolute;
      inset: 0;
      z-index: 0;
      pointer-events: none;
    }
    .hero-services-slide {
      position: absolute;
      inset: 0;
      opacity: 0;
      transition: opacity 1.1s var(--ease-premium, cubic-bezier(0.4, 0, 0.2, 1));
      will-change: opacity;
    }
    .hero-services-slide.is-active {
      opacity: 1;
    }
    .hero-services-slide img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      transform: scale(1.02);
    }
    .hero-services-bg {
      position: absolute;
      inset: 0;
      z-index: 1;
      pointer-events: none;
      background:
        linear-gradient(180deg, rgba(5, 4, 3, 0.55) 0%, rgba(5, 4, 3, 0.42) 38%, rgba(3, 2, 2, 0.65) 100%),
        radial-gradient(ellipse 120% 80% at 50% -10%, rgba(126, 200, 206, 0.08), transparent 55%),
        radial-gradient(ellipse 90% 60% at 100% 100%, rgba(201, 184, 150, 0.06), transparent 50%);
    }
    .hero.hero--services .hero__inner {
      position: relative;
      z-index: 2;
      width: 100%;
      max-width: 1040px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: clamp(18px, 3vw, 28px);
    }
    .hero__intro {
      text-align: center;
      max-width: 40rem;
    }
    .hero.hero--services .hero__intro {
      position: relative;
      z-index: 0;
      padding: clamp(8px, 2vw, 16px) clamp(16px, 4vw, 28px);
    }
    .hero.hero--services .hero__intro::before {
      content: "";
      position: absolute;
      left: 50%;
      top: 42%;
      transform: translate(-50%, -50%);
      width: min(120%, 480px);
      height: min(220%, 280px);
      background: radial-gradient(ellipse 75% 65% at 50% 50%, rgba(48, 26, 22, 0.42), transparent 62%);
      pointer-events: none;
      z-index: -1;
    }
    .hero-services-headline {
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
    }
    .hero-services-sub {
      font-size: clamp(0.95rem, 1.85vw, 1.1rem);
      line-height: 1.55;
      color: rgba(226, 220, 210, 0.92);
      margin: 0 0 20px;
      max-width: 36rem;
      margin-left: auto;
      margin-right: auto;
    }
    .hero-services-cta {
      margin-top: 4px;
    }
    .hero-services {
      width: 100%;
    }
    .hero-services__strip {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      align-items: center;
      gap: 10px;
      max-width: 920px;
      margin: 0 auto;
      padding: 0;
      list-style: none;
    }
    .hero-services-strip__item {
      font-family: var(--font-body);
      font-size: clamp(0.68rem, 1.35vw, 0.8rem);
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: rgba(250, 246, 240, 0.9);
      padding: 10px 16px;
      border-radius: 999px;
      border: 1px solid rgba(255, 255, 255, 0.22);
      background: rgba(0, 0, 0, 0.38);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
      cursor: pointer;
      transition: background 0.35s var(--ease-premium), border-color 0.35s var(--ease-premium), transform 0.35s var(--ease-premium);
    }
    .hero-services-strip__item:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.35);
    }
    .hero-services-strip__item.is-active {
      border-color: rgba(201, 184, 150, 0.75);
      background: rgba(201, 184, 150, 0.14);
      box-shadow: 0 8px 28px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(201, 184, 150, 0.2);
    }
    .hero-services-strip__item:focus-visible {
      outline: 2px solid var(--champagne);
      outline-offset: 3px;
    }
    .hero-services-live {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    .hero-services__dots {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 8px;
      margin-top: 4px;
    }
    .hero-services__dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      border: none;
      padding: 0;
      background: rgba(255, 255, 255, 0.28);
      cursor: pointer;
      transition: background 0.3s var(--ease), transform 0.3s var(--ease);
    }
    .hero-services__dot[aria-current="true"] {
      background: var(--champagne);
      transform: scale(1.2);
    }
    @media (max-width: 699px) {
      .hero.hero--services {
        min-height: auto;
        padding-bottom: 24px;
      }
      .hero-services__strip {
        gap: 8px;
      }
      .hero-services-strip__item {
        padding: 8px 12px;
        flex: 1 1 calc(50% - 8px);
        min-width: 0;
        text-align: center;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      .hero-services-slide {
        transition: opacity 0.2s ease;
      }
    }
"""

NEW_HERO = """<section id="home" class="hero hero--services">
      <div class="hero-services-slideshow" data-hero-slideshow aria-hidden="true">
        <div class="hero-services-slide is-active" data-slide="0">
          <img src="images/hero-360-video-booth.png" alt="" width="800" height="1000" loading="eager" fetchpriority="high" decoding="async">
        </div>
        <div class="hero-services-slide" data-slide="1">
          <img src="images/hero-selfie-booth.png" alt="" width="800" height="1000" loading="eager" decoding="async">
        </div>
        <div class="hero-services-slide" data-slide="2">
          <img src="images/hero-pancake-cart.png" alt="" width="1600" height="900" loading="eager" decoding="async">
        </div>
        <div class="hero-services-slide" data-slide="3">
          <img src="images/hero-chocolate-fountain.png" alt="" width="800" height="1000" loading="eager" decoding="async">
        </div>
      </div>
      <div class="hero-services-bg" aria-hidden="true"></div>
      <div class="hero__inner">
        <header class="hero__intro fade-in">
          <h1 class="hero-services-headline">
            <span class="hero-services-headline__line">Take Your Event To The Next</span>
            <span class="hero-services-headline__brand">
              <img class="hero-services-headline__logo" src="https://images.squarespace-cdn.com/content/v1/65390bdc8b505402583f3d5b/707db16c-7f27-44f5-88ee-e5badc2a7ddd/LEVELS+LOGO.png?format=500w" width="315" height="60" alt="Levels" fetchpriority="high" decoding="async">
            </span>
          </h1>
          <p class="hero-services-sub">All-in-one event experiences — from 360 Video Booth to catering setups.</p>
          <a class="btn-pill btn-pill--primary hero-services-cta" href="#booking">Book Your Date</a>
        </header>
        <div class="hero-services" data-hero-services>
          <nav class="hero-services__strip" aria-label="Our services">
            <button type="button" class="hero-services-strip__item fade-in is-active" data-service-index="0" aria-pressed="true">360 Video Booth</button>
            <button type="button" class="hero-services-strip__item fade-in" data-service-index="1" aria-pressed="false">Selfie Booth</button>
            <button type="button" class="hero-services-strip__item fade-in" data-service-index="2" aria-pressed="false">Pancake Cart</button>
            <button type="button" class="hero-services-strip__item fade-in" data-service-index="3" aria-pressed="false">Chocolate Fountain</button>
          </nav>
          <span id="heroServicesLive" class="hero-services-live" aria-live="polite" aria-atomic="true"></span>
          <div class="hero-services__dots" data-hero-dots aria-label="Service slides"></div>
        </div>
      </div>
    </section>"""

INIT_JS = """
      function initHeroServices() {
        var wrap = document.querySelector('[data-hero-services]');
        if (!wrap) return;
        var root = document.getElementById('home');
        var slides = root ? root.querySelectorAll('.hero-services-slide') : [];
        var strip = wrap.querySelector('.hero-services__strip');
        var dotsWrap = wrap.querySelector('[data-hero-dots]');
        var live = document.getElementById('heroServicesLive');
        if (!slides.length || !strip) return;
        var buttons = strip.querySelectorAll('.hero-services-strip__item');
        var labels = ['360 Video Booth', 'Selfie Booth', 'Pancake Cart', 'Chocolate Fountain'];
        var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        var idx = 0;
        var timer = null;

        function setSlide(i) {
          idx = (i + slides.length) % slides.length;
          slides.forEach(function (s, j) {
            s.classList.toggle('is-active', j === idx);
          });
          buttons.forEach(function (b, j) {
            b.classList.toggle('is-active', j === idx);
            b.setAttribute('aria-pressed', j === idx ? 'true' : 'false');
          });
          if (dotsWrap) {
            var dots = dotsWrap.querySelectorAll('.hero-services__dot');
            dots.forEach(function (d, j) {
              d.setAttribute('aria-current', j === idx ? 'true' : 'false');
            });
          }
          if (live) {
            live.textContent = 'Now showing: ' + labels[idx];
          }
        }

        function buildDots() {
          if (!dotsWrap) return;
          dotsWrap.innerHTML = '';
          for (var di = 0; di < slides.length; di++) {
            (function (n) {
              var b = document.createElement('button');
              b.type = 'button';
              b.className = 'hero-services__dot';
              b.setAttribute('aria-label', 'Show service ' + (n + 1));
              b.addEventListener('click', function () {
                setSlide(n);
                resetTimer();
              });
              dotsWrap.appendChild(b);
            })(di);
          }
        }

        function nextTick() {
          setSlide(idx + 1);
        }

        function resetTimer() {
          if (timer) window.clearInterval(timer);
          if (!reduced) {
            timer = window.setInterval(nextTick, 5000);
          }
        }

        for (var bi = 0; bi < buttons.length; bi++) {
          (function (n) {
            buttons[n].addEventListener('click', function () {
              setSlide(n);
              resetTimer();
            });
          })(bi);
        }

        buildDots();
        setSlide(0);
        resetTimer();
      }

"""


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    if "hero-services-slideshow" in text and "hero-services-slide" in text:
        print("Already patched (slideshow present). Skipping.")
        return

    start = text.index("    .hero.hero--services {")
    s = text[start : start + 15000]
    m = re.search(
        r"    @media \(prefers-reduced-motion: reduce\) \{\n      \.hero-service-card\.is-highlight[\s\S]*?\n    \}\n",
        s,
    )
    if not m:
        raise SystemExit("Could not find hero CSS block to replace.")
    end = start + m.end()
    text = text[:start] + NEW_CSS + text[end:]

    text = re.sub(
        r"<section id=\"home\" class=\"hero hero--services\">[\s\S]*?</section>",
        NEW_HERO,
        text,
        count=1,
    )

    a = text.index("      function initHeroServices()")
    b = text.index("      function initAmbientVideos()", a)
    text = text[:a] + INIT_JS + text[b:]

    text = text.replace(
        "document.querySelectorAll('.card-grid, .testimonial-grid, .premium-grid, .gallery-masonry, .process-steps, .hero-services__grid')",
        "document.querySelectorAll('.card-grid, .testimonial-grid, .premium-grid, .gallery-masonry, .process-steps, .hero-services__strip')",
    )

    INDEX.write_text(text, encoding="utf-8")
    print("OK: hero slideshow + strip applied.")


if __name__ == "__main__":
    main()
