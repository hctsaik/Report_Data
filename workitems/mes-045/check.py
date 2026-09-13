from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-045');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref in ['2673:srts','2673:srts-link']:
   page.evaluate('(r)=>ER_ATLAS.selectNode(ER_ATLAS.model.mapping[r])',ref)
   for term in ['Sampling rule','Part','30%']:assert term in page.locator('#meaning').text_content()
  page.locator('#find').fill('csfrsrts');nid=page.evaluate('ER_ATLAS.model.mapping["2673:srts"]')
  btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
  page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
  page.locator('#selection-details').screenshot(path=str(out/f'{width}-lesson.png'))
  page.locator('#open-teaching').click();assert page.locator('#teaching-large').get_attribute('src').endswith('srts-sampling-mobile-v2.png' if width==390 else 'srts-sampling-v1.png')
  assert not errors,errors
  page.close()
 b.close()
print('PASS SRTS: entity/relationship, search click, desktop/mobile lesson and enlargement')
