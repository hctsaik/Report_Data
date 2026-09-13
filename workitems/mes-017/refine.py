"""One-time readability refinement; do not rerun."""
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'er-focus.js';s=p.read_text(encoding='utf-8')
s=s.replace("const $=id=>document.getElementById(id);", "const $=id=>document.getElementById(id);\n  const pageSize=()=>window.innerWidth<=950?2:4;")
s=s.replace('branches.slice(page*4,page*4+4)','branches.slice(page*pageSize(),(page+1)*pageSize())')
s=s.replace('Math.ceil(branches.length/4)','Math.ceil(branches.length/pageSize())')
s=s.replace("$('focus-title').textContent=nodes.get(root).labels[0]", "page=Math.min(page,pages-1);$('focus-title').textContent=nodes.get(root).labels[0]")
s=s.replace('`${p*4+1}', '`${p*pageSize()+1}') if False else s
s=s.replace('p*4+1','p*pageSize()+1').replace('p*4+4','(p+1)*pageSize()')
s=s.replace('點相關節點可改換主詞；菱形保留原圖關係與鍵。','點相關節點可改換主詞。同一實體可重複顯示，以分開不同關係；此圖未展開所有間接關聯。')
s=s.replace("const more=$('focus-more');", "if(nodes.get(root).refs.some(r=>r.node==='lot'))$('focus-note').append(' 來源未列 Wafer entity，本圖不補造其連線。');const more=$('focus-more');")
s=s.replace("paint();if(nodes.get(id).refs.some(r=>r.node==='lot'))$('focus-note').append(' 來源未列 Wafer entity，因此本圖不補造 Wafer 連線。');","paint();")
p.write_text(s,encoding='utf-8')
p=r/'er-atlas.html';s=p.read_text(encoding='utf-8').replace('<div id="focus-graph"></div><div id="focus-more"></div>','<div id="focus-more"></div><div id="focus-graph"></div>')
s=s.replace('<h3>這一段關係</h3><div id="path-list"></div>','<details><summary>原圖逐線對照</summary><div id="path-list"></div></details>')
p.write_text(s,encoding='utf-8')
p=r/'er-focus.css';s=p.read_text(encoding='utf-8').replace('#inspector>h3:has(+ #path-list),#path-list{display:none}\n','');p.write_text(s,encoding='utf-8')
p=r/'er-atlas.js';s=p.read_text(encoding='utf-8').replace("framedIds=[id];drawFrames();}","framedIds=[id];drawFrames();if(innerWidth<=950&&!$('focus-dialog').open)$('focus-panel').scrollIntoView({block:'start'});}")
p.write_text(s,encoding='utf-8')
