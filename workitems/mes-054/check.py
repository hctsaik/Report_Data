"""MES-054 browser checks. Actual browser input; no visual quality scoring."""
from pathlib import Path
from urllib.parse import urljoin, urlsplit, parse_qs
import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
BASE = 'http://127.0.0.1:4175/'
OUT = Path('tests/evidence/mes-054')
OUT.mkdir(parents=True, exist_ok=True)
results, failures = [], []


def record(name, success, detail=None):
    entry = {'name': name, 'pass': bool(success), 'detail': detail}
    results.append(entry)
    if not success:
        failures.append(entry)
        print('FAIL', name, detail, flush=True)


def audit(page, path, width, screenshot=False):
    errors, bad = [], []
    def err(e): errors.append(str(e))
    def response(r):
        if r.status >= 400 and r.url.startswith(BASE): bad.append([r.status, r.url])
    page.on('pageerror', err)
    page.on('response', response)
    try:
        res = page.goto(urljoin(BASE, path), wait_until='networkidle')
        page.wait_for_timeout(80)
        page.evaluate("""async()=>{await Promise.all([...document.images].filter(i=>i.getAttribute('src')&&!i.closest('dialog')).map(i=>{i.loading='eager';return i.complete?Promise.resolve():new Promise(r=>{i.onload=r;i.onerror=r;setTimeout(r,3000)})}))}""")
        metrics = page.evaluate("""()=>({title:document.title,h1:document.querySelector('h1')?.textContent,overflow:document.documentElement.scrollWidth-innerWidth,broken:[...document.images].filter(i=>i.getAttribute('src')&&!i.closest('dialog')&&(!i.complete||!i.naturalWidth)).map(i=>i.getAttribute('src'))})""")
        status=res.status if res else 'same-document'
        success = status in [200,'same-document'] and not errors and not bad and metrics['overflow'] <= 2 and not metrics['broken']
        record(f'load:{width}:{path}', success, {'status':status, **metrics, 'errors':errors, 'http':bad})
        if screenshot:
            name = path.replace('?', '-').replace('=', '-').replace('&','-').replace('#','-').replace('/','-')
            page.screenshot(path=str(OUT/f'{width}-{name}.png'), full_page=True)
        return page.eval_on_selector_all('a[href]', '(es)=>es.map(e=>e.getAttribute("href"))')
    except Exception as exc:
        record(f'load:{width}:{path}', False, str(exc))
        return []
    finally:
        page.remove_listener('pageerror', err)
        page.remove_listener('response', response)


def run():
    with sync_playwright() as p:
        browser=p.chromium.launch()
        discover=browser.new_page()
        discover.goto(BASE+'er-atlas.html')
        discover.wait_for_function('window.ER_TOPIC_CONTENT&&window.ER_ATLAS')
        keys=discover.evaluate('Object.keys(ER_TOPIC_CONTENT.topics)')
        topic_keys=sorted(set(keys+['lot','carrier','equipment','flow','recipe','qtime','predispatch','wph']))
        discover.goto(BASE+'learning.html')
        lesson_paths=discover.evaluate('MES_CATALOG.units.flatMap(u=>u.lessons.map(l=>l.href))')
        discover.close()
        for width in [1440,390]:
            page=browser.new_page(viewport={'width':width,'height':1000},has_touch=width==390)
            paths=['learning.html']+[f'learning.html?unit={n}' for n in range(10)]+['tasks.html','topic.html']
            paths += [f'topic.html?topic={key}' for key in topic_keys]
            paths += ['index.html#fab','operations.html#tool','operations.html#lab','flow.html#lab','freshness.html','advanced.html','support.html','data-map.html','subject-er.html','er-atlas.html']
            paths=list(dict.fromkeys(paths+lesson_paths+['learning.html?view=instructor','learning.html?view=reference','learning.html?route=field','learning.html?route=data']))
            discovered=set()
            for path in paths:
                links=audit(page,path,width,screenshot=path in ['learning.html','learning.html?unit=3','tasks.html','topic.html?topic=lot','operations.html#lab','flow.html#lab'])
                for link in links:
                    target=urlsplit(urljoin(BASE+path,link))
                    if target.netloc==urlsplit(BASE).netloc and target.path.endswith('/tasks.html') and target.fragment:
                        discovered.add('tasks.html#'+target.fragment)
            for path in sorted(discovered):
                audit(page,path,width,screenshot=True)
            # No-hash legacy home must resolve to new orientation.
            page.goto(BASE+'index.html');page.wait_for_timeout(200)
            record(f'home-redirect:{width}', 'learning.html' in page.url, page.url)
            # Existing ER actual pointer selections remain usable.
            page.goto(BASE+'er-atlas.html');page.wait_for_function('window.ER_ATLAS')
            for ref,label in [('2671:lot','Lot'),('2671:cast','FOUP'),('2671:eqp','EQP'),('2673:flow','Flow'),('2677:recipe','Recipe')]:
                page.locator('#overview').click()
                nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',ref)
                node=page.locator('[data-node="'+nid+'"]')
                node.scroll_into_view_if_needed();page.wait_for_timeout(120)
                box=node.bounding_box()
                x,y=box['x']+box['width']/2,box['y']+box['height']/2
                if width==390: page.touchscreen.tap(x,y)
                else: page.mouse.click(x,y)
                topic=page.locator('#selection-details').get_attribute('data-topic')
                record(f'er-pointer:{width}:{label}', topic=={'Lot':'lot','FOUP':'carrier','EQP':'equipment','Flow':'flow','Recipe':'recipe'}[label],topic)
            # Keyboard can reach and activate navigation using actual keys.
            page.goto(BASE+'learning.html')
            page.keyboard.press('Tab')
            focus=page.evaluate('({tag:document.activeElement.tagName,text:document.activeElement.textContent,href:document.activeElement.getAttribute("href")})')
            record(f'keyboard-focus:{width}',focus['tag'] in ['A','BUTTON'],focus)
            page.keyboard.press('Enter')
            page.wait_for_timeout(100)
            target=urlsplit(urljoin(BASE+'learning.html',focus['href'] or ''))
            record(f'keyboard-activation:{width}',urlsplit(page.url).path==target.path,page.url)
            page.close()
        browser.close()


if __name__=='__main__':
    try: run()
    except Exception as exc: record('uncaught',False,str(exc))
    (OUT/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(results)-len(failures)}/{len(results)} checks passed; {len(failures)} failures',flush=True)
    raise SystemExit(bool(failures))
