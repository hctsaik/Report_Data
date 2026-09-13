from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-025');out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html?subject=qtime');page.wait_for_function('window.ER_ATLAS')
  for ref in ['2672:qtime','2672:qtime-link']:
   page.locator('#find').fill('Qtime');nid=page.evaluate('(ref)=>ER_ATLAS.model.mapping[ref]',ref)
   btn=page.locator(f'[data-result="{nid}"]')
   if width==390:btn.tap()
   else:btn.click()
   assert page.evaluate('''()=>{const m=ER_ATLAS.model,b=ER_FOCUS.getState().branches[0];return b.ids.includes(m.mapping['2671:lot'])&&b.ids.includes(m.mapping['2672:step'])&&b.edges.every((id,i)=>m.edges.some(e=>e.id===id&&((e.a===b.ids[i]&&e.b===b.ids[i+1])||(e.b===b.ids[i]&&e.a===b.ids[i+1]))))}''')
   assert page.locator('#selection-details').get_attribute('open') is not None
   for term in ['起算事件','停止事件','時間限制']:assert term in page.locator('#meaning').text_content()
   for term in ['30 分鐘','10:35','5 分鐘','Hold']:assert term in page.locator('#topic-detail').text_content()
   assert page.locator('#teaching-image').get_attribute('src')=='assets/mes-009/qtime.png'
   assert page.locator('#teaching-link').get_attribute('href')=='advanced.html#qtime'
   page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
   page.locator('#focus-panel').screenshot(path=str(out/f'{width}-{ref.split(":")[1]}-graph.png'))
   page.locator('#selection-details').screenshot(path=str(out/f'{width}-{ref.split(":")[1]}-lesson.png'))
   page.locator('#open-teaching').click()
   assert page.locator('#teaching-large').get_attribute('src').endswith('assets/mes-025/qtime-mobile-v1.png' if width==390 else 'assets/mes-009/qtime.png')
   page.keyboard.press('Escape')
  page.locator('#routes [data-route="qtime"]').click()
  assert page.evaluate('ER_FOCUS.getState().root===ER_ATLAS.model.mapping["2672:qtime"]')
  page.locator('#inspector-expand').click();assert page.locator('#inspector-dialog').is_visible();page.keyboard.press('Escape')
  page.locator('[data-entity="lot"]').click();assert page.locator('#topic-detail').text_content()==''
  assert page.locator('#teaching-image').get_attribute('src')=='examples/fab-physical-data-v01.png'
  assert '帶到' in page.locator('#focus-graph').text_content()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  assert not errors,errors
  results.append({'width':width,'qtime_lot_complete_source_path':True,'lesson_image_dialog_route':'pass','topic_reset':'pass','errors':errors})
 b.close()
(out/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
