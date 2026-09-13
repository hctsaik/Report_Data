from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[2]
p=root/'course.js'
s=p.read_text(encoding='utf-8')
old='<a href="freshness.html">第四部分 · 資料新鮮度</a></div></aside>'
new='<a href="freshness.html">第四部分 · 資料新鮮度</a><br><a href="data-map.html#2676" data-er-sidebar>ER 圖 · 資料與物理意義</a></div></aside>'
if old in s:
    (root/'workitems/mes-011/baseline/course-before-sidebar.js').write_text(s,encoding='utf-8')
    p.write_text(s.replace(old,new),encoding='utf-8')
else:
    assert 'data-er-sidebar' in s
for name in ['operations.html','flow.html']:
    p=root/name
    s=p.read_text(encoding='utf-8').replace('src="course.js"','src="course.js?v=er-sidebar-20260913"')
    p.write_text(s,encoding='utf-8')

with sync_playwright() as pw:
    b=pw.chromium.launch()
    page=b.new_page()
    for name,anchor in [('operations','port'),('flow','stage')]:
        for width in [1440,360]:
            page.set_viewport_size({'width':width,'height':900})
            page.goto(f'http://127.0.0.1:4175/{name}.html#{anchor}')
            link=page.locator('[data-er-sidebar]')
            link.wait_for(state='attached')
            if width==360:
                page.locator('#menu-toggle').click()
            link.scroll_into_view_if_needed()
            assert link.is_visible()
            page.locator('.aside-foot').screenshot(path=str(root/f'tests/evidence/mes-011/{name}-sidebar-{width}.png'))
            link.click()
            page.wait_for_selector('[data-case]')
            assert page.url.endswith('data-map.html#2676')
    b.close()
print('PASS: operations/flow sidebar ER link visible and clickable on desktop/mobile')
