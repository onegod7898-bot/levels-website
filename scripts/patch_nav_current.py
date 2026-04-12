from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for name in ("services.html", "how-it-works.html", "360-videobooth.html"):
    p = ROOT / name
    t = p.read_text(encoding="utf-8")
    t = t.replace(
        '<div class="nav-dropdown" id="navDropdown">',
        '<div class="nav-dropdown nav-dropdown--current" id="navDropdown">',
        1,
    )
    p.write_text(t, encoding="utf-8")
    print("patched", name)
