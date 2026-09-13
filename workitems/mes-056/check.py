from pathlib import Path
from playwright.sync_api import sync_playwright
import json
out=Path('tests/evidence/mes-056');out.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(v,label):
 assert v,label
 checks.append(label)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html',wait_until='networkidle');page.wait_for_function('window.ER_ATLAS')
  check(page.locator('.map-side').bounding_box()['y']+page.locator('.map-side').bounding_box()['height']<=page.locator('#inspector').bounding_box()['y'],f'{width} vertical order')
  total=page.locator('#canvas [data-node]').count()
  for entity,ref in [('lot','2671:lot'),('carrier','2671:cast'),('equipment','2671:eqp'),('flow','2673:flow'),('recipe','2677:recipe')]:
   page.locator('[data-entity="'+entity+'"]').click()
   nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',ref)
   check(page.evaluate('ER_FOCUS.getState().root')==nid,f'{width}/{entity} lower sync')
   view=page.evaluate('ER_ATLAS.getView()')
   page.locator('#overview').click();check(page.evaluate('ER_ATLAS.getView()[2]')>view[2]*2,f'{width}/{entity} zoomed')
   full_width=page.evaluate('ER_ATLAS.getView()[2]')
   page.locator('#clear-entity').click()
   node=page.locator('#canvas [data-node="'+nid+'"]');page.locator('#canvas').evaluate('(el)=>window.scrollTo(0,el.getBoundingClientRect().top+scrollY-100)');page.wait_for_timeout(150);r=node.bounding_box()
   if width==390:page.touchscreen.tap(r['x']+r['width']/2,r['y']+r['height']/2)
   else:page.mouse.click(r['x']+r['width']/2,r['y']+r['height']/2)
   page.wait_for_timeout(200)
   check(page.evaluate('ER_FOCUS.getState().root')==nid,f'{width}/{entity} actual click')
   check(page.evaluate('ER_ATLAS.getView()[2]')<full_width/2,f'{width}/{entity} click zoom')
   page.locator('#map-subject').evaluate('(el)=>el.scrollIntoView({block:"start",behavior:"instant"})');page.screenshot(path=str(out/f'{entity}-map-{width}.png'))
   page.locator('#inspector').evaluate('(el)=>el.scrollIntoView({block:"start",behavior:"instant"})');page.screenshot(path=str(out/f'{entity}-lesson-{width}.png'))
  # Every source node uses the same focus behavior; this supplements real clicks.
  for nid in page.evaluate('ER_ATLAS.model.nodes.map(n=>n.id)'):
   result=page.evaluate('''id=>{ER_ATLAS.selectNode(id);const b=ER_ATLAS.box(id),v=ER_ATLAS.getView();return {root:ER_FOCUS.getState().root,center:Math.abs(b.x+b.w/2-v[0]-v[2]/2)<1&&Math.abs(b.y+b.h/2-v[1]-v[3]/2)<1}}''',nid)
   check(result['root']==nid and result['center'],f'{width}/{nid} centered and sync')
  check(page.locator('#canvas [data-node]').count()==total,f'{width} all nodes retained')
  for route_id in page.locator('#routes [data-route]').evaluate_all('(bs)=>bs.map(b=>b.dataset.route)'):
   page.evaluate('(r)=>ER_ATLAS.route(r)',route_id)
   check(page.evaluate('ER_FOCUS.getState().root!==null') and not page.locator('#focus-current').is_disabled(),f'{width}/{route_id} route focus')
  page.locator('#step-next').click()
  check(page.evaluate('ER_FOCUS.getState().root===ER_ATLAS.getWalk()[1]'),f'{width} step sync')
  target=page.locator('#focus-graph [data-focus-node]').last
  target_id=target.get_attribute('data-focus-node');target.click()
  check(page.evaluate('ER_FOCUS.getState().root')==target_id,f'{width} lower graph click sync')
  page.locator('#find').fill('Qtime');page.locator('#search-results button').first.click()
  root=page.evaluate('ER_FOCUS.getState().root');view=page.evaluate('ER_ATLAS.getView()')
  page.locator('#zoom-in').click();check(page.evaluate('ER_ATLAS.getView()[2]')<view[2],f'{width} manual zoom')
  page.locator('#overview').click();check(page.evaluate('ER_FOCUS.getState().root')==root,f'{width} overview preserves lesson')
  page.locator('#focus-current').click();check(abs(page.evaluate('ER_ATLAS.getView()[2]')-view[2])<1,f'{width} restore subject zoom')
  page.locator('#inspector-expand').click();check(page.locator('#inspector-dialog').evaluate('(d)=>d.open'),f'{width} enlarge introduction')
  page.keyboard.press('Escape');page.locator('.workspace > #inspector').wait_for();check(page.locator('.workspace > #inspector').count()==1,f'{width} restore introduction')
  page.goto('http://127.0.0.1:4175/er-atlas.html?erNode='+root,wait_until='networkidle');page.wait_for_function('window.ER_ATLAS')
  check(page.evaluate('ER_FOCUS.getState().root')==root,f'{width} deep link')
  page.locator('[data-entity="flow"]').click();page.locator('#er-back').click();page.wait_for_timeout(300)
  check(page.evaluate('ER_FOCUS.getState().root')==root,f'{width} back restores subject')
  check(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'{width} no overflow')
  page.close()
 check(not errors,'No JavaScript errors')
 b.close()
(out/'checks.json').write_text(json.dumps({'count':len(checks),'checks':checks,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS',len(checks))
