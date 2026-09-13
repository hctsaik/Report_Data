from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    page=b.new_page()
    for w in [1440,360]:
        page.set_viewport_size({'width':w,'height':900})
        page.goto('http://127.0.0.1:4175/index.html#fab')
        page.wait_for_timeout(700)
        box=page.locator('.er-course-entry').bounding_box()
        assert box['y']>=72 and box['y']+box['height']<900,box
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        page.screenshot(path=f'tests/evidence/mes-011/home-entry-{w}.png')
    page.locator('.er-course-entry').click()
    page.wait_for_selector('[data-case]')
    print('PASS: entry within first viewport at both widths; navigation works')
    b.close()
