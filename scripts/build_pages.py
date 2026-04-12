"""
Split levels-website index into multiple pages (UTF-8). Run from repo root:
  py scripts/build_pages.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"


def subpage_link_fixes(html: str) -> str:
    """Point hash links to real pages."""
    repl = [
        ('href="#booking"', 'href="book.html"'),
        ('href="#services"', 'href="services.html"'),
        ('href="#how-it-works"', 'href="how-it-works.html"'),
        ('href="#booth"', 'href="360-videobooth.html"'),
        ('href="#package"', 'href="package.html"'),
        ('href="#gallery"', 'href="gallery.html"'),
        ('href="#instagram"', 'href="instagram.html"'),
        ('href="#why"', 'href="why.html"'),
        ('href="#testimonials"', 'href="why.html#testimonials"'),
    ]
    for a, b in repl:
        html = html.replace(a, b)
    return html


def singular_copy(html: str) -> str:
    """Remove plural 's' on service product names where requested."""
    pairs = [
        ("360 Video Booths ·", "360 videobooth ·"),
        ("Chocolate Fountains ·", "Chocolate fountain ·"),
        ("Pancake Carts ·", "Pancake cart ·"),
        ("Selfie Booths —", "Selfie booth —"),
        ("Selfie Booths", "Selfie booth"),
        ("Premium Services", "Signature hire"),
        ("Premium services", "Signature hire"),
        ("Recent setups — 360 booths, chocolate fountains, pancake carts",
         "Recent setups — 360 videobooth, chocolate fountain, pancake cart"),
        ("curated reels from the 360 booth, chocolate fountains, and pancake carts",
         "curated reels from the 360 videobooth, chocolate fountain, and pancake cart"),
        ("Chocolate fountains &amp; catering", "Chocolate fountain &amp; catering"),
    ]
    for a, b in pairs:
        html = html.replace(a, b)
    return html


def extract_between(html: str, start: str, end: str | None, end_else: str | None = None) -> str:
    i = html.find(start)
    if i < 0:
        raise ValueError(f"missing start: {start[:40]}")
    rest = html[i:]
    if end:
        j = rest.find(end)
        if j < 0 and end_else:
            j = rest.find(end_else)
        if j < 0:
            raise ValueError(f"missing end after {start[:30]}")
        return rest[:j]
    return rest


def nav_block(active: str) -> str:
    """active: home | services | package | how | booth | gallery | instagram | why | book"""
    def cl(page: str) -> str:
        return ' class="active"' if active == page else ""

    dd_extra = ' nav-dropdown--current' if active in ("services", "how", "booth") else ""

    return f"""  <header class="site-header" id="siteHeader">
    <div class="header-inner">
      <a class="logo" href="index.html" aria-label="Levels home">
        <span class="logo__crop">
          <span class="logo__stage">
            <img class="logo__img" src="https://images.squarespace-cdn.com/content/v1/65390bdc8b505402583f3d5b/707db16c-7f27-44f5-88ee-e5badc2a7ddd/LEVELS+LOGO.png?format=500w" width="315" height="60" alt="Levels" fetchpriority="high" decoding="async">
          </span>
        </span>
      </a>
      <nav class="nav-desktop" aria-label="Primary">
        <a href="index.html"{cl("home")}>Home</a>
        <div class="nav-dropdown{dd_extra}" id="navDropdown">
          <button type="button" class="nav-dropdown__btn" id="navDropdownBtn" aria-expanded="false" aria-controls="navDropdownPanel" aria-haspopup="true">Services</button>
          <div class="nav-dropdown__panel" id="navDropdownPanel" role="menu">
            <a href="services.html" role="menuitem">What we offer</a>
            <a href="how-it-works.html" role="menuitem">How it works</a>
            <a href="360-videobooth.html" role="menuitem">360 videobooth</a>
            <a href="book.html" role="menuitem">Book</a>
          </div>
        </div>
        <a href="package.html"{cl("package")}>The Package</a>
        <a href="how-it-works.html"{cl("how")}>How it works</a>
        <a href="why.html"{cl("why")}>Why Levels</a>
        <a href="instagram.html"{cl("instagram")}>Instagram</a>
        <a href="book.html"{cl("book")}>Book</a>
        <div class="header-social" aria-label="Social">
          <a href="https://www.instagram.com/levels360_" target="_blank" rel="noopener noreferrer" aria-label="Instagram">Instagram</a>
          <a href="https://www.facebook.com/profile.php?id=61552172457876" target="_blank" rel="noopener noreferrer" aria-label="Facebook">Facebook</a>
        </div>
        <a class="btn-pill btn-pill--primary" href="book.html">Book now</a>
      </nav>
      <button type="button" class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navMobile" aria-label="Open menu">
        <span></span>
      </button>
    </div>
    <nav class="nav-mobile" id="navMobile" aria-label="Mobile">
      <a href="index.html">Home</a>
      <a href="services.html">Services</a>
      <a href="360-videobooth.html">360 videobooth</a>
      <a href="package.html">The Package</a>
      <a href="how-it-works.html">How it works</a>
      <a href="why.html">Why Levels</a>
      <a href="instagram.html">Instagram</a>
      <a href="book.html">Book</a>
      <a class="btn-pill btn-pill--primary" href="book.html">Book now</a>
    </nav>
  </header>
"""


def hub_section() -> str:
    return """
    <section class="section section--hub" aria-labelledby="hub-heading">
      <div class="section-inner">
        <p class="section-kicker fade-in">Explore</p>
        <h2 id="hub-heading" class="section-title section-title--mega fade-in">Premium event hire</h2>
        <p class="client-caption hamid-caption fade-in">Captions for each area are in progress — Hamid to supply final copy for every section.</p>
        <p class="section-lead fade-in">Open a page below, or <a href="book.html">book your date</a> directly.</p>
        <div class="page-hub">
          <a class="page-hub__card fade-in" href="services.html"><span class="page-hub__label">What we offer</span><span class="page-hub__desc">360 videobooth, chocolate fountain, selfie booth, pancake cart</span></a>
          <a class="page-hub__card fade-in" href="how-it-works.html"><span class="page-hub__label">How it works</span><span class="page-hub__desc">Enquire, quote, setup, celebrate</span></a>
          <a class="page-hub__card fade-in" href="360-videobooth.html"><span class="page-hub__label">360 videobooth</span><span class="page-hub__desc">HD slow-mo platform &amp; crew</span></a>
          <a class="page-hub__card fade-in" href="package.html"><span class="page-hub__label">The package</span><span class="page-hub__desc">What we bring on the night</span></a>
          <a class="page-hub__card fade-in" href="gallery.html"><span class="page-hub__label">Gallery</span><span class="page-hub__desc">Recent setups across Scotland</span></a>
          <a class="page-hub__card fade-in" href="instagram.html"><span class="page-hub__label">Instagram</span><span class="page-hub__desc">Reels &amp; highlights</span></a>
          <a class="page-hub__card fade-in" href="why.html"><span class="page-hub__label">Why Levels</span><span class="page-hub__desc">FAQs &amp; testimonials</span></a>
          <a class="page-hub__card fade-in" href="book.html"><span class="page-hub__label">Book</span><span class="page-hub__desc">Request a date</span></a>
        </div>
      </div>
    </section>
"""


def footer_block() -> str:
    return """  <footer>
    <p class="footer-region fade-in" style="text-align:center;margin-bottom:12px;color:var(--text-muted);font-size:0.95rem;">Serving all of Scotland</p>
    <p>&copy; Levels. All rights reserved.</p>
    <p class="footer-social">
      <a href="https://www.instagram.com/levels360_/" target="_blank" rel="noopener noreferrer">Instagram</a>
      <span aria-hidden="true"> · </span>
      <a href="instagram.html">Reels</a>
    </p>
  </footer>
"""


def loader_block() -> str:
    return """  <div id="loader" class="sacco-loader" role="status" aria-live="polite" aria-busy="true">
    <div class="loader-inner">
      <div class="loader-halo" aria-hidden="true"></div>
      <div class="loader-mark-wrap">
        <img class="loader-mark" src="https://images.squarespace-cdn.com/content/v1/65390bdc8b505402583f3d5b/707db16c-7f27-44f5-88ee-e5badc2a7ddd/LEVELS+LOGO.png?format=500w" width="315" height="60" alt="" decoding="async">
      </div>
      <div class="loader-line" aria-hidden="true"></div>
      <p class="loader-tagline">Premium event experiences</p>
    </div>
  </div>
"""


def head_variant(
    title: str,
    desc: str,
    canonical: str,
    og_title: str | None = None,
    preload_hero: bool = True,
) -> str:
    og_title = og_title or title
    preload_lines = ""
    if preload_hero:
        preload_lines = """  <link rel="preload" href="assets/hero-bg.mp4" as="video" type="video/mp4">
  <link rel="preload" href="https://images.squarespace-cdn.com/content/v1/65390bdc8b505402583f3d5b/74725833-ff01-45a1-a950-fb6e02e1976c/IMG_6154.jpg" as="image" fetchpriority="high">
"""
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{canonical}">
  <meta name="theme-color" content="#0a0908">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Levels">
  <meta property="og:url" content="{canonical}">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://levels-website.vercel.app/og-image.png">
  <link rel="icon" href="https://images.squarespace-cdn.com/content/v1/65390bdc8b505402583f3d5b/707db16c-7f27-44f5-88ee-e5badc2a7ddd/LEVELS+LOGO.png?format=100w" type="image/png">
  <link rel="preconnect" href="https://images.squarespace-cdn.com" crossorigin>
  <link rel="dns-prefetch" href="https://cdn.jsdelivr.net">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400&family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700&family=Fraunces:ital,opsz,wght@0,9..144,100..900;1,9..144,100..900&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/site.css">
{preload_lines}</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
"""


def scripts_block(include_hls: bool) -> str:
    hls = (
        '  <script src="https://cdn.jsdelivr.net/npm/hls.js@1.5.7/dist/hls.min.js"></script>\n'
        if include_hls
        else ""
    )
    return f"""{hls}  <script src="assets/site.js"></script>
</body>
</html>
"""


def main() -> None:
    raw = INDEX.read_text(encoding="utf-8")

    # --- extract inner parts from current index ---
    home_part = extract_between(raw, '<section id="home"', '<div class="marquee-wrap"', None)
    marquees = extract_between(raw, '<div class="marquee-wrap"', '<div class="photo-strip photo-strip--a"', None)
    photo_a = extract_between(raw, '<div class="photo-strip photo-strip--a"', '<section id="services"', None)

    sec_services = extract_between(raw, '<section id="services"', '<section id="how-it-works"', None)
    sec_hiw = extract_between(raw, '<section id="how-it-works"', '<section id="booth"', None)
    sec_booth = extract_between(raw, '<section id="booth"', '<section id="package"', None)
    sec_pkg = extract_between(raw, '<section id="package"', '<section id="gallery"', None)
    sec_gal = extract_between(raw, '<section id="gallery"', '<section id="instagram"', None)
    sec_ig = extract_between(raw, '<section id="instagram"', '<div class="photo-strip photo-strip--b"', None)
    strip_b = extract_between(raw, '<div class="photo-strip photo-strip--b"', '<section id="why"', None)
    sec_why = extract_between(raw, '<section id="why"', '<section id="testimonials"', None)
    sec_test = extract_between(raw, '<section id="testimonials"', '<section id="booking"', None)
    sec_book = extract_between(raw, '<section id="booking"', "</main>", None)

    # --- apply copy fixes ---
    home_part = singular_copy(home_part)
    # Hero title + logo wordmark
    home_part = home_part.replace(
        """        <h1 class="hero-title">
          <span class="hero-title__line">Take your event to the</span>
          <span class="hero-title__gradient">next level</span>
        </h1>""",
        """        <h1 class="hero-title">
          <span class="hero-title__line">Take your event to the next</span>
          <span class="hero-title__brand">Level</span>
        </h1>""",
    )
    home_part = home_part.replace('href="#booking"', 'href="book.html"')
    home_part = home_part.replace('href="#services"', 'href="services.html"')

    sec_services = singular_copy(subpage_link_fixes(sec_services))
    sec_hiw = singular_copy(subpage_link_fixes(sec_hiw))
    sec_booth = singular_copy(subpage_link_fixes(sec_booth))
    sec_pkg = singular_copy(subpage_link_fixes(sec_pkg))
    sec_gal = singular_copy(subpage_link_fixes(sec_gal))
    sec_ig = singular_copy(subpage_link_fixes(sec_ig))
    strip_b = singular_copy(subpage_link_fixes(strip_b))
    sec_why = singular_copy(subpage_link_fixes(sec_why))
    sec_test = singular_copy(subpage_link_fixes(sec_test))
    sec_book = singular_copy(subpage_link_fixes(sec_book))
    sec_book = sec_book.replace("Reels on this page", "Reels on site")

    # Hamid caption on services
    sec_services = sec_services.replace(
        '<p class="section-kicker fade-in">What We Offer</p>',
        '<p class="section-kicker fade-in">What We Offer</p>\n        <p class="client-caption hamid-caption fade-in">Caption to follow — Hamid</p>',
        1,
    )

    # --- site.js from existing inline script (after hls.js) ---
    chunks = raw.split('<script src="https://cdn.jsdelivr.net/npm/hls.js@1.5.7/dist/hls.min.js"></script>', 1)
    if len(chunks) < 2:
        raise RuntimeError("hls.js script tag not found")
    tail = chunks[1]
    inner_script = tail.split("</script>", 1)[0]
    if not inner_script.strip().startswith("<script>"):
        raise RuntimeError("expected inline <script> after hls")
    inner_script = inner_script.replace("<script>", "", 1).strip()
    (ROOT / "assets" / "site.js").write_text(inner_script + "\n", encoding="utf-8")

    ld = re.search(r"<script type=\"application/ld\+json\">([\s\S]*?)</script>", raw)
    ld_block = f"  <script type=\"application/ld+json\">\n{ld.group(1).strip()}\n  </script>\n" if ld else ""

    index_body = f"""{head_variant(
        "Levels | 360 Video Booth, Photobooth Hire & Event Experiences | Scotland",
        "Levels — 360 videobooth, selfie booth, pancake cart, and chocolate fountain hire across Scotland. Book online.",
        "https://levels-website.vercel.app/",
        preload_hero=True,
    ).replace("</head>", ld_block + "</head>")}
{loader_block()}
{nav_block("home")}
  <main id="main">
{home_part}
{marquees}
{photo_a}
{hub_section()}
  </main>
{footer_block()}
  <script src="https://cdn.jsdelivr.net/npm/hls.js@1.5.7/dist/hls.min.js"></script>
  <script src="assets/site.js"></script>
</body>
</html>
"""
    INDEX.write_text(index_body, encoding="utf-8")

    def write_page(
        filename: str,
        active: str,
        title: str,
        desc: str,
        canonical: str,
        main_inner: str,
        include_hls: bool = False,
    ) -> None:
        page = (
            head_variant(title, desc, canonical, preload_hero=False).replace("</head>", ld_block + "</head>")
            + f"""
{loader_block()}
{nav_block(active)}
  <main id="main">
{main_inner}
  </main>
{footer_block()}
"""
            + scripts_block(include_hls=include_hls)
        )
        (ROOT / filename).write_text(page, encoding="utf-8")

    write_page(
        "services.html",
        "services",
        "Services | Levels — 360 videobooth, chocolate fountain, selfie booth, pancake cart | Scotland",
        "Four signature hire options for weddings and events in Scotland: 360 videobooth, chocolate fountain, selfie booth, pancake cart.",
        "https://levels-website.vercel.app/services.html",
        sec_services,
    )
    write_page(
        "how-it-works.html",
        "how",
        "How it works | Levels Event Hire | Scotland",
        "Enquire, get a quote, we set up, you celebrate — simple process for 360 videobooth and event hire in Scotland.",
        "https://levels-website.vercel.app/how-it-works.html",
        sec_hiw,
    )
    write_page(
        "360-videobooth.html",
        "booth",
        "360 videobooth | Levels | Scotland",
        "Professional 360 videobooth — HD slow-motion platform, crew, overlays, and travel across Scotland.",
        "https://levels-website.vercel.app/360-videobooth.html",
        sec_booth,
    )
    write_page(
        "package.html",
        "package",
        "The package | Levels 360 videobooth | Scotland",
        "Everything we bring on the night — props, overlays, attendants, and memories from your 360 videobooth booking.",
        "https://levels-website.vercel.app/package.html",
        sec_pkg,
    )
    write_page(
        "gallery.html",
        "gallery",
        "Gallery | Levels Event Hire | Scotland",
        "Recent setups — 360 videobooth, chocolate fountain, pancake cart, and branded hospitality across Scotland.",
        "https://levels-website.vercel.app/gallery.html",
        sec_gal,
    )
    instagram_main = sec_ig + "\n" + strip_b
    write_page(
        "instagram.html",
        "instagram",
        "Instagram & reels | Levels | Scotland",
        "Curated reels from the 360 videobooth, chocolate fountain, and pancake cart — Levels on Instagram.",
        "https://levels-website.vercel.app/instagram.html",
        instagram_main,
    )
    why_main = sec_why + "\n" + sec_test
    write_page(
        "why.html",
        "why",
        "Why Levels | FAQs & testimonials | Scotland",
        "Why book Levels — tailored service, experienced crew, calm logistics, and testimonials from Scottish weddings and events.",
        "https://levels-website.vercel.app/why.html",
        why_main,
    )
    write_page(
        "book.html",
        "book",
        "Book your event | Levels | Scotland",
        "Book 360 videobooth, chocolate fountain, selfie booth, or pancake cart — tell us your date and venue.",
        "https://levels-website.vercel.app/book.html",
        sec_book,
    )

    print("Wrote: index.html + services, how-it-works, 360-videobooth, package, gallery, instagram, why, book + assets/site.js")


if __name__ == "__main__":
    main()
