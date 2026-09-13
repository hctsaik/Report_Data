from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-037');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref,query in [('2672:predispatch','CSFHPREDISP'),('2672:pre-link','預派機台')]:
   page.locator('#find').fill(query);nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',ref)
   btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
   for term in ['預先知道','Lot_ID','不代表已經開工']:assert term in page.locator('#meaning').text_content()
   assert page.locator('#selection-details').get_attribute('data-topic')=='prehistory'
   page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
   page.locator('#open-teaching').click();assert page.locator('#teaching-large').get_attribute('src').endswith('predispatch-history-mobile-v1.png' if width==390 else 'predispatch-history-v2.png');page.keyboard.press('Escape')
   page.locator('#selection-details').screenshot(path=str(out/f'{width}-{ref.split(":")[1]}.png'))
  assert not errors,errors
 b.close()
print('PASS predispatch history two refs, desktop/mobile text/images/dialog and real selection')
