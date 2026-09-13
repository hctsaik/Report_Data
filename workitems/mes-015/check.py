from playwright.sync_api import sync_playwright
from pathlib import Path
import json
out=Path('tests/evidence/mes-015');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 results=[]
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},device_scale_factor=1)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/integrated-map.html?view=original');page.wait_for_function('window.ER_ATLAS')
  initial=page.evaluate('ER_ATLAS.getView()')
  assert page.locator('#canvas [data-node]').count()==121
  page.screenshot(path=str(out/f'{width}-overview.png'),full_page=True)
  for key in ['lot','carrier','equipment','flow','recipe']:
   page.locator(f'[data-entity={key}]').click()
   assert page.evaluate('ER_ATLAS.getView()')==initial
   assert page.locator('#entity-frames rect').count()>0,key
   assert page.evaluate("[...document.querySelectorAll('#canvas [data-node],#canvas [data-edge]')].every(n=>n.style.opacity==='1')")
   page.wait_for_function('document.getElementById("teaching-image").naturalWidth>0')
   page.screenshot(path=str(out/f'{width}-{key}.png'),full_page=True)
   page.locator('#open-teaching').click();assert page.locator('#teaching-dialog').is_visible()
   page.keyboard.press('Escape');assert not page.locator('#teaching-dialog').is_visible()
   page.locator('[data-target]').first.click();assert page.evaluate('ER_ATLAS.getView()')!=initial
  page.locator('#overview').click();assert page.evaluate('ER_ATLAS.getView()')==initial
  assert page.locator('#entity-frames').count()==0
  page.locator('[data-entity=lot]').click();page.set_viewport_size({'width':width-10,'height':900});page.wait_for_timeout(150)
  assert page.evaluate('ER_ATLAS.getView()')==initial
  assert page.locator('#entity-frames rect').count()>0
  for ref in ['2677:recipe','2673:lr-eqp']:
   page.evaluate('(r)=>ER_ATLAS.selectNode(ER_ATLAS.model.mapping[r])',ref)
   assert page.locator('#teaching-image').get_attribute('src')=='assets/mes-009/recipes.png'
  for ref in ['2675:eqp-oee','2677:eqp-id']:
   page.evaluate('(r)=>ER_ATLAS.selectNode(ER_ATLAS.model.mapping[r])',ref)
   assert 'L023' not in page.locator('#teaching-caption').inner_text()
  assert not errors,errors
  results.append({'width':width,'pass':True,'errors':errors})
 b.close()
(out/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(results)
