"""Replace home hero section with 4-service grid (UTF-8)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")

NEW_HERO = r"""<section id="home" class="hero hero--services">
      <div class="hero-services-bg" aria-hidden="true"></div>
      <div class="hero__inner">
        <header class="hero__intro fade-in">
          <h1 class="hero-services-headline">
            <span class="hero-services-headline__line">Take Your Event To The</span>
            <span class="hero-services-headline__brand">Next Level</span>
          </h1>
          <p class="hero-services-sub">All-in-one event experiences — from 360 Video Booth to catering setups.</p>
          <a class="btn-pill btn-pill--primary hero-services-cta" href="book.html">Book Your Date</a>
        </header>
        <div class="hero-services" data-hero-services>
          <div class="hero-services__grid" role="list">
            <article class="hero-service-card fade-in" role="listitem" data-service-index="0">
              <a href="360-videobooth.html" class="hero-service-card__link">
                <div class="hero-service-card__media">
                  <img src="images/premium-360-video-booth.png" alt="360 Video Booth — LED platform, ring light, and Levels branding" width="800" height="1000" loading="eager" fetchpriority="high" decoding="async">
                  <div class="hero-service-card__overlay"></div>
                </div>
                <h2 class="hero-service-card__title">360 Video Booth</h2>
              </a>
            </article>
            <article class="hero-service-card fade-in" role="listitem" data-service-index="1">
              <a href="services.html" class="hero-service-card__link">
                <div class="hero-service-card__media">
                  <img src="images/gallery-luxury-selfie-booth.png" alt="Luxury selfie booth with ring light and backdrop" width="800" height="1000" loading="eager" decoding="async">
                  <div class="hero-service-card__overlay"></div>
                </div>
                <h2 class="hero-service-card__title">Selfie Booth</h2>
              </a>
            </article>
            <article class="hero-service-card fade-in" role="listitem" data-service-index="2">
              <a href="services.html" class="hero-service-card__link">
                <div class="hero-service-card__media">
                  <img src="images/premium-pancake-cart.png" alt="Pancake cart with mini pancakes, sauces, and toppings" width="1600" height="900" loading="eager" decoding="async">
                  <div class="hero-service-card__overlay"></div>
                </div>
                <h2 class="hero-service-card__title">Pancake Cart</h2>
              </a>
            </article>
            <article class="hero-service-card fade-in" role="listitem" data-service-index="3">
              <a href="services.html" class="hero-service-card__link">
                <div class="hero-service-card__media">
                  <img src="images/gallery-chocolate-fountain-milk.png" alt="Chocolate fountain with fruit and dipping treats" width="800" height="1000" loading="eager" decoding="async">
                  <div class="hero-service-card__overlay"></div>
                </div>
                <h2 class="hero-service-card__title">Chocolate Fountain</h2>
              </a>
            </article>
          </div>
        </div>
      </div>
    </section>"""

import re

pattern = re.compile(
    r"<section id=\"home\" class=\"hero\">.*?</section>",
    re.DOTALL,
)
m = pattern.search(text)
if not m:
    raise SystemExit("Could not find hero section")
text = pattern.sub(NEW_HERO, text, count=1)

# Remove video preload (hero no longer uses full-bleed video)
text = text.replace(
    '  <link rel="preload" href="assets/hero-bg.mp4" as="video" type="video/mp4">\n',
    "",
)

index.write_text(text, encoding="utf-8")
print("OK: hero replaced, video preload removed")
