from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];O=R/'tests/evidence/mes-014';O.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1500,'height':1050})
 for name in ['er-prototype-v1','fab-er-v1']:
  page.goto('http://127.0.0.1:4175/ER/INTEGRATED/'+name+'.svg')
  page.evaluate("document.documentElement.setAttribute('width','1500');document.documentElement.setAttribute('height','1050')")
  page.screenshot(path=str(O/(name+'.png')))
 b.close()
