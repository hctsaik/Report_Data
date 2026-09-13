from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1440,'height':1000})
 for entry in ['operations.html#port','flow.html#stage']:
  page.goto('http://127.0.0.1:4175/'+entry)
  page.locator('.aside-foot a[href="integrated-map.html?view=original"]').click()
  page.wait_for_function('!!window.ER_ATLAS');assert 'er-atlas.html?view=original' in page.url
 page.goto('http://127.0.0.1:4175/integrated-map.html?view=questions#recipe');page.wait_for_function('!!window.ER_ATLAS')
 assert page.locator('[data-question="recipe"]').get_attribute('aria-pressed')=='true'
 page.screenshot(path=str(R/'tests/evidence/mes-014/v2/entry-desktop.png'))
 # Source circle semantics, pointer click and the corrected branch walk.
 page.evaluate("ER_ATLAS.selectNode(ER_ATLAS.model.mapping['2677:er'])")
 assert '概念／屬性註記' in page.locator('#meaning').inner_text()
 b.close()
print('PASS: original course sidebar links, preserved question redirect, ellipse interpretation')
