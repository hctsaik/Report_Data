from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-028');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html?subject=wph');page.wait_for_function('window.ER_ATLAS&&history.state?.mesErNav')
  assert page.locator('#er-back').is_disabled()
  wph=page.evaluate('ER_ATLAS.model.mapping["2673:wph"]')
  target=page.locator('#focus-graph [data-focus-node]').last;target.tap() if width==390 else target.click()
  assert page.locator('#er-back').is_enabled()
  page.locator('#er-back').click();page.wait_for_function('(id)=>ER_FOCUS.getState().root===id',arg=wph)
  assert page.locator('#selection-details').get_attribute('data-topic')=='wph'
  page.locator('[data-entity="lot"]').click()
  # Nested overview() must not add an extra history entry.
  assert page.evaluate('history.state.mesErNav.index')==1
  page.locator('#focus-more button').nth(1).click()
  view=page.evaluate('ER_ATLAS.getView()')
  oldroot=page.evaluate('ER_FOCUS.getState().root')
  target=page.locator('#focus-graph [data-focus-node]').last;target.tap() if width==390 else target.click()
  page.locator('#er-back').click();page.wait_for_function('(id)=>ER_FOCUS.getState().root===id',arg=oldroot)
  assert page.evaluate('ER_FOCUS.getState().page')==1
  assert page.evaluate('ER_ATLAS.getView()')==view
  page.locator('#inspector-expand').click()
  page.locator('#focus-expand').click()
  target=page.locator('#focus-large [data-focus-node]').last;target.tap() if width==390 else target.click()
  page.locator('#er-large-back').click();page.wait_for_function('(id)=>ER_FOCUS.getState().root===id',arg=oldroot)
  assert page.evaluate('ER_FOCUS.getState().page')==1
  page.keyboard.press('Escape');assert page.locator('#inspector-dialog').is_visible()
  page.keyboard.press('Escape')
  page.locator('#find').fill('Qtime');qid=page.evaluate('ER_ATLAS.model.mapping["2672:qtime"]')
  page.locator(f'[data-result="{qid}"]').click()
  page.locator('#teaching-link').click();page.wait_for_url('**/advanced.html?erReturn=*')
  back=page.locator('[data-er-return]')
  # Return control exposed by the shared destination script.
  if not back.count():back=page.get_by_role('link',name='返回 ER',exact=False)
  back.first.click();page.wait_for_function('window.ER_ATLAS&&history.state?.mesErNav')
  assert page.evaluate('ER_FOCUS.getState().root')==qid
  assert page.locator('#er-back').is_enabled()
  page.locator('#er-back').click();page.wait_for_function('(id)=>ER_FOCUS.getState().root===id',arg=oldroot)
  page.go_forward();page.wait_for_function('(id)=>ER_FOCUS.getState().root===id',arg=qid)
  page.reload();page.wait_for_function('window.ER_ATLAS&&history.state?.mesErNav')
  assert page.evaluate('ER_FOCUS.getState().root')==qid
  page.go_back();page.wait_for_function('(id)=>ER_FOCUS.getState().root===id',arg=oldroot)
  assert page.evaluate('ER_FOCUS.getState().page')==1
  page.locator('#routes [data-route="qtime"]').click();page.locator('#step-next').click()
  route_view=page.evaluate('ER_ATLAS.getView()');step=page.locator('#step-label').text_content()
  page.locator('#find').fill('CSFRPREDISPATCH');pid=page.evaluate('ER_ATLAS.model.mapping["2671:predispatch"]')
  page.locator(f'[data-result="{pid}"]').click();page.locator('#er-back').click()
  page.wait_for_function('(id)=>ER_FOCUS.getState().root===id',arg=qid)
  assert page.evaluate('ER_ATLAS.getView()')==route_view
  assert page.locator('#step-label').text_content()==step
  page.locator('#inspector').screenshot(path=str(out/f'{width}-navigation.png'))
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  assert not errors,errors
 b.close()
print('PASS: desktop/mobile subject back, group/view restore, nested dialogs, lesson round trip')
