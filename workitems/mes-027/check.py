from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-027');out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref,query in [('2671:lot','Siview.Frlot'),('2671:predispatch','CSFRPREDISPATCH'),('2671:cast','Siview.Frcast'),('2671:eqp','Siview.freqp')]:
   page.locator('#find').fill(query);nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',ref)
   btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
   assert page.evaluate('''()=>{const m=ER_ATLAS.model.mapping,s=ER_FOCUS.getState();return s.branches.every(b=>b.ids.every((id,i)=>!i||!([b.ids[i-1],id].includes(m['2671:predispatch'])&&[b.ids[i-1],id].includes(m['2671:cast']))));}''')
   if ref=='2671:lot':
    assert page.evaluate('''()=>{const m=ER_ATLAS.model.mapping,bs=ER_FOCUS.getState().branches;return bs.filter(b=>b.ids.includes(m['2671:predispatch'])).length===1&&bs.some(b=>JSON.stringify(b.ids)===JSON.stringify([m['2671:lot'],m['2671:predispatch'],m['2671:eqp']]))&&bs.some(b=>b.ids.includes(m['2671:cast-link'])&&b.ids.includes(m['2671:cast']));}''')
   if ref=='2671:predispatch':
    assert page.evaluate('''()=>{const m=ER_ATLAS.model.mapping,bs=ER_FOCUS.getState().branches;return bs.length===2&&bs.some(b=>b.ids.includes(m['2671:lot']))&&bs.some(b=>b.ids.includes(m['2671:eqp']));}''')
    assert 'Siview.freqp' in page.locator('#focus-graph').text_content()
    assert 'Siview.Frcast' not in page.locator('#focus-graph').text_content()
    page.locator('#focus-panel').screenshot(path=str(out/f'{width}-predispatch.png'))
    page.locator('#focus-expand').click();assert 'Siview.freqp' in page.locator('#focus-large').text_content();page.keyboard.press('Escape')
  assert not errors,errors
  results.append({'width':width,'four_direction_no_predispatch_carrier_edge':True,'lot_to_predispatch_to_eqp':True,'errors':errors})
 b.close()
(out/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
