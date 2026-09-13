from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-024');out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html?subject=lot-step');page.wait_for_function('window.ER_ATLAS')
  assert page.evaluate('ER_FOCUS.getState().branches[0].ids.includes(ER_ATLAS.model.mapping["2671:lot"])')
  assert page.locator('#focus-graph [data-focus-node="t_cfc81de70314"]').count()>0
  page.locator('#focus-panel').screenshot(path=str(out/f'{width}-lot-step.png'))
  page.locator('[data-entity="carrier"]').click()
  assert page.evaluate('''()=>{const m=ER_ATLAS.model,b=ER_FOCUS.getState().branches[0];return ['2671:cast','2671:cast-link','2671:lot','2672:summary','2672:step'].every((r,i)=>m.mapping[r]===b.ids[i])&&b.edges.every((id,i)=>m.edges.some(e=>e.id===id&&((e.a===b.ids[i]&&e.b===b.ids[i+1])||(e.b===b.ids[i]&&e.a===b.ids[i+1]))))}''')
  assert page.evaluate('ER_FOCUS.getState().branches.every(b=>!b.ids.includes("n_2672_cast-link"))')
  page.locator('#focus-panel').screenshot(path=str(out/f'{width}-foup-lot-step.png'))
  page.locator('#routes [data-route="lot-step"]').click()
  assert 'Lot' in page.locator('#selection-title').text_content()
  assert not errors,errors
  results.append({'width':width,'lot_step_and_foup_complete_path':'pass','all_path_edges_in_source':True,'errors':errors})
 b.close()
(out/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
