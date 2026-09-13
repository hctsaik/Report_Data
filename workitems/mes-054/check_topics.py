from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-054/topics');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 total=0
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/topic.html?topic=lot')
  keys=page.evaluate('Object.keys(ER_TEACHING).filter(k=>!["overview","source"].includes(k))')
  for key in keys:
   page.goto('http://127.0.0.1:4175/topic.html?topic='+key)
   page.wait_for_function('document.getElementById("topic-refs").children.length>0')
   assert page.locator('#topic-title').text_content()==page.evaluate('(k)=>ER_TEACHING[k].title',key)
   assert page.locator('#topic-meaning').text_content()==page.evaluate('(k)=>ER_TEACHING[k].meaning',key)
   if page.locator('#topic-figure').is_visible():
    page.wait_for_function('document.getElementById("topic-image").naturalWidth>0')
    page.locator('#topic-enlarge').click();assert page.locator('#topic-dialog').is_visible()
    assert page.locator('#topic-large').get_attribute('src')==page.locator('#topic-image').evaluate('(x)=>x.currentSrc')
    page.keyboard.press('Escape')
   if key in ['lot','carrier','load']:
    page.locator('[data-lw-mode="multiple"]').click();page.locator('[data-lw-slot="25"]').click()
    assert 'L024' in page.locator('.wafer-record').text_content()
   if key=='mcs':
    page.locator('[data-mcs-event="3"]').click();assert '10:03' in page.locator('.mcs-event-detail').text_content()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),key
   page.screenshot(path=str(out/f'{key}-{width}.png'),full_page=True)
   total+=1
  assert not errors,errors
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  assert page.evaluate('ER_TEACHING.load===ER_TOPIC_CONTENT.topics.load')
  page.close()
 b.close()
print('PASS',total,'topic views, shared definitions, images, dialogs, Lot and MCS interaction; ER loads')
