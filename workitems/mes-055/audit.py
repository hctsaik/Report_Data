from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
phase=sys.argv[1] if len(sys.argv)>1 else 'before'
out=Path('tests/evidence/mes-055')/phase;out.mkdir(parents=True,exist_ok=True)
urls=[*(f'index.html#{k}' for k in ['slot','foup','lot','explore']),*(f'topic.html?topic={k}' for k in ['load','flowkey','available','eqpstatus','eqpkey','location','lotstep','contents','material'])]
rows=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000})
  for u in urls:
   page.goto('http://127.0.0.1:4175/'+u,wait_until='networkidle')
   name=u.replace('index.html#','index-').replace('topic.html?topic=','topic-')
   page.screenshot(path=str(out/f'{name}-{width}.png'),full_page=True)
   rows.append({'url':u,'width':width,**page.evaluate('''()=>({overflow:document.documentElement.scrollWidth>innerWidth,images:[...document.images].filter(i=>i.getBoundingClientRect().width).map(i=>({src:i.currentSrc,w:i.getBoundingClientRect().width,h:i.getBoundingClientRect().height,loaded:i.complete&&i.naturalWidth>0})),text:document.querySelector('main').innerText})''')})
  page.close()
 b.close()
(out/'audit.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(phase,len(rows),'views recorded')
