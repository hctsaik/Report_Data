from pathlib import Path
import json
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[2]
out=root/'tests/evidence/mes-053';out.mkdir(parents=True,exist_ok=True)
pages=['index.html','operations.html','flow.html','freshness.html','advanced.html','support.html','er-atlas.html','data-map.html','subject-er.html','ER/NEW/index.html']
report=[]
with sync_playwright() as p:
 browser=p.chromium.launch()
 for width in [1440,390]:
  page=browser.new_page(viewport={'width':width,'height':950})
  for name in pages:
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   response=page.goto('http://127.0.0.1:4175/'+name)
   page.wait_for_timeout(700)
   data=page.evaluate('''()=>({title:document.title,url:location.href,headings:[...document.querySelectorAll('h1,h2')].map(x=>x.textContent),links:[...document.querySelectorAll('a[href]')].map(x=>({text:x.textContent.trim(),href:x.getAttribute('href')})),buttons:[...document.querySelectorAll('button')].filter(x=>x.getBoundingClientRect().width>0).map(x=>({text:x.textContent.trim(),disabled:x.disabled})),overflow:document.documentElement.scrollWidth>innerWidth})''')
   data.update(file=name,width=width,status=response.status,errors=errors)
   report.append(data)
   page.screenshot(path=str(out/(name.replace('/','_').replace('.html','')+f'-{width}.png')))
  page.close()
 page=browser.new_page()
 page.goto('http://127.0.0.1:4175/operations.html')
 page.wait_for_selector('#next')
 curriculum=page.evaluate('''()=>Object.fromEntries(Object.entries(COURSES).map(([k,c])=>[k,{title:c.title,next:c.next,lessons:c.lessons.map(l=>({id:l.id,title:l.title,nav:l.nav}))}]))''')
 topics=browser.new_page();topics.goto('http://127.0.0.1:4175/er-atlas.html');topics.wait_for_function('window.ER_TOPIC_CONTENT')
 registry=topics.evaluate('''()=>Object.entries(ER_TOPIC_CONTENT.topics).map(([id,t])=>({id,title:t.title,refs:t.refs,link:t.link,image:!!t.image,mobile:!!t.mobile}))''')
 (out/'inventory.json').write_text(json.dumps({'pages':report,'curriculum':curriculum,'topics':registry},ensure_ascii=False,indent=2),encoding='utf-8')
 browser.close()
print('Saved 20 entry-page observations/screenshots, runtime curriculum and topic inventory. No learning-quality score assigned.')
