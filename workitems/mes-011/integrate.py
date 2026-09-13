from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[2]
baseline=root/'workitems/mes-011/baseline';baseline.mkdir(exist_ok=True)
files=['index.html','advanced.html','support.html','course-extension.js','freshness.html','ER/NEW/index.html']
for name in files:
    p=root/name; dest=baseline/name;dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():dest.write_bytes(p.read_bytes())
def edit(name,old,new):
    p=root/name;s=p.read_text(encoding='utf-8');assert old in s,name;p.write_text(s.replace(old,new,1),encoding='utf-8')
edit('index.html','<p class="eyebrow">第一課','<a class="course-link" href="data-map.html#2676">資料與物理意義：ER 圖導讀 →</a>\n      <p class="eyebrow">第一課')
for name in ['advanced.html','support.html']:
    edit(name,'</nav></header>','<a href="data-map.html">ER 圖導讀</a></nav></header>')
edit('course-extension.js',"  const main=document.querySelector('main');","  if(nav&&!nav.querySelector('[data-er]')){const a=document.createElement('a');a.href='data-map.html';a.textContent='ER 圖導讀';a.dataset.er='true';nav.append(a);}\n  const main=document.querySelector('main');")
edit('freshness.html','</head>','<script defer src="data-map-link.js"></script></head>')
edit('ER/NEW/index.html','<h1>ER 原圖 → SVG 重畫</h1>','<a href="../../data-map.html">← 回到資料與物理意義教學</a><h1>ER 原圖 → SVG 重畫</h1>')
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'ER/NEW').glob('267*.svg')}
(root/'workitems/mes-011/original-svg-hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
print('Integrated six course entry points; preserved seven SVG hashes.')
