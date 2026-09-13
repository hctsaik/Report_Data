"""Replay every reachable lab node with real clicks, record visible state."""
from pathlib import Path
from collections import deque
import json
from playwright.sync_api import sync_playwright
OUT=Path('tests/evidence/mes-054/lab');OUT.mkdir(parents=True,exist_ok=True)
rows=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':1000},has_touch=width==390)
  for course in ['operations','flow']:
   page.goto(f'http://127.0.0.1:4175/{course}.html#lab');page.wait_for_selector('[data-scenario]')
   scenarios=page.evaluate('(k)=>SCENARIOS[k].map(s=>({id:s.id,nodes:s.nodes}))',course)
   for scenario in scenarios:
    paths={'start':[]};queue=deque(['start'])
    while queue:
     node=queue.popleft()
     for i,a in enumerate(scenario['nodes'][node]['actions']):
      nxt=a.get('next')
      if nxt and nxt not in paths: paths[nxt]=paths[node]+[i];queue.append(nxt)
    for node,path in paths.items():
     page.locator(f'[data-scenario="{scenario["id"]}"]').click()
     page.locator('#reset-scenario').click()
     for action in path: page.locator(f'[data-action="{action}"]').click()
     actual=page.locator('#scenario-prompt').text_content()
     expected=scenario['nodes'][node]['prompt']
     overflow=page.evaluate('document.documentElement.scrollWidth-innerWidth')
     assert actual==expected,(course,scenario['id'],node,actual,expected)
     assert overflow<=2,(course,scenario['id'],node,overflow)
     page.locator('#sim-state').screenshot(path=str(OUT/f'{width}-{course}-{scenario["id"]}-{node}.png'))
     rows.append({'width':width,'course':course,'scenario':scenario['id'],'node':node,'prompt':actual,'overflow':overflow})
    print(width,course,scenario['id'],len(paths),flush=True)
  page.close()
 b.close()
(OUT/'states.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS',len(rows),'reachable lab states with real clicks; screenshots are evidence, not quality scores')
