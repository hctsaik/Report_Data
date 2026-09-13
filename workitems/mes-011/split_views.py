from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'data-map.js'
s=p.read_text(encoding='utf-8')
needle="$('content').innerHTML=`<p class=\"eyebrow\">FAB × DATA / ER"
replacement="""const original=new URLSearchParams(location.search).get('view')==='original';for(const [id,view] of [['original-part','original'],['questions-part','questions']]){const a=$(id);a.href=`?view=${view}#${active.id}`;if(original===(view==='original'))a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');}if(original){renderOriginal();return;}$('content').innerHTML=`<p class="eyebrow">FAB × DATA / ER"""
assert needle in s
s=s.replace(needle,replacement)
s=s.replace("window.addEventListener('hashchange',render);render();", """
function renderOriginal(){
 $('content').innerHTML=`<p class="eyebrow">01 原圖 / ER ${active.id}</p><h1>${active.short}</h1><p>完整呈現已校字的 SVG 關係圖，保留所有節點與連線。可放大查看細節，或對照原始照片。</p><section class="map-panel"><div class="map-tools"><button id="original-fit">完整圖</button><button id="original-minus">− 縮小</button><output id="original-scale">100%</output><button id="original-plus">＋ 放大</button><a href="ER/NEW/${active.id}.svg" target="_blank" rel="noopener">另開原圖</a><a href="ER/NEW/${active.id}.svg" download>下載 SVG</a></div><div class="map-scroll original-scroll"><object id="original-object" data="ER/NEW/${active.id}.svg" type="image/svg+xml" aria-label="完整 ER ${active.id}"></object></div></section><details class="original-photo"><summary>對照原始照片（未修改）</summary><a href="ER/ORG/${active.id}.jpg" target="_blank" rel="noopener"><img src="ER/ORG/${active.id}.jpg" alt="ER ${active.id} 原始照片" loading="lazy"></a></details><p class="related"><a href="?view=questions#${active.id}">前往這張圖的聚焦題目 →</a></p>`;
 let z=1;const o=$('original-object');const resize=()=>{o.style.width=z*100+'%';o.style.height=z*100+'%';$('original-scale').textContent=Math.round(z*100)+'%';};o.onload=()=>{const svg=o.contentDocument?.documentElement;if(svg?.tagName.toLowerCase()==='svg'){svg.setAttribute('width','100%');svg.setAttribute('height','100%');}};$('original-fit').onclick=()=>{z=1;resize()};$('original-plus').onclick=()=>{z=Math.min(6,z+.5);resize()};$('original-minus').onclick=()=>{z=Math.max(1,z-.5);resize()};
}
window.addEventListener('hashchange',render);render();""")
p.write_text(s,encoding='utf-8')
p=root/'course.js';s=p.read_text(encoding='utf-8');s=s.replace('<a href="data-map.html#2676" data-er-sidebar>ER 圖 · 資料與物理意義</a>','<a href="data-map.html?view=original#2676" data-er-sidebar>ER 圖 · 原圖</a><br><a href="data-map.html?view=questions#2676">ER 圖 · 聚焦題目</a>');p.write_text(s,encoding='utf-8')
for name in ['operations.html','flow.html']:
 p=root/name;s=p.read_text(encoding='utf-8').replace('er-sidebar-20260913','er-parts-20260913');p.write_text(s,encoding='utf-8')
