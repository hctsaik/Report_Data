from pathlib import Path
from playwright.sync_api import sync_playwright
import json
out=Path('tests/evidence/mes-055');errors=[];checks=[]
def ok(condition,label):
 assert condition,label
 checks.append(label)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)))
  for key in ['load','flowkey','available','eqpstatus','eqpkey','location','lotstep','contents','material']:
   page.goto('http://127.0.0.1:4175/topic.html?topic='+key+'&mesFrom=expired-test',wait_until='networkidle')
   ok(page.locator('#topic-figure').is_visible(),f'{key}/{width} figure')
   ok(page.locator('#topic-detail').inner_text().__len__()>200,f'{key}/{width} explanation')
   page.locator('#topic-enlarge').click();ok(page.locator('#topic-dialog').is_visible(),f'{key}/{width} enlarge');page.keyboard.press('Escape')
   ok(page.locator('#topic-context a').count()>0,f'{key}/{width} return')
   ok(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'{key}/{width} no overflow')
   if key=='load':
    page.locator('.refresh-lab summary').click()
    page.locator('[data-lw-mode="multiple"]').click();page.locator('[data-lw-slot="25"]').click()
    ok('L024' in page.locator('.wafer-record').inner_text(),f'load/{width} multiple Lot')
  for key in ['foup','slot','lot','explore']:
   page.goto('http://127.0.0.1:4175/index.html?mesFrom=expired-test#'+key,wait_until='networkidle')
   ok(page.locator('#'+key+' .refresh-figure img').is_visible(),f'{key}/{width} physical reference')
   ok(page.locator('#mes-sequence a').count()>0,f'{key}/{width} sequence')
   ok(page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'{key}/{width} no overflow')
  page.locator('[data-slot="7"]').click();page.locator('#transfer').click()
  ok(page.locator('#value-foup').inner_text()=='F018' and page.locator('#value-wafer').inner_text()=='W07' and page.locator('#value-slot').inner_text()=='03',f'explore/{width} move preserves identity')
  page.locator('#reset').click();page.locator('[data-slot="5"]').click()
  ok(page.locator('#value-wafer').inner_text()=='—',f'explore/{width} empty slot')
  page.screenshot(path=str(out/f'explore-empty-{width}.png'),full_page=True)
  page.goto('http://127.0.0.1:4175/er-atlas.html',wait_until='networkidle')
  ok(page.evaluate('ER_TEACHING.flowkey.image.includes("mes-055")'),f'ER/{width} shared content')
  page.close()
 b.close()
ok(not errors,'No JavaScript errors')
audit=json.loads((out/'after/audit.json').read_text(encoding='utf-8'))
for row in audit:
 ok(not row['overflow'] and all(i['loaded'] for i in row['images']),row['url']+str(row['width'])+' assets loaded')
(out/'checks.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS',len(checks),'checks')
