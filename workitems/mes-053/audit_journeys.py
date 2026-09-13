from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-053');results=[]
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1440,'height':950})
 for file in ['operations.html','flow.html']:
  page.goto('http://127.0.0.1:4175/'+file+'#lab');page.wait_for_selector('#next')
  row={'task':'course-end','file':file,'before':page.url,'primary':page.locator('#next').inner_text(),'courseNext':page.locator('.page-foot a').get_attribute('href')}
  page.locator('#next').click();row['after']=page.url;results.append(row)
 page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_selector('[data-entity="lot"]')
 page.locator('[data-entity="lot"]').click();first=page.locator('#selection-title').inner_text()
 page.locator('[data-entity="equipment"]').click();second=page.locator('#selection-title').inner_text()
 page.locator('#er-back').click();page.wait_for_timeout(200)
 results.append({'task':'ER UI back','first':first,'second':second,'restored':page.locator('#selection-title').inner_text()})
 page.locator('[data-entity="equipment"]').click();page.locator('#teaching-link').click();page.wait_for_timeout(300)
 back=page.locator('.er-return-bar a').first
 if not back.count():back=page.get_by_role('link',name='← 返回 ER：',exact=False)
 results.append({'task':'ER to lesson','url':page.url,'returnLinks':back.count(),'returnText':back.first.inner_text() if back.count() else None})
 if back.count():
  back.first.click();page.wait_for_timeout(500);results.append({'task':'lesson back to ER','url':page.url,'selection':page.locator('#selection-title').inner_text()})
 (out/'journeys.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');b.close()
print('Saved observed course-end and ER round-trip journeys')
