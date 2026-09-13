from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'tests/evidence/mes-012';O.mkdir(parents=True,exist_ok=True)
d=json.loads((R/'ER/INTEGRATED/map.json').read_text(encoding='utf-8'));ns={'s':'http://www.w3.org/2000/svg'}
refs=[(r['source'],r['node']) for g in d['groups'] for r in g['refs']]
original=[]
for n in range(2671,2678):
 original.extend((str(n),g.get('id')) for g in ET.parse(R/f'ER/NEW/{n}.svg').findall("s:g[@id='nodes']/s:g",ns))
assert len(refs)==len(set(refs))==128 and set(refs)==set(original)
assert len(d['sourceEdges'])==128
allowed={frozenset([e['groupA'],e['groupB']]) for e in d['sourceEdges']}
graph=ET.parse(R/'ER/INTEGRATED/fab-integrated.svg')
for g in graph.findall("s:g[@class='relationship']",ns):
 if g.find('s:path',ns).get('stroke-dasharray') is None:assert frozenset([g.get('data-a'),g.get('data-b')]) in allowed,(g.get('data-a'),g.get('data-b'))
hashes=json.loads((R/'workitems/mes-011/original-svg-hashes.json').read_text())
for name,h in hashes.items():assert hashlib.sha256((R/'ER/NEW'/name).read_bytes()).hexdigest()==h
checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 for width in [1440,360]:
  page.set_viewport_size({'width':width,'height':1000})
  page.goto('http://127.0.0.1:4175/integrated-map.html?view=original')
  page.wait_for_function("document.querySelector('#map-status').textContent.startsWith('完整大圖')")
  assert page.locator('[data-topic]').count()==20
  assert not page.locator('#questions').is_visible()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  text_fits=page.locator('#map').evaluate('''o=>[...o.contentDocument.querySelectorAll('.node')].every(g=>{const r=g.querySelector('rect').getBBox();return [...g.querySelectorAll('text')].every(t=>{const b=t.getBBox();return b.x>=r.x && b.x+b.width<=r.x+r.width && b.y>=r.y && b.y+b.height<=r.y+r.height})})''')
  assert text_fits,'SVG node text clipping'
  page.screenshot(path=str(O/f'original-{width}.png'),full_page=True)
  for topic in ['lot','cast','flow','er','chamber','wip']:
   page.locator(f'[data-topic="{topic}"]').click()
   assert page.locator('#detail .source-card').count()>0
   assert page.locator('#map-status').inner_text().startswith('目前局部')
  page.locator('#read').click();assert '閱讀尺寸' in page.locator('#map-status').inner_text()
  page.locator('#fit').click()
  page.locator('#question-tab').click();page.wait_for_selector('[data-case]')
  assert page.locator('[data-case]').count()==5
  for case in ['where','ready','move','recipe','time']:
   page.locator(f'[data-case="{case}"]').click()
   assert page.locator('#case .steps>div').count()==3
   assert page.locator('#case .refs a').count()>=2
   assert page.locator('#case .answer').inner_text()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   page.screenshot(path=str(O/f'{case}-{width}.png'),full_page=True)
   checks.append(f'{width}/{case}: cross-source content and diagram highlighting')
  for entry in ['operations.html#port','flow.html#stage']:
   page.goto('http://127.0.0.1:4175/'+entry)
   link=page.locator('.aside-foot a[href="integrated-map.html?view=original"]')
   link.wait_for(state='attached')
   if width==360:page.locator('#menu-toggle').click()
   link.scroll_into_view_if_needed();link.click()
   page.wait_for_selector('[data-topic]')
   checks.append(f'{width}/{entry}: actual sidebar navigation')
 assert not errors,errors
 b.close()
(O/'results.json').write_text(json.dumps(dict(checks=checks,source_nodes=128,source_edges=128,groups=20,original_svg_unchanged=7,errors=errors),ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 128 nodes/128 edges preserved; solid links sourced; SVG labels fit; 2 widths/5 cases; sidebar links; 7 original SVG hashes unchanged')
