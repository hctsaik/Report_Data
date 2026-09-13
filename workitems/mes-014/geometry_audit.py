from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1440,'height':1000});page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('!!window.ER_ATLAS')
 result=page.evaluate('''()=>{
 const svg=document.querySelector('#canvas svg'),ns=[...svg.querySelectorAll('[data-node]')].map(g=>{const shape=g.querySelector('polygon,ellipse,path');return {id:g.id,shape,box:shape.getBBox()}});
 const collisions=[],textOutside=[];
 for(const n of ns){for(const t of svg.getElementById(n.id).querySelectorAll('text')){const b=t.getBBox();if(b.x<n.box.x-1||b.x+b.width>n.box.x+n.box.width+1)textOutside.push([n.id,t.textContent]);}}
 for(const e of svg.querySelectorAll('[data-edge]')){const p=e.querySelector('path'),len=p.getTotalLength();for(let t=6;t<len-6;t+=6){const q=p.getPointAtLength(t);for(const n of ns){if(n.id===e.dataset.a||n.id===e.dataset.b)continue;const b=n.box;if(q.x>b.x+1&&q.x<b.x+b.width-1&&q.y>b.y+1&&q.y<b.y+b.height-1&&n.shape.isPointInFill(q)){collisions.push([e.id,n.id]);break;}}}}
 return {crossings:[...new Map(collisions.map(x=>[x.join('|'),x])).values()],textOutside};}''')
 b.close()
(R/'tests/evidence/mes-014/v2/geometry.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
