from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-023');out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html?subject=predispatch');page.wait_for_function('window.ER_ATLAS')
  assert page.evaluate('''()=>{const m=ER_ATLAS.model.mapping,b=ER_FOCUS.getState().branches;return b[0].ids.at(-1)===m['2671:lot']&&b[1].ids.at(-1)===m['2671:eqp']&&b[2].ids.at(-1)===m['2671:cast']}''')
  assert page.locator('#focus-graph [data-edge-provenance="user-confirmed-business"]').get_attribute('stroke-dasharray')=='8 5'
  assert '派工系統預先安排' in page.locator('#meaning').text_content()
  assert 'FOUP 是輔助' in page.locator('#meaning').text_content()
  assert page.locator('#teaching-image').get_attribute('src')=='assets/mes-023/lot-predispatch-v1.png'
  page.wait_for_function('document.getElementById("teaching-image").complete')
  page.locator('#focus-panel').screenshot(path=str(out/f'{width}-graph.png'))
  page.locator('#selection-details').screenshot(path=str(out/f'{width}-illustration.png'))
  page.locator('#open-teaching').click()
  assert page.locator('#teaching-large').get_attribute('src').endswith('lot-predispatch-mobile-v1.png' if width==390 else 'lot-predispatch-v1.png')
  page.keyboard.press('Escape')
  page.locator('#inspector-expand').click();assert page.locator('#inspector-dialog').is_visible();page.keyboard.press('Escape')
  # Real input on the new Lot endpoint must switch subject.
  lot=page.evaluate('ER_ATLAS.model.mapping["2671:lot"]');g=page.locator(f'#focus-graph [data-focus-node="{lot}"]')
  if width==390:g.tap()
  else:g.click()
  assert page.evaluate('(id)=>ER_FOCUS.getState().root===id',lot)
  page.locator('#routes [data-route="predispatch"]').click()
  assert page.evaluate('ER_FOCUS.getState().root===ER_ATLAS.model.mapping["2671:predispatch"]')
  assert page.locator('#teaching-image').get_attribute('src')=='assets/mes-023/lot-predispatch-v1.png'
  # Source lines remain exact; only the explicitly confirmed business relation is additional.
  assert page.evaluate('''()=>{const m=ER_ATLAS.model;return m.nodes.every(n=>{ER_FOCUS.show(n.id);return ER_FOCUS.getState().branches.every(b=>b.edges.every((id,i)=>{if(id==='business-lot-predispatch')return b.businessEdges.includes(id)&&[b.ids[i],b.ids[i+1]].includes(m.mapping['2671:lot'])&&[b.ids[i],b.ids[i+1]].includes(m.mapping['2671:predispatch']);const e=m.edges.find(e=>e.id===id);return e&&((e.a===b.ids[i]&&e.b===b.ids[i+1])||(e.b===b.ids[i]&&e.a===b.ids[i+1]));}));})}''')
  page.locator('#routes [data-route="lot-pre"]').click();assert '可用機台' in page.locator('#meaning').text_content()
  page.locator('#routes [data-route="slot"]').click();assert 'Split／Merge' in page.locator('#meaning').text_content()
  page.locator('#find').fill('WPH');page.locator('[data-result]').first.click();assert 'mes-019' in page.locator('#teaching-image').get_attribute('src')
  assert not errors,errors
  results.append({'width':width,'lot_eqp_primary_carrier_auxiliary':True,'business_edge_distinct':True,'image_dialog_pointer_regressions':'pass','errors':errors})
 b.close()
(out/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
