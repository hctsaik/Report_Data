from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-029');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html?subject=pd');page.wait_for_function('window.ER_ATLAS&&history.state?.mesErNav')
  assert 'Process Definition' in page.locator('#focus-title').text_content()
  for ref in ['2673:pd','2673:pd-eqp','2673:pd-eqp-link','2673:pd-link','2677:pd','2677:pd-key','2677:pd-eqp']:
   page.evaluate('(ref)=>ER_ATLAS.selectNode(ER_ATLAS.model.mapping[ref])',ref)
   for term in ['Process Definition','細部加工定義','Recipe','Tool']:assert term in page.locator('#meaning').text_content(),(ref,term)
   assert page.locator('#selection-details').get_attribute('data-topic')=='pd'
   assert page.locator('#teaching-image').get_attribute('src')=='assets/mes-029/pd-definition-v2.png'
  page.locator('#find').fill('Siview.frpd');nid=page.evaluate('ER_ATLAS.model.mapping["2673:pd"]')
  btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
  page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
  page.locator('#focus-panel').screenshot(path=str(out/f'{width}-graph.png'))
  page.locator('#selection-details').screenshot(path=str(out/f'{width}-lesson.png'))
  page.locator('#open-teaching').click();assert page.locator('#teaching-large').get_attribute('src').endswith('pd-definition-mobile-v1.png' if width==390 else 'pd-definition-v2.png');page.keyboard.press('Escape')
  page.locator('#routes [data-route="pd"]').click();assert 'Process Definition' in page.locator('#meaning').text_content()
  page.locator('[data-entity="lot"]').click();assert 'PD-A' not in page.locator('#topic-detail').text_content()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  assert not errors,errors
 b.close()
print('PASS: seven PD refs, route, desktop/mobile illustration, real search selection, reset')
