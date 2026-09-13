from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-031');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref in ['2672:mcs-history','2672:mcs-transfer']:
   page.locator('#find').fill('MCS');nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',ref)
   btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
   for term in ['Macro','Micro','E2E','轉彎','FOUP']:assert term in page.locator('#meaning').text_content()
   assert page.locator('#selection-details').get_attribute('data-topic')=='mcs'
   for i in range(4):
    page.locator(f'[data-mcs-event="{i}"]').click()
    assert f'10:0{i}' in page.locator('.mcs-event-detail').text_content()
    assert ['起點 A','轉彎 B','轉彎 C','終點 D'][i] in page.locator('.mcs-event-detail').text_content()
   page.locator('[data-mcs-event="1"]').click()
   assert '轉彎 B → 轉彎 C' in page.locator('.mcs-event-detail').text_content()
  page.locator('#mcs-command-demo').screenshot(path=str(out/f'{width}-trace.png'))
  page.locator('#selection-details').screenshot(path=str(out/f'{width}-lesson.png'))
  page.locator('#inspector-expand').click();assert page.locator('#inspector-dialog [data-mcs-event="1"]').get_attribute('aria-pressed')=='true';page.keyboard.press('Escape')
  page.locator('#routes [data-route="transfer"]').click();assert 'Macro' in page.locator('#meaning').text_content()
  page.evaluate('ER_ATLAS.selectNode(ER_ATLAS.model.mapping["2672:mes-transfer"])')
  assert page.locator('#mcs-command-demo').count()==0
  assert page.locator('#selection-details').get_attribute('data-topic')=='transfer'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  assert not errors,errors
 b.close()
print('PASS MCS nodes, four events, route, MES separation, desktop/mobile/expand')
