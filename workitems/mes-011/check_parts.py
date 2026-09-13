from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page();errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 for width in [1440,360]:
  page.set_viewport_size({'width':width,'height':900})
  for n in range(2671,2678):
   page.goto(f'http://127.0.0.1:4175/data-map.html?view=original#{n}')
   page.wait_for_function("document.querySelector('#original-object')?.contentDocument?.documentElement.tagName==='svg'")
   assert page.locator('[data-case]').count()==0
   assert page.locator('#original-part').get_attribute('aria-current')=='page'
   page.locator('#original-plus').click();assert page.locator('#original-scale').inner_text()=='150%'
   page.locator('#original-fit').click()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   if n==2676:page.screenshot(path=str(root/f'tests/evidence/mes-011/parts-original-{width}.png'),full_page=True)
   page.locator('#questions-part').click();page.wait_for_selector('[data-case]')
   assert page.url.endswith(f'view=questions#{n}')
   assert page.locator('[data-case]').count()==2
   assert page.locator('#questions-part').get_attribute('aria-current')=='page'
   if n==2676:page.screenshot(path=str(root/f'tests/evidence/mes-011/parts-questions-{width}.png'))
 assert not errors,errors
 b.close()
print('PASS: 7 diagrams x 2 parts x 2 widths; original zoom/reset and same-diagram navigation')
