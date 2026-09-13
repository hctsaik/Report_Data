from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-019');out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html?view=original&subject=wph');page.wait_for_function('window.ER_ATLAS')
  for ref in ['2673:wph','2673:wph-link']:
   page.locator('#overview').click()
   page.locator('#find').fill('WPH')
   nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',ref)
   item=page.locator(f'[data-result="{nid}"]')
   if width==390:item.tap()
   else:item.click()
   assert page.locator('#selection-details').get_attribute('open') is not None
   assert '生管' in page.locator('#selection-title').inner_text()
   assert '生產管理部門' in page.locator('#meaning').inner_text()
   assert page.locator('#teaching-image').get_attribute('src')=='assets/mes-019/group-wph-v1.png'
   page.wait_for_function('document.getElementById("teaching-image").naturalWidth>0')
   page.locator('#selection-details').screenshot(path=str(out/f'{width}-{ref.split(":")[1]}.png'))
   page.locator('#open-teaching').click();assert page.locator('#teaching-dialog').is_visible()
   assert page.locator('#teaching-large').get_attribute('src').endswith('assets/mes-019/group-wph-mobile-v1.png' if width==390 else 'assets/mes-019/group-wph-v1.png')
   page.locator('#teaching-dialog').screenshot(path=str(out/f'{width}-large-{ref.split(":")[1]}.png'));page.keyboard.press('Escape')
  page.locator('[data-entity="lot"]').click()
  assert page.locator('#teaching-image').get_attribute('src')=='examples/fab-physical-data-v01.png'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  assert not errors,errors
  results.append({'width':width,'wph_node_and_relation':'pass','image_and_dialog':'pass','lot_reference_unchanged':True,'errors':errors})
 b.close()
(out/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
