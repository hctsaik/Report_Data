from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-030');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for key in ['carrier','lot']:
   page.locator(f'[data-entity="{key}"]').click()
   assert '不同 Lot ID' in page.locator('#meaning').text_content()
   assert page.locator('[data-lw-slot]').count()==25
   assert page.locator('.wafer-slot.lot-a').count()==25
   assert len(set(page.locator('.wafer-disc').all_text_contents()))==25
   page.locator('[data-lw-mode="multiple"]').click()
   assert page.locator('.wafer-slot.lot-a').count()==10
   assert page.locator('.wafer-slot.lot-b').count()==15
   page.locator('[data-lw-slot="11"]').click()
   assert page.locator('.wafer-record dd').all_text_contents()==['W011','L024','F012','11']
   page.locator('[data-lw-mode="single"]').click()
   assert page.locator('.wafer-record dd').all_text_contents()==['W011','L023','F012','11']
  page.locator('[data-entity="carrier"]').click()
  page.locator('#lot-wafer-demo').screenshot(path=str(out/f'{width}-single.png'))
  page.locator('[data-lw-mode="multiple"]').click();page.locator('[data-lw-slot="11"]').click()
  page.locator('#lot-wafer-demo').screenshot(path=str(out/f'{width}-multiple.png'))
  page.locator('#inspector-expand').click()
  assert page.locator('#inspector-dialog [data-lw-slot]').count()==25
  assert page.locator('.wafer-record dd').all_text_contents()==['W011','L024','F012','11']
  page.keyboard.press('Escape')
  page.locator('#routes [data-route="load"]').click();assert page.locator('[data-lw-slot]').count()==25
  page.locator('#find').fill('Siview.Frcast_lot');nid=page.evaluate('ER_ATLAS.model.mapping["2671:cast-link"]')
  target=page.locator(f'[data-result="{nid}"]');target.tap() if width==390 else target.click()
  assert page.locator('[data-lw-slot]').count()==25
  page.locator('[data-entity="recipe"]').click();assert page.locator('#lot-wafer-demo').count()==0
  assert page.locator('.teaching-figure').is_visible()
  assert not errors,errors
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 b.close()
print('PASS: single/multiple lot, 25 unique wafers/slots, click details, entity/relation/route, desktop/mobile/dialog')
