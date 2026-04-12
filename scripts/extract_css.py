"""Extract first <style> block from index.html to assets/site.css and replace with <link>. UTF-8 safe."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
index = ROOT / "index.html"
text = index.read_text(encoding="utf-8")
start = text.index("<style>")
end = text.index("</style>") + len("</style>")
css = text[start + len("<style>") : end - len("</style>")].strip() + "\n"
(ROOT / "assets").mkdir(exist_ok=True)
(ROOT / "assets" / "site.css").write_text(css, encoding="utf-8")
replacement = '  <link rel="stylesheet" href="assets/site.css">'
new_text = text[:start] + replacement + "\n" + text[end:]
index.write_text(new_text, encoding="utf-8")
print("OK: assets/site.css written, index.html updated")
