from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-038');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref in ['2672:history','2675:history','2672:all-actions','2675:all-actions']:
   page.evaluate('(r)=>ER_ATLAS.selectNode(ER_ATLAS.model.mapping[r])',ref)
   for term in ['批貨歷史','Hold','Process','Split']:assert term in page.locator('#meaning').text_content()
  page.locator('#find').fill('FHOPEHS_S');nid=page.evaluate('ER_ATLAS.model.mapping["2672:history"]')
  btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
  page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
  page.locator('#selection-details').screenshot(path=str(out/f'{width}-lesson.png'))
  page.locator('#open-teaching').click();assert page.locator('#teaching-large').get_attribute('src').endswith('lot-history-mobile-v1.png' if width==390 else 'lot-history-v2.png');page.keyboard.press('Escape')
  assert not errors,errors
 b.close()
print('PASS Lot action history refs, desktop/mobile image/dialog and real selection')
