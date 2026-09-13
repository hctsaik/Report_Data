from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-018');out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html?view=original');page.wait_for_function('window.ER_ATLAS')
  for key in ['lot','carrier']:
   button=page.locator(f'[data-entity="{key}"]')
   if width==390:button.tap()
   else:button.click()
   assert page.evaluate('''()=>{const m=ER_ATLAS.model.mapping,s=ER_FOCUS.getState();return s.branches.some(b=>b.ids.includes(m['2671:lot'])&&b.ids.includes(m['2671:cast-link'])&&b.ids.includes(m['2671:cast']))}''')
   page.locator('#focus-panel').screenshot(path=str(out/f'{width}-{key}.png'))
   for i in range(page.locator('#focus-more button').count()):
    page.locator('#focus-more button').nth(i).click()
    assert 'Lot 在 Foup 內' not in page.locator('#focus-graph').inner_text()
    assert page.locator('#focus-graph [data-focus-node="n_2672_cast-link"]').count()==0
  # Verify withdrawal from every subject, not just a paginated FOUP screenshot.
  assert page.evaluate('''()=>{const bad=ER_ATLAS.model.mapping['2672:cast-link'];return ER_ATLAS.model.nodes.every(n=>{ER_FOCUS.show(n.id);return ER_FOCUS.getState().branches.every(b=>!b.ids.includes(bad))})}''')
  assert not errors,errors
  results.append({'width':width,'correct_loading_chain':True,'all_pages_checked':True,'all_121_roots_checked':True,'errors':errors})
 b.close()
(out/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
# Same functional assertions as MES-017, but save this revision's evidence separately.
root=Path(__file__).resolve().parents[2]
source=root/'workitems/mes-017/check.py'
code=source.read_text(encoding='utf-8').replace("ROOT/'tests/evidence/mes-017'","ROOT/'tests/evidence/mes-018/regression'")
exec(compile(code,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
