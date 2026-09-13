from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-052');out.mkdir(parents=True,exist_ok=True)
keys=['bmir','portmode','lotstatus','wip']
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto('http://127.0.0.1:4175/er-atlas.html');page.wait_for_function('window.ER_ATLAS')
  for key in keys:
   refs=page.evaluate('(k)=>ER_TOPIC_CONTENT.topics[k].refs',key)
   for ref in refs:
    page.evaluate('(r)=>ER_ATLAS.selectNode(ER_ATLAS.model.mapping[r])',ref)
    assert page.locator('#selection-details').get_attribute('data-topic')==key
    assert page.locator('#selection-title').text_content()==page.evaluate('(k)=>ER_TOPIC_CONTENT.topics[k].title',key)
    assert page.locator('.teaching-figure').is_visible()
   nid=page.evaluate('(r)=>ER_ATLAS.model.mapping[r]',refs[0])
   # Trigger actual search selection using the node's source text.
   label=page.evaluate('(id)=>document.getElementById(id).textContent',nid)
   page.locator('#find').fill(label.strip().split('\n')[0][:12])
   result=page.locator(f'[data-result="{nid}"]')
   if result.count()==0:
    page.locator('#find').fill({'bmir':'BMIR','portmode':'模式','lotstatus':'Status','wip':'KER_WIP_BT'}[key])
   result.tap() if width==390 else result.click()
   page.wait_for_function('document.getElementById("teaching-image").complete && document.getElementById("teaching-image").naturalWidth>0')
   page.locator('#selection-details').screenshot(path=str(out/f'{key}-{width}.png'))
   expected=page.evaluate('(x)=>ER_TOPIC_CONTENT.topics[x[0]][x[1]]',[key,'mobile' if width==390 else 'image'])
   page.locator('#open-teaching').click();assert page.locator('#teaching-large').get_attribute('src').endswith(expected);page.keyboard.press('Escape')
  page.locator('#routes [data-route="wip"]').click()
  assert '每天' in page.locator('#meaning').text_content()
  snap=page.evaluate('ER_ATLAS.model.mapping["2675:wip-history"]')
  assert '星期一' not in page.locator('[id="'+snap+'"]').text_content()
  assert page.evaluate('ER_TOPIC_CONTENT.topics.portdata.details')==''
  assert not errors,errors
  page.close()
 b.close()
print('PASS four topics, eight references, eight responsive views, search and enlargement; Port detail remains withdrawn')
