from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];out=R/'tests/evidence/mes-012';out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1390,'height':920})
 page.goto('http://127.0.0.1:4175/ER/INTEGRATED/fab-integrated.svg')
 page.evaluate("document.documentElement.setAttribute('width','1390');document.documentElement.setAttribute('height','890')")
 page.screenshot(path=str(out/'prototype.png'))
 b.close()
