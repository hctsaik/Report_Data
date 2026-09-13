const $=id=>document.getElementById(id),esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let model,topics,nodes,edges,current,branch,svg,base,zoom=1,request=0;
const teaching={
overview:{image:'examples/fab-physical-data-v01.png',alt:'機台、FOUP、Slot、Wafer 與 Lot 資料對照',caption:'左側是現場，右側是資料。Lot 是生產批次；FOUP 是承載晶圓的實體容器。',link:'index.html#fab'},
lot:{title:'Lot：生產批次',refs:['2671:lot','2676:lot'],color:'#176ac2',image:'examples/fab-physical-data-v01.png',alt:'現場物件與右側 Lot L023 的資料對照',caption:'看右側 lot_id = L023：Lot 將這批晶圓組織成生產與追蹤單位。',meaning:'藍框標出 Lot 資料實體。Lot 本身不是盒子；沿著「放在」關係，才會找到承載它的 FOUP。不同 schema 證據的節點仍各自保留。',link:'index.html#lot'},
carrier:{title:'FOUP：承載晶圓的容器',refs:['2671:cast','2676:cast'],color:'#008775',image:'examples/fab-physical-data-v01.png',alt:'FOUP F012 內的 Slot 07 與 Wafer W07',caption:'看中間剖面：FOUP 內有 Slot，晶圓放在對應位置。',meaning:'綠框標出 FOUP 資料實體。FRCAST 描述載具，FRCAST_LOT 表達與 Lot 的裝載關係；兩者不是同一個物件。',link:'index.html#foup'},
equipment:{title:'EQP：執行作業的設備',refs:['2671:eqp','2676:eqp','2677:eqp'],color:'#b26018',image:'examples/fab-physical-data-v01.png',alt:'FOUP F012 放在 ETCH-03 設備的 LP1',caption:'看左側 ETCH-03 與 LP1：設備、Port、FOUP 有不同身分。',meaning:'橘框標出 EQP 資料實體。設備可與 Port、Chamber、派工及 Recipe 配置相連；「預派」不能直接證明載具已經到達。',link:'operations.html#port'},
flow:{title:'Flow：批次遵循的製程路徑',refs:['2673:flow'],color:'#7756af',image:'assets/mes-v3/stage-v2.png',alt:'三個 Stage、六個 Step，以及目前在 S50 的 Lot',caption:'整條是 Flow；每段是 Stage；每一站是 Step。Lot 有自己的執行進度。',meaning:'紫框標出 Flow 資料對象。從 Lot 的 Part／Mainpd_id 關係找到流程定義，再區分「路徑如何定義」與「這批目前走到哪裡」。',link:'flow.html#stage'},
recipe:{title:'Recipe：從邏輯要求到設備配置',refs:['2673:lr-eqp','2677:recipe'],color:'#7756af',image:'assets/mes-009/recipes.png',alt:'LR、ER 與實際加工 Physical Recipe 的教學對照',caption:'示意值用來理解三層概念；實際名稱與映射仍以廠內定義為準。',meaning:'紫框分別指出 LR 與 ER 相關資料。ER 連線呈現配置關係；要知道某批實際用了哪個 Physical Recipe，還需要該次執行紀錄及版本證據。',link:'advanced.html#recipes'}
};
function teachingForNode(id){
 for(const key of ['recipe','equipment','carrier','lot','flow'])if(teaching[key].refs.some(ref=>model.mapping[ref]===id))return key;
 const recipeRefs=['2677:recipe-key','2677:recipe-eqp','2677:pd','2677:pd-key','2677:pd-eqp','2673:lr-eqp-link'];
 if(recipeRefs.some(ref=>model.mapping[ref]===id))return 'recipe';
 return 'overview';
}

function showNode(id){const n=nodes.get(id),key=teachingForNode(id),t=teaching[key];$('selection').textContent=n.labels[0];$('meaning').textContent=t.meaning||'這是原圖保留的資料物件或關係／鍵。請沿圖中的實際連線閱讀，表名相近不代表同一資料或即時狀態。';
$('art').src=t.image;$('art').alt=t.alt;$('caption').textContent=key==='overview'?'現場物件基礎參考；不是此節點專屬示意。':t.caption;$('lesson').href=t.link;
const f={lot:[68,63,28,16],carrier:[34,19,33,65],equipment:[1,19,33,65]}[key];$('focus').hidden=!f;if(f){const a=$('focus');a.style.left=f[0]+'%';a.style.top=f[1]+'%';a.style.width=f[2]+'%';a.style.height=f[3]+'%';a.style.borderColor=t.color;}
const target=topics.find(x=>x.subject===id&&x.key!==current.key);$('switch').hidden=!target;if(target){$('switch').textContent='改以 '+({lot:'Lot',carrier:'FOUP',equipment:'EQP',flow:'Flow'})[target.key]+' 為主詞 →';$('switch').onclick=()=>navigate(target.key,'core');}
$('sources').innerHTML=n.labels.map(x=>`<strong>${esc(x)}</strong><br>`).join('')+n.refs.map(r=>`<p><a href="data-map.html?view=original#${r.source}">查看來源</a><br>${r.labels.map(esc).join('<br>')}</p>`).join('');
svg.querySelectorAll('[data-node]').forEach(g=>g.classList.toggle('selected',g.id===id));}
function scale(value){zoom=Math.max(.25,Math.min(2,value));svg.style.width=base[2]*zoom+'px';svg.style.height=base[3]*zoom+'px';$('scale').textContent=Math.round(zoom*100)+'%';}
function navigate(key,part){const p=new URLSearchParams({subject:key,part});location.hash=p.toString();}
async function render(){const token=++request,p=new URLSearchParams(location.hash.slice(1));current=topics.find(t=>t.key===p.get('subject'))||topics[0];branch=current.branches.find(v=>v.key===p.get('part'))||null;const v=branch||current.core;
$('title').textContent=current.title+(branch?' · '+branch.title:'');$('description').textContent=branch?.description||current.description;
$('topics').innerHTML=topics.map(t=>`<button data-topic="${t.key}" style="--color:${teaching[t.key].color}" aria-pressed="${t.key===current.key}">${({lot:"Lot",carrier:"FOUP",equipment:"EQP",flow:"Flow"})[t.key]}</button>`).join('');document.querySelectorAll('[data-topic]').forEach(b=>b.onclick=()=>navigate(b.dataset.topic,'core'));
$('branches').innerHTML=`<button data-part="core" aria-pressed="${!branch}">核心關係</button>`+current.branches.map(v=>`<button data-part="${v.key}" aria-pressed="${v===branch}">${v.title}</button>`).join('');document.querySelectorAll('[data-part]').forEach(b=>b.onclick=()=>navigate(current.key,b.dataset.part));
$('scope').textContent=`${v.nodes.length} 個節點 · ${v.edges.length} 條原始連線 · ${branch?'單一完整分支詳圖':'核心主題圖'}，另有 ${current.branches.length} 段詳圖可選`;
const url=`ER/SUBJECTS/${current.key}-${branch?.key||'core'}.svg`;const response=await fetch(url);if(!response.ok)throw Error('主題圖載入失敗');const text=await response.text();if(token!==request)return;
svg=document.importNode(new DOMParser().parseFromString(text,'image/svg+xml').documentElement,true);$('canvas').replaceChildren(svg);base=svg.getAttribute('viewBox').split(/\s+/).map(Number);scale(Math.max(innerWidth<950?.85:.75,Math.min(1,$('canvas').clientWidth/base[2])));$('canvas').scrollTo(0,0);$('download').href=url;
svg.querySelectorAll('[data-node]').forEach(g=>{g.addEventListener('click',()=>showNode(g.id));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();showNode(g.id)}})});showNode(current.subject);window.SUBJECT_ER={model,topics,current:current.key,branch:branch?.key||'core'};}
$('fit').onclick=()=>scale(Math.min($('canvas').clientWidth/base[2],$('canvas').clientHeight/base[3]));$('readable').onclick=()=>scale(1);$('plus').onclick=()=>scale(zoom*1.2);$('minus').onclick=()=>scale(zoom/1.2);
$('open-image').onclick=()=>{$('large-art').src=$('art').src;$('large-art').alt=$('art').alt;$('large-caption').textContent=$('caption').textContent;$('large-focus').style.cssText=$('focus').style.cssText;$('large-focus').hidden=$('focus').hidden;$('image-dialog').showModal()};
async function start(){const [m,data]=await Promise.all([fetch('ER/INTEGRATED/er-model-v2.json').then(r=>r.json()),fetch('ER/SUBJECTS/subjects.json').then(r=>r.json())]);const corrected=m.nodes.find(n=>n.id===m.mapping['2671:lot-eqp']);if(corrected){corrected.labels=corrected.labels.map(t=>t==='預到'?'帶到':t);}const contents=m.nodes.find(n=>n.id===m.mapping['2671:slot']);if(contents){contents.labels=contents.labels.map(t=>t==='在 Slot'?'內容物歷史':t);}model=m;topics=data.subjects;nodes=new Map(m.nodes.map(n=>[n.id,n]));edges=m.edges;window.addEventListener('hashchange',()=>render().catch(fail));await render();}function fail(e){$('title').textContent='載入失敗：'+e.message;console.error(e)}start().catch(fail);
