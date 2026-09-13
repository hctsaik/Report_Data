"""Only the new navigation added to existing lessons; old lesson content is unchanged."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parent/'evidence/mes-009/navigation'
OUT.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    page=b.new_page()
    for course in ['flow','operations']:
        page.goto(f'http://127.0.0.1:4175/{course}.html')
        anchors=page.locator('#sidebar nav a').evaluate_all('(items)=>items.map(a=>a.hash)')
        for width in [1440,800,360]:
            page.set_viewport_size({'width':width,'height':1000 if width>760 else 800})
            for anchor in anchors:
                page.goto(f'http://127.0.0.1:4175/{course}.html{anchor}')
                page.wait_for_function("document.querySelector('[data-advanced-note] a')!==null")
                assert page.locator('[data-advanced-note]').count()==1
                assert page.locator('[data-advanced]').count()==1
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                label=f'{course}-{anchor[1:]}-{width}'
                page.screenshot(path=str(OUT/(label+'.png')))
                results.append(label)
    b.close()
(OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS:',len(results),'existing-lesson navigation layouts')
