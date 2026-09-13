"""MES-008: actual HTTP pages, source-age semantics and keyboard/UI checks.
Screenshots are evidence for human inspection, never an automatic quality score.
"""
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'tests/evidence/mes-008'
OUT.mkdir(parents=True,exist_ok=True)
chapters=['architecture','decision','ai','history','join','contract']
report={'pages':[],'interactions':[],'errors':[],'assets':{}}
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def shot(page,name,locator=None):
    dest=OUT/(name+'.png')
    if locator: locator.screenshot(path=str(dest),animations='disabled',style='.topbar{visibility:hidden!important}')
    else:
        page.evaluate('scrollTo(0,0)')
        page.screenshot(path=str(dest),full_page=True,animations='disabled')
    return {'path':dest.relative_to(ROOT).as_posix(),'sha256':digest(dest)}
def check(page,chapter,width,kind):
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(chapter,width,kind,'horizontal overflow')
    report['interactions'].append([chapter,width,kind])
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    for width in [1440,800,360]:
        page=browser.new_page(viewport={'width':width,'height':960 if width>700 else 844},reduced_motion='reduce')
        page.on('pageerror',lambda e:report['errors'].append(str(e)))
        for chapter in chapters:
            page.goto(f'http://127.0.0.1:4175/freshness.html#{chapter}',wait_until='networkidle')
            page.wait_for_function('Array.from(document.images).filter(i=>i.getAttribute("src")).every(i=>i.complete&&i.naturalWidth>0)')
            assert page.locator('h1').count()==1
            assert page.locator('.lesson-art').count()==1
            assert page.locator('[aria-current=step]').get_attribute('data-chapter')==chapter
            image=page.locator('.lesson-art img')
            current=urlparse(image.evaluate('(i)=>i.currentSrc')).path.lstrip('/')
            assert ('mobile' in current)==(width<=700),(width,current)
            data=urlopen('http://127.0.0.1:4175/'+current).read()
            assert hashlib.sha256(data).hexdigest()==digest(ROOT/current)
            report['assets'][current]=digest(ROOT/current)
            row={'id':chapter,'width':width,'image':current,'box':image.bounding_box(),
                 'page':shot(page,f'{chapter}-{width}'),
                 'art':shot(page,f'{chapter}-{width}-art',page.locator('.lesson-art'))}
            report['pages'].append(row)
            check(page,chapter,width,'default')
            page.locator('[data-fresh-zoom]').click()
            assert page.locator('#fresh-art-dialog').evaluate('(d)=>d.open')
            page.wait_for_function('document.querySelector("#fresh-art-dialog img").naturalWidth>0')
            page.keyboard.press('Escape')
            assert not page.locator('#fresh-art-dialog').evaluate('(d)=>d.open')
            assert page.locator('[data-fresh-zoom]').evaluate('(b)=>b===document.activeElement')
            check(page,chapter,width,'zoom and Escape restore focus')
            for i in range(3):
                choice=page.locator(f'[data-challenge-choice="{i}"]')
                choice.click()
                assert choice.get_attribute('aria-pressed')=='true'
                assert len(page.locator('.challenge-feedback').inner_text())>20
                check(page,chapter,width,f'transfer choice {i}')
            shot(page,f'{chapter}-{width}-exercise',page.locator('.transfer-question'))
            for d in page.locator('.fresh-detail').all():
                d.locator('summary').click()
                assert d.evaluate('(d)=>d.open')
                check(page,chapter,width,'expanded reference')
                if chapter in ['architecture','contract','join']:
                    shot(page,f'{chapter}-{width}-reference',d)
                d.locator('summary').click()
            if chapter=='architecture':
                for key,expected in [('native','Reporting DB'),('mart','整理／刷新'),('tx','TX 交易介面')]:
                    page.locator(f'[data-route="{key}"]').click()
                    assert expected in page.locator('#route-trace').inner_text()
                    if key=='tx': assert 'Reporting' not in page.locator('#route-trace').inner_text()
                    check(page,chapter,width,'route '+key)
                    shot(page,f'architecture-{width}-{key}',page.locator('.fresh-activity'))
            elif chapter=='decision':
                for key in ['analysis','monitor','control']:
                    page.select_option('#decision-purpose',key)
                    assert page.locator(f'[data-level="{key}"]').evaluate('(e)=>e.classList.contains("selected")')
                    answer=page.locator('#decision-answer').inner_text()
                    assert {'analysis':'Data Mart','monitor':'來源時間','control':'重新驗證'}[key] in answer
                    check(page,chapter,width,'purpose '+key)
                    shot(page,f'decision-{width}-{key}',page.locator('.fresh-activity'))
            elif chapter=='ai':
                for key,step,time,age in [('native','ETCH','10:00','1 分鐘'),('mart','DEV','09:51','10 分鐘'),('tx','ETCH','10:01','0 分鐘')]:
                    for purpose in ['monitor','control']:
                        page.select_option('#ai-source',key)
                        page.select_option('#ai-tolerance',purpose)
                        assert page.locator('#query-step').inner_text()==step
                        assert page.locator('#query-time').inner_text()==time
                        assert page.locator('#query-age').inner_text()==age
                        if purpose=='control':
                            assert '重驗' in page.locator('#ai-answer').inner_text()
                            assert '改找 Native 或 TX' not in page.locator('#ai-answer').inner_text()
                        check(page,chapter,width,key+' '+purpose)
                        shot(page,f'ai-{width}-{key}-{purpose}',page.locator('.fresh-activity'))
            elif chapter=='history':
                for kind in ['event','current']:
                    for complete in ['yes','no']:
                        page.select_option('#history-question',kind)
                        page.select_option('#history-complete',complete)
                        text=page.locator('#history-answer').inner_text()
                        if kind=='current': assert '不能證明現在' in text
                        elif complete=='no': assert '不能回答「沒經過」' in text
                        else: assert '昨天有經過 DEV' in text
                        fill=page.locator('#coverage-fill').evaluate('(e)=>e.style.width')
                        assert fill==('100%' if complete=='yes' else '50%')
                        check(page,chapter,width,kind+' '+complete)
                        shot(page,f'history-{width}-{kind}-{complete}',page.locator('.fresh-activity'))
            elif chapter=='join':
                before=page.locator('.older-field').inner_text()
                page.locator('#refresh-table').click()
                assert page.locator('#join-refresh-time').inner_text()=='10:01'
                assert page.locator('.older-field').inner_text()==before
                assert page.locator('#refresh-table').is_disabled()
                assert '09:51' in page.locator('#join-answer').inner_text()
                check(page,chapter,width,'refresh keeps source age')
                shot(page,f'join-{width}-refreshed',page.locator('.fresh-activity'))
                page.locator('#reset-join').click()
                assert page.locator('#join-refresh-time').inner_text()=='10:00'
                check(page,chapter,width,'reset')
            elif chapter=='contract':
                for key,source,time in [('step','SiView Native','10:00'),('hold','Hold Mart','09:51')]:
                    page.locator(f'[data-contract-field="{key}"]').click()
                    assert source in page.locator('#contract-facts').inner_text()
                    assert time in page.locator('#contract-facts').inner_text()
                    check(page,chapter,width,'column '+key)
                    shot(page,f'contract-{width}-{key}',page.locator('.fresh-activity'))
                with page.expect_download() as download:
                    page.locator('#download-contract').click()
                artifact=OUT/f'contract-{width}.json'
                download.value.save_as(str(artifact))
                contract=json.loads(artifact.read_text(encoding='utf-8'))
                assert contract['example'] is True
                assert contract['columns']['hold']['source_data_time']=='09:51'
                assert contract['loaded_at']=='10:01'
                assert contract['auto_control'].startswith('No;')
                check(page,chapter,width,'contract download')
            next_id=chapters[(chapters.index(chapter)+1)%len(chapters)]
            page.locator('#fresh-next').click()
            page.wait_for_url('**#'+next_id)
            assert page.locator('[aria-current=step]').get_attribute('data-chapter')==next_id
            check(page,chapter,width,'next lesson')
        if width==360:
            page.locator('#fresh-menu').click()
            assert page.locator('#fresh-menu').get_attribute('aria-expanded')=='true'
            page.locator('nav [data-chapter="join"]').click()
            assert page.locator('#fresh-menu').get_attribute('aria-expanded')=='false'
            check(page,'navigation',width,'mobile menu')
        page.close()
    browser.close()
for f in ['freshness.html','freshness.js','freshness.css','freshness-v2.js','freshness-v2.css']:
    assert urlopen('http://127.0.0.1:4175/'+f).read()==(ROOT/f).read_bytes(),f
    report['assets'][f]=digest(ROOT/f)
assert not report['errors'],report['errors']
(OUT/'browser-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'PASS: {len(report["pages"])} layouts, {len(report["interactions"])} behavior checks, {len(report["assets"])} HTTP/disk assets, no JS errors.')
