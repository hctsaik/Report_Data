from pathlib import Path
import json,re,xml.etree.ElementTree as ET,hashlib
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'tests/evidence/mes-014';O.mkdir(parents=True,exist_ok=True)
m=json.loads((R/'ER/INTEGRATED/er-model-v1.json').read_text(encoding='utf-8'));NS={'s':'http://www.w3.org/2000/svg'}
svg=ET.parse(R/'ER/INTEGRATED/fab-er-v1.svg');drawn={g.get('id'):g for g in svg.findall('.//s:g',NS)}
assert len(m['originalNodes'])==128 and sum(len(e['refs']) for e in m['edges'])==128
for n in m['nodes']:
 assert n['id'] in drawn
 text=''.join(''.join(t.itertext()) for t in drawn[n['id']].findall('.//s:text',NS)).casefold()
 for ref in n['refs']:
  for label in ref['labels']:assert label.casefold() in text,(n['id'],label,text)
for e in m['edges']:
 assert e['id'] in drawn and drawn[e['id']].get('data-a')==e['a'] and drawn[e['id']].get('data-b')==e['b']
 for ref in e['refs']:
  assert m['mapping'][f'{ref["source"]}:{ref["a"]}']==e['a']
  assert m['mapping'][f'{ref["source"]}:{ref["b"]}']==e['b']
assert m['mapping']['2677:pd-key']!=m['mapping']['2677:recipe-key']
assert m['mapping']['2671:port']!=m['mapping']['2674:port']
assert m['mapping']['2671:lot']!=m['mapping']['2675:lot']
old=json.loads((R/'workitems/mes-011/original-svg-hashes.json').read_text())
for f,h in old.items():assert hashlib.sha256((R/'ER/NEW'/f).read_bytes()).hexdigest()==h
checks=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 for width in [1440,390]:
  page.set_viewport_size({'width':width,'height':1000});page.goto('http://127.0.0.1:4175/er-atlas.html?view=original');page.wait_for_function('!!window.ER_ATLAS')
  assert page.locator('#canvas [data-node]').count()==119
  assert page.locator('#canvas [data-edge]').count()==128
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  for route in ['load','slot','location','predispatch','lot-pre','port','flow','lr','pd','recipe','chamber','hold','move','transfer','qtime','wip','oee']:
   page.evaluate('(id)=>ER_ATLAS.route(id)',route)
   assert page.locator('#path-list button').count()>=3
   assert not errors,errors
   if route in ['load','location','predispatch','recipe','move','flow']:
    page.locator('.workspace').screenshot(path=str(O/f'{route}-{width}.png'))
   checks.append(f'{width}/{route}: existing edge path focus')
  page.locator('#overview').click();page.locator('#canvas').screenshot(path=str(O/f'overview-{width}.png'))
  page.locator('#find').fill('FRCAST_LOT');page.locator('[data-result]').first.click();assert '已定位' in page.locator('#status').inner_text()
  before=page.evaluate('ER_ATLAS.getView()');page.locator('#zoom-in').click();after=page.evaluate('ER_ATLAS.getView()');assert after[2]<before[2]
  page.locator('#canvas').focus();page.keyboard.press('ArrowRight');assert page.evaluate('ER_ATLAS.getView()[0]')!=after[0]
  page.goto('http://127.0.0.1:4175/er-atlas.html?view=questions');page.wait_for_function('!!window.ER_ATLAS')
  for q in ['where','ready','recipe','move','time']:
   page.locator(f'[data-question="{q}"]').click();assert page.locator('#question-copy .answer').inner_text()
   page.locator('#question-panel').screenshot(path=str(O/f'question-{q}-{width}.png'))
  checks.append(f'{width}: search, zoom, keyboard pan, five questions')
 b.close()
assert not errors,errors
(O/'verification.json').write_text(json.dumps(dict(canonical_nodes=119,source_nodes=128,visible_edges=128,source_edges=128,originals_unchanged=7,checks=checks,errors=errors),ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: 128 original nodes/edges mapped to visible graph; 119 canonical nodes; originals unchanged; 17 routes and 5 questions at both widths')
