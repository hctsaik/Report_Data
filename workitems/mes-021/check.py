from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-021');out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  page.locator('[data-entity="lot"]').click()
  assert '帶到' in page.locator('#focus-graph').text_content()
  assert '預到' not in page.locator('#focus-graph').text_content()
  assert '這個站點有可用機台' in page.locator('#focus-note').text_content()
  assert '帶到' in page.locator('#canvas #n_2671_lot-eqp').text_content()
  assert '預派機台' in page.locator('#canvas #n_2671_predispatch').text_content()
  page.locator('#focus-panel').screenshot(path=str(out/f'{width}-lot.png'))
  g=page.locator('#focus-graph [data-focus-node="n_2671_lot-eqp"]')
  if width==390:g.tap()
  else:g.click()
  page.locator('#selection-details').evaluate('(d)=>d.open=true')
  assert '這個站點有可用機台' in page.locator('#meaning').text_content()
  page.locator('#routes [data-route="lot-pre"]').click()
  assert '可用機台' in page.locator('#selection-title').text_content()
  assert '批次安排' not in page.locator('#meaning').text_content()
  assert not errors,errors
  results.append({'width':width,'label_and_station_available_tools':'pass','carrier_predispatch_unchanged':True,'errors':errors})
 b.close()
(out/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
