from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-036');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref,query in [('2671:material','FRLot_MtrlContnrs'),('2671:material-link','FrlotMtrl')]:
   page.locator('#find').fill(query);nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',ref)
   btn=page.locator(f'[data-result="{nid}"]');btn.tap() if width==390 else btn.click()
   for term in ['主詞是 FOUP','FRCAST_LOT','相同']:assert term in page.locator('#meaning').text_content()
   assert '互換' in page.locator('#topic-detail').text_content()
   page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
   page.locator('#open-teaching').click();assert page.locator('#teaching-large').get_attribute('src').endswith('foup-query-lot-mobile-v1.png' if width==390 else 'foup-query-lot-v1.png');page.keyboard.press('Escape')
   page.locator('#selection-details').screenshot(path=str(out/f'{width}-{ref.split(":")[1]}.png'))
  assert not errors,errors
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 b.close()
print('PASS material FOUP/relationship: confirmed semantics, desktop/mobile figures and real selection')
