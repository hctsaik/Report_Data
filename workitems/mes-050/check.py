from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-050');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref in ['2675:eqp','2675:group-link','2675:chamber','2675:chamber-link','2675:virtual','2675:virtual-link','2675:eqp-oee','2675:eqp-oee-link','2675:group-oee','2675:group-oee-link','2675:group-history','2675:group-history-link']:
   page.evaluate('(r)=>ER_ATLAS.selectNode(ER_ATLAS.model.mapping[r])',ref)
   for term in ['KER','Report']:assert term in page.locator('#meaning').text_content()
  page.locator('#find').fill('KER_EMP_EQP_GRP_CAP_UT');nid=page.evaluate('ER_ATLAS.model.mapping["2675:eqp"]')
  btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
  page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
  page.locator('#selection-details').screenshot(path=str(out/f'{width}-lesson.png'))
  page.locator('#open-teaching').click();assert page.locator('#teaching-large').get_attribute('src').endswith('ker-overview-mobile-v1.png' if width==390 else 'ker-overview-v1.png')
  assert not errors,errors
  page.close()
 b.close()
print('PASS KER: entity/relationship, search click, desktop/mobile lesson and enlargement')
