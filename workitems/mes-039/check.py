from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-039');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref in ['2672:move','2675:move','2672:move-link','2675:move-link']:
   page.evaluate('(r)=>ER_ATLAS.selectNode(ER_ATLAS.model.mapping[r])',ref)
   for term in ['進機事件','一筆','廠區','DM_MOVE_STEP']:assert term in page.locator('#meaning').text_content()
  page.locator('#find').fill('DM_Move_Step');nid=page.evaluate('ER_ATLAS.model.mapping["2672:move"]')
  btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
  page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
  page.locator('#selection-details').screenshot(path=str(out/f'{width}-lesson.png'))
  page.locator('#open-teaching').click();assert page.locator('#teaching-large').get_attribute('src').endswith('move-uses-mobile-v2.png' if width==390 else 'move-uses-v2.png');page.keyboard.press('Escape')
  page.locator('#routes [data-route="move"]').click();assert '進機事件' in page.locator('#meaning').text_content()
  assert not errors,errors
 b.close()
print('PASS Move history refs, route, entry definition and two uses, desktop/mobile images')
