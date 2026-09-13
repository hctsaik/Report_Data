from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-026');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={'width':1440,'height':1000})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
 audit=page.evaluate('''()=>ER_ATLAS.model.nodes.map(n=>{
  ER_ATLAS.selectNode(n.id);const d=document.getElementById('selection-details'),img=document.getElementById('teaching-image');
  return {id:n.id,refs:n.refs.map(r=>r.source+':'+r.node),topic:d.dataset.topic,title:document.getElementById('selection-title').textContent,meaning:document.getElementById('meaning').textContent,image:img.getAttribute('src'),visibleImage:!document.querySelector('.teaching-figure').hidden};
 })''')
 for row in audit:
  assert row['topic']!='overview',row
  assert len(row['meaning'])>20,row
  if row['image']=='examples/fab-physical-data-v01.png':assert row['topic'] in ['lot','carrier','equipment'],row
  if row['topic']=='source':assert not row['visibleImage'] and row['image'] is None,row
 routes=[]
 for button in page.locator('#routes [data-route]').all():
  rid=button.get_attribute('data-route');button.click()
  topic=page.locator('#selection-details').get_attribute('data-topic')
  assert topic not in ['overview','source','lot','carrier','equipment'],(rid,topic)
  routes.append({'route':rid,'topic':topic})
 assert not errors,errors
 (out/'teaching-audit.json').write_text(json.dumps({'nodes':audit,'routes':routes},ensure_ascii=False,indent=2),encoding='utf-8')
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref,expected in [('2671:lot','lot'),('2671:cast','carrier'),('2671:eqp','equipment'),('2673:flow','flow'),('2677:recipe','recipe'),('2673:future','future'),('2672:qtime','qtime')]:
   page.locator('#overview').click()
   nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',ref)
   node=page.locator(f'#canvas [data-node="{nid}"]');node.scroll_into_view_if_needed();page.wait_for_timeout(200);r=node.bounding_box()
   x,y=r['x']+r['width']/2,r['y']+r['height']/2
   page.touchscreen.tap(x,y) if width==390 else page.mouse.click(x,y)
   assert page.locator('#selection-details').get_attribute('data-topic')==expected,(width,ref)
  page.locator('#overview').click();title=page.locator('#selection-title').text_content()
  node.scroll_into_view_if_needed();r=node.bounding_box()
  page.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2);page.mouse.down();page.mouse.move(r['x']+70,r['y']+50,steps=6);page.mouse.up()
  assert page.locator('#selection-title').text_content()==title
  for ref,query,topic in [('2673:future','Future','future'),('2672:qtime','Qtime','qtime'),('2673:future-link','Future','future'),('2675:eqp-oee','OEE','oee')]:
   page.locator('#find').fill(query);nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',ref)
   target=page.locator(f'[data-result="{nid}"]')
   target.tap() if width==390 else target.click()
   assert page.locator('#selection-details').get_attribute('data-topic')==topic
   assert page.locator('#selection-details').get_attribute('open') is not None
   if topic=='future':
    assert '登記' in page.locator('#meaning').text_content()
    assert page.locator('#teaching-image').get_attribute('src')=='assets/mes-009/future.png'
    assert page.locator('#teaching-link').get_attribute('href')=='advanced.html#future-hold'
    assert page.evaluate('ER_FOCUS.getState().branches.some(b=>b.ids.includes(ER_ATLAS.model.mapping["2671:lot"]))')
   if topic=='qtime':assert page.locator('#teaching-image').get_attribute('src')=='assets/mes-009/qtime.png'
   if topic=='oee':assert not page.locator('.teaching-figure').is_visible()
   else:
    page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
    page.locator('#open-teaching').click();assert page.locator('#teaching-dialog').is_visible()
    if topic=='future':assert page.locator('#teaching-large').get_attribute('src').endswith('assets/mes-026/future-mobile-v1.png' if width==390 else 'assets/mes-009/future.png')
    page.keyboard.press('Escape')
   page.locator('#selection-details').screenshot(path=str(out/f'{width}-{ref.replace(":","-")}-lesson.png'))
  page.locator('#routes [data-route="hold"]').click()
  assert page.locator('#selection-details').get_attribute('data-topic')=='future'
  assert page.evaluate('ER_FOCUS.getState().root===ER_ATLAS.model.mapping["2673:future"]')
  page.locator('#inspector-expand').click();assert page.locator('#inspector-dialog').is_visible()
  page.locator('#inspector-dialog').screenshot(path=str(out/f'{width}-expanded.png'));page.keyboard.press('Escape')
  page.locator('[data-entity="lot"]').click();assert page.locator('#topic-detail').text_content()==''
  assert page.locator('.teaching-figure').is_visible()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 assert not errors,errors
 b.close()
print(json.dumps({'nodes':len(audit),'routes':len(routes),'source_only':[r['refs'] for r in audit if r['topic']=='source'],'errors':errors}))
