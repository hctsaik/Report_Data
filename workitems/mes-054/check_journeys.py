from pathlib import Path
import json
from playwright.sync_api import sync_playwright
OUT=Path('tests/evidence/mes-054');OUT.mkdir(parents=True,exist_ok=True)
rows=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=width==390)
  page.goto('http://127.0.0.1:4175/learning.html?unit=1')
  page.wait_for_selector('#unit-check')
  assert page.evaluate('localStorage.getItem("mes-unit-answers")') is None
  correct=page.evaluate('MES_CATALOG.units[1].check[2]')
  page.locator(f'#unit-check input[value="{correct}"]').check();page.locator('#unit-check button').click()
  assert page.evaluate('JSON.parse(localStorage.getItem("mes-unit-answers"))[1].correct')
  page.reload();assert page.locator(f'#unit-check input[value="{correct}"]').is_checked()
  rows.append({'width':width,'check':'reading-does-not-auto-answer; answer-persist','pass':True})
  page.goto('http://127.0.0.1:4175/learning.html?view=reference')
  page.locator('#topic-search').fill('mainpd_id')
  page.locator('#topic-results a[href*="topic=part"]').click()
  page.wait_for_selector('#topic-title');assert page.locator('#topic-title').text_content().startswith('PART')
  assert page.locator('#mes-return').is_visible()
  page.locator('#topic-enlarge').click();assert page.locator('#topic-dialog').is_visible()
  page.keyboard.press('Escape');assert not page.locator('#topic-dialog').is_visible()
  page.locator('#topic-refs a[href*="er-atlas"]').first.click()
  page.wait_for_function('window.ER_ATLAS')
  assert page.locator('#selection-details').get_attribute('data-topic')=='part'
  page.locator('#mes-return').click();page.wait_for_selector('#topic-title')
  assert page.locator('#topic-title').text_content().startswith('PART')
  page.locator('#mes-return').click();page.wait_for_selector('#topic-search')
  rows.append({'width':width,'check':'search-topic-image-ER-return-topic-return-search','pass':True})
  page.goto('http://127.0.0.1:4175/tasks.html#not-running')
  page.locator('input[name="object"]').fill('L-REPLAY')
  page.locator('input[name="time"]').fill('09:30')
  page.locator('[data-topic-link="lotstatus"]').click();page.wait_for_selector('#topic-title')
  page.locator('#mes-return').click();page.wait_for_selector('input[name="object"]')
  assert page.locator('input[name="object"]').input_value()=='L-REPLAY'
  assert page.locator('input[name="time"]').input_value()=='09:30'
  assert page.url.endswith('#not-running')
  rows.append({'width':width,'check':'task-topic-return-keeps-object-time','pass':True})
  for path,selector in [('operations.html#lab','#next'),('flow.html#lab','#next'),('freshness.html#join','#fresh-next')]:
   page.goto('http://127.0.0.1:4175/'+path);page.wait_for_selector(selector);page.wait_for_timeout(350)
   expected=page.locator('#mes-sequence .mes-next').get_attribute('href')
   page.locator(selector).click();page.wait_for_load_state('networkidle')
   from urllib.parse import urlsplit,parse_qs
   wanted=urlsplit(expected);actual=urlsplit(page.url)
   assert wanted.path==actual.path and wanted.fragment==actual.fragment,(expected,page.url)
   for key,values in parse_qs(wanted.query).items(): assert parse_qs(actual.query).get(key)==values
   rows.append({'width':width,'check':'catalog-next:'+path,'destination':page.url,'pass':True})
  page.close()
 b.close()
(OUT/'journeys.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS',len(rows),'journeys; actual controls, persistence, source returns and course continuation')
