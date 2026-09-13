from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-044');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref in ['2673:stage','2673:stage-link']:
   page.evaluate('(r)=>ER_ATLAS.selectNode(ER_ATLAS.model.mapping[r])',ref)
   for term in ['黃光','多個 Stage','Step']:assert term in page.locator('#meaning').text_content()
  page.locator('#find').fill('dm_tbl_info_stage');nid=page.evaluate('ER_ATLAS.model.mapping["2673:stage"]')
  btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
  page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
  page.locator('#selection-details').screenshot(path=str(out/f'{width}-lesson.png'))
  page.locator('#open-teaching').click();assert page.locator('#teaching-large').get_attribute('src').endswith('module-stage-step-mobile-v2.png' if width==390 else 'module-stage-step-v2.png')
  assert not errors,errors
  page.close()
 b.close()
print('PASS Stage Module: entity/relationship, search click, desktop/mobile lesson and enlargement')
