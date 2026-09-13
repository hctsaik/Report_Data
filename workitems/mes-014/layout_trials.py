from pathlib import Path
import subprocess
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];O=R/'ER/INTEGRATED';exe=next((R/'tools/vendor/graphviz').rglob('dot.exe'))
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1500,'height':1100})
 for layout in ['dot','fdp','sfdp']:
  src=(O/'er-prototype-v1.dot').read_text(encoding='utf-8').replace('layout=neato',f'layout={layout}').replace('sep="+32"','sep="+14"')
  src=src.replace('overlap=prism','overlap=prism,overlap_shrink=true')
  name='trial-'+layout;(O/(name+'.dot')).write_text(src,encoding='utf-8')
  r=subprocess.run([str(exe),'-Tsvg',str(O/(name+'.dot')),'-o',str(O/(name+'.svg'))],capture_output=True,text=True);print(layout,r.returncode,r.stderr[:500])
  page.goto('http://127.0.0.1:4175/ER/INTEGRATED/'+name+'.svg');page.evaluate("document.documentElement.setAttribute('width','1500');document.documentElement.setAttribute('height','1100')")
  page.screenshot(path=str(R/'tests/evidence/mes-014'/(name+'.png')))
 b.close()
