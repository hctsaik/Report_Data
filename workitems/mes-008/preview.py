from playwright.sync_api import sync_playwright
from pathlib import Path
r=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,360]:
  page=b.new_page(viewport={'width':width,'height':1000 if width==1440 else 844})
  page.on('pageerror',lambda e:print('ERROR',e))
  page.goto('http://127.0.0.1:4175/freshness.html#ai',wait_until='networkidle')
  page.screenshot(path=str(r/f'tests/evidence/mes-008/preview-ai-{width}.png'),full_page=True)
  print(width,page.evaluate('document.documentElement.scrollWidth'),page.locator('.lesson-art img').bounding_box())
  page.locator('.fresh-activity').screenshot(path=str(r/f'tests/evidence/mes-008/preview-ai-{width}-activity.png'),style='.topbar{visibility:hidden!important}')
 b.close()
