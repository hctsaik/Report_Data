from playwright.sync_api import sync_playwright
from pathlib import Path
import json
out=Path('tests/evidence/mes-016');out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/integrated-map.html?view=original');page.wait_for_function('window.ER_ATLAS')
  for ref,key in [('2671:lot','Lot'),('2671:cast','FOUP'),('2671:eqp','EQP'),('2673:flow','Flow'),('2677:recipe','Recipe')]:
   page.locator('#overview').click()
   nid=page.evaluate('(ref)=>ER_ATLAS.model.mapping[ref]',ref)
   node=page.locator(f'[data-node="{nid}"]');node.scroll_into_view_if_needed();page.wait_for_timeout(200);r=node.bounding_box()
   x=r['x']+r['width']/2;y=r['y']+r['height']/2
   print(width,key,page.evaluate('([x,y])=>document.elementFromPoint(x,y).outerHTML',[x,y])[:200])
   if width==390:page.touchscreen.tap(x,y)
   else:page.mouse.click(x,y)
   assert key in page.locator('#teaching-current').inner_text(),(width,key,page.locator('#teaching-current').inner_text(),page.locator('#selection-title').inner_text(),page.evaluate('(id)=>teachingForNode(id)',nid),errors)
   assert page.locator('#selection-title').inner_text()!='完整 ER × 現場物件'
   assert page.locator('#teaching-focus').is_visible()==(key in ['Lot','FOUP','EQP'])
   page.locator('#inspector').screenshot(path=str(out/f'{width}-{key}.png'))
  # Miss the node by 5 px: still select it, using real pointer input.
  page.locator('#overview').click();nid=page.evaluate('ER_ATLAS.model.mapping["2671:lot"]')
  node=page.locator(f'[data-node="{nid}"]');node.scroll_into_view_if_needed();page.wait_for_timeout(200);r=node.bounding_box()
  page.mouse.click(r['x']+r['width']+3 if width==1440 else r['x']+r['width']/2,r['y']+r['height']/2)
  assert 'Lot' in page.locator('#teaching-current').inner_text(),(page.locator('#selection-title').inner_text(),r)
  page.locator('#open-teaching').click();assert page.locator('#teaching-large-focus').is_visible();page.keyboard.press('Escape')
  page.locator('#overview').click();node.scroll_into_view_if_needed();page.wait_for_timeout(200);r=node.bounding_box()
  page.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2);page.mouse.down();page.mouse.move(r['x']+70,r['y']+50,steps=6);page.mouse.up()
  assert page.locator('#selection-title').inner_text()=='完整 ER × 現場物件'
  assert not errors,errors
  results.append({'width':width,'real_pointer_checks':'passed','errors':errors})
 b.close()
(out/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
