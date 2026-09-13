from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-032');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  page.locator('#find').fill('Chamber');nid=page.evaluate('ER_ATLAS.model.mapping["2674:chamber"]')
  btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
  assert page.locator('#teaching-link').get_attribute('href')=='operations.html#chamber'
  for term in ['CH-A','CH-B','procrsc_id','Wafer']:assert term in page.locator('#topic-detail').text_content()
  page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
  page.locator('#selection-details').screenshot(path=str(out/f'{width}-lesson.png'))
  page.locator('#open-teaching').click();assert page.locator('#teaching-large').get_attribute('src').endswith('chamber-mobile-v1.png' if width==390 else 'chamber-v1.png');page.keyboard.press('Escape')
  page.locator('#teaching-link').click();page.wait_for_url('**/operations.html?erReturn=*')
  assert 'L023' in page.locator('#lesson-container h1').text_content()
  page.locator('#return-to-er').click();page.wait_for_function('window.ER_ATLAS&&history.state?.mesErNav')
  assert page.evaluate('ER_FOCUS.getState().root')==nid
  for ref in ['2674:chamber-link','2674:detail-link','2674:chamber-detail','2676:chamber']:
   page.evaluate('(r)=>ER_ATLAS.selectNode(ER_ATLAS.model.mapping[r])',ref)
   assert page.locator('#teaching-link').get_attribute('href')=='operations.html#chamber'
  assert not errors,errors
 b.close()
print('PASS Chamber five refs, illustrations, full lesson and return, desktop/mobile')
