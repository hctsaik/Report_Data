from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-022');out.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True)
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  assert '內容物歷史' in page.locator('#canvas #n_2671_slot').text_content()
  page.locator('[data-entity="carrier"]').click()
  assert 'Split／Merge' in page.locator('#focus-note').text_content()
  page.locator('#find').fill('fhwlths')
  choice=page.locator('[data-result="n_2671_slot"]')
  if width==390:choice.tap()
  else:choice.click()
  assert '內容物歷史' in page.locator('#focus-graph').text_content()
  for term in ['什麼時間點','哪些 Wafer','Split／Merge','目前裝載狀態']:
   assert term in page.locator('#meaning').text_content()
  assert page.locator('#selection-details').get_attribute('open') is not None
  assert '不是內容物歷史紀錄' in page.locator('#teaching-caption').text_content()
  page.locator('#focus-panel').screenshot(path=str(out/f'{width}-history.png'))
  page.locator('#selection-details').screenshot(path=str(out/f'{width}-meaning.png'))
  page.locator('#routes [data-route="slot"]').click()
  assert 'Split／Merge' in page.locator('#meaning').text_content()
  assert '時間點' in page.locator('#selection-title').text_content()
  page.locator('[data-entity="lot"]').click()
  assert '帶到' in page.locator('#focus-graph').text_content()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
  assert not errors,errors
  results.append({'width':width,'history_label_time_wafer_split_merge':'pass','route_and_prior_correction':'pass','errors':errors})
 b.close()
(out/'verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(results)
