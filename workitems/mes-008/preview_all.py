from playwright.sync_api import sync_playwright
from pathlib import Path
r=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
 for chapter in ['architecture','decision','ai','history','join','contract']:
  page.goto('http://127.0.0.1:4175/freshness.html#'+chapter,wait_until='networkidle')
  page.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
  page.screenshot(path=str(r/f'tests/evidence/mes-008/precheck-{chapter}.png'),full_page=True)
  page.locator('.fresh-activity').screenshot(path=str(r/f'tests/evidence/mes-008/precheck-{chapter}-activity.png'),style='.topbar{visibility:hidden!important}')
  print(chapter,'screenshot',flush=True)
 b.close()
