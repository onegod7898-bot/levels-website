from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "index.html"
t = p.read_text(encoding="utf-8")

# Move h2 inside .hero-service-card__media (before closing </div> of media)
t = re.sub(
    r'(<div class="hero-service-card__overlay"></div>)\s*</div>\s*<h2 class="hero-service-card__title">([^<]+)</h2>',
    r'\1\n                  <h2 class="hero-service-card__title">\2</h2>\n                </div>',
    t,
)

# Dots after grid
t = t.replace(
    """          </div>
        </div>
      </div>
    </section>

    
<div class="marquee-wrap" aria-hidden="true">""",
    """          </div>
          <div class="hero-services__dots" data-hero-dots aria-label="Service slides"></div>
        </div>
      </div>
    </section>

    
<div class="marquee-wrap" aria-hidden="true">""",
)

# Fix common mojibake em dash
t = t.replace("\u2014", "\u2014")  # no-op if already correct
t = t.replace("All-in-one event experiences ?", "All-in-one event experiences —")

p.write_text(t, encoding="utf-8")
print("OK")
