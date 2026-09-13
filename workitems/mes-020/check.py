from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-020');out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html?subject=wph');page.wait_for_function('window.ER_ATLAS')
  root=page.evaluate('ER_FOCUS.getState().root');old=page.locator('#inspector').bounding_box()['width']
  button=page.locator('#inspector-expand')
  if width==390:button.tap()
  else:button.click()
  assert page.locator('#inspector-dialog').is_visible()
  assert page.locator('#inspector-dialog #inspector').count()==1
  assert page.locator('#selection-details').get_attribute('open') is not None
  assert page.evaluate('ER_FOCUS.getState().root')==root
  if width==1440:assert page.locator('#inspector').bounding_box()['width']>old*1.5
  page.locator('#inspector-dialog').screenshot(path=str(out/f'{width}-expanded.png'))
  page.locator('#meaning').scroll_into_view_if_needed()
  page.locator('#inspector-dialog').screenshot(path=str(out/f'{width}-explanation.png'))
  page.locator('#open-teaching').click();assert page.locator('#teaching-dialog').is_visible()
  page.keyboard.press('Escape');assert page.locator('#inspector-dialog').is_visible()
  page.locator('#inspector-expand').click();assert not page.locator('#inspector-dialog').is_visible()
  assert page.locator('.workspace > #inspector').count()==1
  assert page.evaluate('ER_FOCUS.getState().root')==root
  page.locator('[data-entity="lot"]').click()
  page.locator('#selection-details').evaluate('(d)=>d.open=false')
  page.locator('#focus-more button').last.click();index=page.evaluate('ER_FOCUS.getState().page')
  page.locator('#inspector-expand').click()
  assert page.evaluate('ER_FOCUS.getState().page')==index
  page.keyboard.press('Escape')
  assert not page.locator('#inspector-dialog').is_visible()
  assert page.locator('#selection-details').get_attribute('open') is None
  assert page.evaluate('ER_FOCUS.getState().page')==index
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  assert not errors,errors
  results.append({'width':width,'expand_return_escape_nested_image':'pass','subject_and_page_preserved':True,'errors':errors})
 b.close()
(out/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
