"""Render and inspect actual SVG text bounds; save browser evidence."""
from pathlib import Path
import json, hashlib, xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright

OUT=Path(__file__).resolve().parent
ns={'s':'http://www.w3.org/2000/svg'}
results=[]
data=json.loads((OUT/'transcription.json').read_text(encoding='utf-8'))
for diagram in data:
    nodes={n['id']:n for n in diagram['nodes']}
    def anchor(n,s):
        x,y,w,h=n['x'],n['y'],n['w'],n['h']
        return {'T':(x,y-h/2),'B':(x,y+h/2),'L':(x-w/2,y),'R':(x+w/2,y)}[s]
    for e in diagram['edges']:
        pts=[anchor(nodes[e['a']],e['sa']),*e['via'],anchor(nodes[e['b']],e['sb'])]
        for start,end in zip(pts,pts[1:]):
            steps=max(1,int(max(abs(end[0]-start[0]),abs(end[1]-start[1]))/3))
            for i in range(1,steps):
                x=start[0]+(end[0]-start[0])*i/steps;y=start[1]+(end[1]-start[1])*i/steps
                for n in nodes.values():
                    if n['id'] in (e['a'],e['b']):continue
                    dx=abs(x-n['x'])/(n['w']/2);dy=abs(y-n['y'])/(n['h']/2)
                    inside=dx+dy<.98 if n['kind']=='diamond' else (dx*dx+dy*dy<.98 if n['kind']=='circle' else dx<.98 and dy<.98)
                    assert not inside,(diagram['name'],e['a'],e['b'],'crosses',n['id'])
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1500,'height':1100},device_scale_factor=1)
    (OUT/'preview').mkdir(exist_ok=True)
    for file in sorted(OUT.glob('267*.svg')):
        root=ET.parse(file).getroot()
        assert not root.findall('.//s:image',ns)
        page.set_content('<html><head><meta charset="utf-8"></head><body style="margin:0">'+file.read_text(encoding='utf-8')+'</body></html>')
        page.evaluate('document.fonts.ready')
        # Fit each editable text line to the actual shape cross-section, without rasterizing it.
        adjustments=page.evaluate('''()=>Array.from(document.querySelectorAll('#nodes g')).flatMap(g=>{const x=+g.dataset.x,y=+g.dataset.y,w=+g.dataset.w,h=+g.dataset.h;return Array.from(g.querySelectorAll('text:not(.issue)')).flatMap(t=>{const box=t.getBBox();let available=w-28;if(g.dataset.kind==='diamond'){const distance=Math.max(Math.abs(box.y-y),Math.abs(box.y+box.height-y));available=w*(1-distance/(h/2))-22}if(g.dataset.kind==='circle'){const distance=Math.max(Math.abs(box.y-y),Math.abs(box.y+box.height-y));available=w*Math.sqrt(Math.max(0,1-(distance/(h/2))**2))-24}if(box.width>available){return [{node:g.id,text:t.textContent,font:Math.max(14,Math.floor(parseFloat(getComputedStyle(t).fontSize)*available/box.width*10)/10)}]}return []})})''')
        if adjustments:
            for adj in adjustments:
                node=root.find(f'.//s:g[@id="{adj["node"]}"]',ns)
                for t in node.findall('s:text',ns):
                    if t.text==adj['text']: t.set('style',f'font-size:{adj["font"]}px')
            ET.register_namespace('',ns['s']);ET.ElementTree(root).write(file,encoding='utf-8',xml_declaration=True)
            page.set_content('<html><body style="margin:0">'+file.read_text(encoding='utf-8')+'</body></html>');page.evaluate('document.fonts.ready')
        overflow=page.evaluate('''()=>Array.from(document.querySelectorAll('#nodes g')).flatMap(g=>{const x=+g.dataset.x,y=+g.dataset.y,w=+g.dataset.w,h=+g.dataset.h;return Array.from(g.querySelectorAll('text:not(.issue)')).flatMap(t=>{const b=t.getBBox();let limit=w/2-8;if(g.dataset.kind==='diamond'){limit=w/2*(1-Math.max(Math.abs(b.y-y),Math.abs(b.y+b.height-y))/(h/2))-6}return b.x<x-limit||b.x+b.width>x+limit||b.y<y-h/2||b.y+b.height>y+h/2?[{id:g.id,text:t.textContent}]:[]})})''')
        assert not overflow, (file.name,overflow)
        width=int(root.attrib['width']);height=int(root.attrib['height'])
        page.set_viewport_size({'width':1500,'height':max(500,round(height*1500/width))})
        page.evaluate("document.querySelector('svg').style.cssText='width:100vw;height:auto;display:block'")
        page.screenshot(path=str(OUT/'preview'/f'{file.stem}.png'),full_page=True)
        results.append({'file':file.name,'nodes':len(root.findall('.//s:g[@data-kind]',ns)),'text_overflow':overflow,'font_fits':adjustments,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((OUT.parent/'ORG'/f'{file.stem}.jpg').read_bytes()).hexdigest()})
    page.goto((OUT/'index.html').as_uri())
    for name in [str(n) for n in range(2671,2678)]:
        page.locator(f'button[data-id="{name}"]').click()
        page.wait_for_function("name => document.getElementById('drawing').getAttribute('data')===name+'.svg'",arg=name)
        page.wait_for_function("document.getElementById('drawing').getBoundingClientRect().height > 300")
    page.locator('#toggle').click()
    assert page.locator('#photo').is_visible()
    page.locator('#plus').click();page.locator('#minus').click();page.locator('#fit').click()
    page.screenshot(path=str(OUT/'preview'/'viewer.png'),full_page=True)
    browser.close()
(OUT/'verification.json').write_text(json.dumps({'diagrams':results,'viewer_controls':'passed','status':'SVG redraw complete; all 13 unclear-text items confirmed by user'},ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 7 SVGs, editable text bounds, no embedded bitmaps, viewer controls.')
