from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-033');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for ref,query in [('2672:transfer','Mfg_Carrier'),('2672:mes-transfer','MES'),('2672:mcs-history','MCS'),('2672:mcs-transfer','MCS')]:
   page.locator('#find').fill(query);nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',ref)
   target=page.locator(f'[data-result="{nid}"]');target.tap() if width==390 else target.click()
   for term in ['presum','原始','FOUP']:assert term in page.locator('#meaning').text_content()
   assert page.locator('.teaching-figure').is_visible()
   page.wait_for_function('document.getElementById("teaching-image").complete&&document.getElementById("teaching-image").naturalWidth>0')
   page.locator('#open-teaching').click()
   assert page.locator('#teaching-large').get_attribute('src').endswith('transfer-history-mobile-v1.png' if width==390 else 'transfer-history-v1.png');page.keyboard.press('Escape')
   if ref in ['2672:transfer','2672:mcs-history']:page.locator('#selection-details').screenshot(path=str(out/f'{width}-{ref.split(":")[1]}.png'))
  page.locator('[data-mcs-event="2"]').click();assert '轉彎 C' in page.locator('.mcs-event-detail').text_content()
  assert not errors,errors
 b.close()
print('PASS four transfer refs: original/presum text, desktop/mobile images, modal, retained MCS trace')
