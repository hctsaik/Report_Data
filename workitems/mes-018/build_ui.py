from pathlib import Path
r=Path(__file__).resolve().parents[2];old=(r/'er-atlas.js').read_text(encoding='utf-8');teaching=old[old.index('const teaching='):old.index('function showTeaching(')]
logic=r'''const $=id=>document.getElementById(id),esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let model,topics,nodes,edges,current,branch,svg,base,zoom=1,request=0;
TEACHING
function showNode(id){const n=nodes.get(id),key=teachingForNode(id),t=teaching[key];$('selection').textContent=n.labels[0];$('meaning').textContent=t.meaning||'這是原圖保留的資料物件或關係／鍵。請沿圖中的實際連線閱讀，表名相近不代表同一資料或即時狀態。';
$('art').src=t.image;$('art').alt=t.alt;$('caption').textContent=key==='overview'?'現場物件基礎參考；不是此節點專屬示意。':t.caption;$('lesson').href=t.link;
const f={lot:[68,63,28,16],carrier:[34,19,33,65],equipment:[1,19,33,65]}[key];$('focus').hidden=!f;if(f){const a=$('focus');a.style.left=f[0]+'%';a.style.top=f[1]+'%';a.style.width=f[2]+'%';a.style.height=f[3]+'%';a.style.borderColor=t.color;}
const target=topics.find(x=>x.subject===id&&x.key!==current.key);$('switch').hidden=!target;if(target){$('switch').textContent='改以 '+target.title+' 為主詞 →';$('switch').onclick=()=>navigate(target.key,'core');}
$('sources').innerHTML=n.labels.map(x=>`<strong>${esc(x)}</strong><br>`).join('')+n.refs.map(r=>`<p><a href="data-map.html?view=original#${r.source}">查看來源</a><br>${r.labels.map(esc).join('<br>')}</p>`).join('');
svg.querySelectorAll('[data-node]').forEach(g=>g.classList.toggle('selected',g.id===id));}
function scale(value){zoom=Math.max(.25,Math.min(2,value));svg.style.width=base[2]*zoom+'px';svg.style.height=base[3]*zoom+'px';$('scale').textContent=Math.round(zoom*100)+'%';}
function navigate(key,part){const p=new URLSearchParams({subject:key,part});location.hash=p.toString();}
async function render(){const token=++request,p=new URLSearchParams(location.hash.slice(1));current=topics.find(t=>t.key===p.get('subject'))||topics[0];branch=current.branches.find(v=>v.key===p.get('part'))||null;const v=branch||current.core;
$('title').textContent='以 '+current.title+' 為主詞'+(branch?' · '+branch.title:'');$('description').textContent=branch?.description||current.description;
$('topics').innerHTML=topics.map(t=>`<button data-topic="${t.key}" style="--color:${teaching[t.key].color}" aria-pressed="${t.key===current.key}">${t.title}</button>`).join('');document.querySelectorAll('[data-topic]').forEach(b=>b.onclick=()=>navigate(b.dataset.topic,'core'));
$('branches').innerHTML=`<button data-part="core" aria-pressed="${!branch}">核心關係</button>`+current.branches.map(v=>`<button data-part="${v.key}" aria-pressed="${v===branch}">${v.title}</button>`).join('');document.querySelectorAll('[data-part]').forEach(b=>b.onclick=()=>navigate(current.key,b.dataset.part));
$('scope').textContent=`${v.nodes.length} 個節點 · ${v.edges.length} 條原始連線 · ${branch?'單一完整分支詳圖':'核心主題圖'}，另有 ${current.branches.length} 段詳圖可選`;
const url=`ER/SUBJECTS/${current.key}-${branch?.key||'core'}.svg`;const response=await fetch(url);if(!response.ok)throw Error('主題圖載入失敗');const text=await response.text();if(token!==request)return;
svg=document.importNode(new DOMParser().parseFromString(text,'image/svg+xml').documentElement,true);$('canvas').replaceChildren(svg);base=svg.getAttribute('viewBox').split(/\s+/).map(Number);scale(Math.max(.85,Math.min(1,$('canvas').clientWidth/base[2])));$('canvas').scrollTo(0,0);$('download').href=url;
svg.querySelectorAll('[data-node]').forEach(g=>{g.addEventListener('click',()=>showNode(g.id));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();showNode(g.id)}})});showNode(current.subject);window.SUBJECT_ER={model,topics,current:current.key,branch:branch?.key||'core'};}
$('fit').onclick=()=>scale(Math.min($('canvas').clientWidth/base[2],$('canvas').clientHeight/base[3]));$('readable').onclick=()=>scale(1);$('plus').onclick=()=>scale(zoom*1.2);$('minus').onclick=()=>scale(zoom/1.2);
$('open-image').onclick=()=>{$('large-art').src=$('art').src;$('large-art').alt=$('art').alt;$('large-caption').textContent=$('caption').textContent;$('large-focus').style.cssText=$('focus').style.cssText;$('large-focus').hidden=$('focus').hidden;$('image-dialog').showModal()};
async function start(){const [m,data]=await Promise.all([fetch('ER/INTEGRATED/er-model-v2.json').then(r=>r.json()),fetch('ER/SUBJECTS/subjects.json').then(r=>r.json())]);model=m;topics=data.subjects;nodes=new Map(m.nodes.map(n=>[n.id,n]));edges=m.edges;window.addEventListener('hashchange',()=>render().catch(fail));await render();}function fail(e){$('title').textContent='載入失敗：'+e.message;console.error(e)}start().catch(fail);
'''
(r/'subject-er.js').write_text(logic.replace('TEACHING',teaching).replace(r'/\\s+/',r'/\s+/'),encoding='utf-8')
