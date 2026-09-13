from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-035');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref in ['2671:port-link','2671:port','2671:has','2674:port','2674:port-link','2676:port','2676:port-id']:
   page.evaluate('(r)=>ER_ATLAS.selectNode(ER_ATLAS.model.mapping[r])',ref)
   for t in ['Load Port','OHT','Wafer','等待加工','搬離']:assert t in page.locator('#meaning').text_content()
  page.locator('#find').fill('Siview.Port');nid=page.evaluate('ER_ATLAS.model.mapping["2671:port"]')
  btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
  page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
  page.locator('#selection-details').screenshot(path=str(out/f'{width}-lesson.png'))
  page.locator('#open-teaching').click();assert page.locator('#teaching-large').get_attribute('src').endswith('load-port-mobile-v1.png' if width==390 else 'load-port-v1.png');page.keyboard.press('Escape')
  page.locator('#routes [data-route="port"]').click();assert '暫置' in page.locator('#meaning').text_content()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  assert not errors,errors
 b.close()
print('PASS seven Port refs, route, desktop/mobile figure and real selection')
