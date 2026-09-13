from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'tests/evidence/mes-017';OUT.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/integrated-map.html?view=original');page.wait_for_function('window.ER_ATLAS')
  for key,ref in [('lot','2671:lot'),('carrier','2671:cast'),('equipment','2671:eqp'),('flow','2673:flow'),('recipe','2677:recipe')]:
   button=page.locator(f'[data-entity="{key}"]')
   if width==390:button.tap()
   else:button.click()
   assert page.evaluate('(r)=>ER_FOCUS.getState().root===ER_ATLAS.model.mapping[r]',ref)
   assert page.locator('#focus-graph [data-focus-node]').count()>1
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   assert page.evaluate('''()=>[...document.querySelectorAll('#focus-graph text')].every(t=>{const r=t.getBoundingClientRect(),s=t.closest('svg').getBoundingClientRect();return r.left>=s.left-1&&r.right<=s.right+1})''')
   page.locator('#focus-panel').screenshot(path=str(OUT/f'{width}-{key}.png'))
   page.screenshot(path=str(OUT/f'{width}-{key}-page.png'),full_page=True)
   if key=='recipe':assert page.evaluate('ER_FOCUS.getState().branches.some(b=>b.ids.includes(ER_ATLAS.model.mapping["2677:eqp"]))')
   page.locator('#focus-expand').click();assert page.locator('#focus-dialog').is_visible();assert page.locator('#focus-large [data-focus-node]').count()>1;page.keyboard.press('Escape')
   # Actual mouse/touch on the full ER, after reset.
   page.locator('#overview').click()
   nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',ref)
   node=page.locator(f'#canvas [data-node="{nid}"]');node.scroll_into_view_if_needed();page.wait_for_timeout(250);r=node.bounding_box()
   x=r['x']+r['width']/2;y=r['y']+r['height']/2
   if width==390:page.touchscreen.tap(x,y)
   else:page.mouse.click(x,y)
   assert page.evaluate('(id)=>ER_FOCUS.getState().root===id',nid),(width,key,page.evaluate('ER_FOCUS.getState().root'),nid)
   results.append(f'{width}/{key}: subject button, actual ER pointer, dialog, screenshot')
  # Related entity becomes new subject using actual interaction.
  page.locator('[data-entity="lot"]').click()
  item=page.locator('#focus-graph [data-focus-node]').nth(2);target=item.get_attribute('data-focus-node');item.click()
  assert page.evaluate('(id)=>ER_FOCUS.getState().root===id',target)
  page.locator('#find').fill('FRMRCP');page.locator('[data-result]').first.click()
  assert 'FRMRCP' in page.locator('#focus-graph').inner_text()
  # Every collected edge is present in source and matches consecutive nodes.
  audit=page.evaluate('''()=>{let paths=0;for(const n of ER_ATLAS.model.nodes){ER_FOCUS.show(n.id);for(const b of ER_FOCUS.getState().branches){paths++;if(b.ids[0]!==n.id||b.edges.length!==b.ids.length-1)throw Error('branch');b.edges.forEach((id,i)=>{const e=ER_ATLAS.model.edges.find(e=>e.id===id);if(!e||!((e.a===b.ids[i]&&e.b===b.ids[i+1])||(e.b===b.ids[i]&&e.a===b.ids[i+1])))throw Error('edge');});}}return paths;}''')
  page.locator('[data-entity="flow"]').click()
  if page.locator('#focus-more button').count()>1:
   page.locator('#focus-more button').last.click();assert page.evaluate('ER_FOCUS.getState().page>0')
  page.locator('#clear-entity').click();assert page.locator('#focus-graph [data-focus-node]').count()==0
  assert not errors,errors
  results.append({'width':width,'all_node_paths':audit,'errors':errors})
  page.close()
 b.close()
(OUT/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))
