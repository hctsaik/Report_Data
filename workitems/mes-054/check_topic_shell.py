from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/topic.html?topic=qtime')
  assert page.locator('#mes-sitebar').is_visible()
  assert '單元 5' in page.locator('#mes-context').text_content()
  assert '單元 5' in page.locator('#mes-sequence').text_content()
  page.locator('#topic-refs a').first.click()
  page.wait_for_function('window.ER_ATLAS')
  assert page.locator('#selection-details').get_attribute('data-topic')=='qtime'
  page.locator('#mes-return').click()
  page.wait_for_url('**/topic.html?**')
  assert page.locator('#topic-title').text_content().startswith('QTime')
  page.locator('#topic-next a').first.click()
  page.wait_for_url('**/learning.html?**')
  assert 'unit=5' in page.url
  assert not errors,errors
  page.close()
 b.close()
print('PASS topic shell units, footer, real ER link and return, learner return at both sizes')
