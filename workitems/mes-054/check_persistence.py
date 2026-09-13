from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page()
 page.goto('http://127.0.0.1:4175/learning.html?route=field')
 page.goto('http://127.0.0.1:4175/learning.html?unit=6')
 assert 'unit=9' in page.locator('.learn-footer a').last.get_attribute('href')
 page.goto('http://127.0.0.1:4175/learning.html?route=newcomer')
 page.goto('http://127.0.0.1:4175/freshness.html#architecture')
 page.locator('#fresh-next').click();page.wait_for_url('**#decision')
 page.goto('http://127.0.0.1:4175/flow.html#lab?case=normal')
 page.locator('#reset-scenario').click()
 action=page.locator('[data-action]').first;action.click()
 state=page.evaluate('getEngine().nodeId')
 assert page.locator('#mes-context').inner_text().find('單元 6')>=0
 page.locator('#mes-sitebar a').first.click()
 page.goto('http://127.0.0.1:4175/flow.html#lab?case=normal')
 assert page.evaluate('getEngine().nodeId')==state
 b.close()
print('PASS role-aware sequence, freshness internal progression, lab-case unit and saved scenario state')
