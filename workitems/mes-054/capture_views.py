from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('tests/evidence/mes-054/views');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000})
  for label,url in [('home','learning.html'),('unit3','learning.html?unit=3'),('task','tasks.html#not-running'),('topic','topic.html?topic=part')]:
   page.goto('http://127.0.0.1:4175/'+url,wait_until='networkidle')
   page.screenshot(path=str(out/f'{label}-{width}.png'))
  page.goto('http://127.0.0.1:4175/flow.html#lab',wait_until='networkidle')
  page.locator('[data-scenario="normal"]').click();page.locator('#reset-scenario').click()
  actions=page.evaluate("""()=>{const ns=SCENARIOS.flow.find(s=>s.id==='normal').nodes;let q=[['start',[]]],seen=new Set;while(q.length){const [id,path]=q.shift();if(id==='finish')return path;if(seen.has(id))continue;seen.add(id);ns[id].actions.forEach((a,i)=>{if(a.next)q.push([a.next,[...path,i]])})}}""")
  for action in actions:page.locator(f'[data-action="{action}"]').click()
  assert '已出貨' in page.locator('.sim').inner_text()
  page.locator('#sim-state').screenshot(path=f'tests/evidence/mes-054/lab/{width}-flow-normal-finish.png')
  page.locator('.sim').screenshot(path=str(out/f'flow-finish-{width}.png'))
  page.close()
 b.close()
