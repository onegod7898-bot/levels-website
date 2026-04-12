from pathlib import Path
import re

p = Path(__file__).resolve().parent.parent / "index.html"
t = p.read_text(encoding="utf-8")
sub = "<p class=\"hero-services-sub\">All-in-one event experiences — from 360 Video Booth to catering setups.</p>"
t2, n = re.subn(r'<p class="hero-services-sub">[^<]*</p>', sub, t, count=1)
if n:
    p.write_text(t2, encoding="utf-8")
    print("fixed hero-services-sub")
else:
    print("no match")
