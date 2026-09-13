from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-017')
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [390,360,950]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  page.locator('[data-entity="equipment"]').click();page.locator('#focus-more button').nth(1).click()
  assert page.evaluate('ER_FOCUS.getState().page===1')
  page.locator('#focus-panel').screenshot(path=str(out/f'{width}-equipment-page2.png'))
  # Keyboard and touch on the small graph must both change the subject.
  for method in ['keyboard','touch']:
   page.locator('[data-entity="lot"]').click();g=page.locator('#focus-graph [data-focus-node]').nth(2);nid=g.get_attribute('data-focus-node')
   if method=='keyboard':g.focus();page.keyboard.press('Enter')
   else:g.tap()
   assert page.evaluate('(id)=>ER_FOCUS.getState().root===id',nid)
  # Distinct unqualified source positions can become their own root.
  page.locator('[data-entity="lot"]').click();page.locator('#selection-details summary').click()
  g=page.locator('[data-target]').last;nid=g.get_attribute('data-target');g.click()
  assert page.evaluate('(id)=>ER_FOCUS.getState().root===id',nid)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  results.append({'width':width,'keyboard_touch_secondary_root':'pass'})
  page.close()
 b.close()
(out/'final-checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
