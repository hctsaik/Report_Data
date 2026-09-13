const $=id=>document.getElementById(id),esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const routes=[
{id:'lot-step',title:'這個 Lot 的 Step 歷史',refs:['2671:lot','2672:summary','2672:step'],meaning:'Lot Step 歷史以 Lot 為對象。原圖透過「站點 Summary／Lot_id」連接 LOT（Siview.Frlot）與 F12DM.DM_Lot_step_st；從 FOUP 查這段資料時，還要經裝載關係找到 Lot，不能省略 Lot。'},
{id:'load',title:'Lot 裝在哪個 FOUP？',refs:['2671:lot','2671:cast-link','2671:cast'],meaning:'LOT 是生產批次，FOUP 是實體載具；中間的「放在／FRCAST_LOT」保留裝載對應。兩個物件的身分不相同。'},
{id:'slot',title:'FOUP 在某個時間點放了哪些 Wafer？',refs:['2671:lot','2671:slot','2671:cast'],meaning:'Siview.fhwlths 記錄 FOUP 內容物（Wafer）的歷史：在什麼時間點，這個 FOUP 放了哪些 Wafer。每次 Split／Merge 進 FOUP 時更新。查詢時要對應時間，不能直接把歷史內容當成目前裝載狀態。'},
{id:'location',title:'FOUP 位於哪台設備？',refs:['2671:cast','2671:location','2671:eqp'],meaning:'「位於／CSFHDOPHS」連接載具與設備，是原圖提供的位置關係。這條線本身不證明晶圓正在加工，還須核對資料時間與執行紀錄。'},
{id:'predispatch',title:'派工系統預先把 Lot 派到哪台機台？',refs:['2671:lot','2671:cast-link','2671:cast','2671:predispatch','2671:eqp'],meaning:'預派以 Lot 為主要對象，派工系統預先安排目標機台；FOUP 是輔助關聯。左側保留原資料的裝載及設備路徑，右側虛線補充 Lot 的已確認業務關係；預派不表示已到站或已加工。'},
{id:'lot-pre',title:'Lot 在這個站點有哪些可用機台？',refs:['2671:lot','2671:lot-eqp','2671:eqp'],meaning:'「帶到／FRLOT_EQP」表示 Lot 在這個站點有可用機台。它描述站點可用機台的關係，不表示預計到達、已到達或已開始加工；派工系統對 Lot 的預派是另一條關係。'},
{id:'port',title:'Lot 與 Port 的交接關係',refs:['2671:lot','2671:port-link','2671:port','2671:has','2671:eqp'],meaning:'原圖保留「EI 在／FREQP_LOT」及設備擁有 Port 的關係。EI 沿用廠內文字；不自行展開縮寫，也不把 Siview.Port 等同未確認的 FRPORT。'},
{id:'flow',title:'Lot 如何接到 Flow？',refs:['2673:lot','2673:flow-link','2673:flow'],meaning:'同一個 FRLOT 匯集不同原圖的關係。這條支線經 Part／Mainpd_id 指向流程定義；Lot 當前進度仍是另一個問題。'},
{id:'lr',title:'Flow 與 LR 的關係',refs:['2673:flow','2673:lr-eqp-link','2673:lr-eqp'],meaning:'Flow 透過 LCRECIPE_ID 關係連到 LR／設備對應表。同表另一個出現位置也匯集在這個實體上，但兩種原始關係都保留。'},
{id:'pd',title:'PD 與設備配對',refs:['2677:pd','2677:pd-key','2677:pd-eqp','2677:eqp-id','2677:eqp'],meaning:'FRPD、SYSTEMKEY、FRPD_EQP 與 EQP_ID 分別保留。這個 SYSTEMKEY 屬於此路徑，不能與 Recipe 的 SYSTEMKEY 合併。'},
{id:'recipe',title:'ER 配置與機台',refs:['2677:recipe','2677:recipe-key','2677:recipe-eqp','2677:eqp-id','2677:eqp'],meaning:'FRMRCP 經 SYSTEMKEY 與 FRMRCP_EQP 接到設備；這是配置關係，不能當作某個 Lot 已使用某份 Physical Recipe 的證據。'},
{id:'chamber',title:'EQP 與 Chamber',refs:['2674:eqp','2674:chamber-link','2674:chamber','2674:detail-link','2674:chamber-detail'],meaning:'設備、Chamber 狀況及 Chamber 細部資料分開存在。原框內同列兩張表時，保留原框，不擅自補出兩表間的 Join。'},
{id:'hold',title:'Lot 的 Future Hold',refs:['2673:lot','2673:future-link','2673:future'],meaning:'Future Hold 是未來條件的管制安排，不表示此刻已經 Hold；不得與 Product Hold 或 Qtime 歷史合成同一個實體。'},
{id:'move',title:'Lot Move 與 WIP 的共同歷史',refs:['2672:lot','2672:move-link','2672:move','2675:move-link','2675:lot'],meaning:'兩圖的 Move 歷史表匯集到同一實體，兩側各保留自己的關係。FRLOT 與 KER_WIP_BT 都描述批次，但不是同一張表。重工過站計入 Move；Join 後重複列不算新事件。'},
{id:'transfer',title:'FOUP 的搬送歷史',refs:['2672:cast','2672:mcs-transfer','2672:mcs-history'],meaning:'Carrier_id／transfer_job_id 的搬送歷史以載具為對象。它與 Lot 過站不同，一次搬送不自動等於一次 Move。'},
{id:'qtime',title:'這個 Lot 的 Qtime 與站點歷史',refs:['2671:lot','2672:summary','2672:step','2672:qtime-link','2672:qtime'],meaning:'QTime 是同一 Lot 指定起訖事件之間的時間限制。原圖由 Lot 經站點 Summary／Lot_id、Step 歷史，再經 Lot_ID／Ope_no 接到 Qtime 歷史；判讀時要核對同一 Lot 的事件、時間與限值。'},
{id:'wip',title:'WIP 與固定時間快照',refs:['2675:lot','2675:wip-link','2675:wip-history'],meaning:'KER_WIP_Y_BTH 每天早上07:20保存機群狀況與KPI快照；固定時點的版本不是目前即時狀況。'},
{id:'oee',title:'機台與期間 OEE',refs:['2675:eqp','2675:eqp-oee-link','2675:eqp-oee'],meaning:'這裡保留機台與 OEE 歷史表的 EQP_ID 關係。UP 是加工狀態，AVL 是期間比率；不把 OEE、AVL、Eff 當同義字。'}
];
const questions=[
{id:'where',title:'預派到 ETCH-03，就代表已到了嗎？',routes:['load','predispatch','location','lot-pre'],text:'先看 Lot 被預派到哪台機台，再查載具實際位置；批次預派與載具位置是不同關係。',answer:'不能。預派是安排；位置需要另一條關係的資料與時間證據。也不能由位置直接推論正在加工。'},
{id:'ready',title:'現在能在這台設備加工嗎？',routes:['flow','lr','hold','chamber'],text:'從 Lot 的流程定義，走到配方配置，再查批次管制及指定加工資源。',answer:'只有設備對應不夠。還需當前站、Hold、設備／Chamber與MON等條件；Daily MON逾期卡EMS是已確認廠內規則，但七圖沒有完整放行schema。'},
{id:'recipe',title:'哪份 Recipe 才是這次實際使用的？',routes:['lr','pd','recipe'],text:'分別沿 LR、PD、ER 配置路徑閱讀。相同 SYSTEMKEY 字樣保留在各自路徑，不做全域合併。',answer:'配置不等於執行紀錄。真正的 Physical Recipe 仍須對到該次 Lot、設備、時間及版本，七圖尚未完整提供這段。'},
{id:'move',title:'搬一次 FOUP，是不是多一次 Move？',routes:['transfer','move'],text:'比較 Carrier／MCS 搬送路徑與 Lot Move 路徑，觀察兩者起點與中介鍵的差異。',answer:'不是。搬送對象是載具；Move是Lot過站事件，重工計入。示例一批過站後重工再過站，共2次Move，不能用搬送次數代替。'},
{id:'time',title:'現在 UP，報表能直接當現在嗎？',routes:['wip','oee'],text:'從 WIP 的固定時間快照，切到設備 OEE 期間資料；留意不同的表與關係。',answer:'不能。UP是加工狀態，AVL是一定期間的Availability比率。固定快照、事件與統計各有時間範圍；逐表延遲仍需資料契約。'}
];
let model,svg,allBox,view,activeRoute='load',nodes,edges,drag=null,moved=false,startNode=null;const pointers=new Map();let focusedSubject=null,walkFocused=false;
let pinch=null;let walkIds=[],walkEdges=[],walkIndex=0;

let displayMode='overview',activeEntity=null,framedIds=[];
const teaching=window.ER_TEACHING;
function teachingForNode(id){
 for(const [key,t] of Object.entries(window.ER_TOPIC_CONTENT.topics))if(t.refs.some(ref=>model.mapping[ref]===id))return key;
 for(const key of ['qtime','predispatch','wph','recipe','equipment','carrier','lot','flow'])if(teaching[key].refs.some(ref=>model.mapping[ref]===id))return key;
 const recipeRefs=['2677:recipe-key','2677:recipe-eqp','2673:lr-eqp-link','2673:lr-link','2677:er','2677:lr'];
 if(recipeRefs.some(ref=>model.mapping[ref]===id))return 'recipe';
 return 'source';
}
function showTeaching(key){
 const t=teaching[key]||teaching.source,hasImage=Boolean(t.image);
 $('selection-details').dataset.topic=key;
 document.querySelector('.teaching-figure').hidden=!hasImage;
 $('teaching-mobile').removeAttribute('srcset');$('teaching-image').removeAttribute('src');
 if(hasImage){$('teaching-mobile').srcset=t.mobile||t.image;$('teaching-image').src=t.image;}
 $('teaching-image').alt=t.alt||'';$('teaching-caption').textContent=t.caption||'';
 $('teaching-link').hidden=!t.link;
 if(t.link)$('teaching-link').href=t.link;else $('teaching-link').removeAttribute('href');
 $('teaching-link').textContent=key==='wph'?'機群 WPH 定義（本頁）':key==='predispatch'?'Lot 預派說明（本頁）':'閱讀完整教學 →';
 $('topic-detail').innerHTML=t.details||'';window.ER_LOT_WAFER.mount();window.ER_MCS.mount();
 if(key!=='overview')$('selection-details').open=true;
 const focus=hasImage?{equipment:[1,19,33,65]}[key]:null;
 $('teaching-focus').hidden=!focus;
 if(focus){const f=$('teaching-focus');f.style.left=focus[0]+'%';f.style.top=focus[1]+'%';f.style.width=focus[2]+'%';f.style.height=focus[3]+'%';f.style.borderColor=t.color;}
 $('teaching-current').textContent=hasImage?(t.title||'現場物件總覽'):'';
 $('teaching-current').hidden=!hasImage;$('teaching-current').style.borderColor=t.color||'#52728e';
}
function nodeContext(id){
 const n=nodes.get(id),connected=edges.filter(e=>e.a===id||e.b===id).map(e=>nodes.get(e.a===id?e.b:e.a));
 return '<section class="node-context"><h3>這個節點在圖中的角色</h3><p>'+esc(n.labels.join(' / '))+'</p>'+
 (connected.length?'<p>直接相連：</p><ul>'+connected.map(v=>'<li>'+esc(v.labels.join(' / '))+'</li>').join('')+'</ul>':'')+
 '<p>沿上方關聯圖閱讀兩端對象；同名鍵必須留在這條關係的上下文中，不自行推定唯一性或一對多。</p></section>';
}
function clearFrames(){framedIds=[];activeEntity=null;svg?.querySelector('#entity-frames')?.remove();$('entity-targets').replaceChildren();document.querySelectorAll('[data-entity]').forEach(b=>b.setAttribute('aria-pressed','false'));}
function drawFrames(){svg.querySelector('#entity-frames')?.remove();if(!framedIds.length)return;const ns='http://www.w3.org/2000/svg',g=document.createElementNS(ns,'g');g.id='entity-frames';g.style.pointerEvents='none';const scale=Math.min($('canvas').clientWidth/view[2],$('canvas').clientHeight/view[3]);const pad=7/scale;for(const id of framedIds){const b=box(id),r=document.createElementNS(ns,'rect');for(const [k,v] of Object.entries({x:b.x-pad,y:b.y-pad,width:b.w+2*pad,height:b.h+2*pad,rx:4/scale,fill:'none',stroke:teaching[activeEntity].color,'stroke-width':3/scale}))r.setAttribute(k,v);g.append(r);}svg.append(g);}
function frameEntity(key){overview();const t=teaching[key];activeEntity=key;displayMode='entity';framedIds=[...new Set(t.refs.map(r=>model.mapping[r]).filter(Boolean))];drawFrames();showTeaching(key);inspect(framedIds,t.title,t.meaning);window.ER_FOCUS.show(model.mapping[key==='recipe'?'2677:recipe':t.refs[0]]);$('entity-targets').innerHTML='<h3>框選位置 · 點一下放大</h3>'+framedIds.map((id,i)=>`<button data-target="${id}">${i+1}. ${nodes.get(id).labels.map(esc).join(' / ')} ↗</button>`).join('');document.querySelectorAll('[data-target]').forEach(b=>b.onclick=()=>{selectNode(b.dataset.target);fitIds([b.dataset.target],true);$('status').textContent='已放大框選物件。按「全圖總覽」回到完整 ER。'});document.querySelector(`[data-entity="${key}"]`).setAttribute('aria-pressed','true');focusSubject(window.ER_FOCUS.getState().root);$('status').textContent=`已框選 ${framedIds.length} 個 ${t.title.split('：')[0]} 資料位置；全部 ${model.nodes.length} 個節點與 ${model.edges.length} 條連線仍保留。`;}
document.querySelectorAll('[data-entity]').forEach(b=>b.onclick=()=>{if(model)frameEntity(b.dataset.entity)});
$('clear-entity').onclick=()=>{if(svg)overview()};
$('open-teaching').onclick=()=>{$('teaching-large').src=$('teaching-image').currentSrc||$('teaching-image').src;$('teaching-large').alt=$('teaching-image').alt;$('teaching-large-caption').textContent=$('teaching-caption').textContent;$('teaching-large-focus').style.cssText=$('teaching-focus').style.cssText;$('teaching-large-focus').hidden=$('teaching-focus').hidden;$('teaching-dialog').showModal()};

const mode=new URLSearchParams(location.search).get('view')==='questions';
$('question-panel').hidden=!mode;$(mode?'question-mode':'original-mode').setAttribute('aria-current','page');
function setView(v){view=v;svg.setAttribute('viewBox',v.join(' '));$('zoom-label').textContent=Math.round($('canvas').clientWidth/v[2]*100)+'%';if(svg)drawFrames();}
function zoom(f,cx=.5,cy=.5){const w=view[2]*f,h=view[3]*f;if(w<140||w>allBox[2]*2)return;setView([view[0]+(view[2]-w)*cx,view[1]+(view[3]-h)*cy,w,h]);}
function box(id){const g=svg.getElementById(id),b=g.getBBox(),m=svg.getCTM().inverse().multiply(g.getCTM());const p=new DOMPoint(b.x,b.y).matrixTransform(m),q=new DOMPoint(b.x+b.width,b.y+b.height).matrixTransform(m);return {x:p.x,y:p.y,w:q.x-p.x,h:q.y-p.y};}
function fitIds(ids,allowTiny=false){const bs=ids.map(box),x=Math.min(...bs.map(b=>b.x)),y=Math.min(...bs.map(b=>b.y)),r=Math.max(...bs.map(b=>b.x+b.w)),bt=Math.max(...bs.map(b=>b.y+b.h));const cw=$('canvas').clientWidth,ch=$('canvas').clientHeight;let w=Math.max(r-x+80,cw/1.2),h=Math.max(bt-y+80,ch/1.2);if(w/h<cw/ch)w=h*cw/ch;else h=w*ch/cw;if(!allowTiny&&cw/w<.8){focusStep(Math.min(1,walkIds.length-1));return false;}setView([x+(r-x-w)/2,y+(bt-y-h)/2,w,h]);return true;}
// Keep the complete SVG, but move its viewport to the current subject.
function focusSubject(id){
 focusedSubject=id;fitIds([id],true);
 $('focus-current').disabled=false;
 $('map-subject').textContent='目前主詞：'+nodes.get(id).labels.join(' / ');
}
function syncWalkSubject(id){
 const key=teachingForNode(id),t=teaching[key];showTeaching(key);
 inspect(walkIds,t.title||nodes.get(id).labels[0],t.meaning||nodes.get(id).labels.join(' / '));
 window.ER_FOCUS.show(id);focusedSubject=id;activeEntity=key;framedIds=[id];drawFrames();
 $('map-subject').textContent='目前主詞：'+nodes.get(id).labels.join(' / ');
 $('focus-current').disabled=false;
 if(key==='source')$('topic-detail').innerHTML=nodeContext(id);
}
function focusStep(i){if(!walkIds.length)return;walkIndex=Math.max(0,Math.min(walkIds.length-1,i));const id=walkIds[walkIndex],b=box(id),cw=$('canvas').clientWidth,ch=$('canvas').clientHeight;walkFocused=true;syncWalkSubject(id);const scale=.9,w=cw/scale,h=ch/scale;setView([b.x+b.w/2-w/2,b.y+b.h/2-h/2,w,h]);$('step-label').textContent=`${walkIndex+1} / ${walkIds.length} · ${nodes.get(id).labels[0]}`;$('status').textContent='沿線閱讀：'+nodes.get(id).labels.join(' / ')+'。保留90%可讀尺寸；超出畫面的相鄰節點可用上一點／下一點定位。';document.querySelectorAll('[data-inspect]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.inspect===id));}
function setupWalk(ids,es){walkFocused=false;walkEdges=es;const adjacent=(a,b)=>edges.some(e=>es.includes(e.id)&&((e.a===a&&e.b===b)||(e.a===b&&e.b===a)));if(ids.every((id,i)=>i===0||adjacent(ids[i-1],id)))walkIds=ids;else{walkIds=[];const visited=new Set();function visit(id){visited.add(id);walkIds.push(id);for(const next of ids){if(!visited.has(next)&&adjacent(id,next)){visit(next);walkIds.push(id)}}}visit(ids[0]);}walkIndex=0;$('step-label').textContent=`${ids.length} 個節點 · 可沿線逐點讀`;}

function mark(ids,edgeIds){svg.querySelectorAll('[data-node]').forEach(g=>g.style.opacity=ids.includes(g.id)?'1':'.14');svg.querySelectorAll('[data-edge]').forEach(g=>{const on=edgeIds.includes(g.id);g.style.opacity=on?'1':'.08';g.querySelectorAll('path').forEach(p=>{p.style.stroke=on?'#244c6b':'#7c8c9c';p.style.strokeWidth=on?'3':'1.7'})});}
function inspect(ids,title,meaning){$('selection-title').textContent=title;$('meaning').textContent=meaning;const actual=edges.filter(e=>ids.includes(e.a)&&ids.includes(e.b));$('path-list').innerHTML=actual.map(e=>`<div class="edge-pair"><button data-inspect="${e.a}">${nodes.get(e.a).labels.map(esc).join('<br>')}</button><span>— 原圖連線 —</span><button data-inspect="${e.b}">${nodes.get(e.b).labels.map(esc).join('<br>')}</button></div>`).join('');$('sources').innerHTML=ids.map(id=>{const n=nodes.get(id);return `<article><strong>${n.labels.map(esc).join(' / ')}</strong>${n.schema_missing?'<p>原圖未列 schema；保留此來源的獨立節點。</p>':''}${n.refs.map(r=>`<p><a href="data-map.html?view=original#${r.source}">來源 ${r.source}</a> · ${esc(r.node)}<br>${r.labels.map(esc).join('<br>')}</p>`).join('')}</article>`}).join('')+(model.sourceNotes||[]).filter(note=>ids.some(id=>nodes.get(id).refs.some(r=>r.source===note.source))).map(note=>`<p>${esc(note.text)}</p>`).join('');document.querySelectorAll('[data-inspect]').forEach(b=>b.onclick=()=>{const i=walkIds.indexOf(b.dataset.inspect);i>=0?focusStep(i):selectNode(b.dataset.inspect)});}

function route(id){clearFrames();displayMode='route';document.querySelector('.walk-tools').hidden=false;showTeaching(window.ER_TOPIC_CONTENT.routeKeys[id]||'source');const r=routes.find(r=>r.id===id)||routes[0];activeRoute=r.id;const ids=r.refs.map(ref=>model.mapping[ref]);const edgeIds=[];for(let i=1;i<ids.length;i++){const e=edges.find(e=>(e.a===ids[i-1]&&e.b===ids[i])||(e.b===ids[i-1]&&e.a===ids[i]));if(!e)throw Error('路徑缺少原始連線 '+r.id);edgeIds.push(e.id)}mark(ids,edgeIds);setupWalk(ids,edgeIds);inspect(ids,r.title,r.id==='pd'?teaching.pd.meaning:r.id==='load'?teaching.load.meaning:r.id==='transfer'?teaching.mcs.meaning:r.id==='port'?teaching.port.meaning:r.id==='move'?teaching.move.meaning:r.meaning);window.ER_FOCUS.show(r.id==='hold'?model.mapping['2673:future']:r.id==='qtime'?model.mapping['2672:qtime']:r.id==='predispatch'?model.mapping['2671:predispatch']:ids[0]);$('status').textContent=r.title+' · '+ids.length+' 個節點／'+edgeIds.length+' 條原始關係';focusSubject(window.ER_FOCUS.getState().root);document.querySelectorAll('[data-route]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.route===r.id));}
function selectNode(id){
 clearFrames();displayMode='node';document.querySelector('.walk-tools').hidden=false;
 const key=teachingForNode(id),t=teaching[key],n=nodes.get(id);showTeaching(key);
 let es=edges.filter(e=>e.a===id||e.b===id);
 if(n.kind==='rect'){const rel=es.find(e=>nodes.get(e.a===id?e.b:e.a).kind==='diamond')||es[0];if(rel){const other=rel.a===id?rel.b:rel.a;es=edges.filter(e=>e.a===other||e.b===other);}}
 const ids=[...new Set([id,...es.flatMap(e=>[e.a,e.b])])];mark(ids,es.map(e=>e.id));setupWalk(ids,es.map(e=>e.id));
 const meaning=t.meaning||(n.kind==='circle'?'這是「'+n.labels.join('／')+'」的概念／屬性註記，須配合相連資料對象閱讀；原圖未將它定義為獨立資料表。':'這個節點以「'+n.labels.join('／')+'」標示來源中的對象或關係。下面列出它實際相連的節點；具體欄位語意仍須核對來源定義。');
 inspect(ids,['wph','bmir','portmode','lotstatus','wip'].includes(key)?t.title:key==='lotstep'?'Lot Step 歷史':key==='contents'?'FOUP 內容物（Wafer）歷史':n.labels[0],meaning);
 // Source-grounded details supplement the lesson; do not borrow another topic's image.
 if(key==='source')$('topic-detail').innerHTML=nodeContext(id);
 $('status').textContent='已定位：'+n.labels.join(' / ');window.ER_FOCUS.show(id);
 focusSubject(id);svg.querySelectorAll('[data-node],[data-edge]').forEach(g=>g.style.opacity='1');
 activeEntity=key;framedIds=[id];drawFrames();
 // A touch-generated click follows pointerup. Keep the page stationary until
 // that gesture finishes, so it cannot accidentally hit a toolbar button.
 if(!pointers.size&&!$('focus-dialog').open&&!$('inspector-dialog').open)$('map-subject').scrollIntoView({block:'start',behavior:'instant'});
}
function overview(){focusedSubject=null;$('focus-current').disabled=true;$('map-subject').textContent='Table 總表 · 選擇主詞後自動放大';window.ER_FOCUS.clear();clearFrames();displayMode='overview';document.querySelector('.walk-tools').hidden=true;walkIds=[];document.querySelectorAll('[data-route]').forEach(b=>b.setAttribute('aria-pressed','false'));inspect([],'完整 ER × 主詞關聯','選擇上方主詞或直接點 ER 節點，下方會重新展開來源中的相關實體與關係。現場插圖保留為補充參考。');showTeaching('overview');setView(allBox.slice());svg.querySelectorAll('[data-node],[data-edge]').forEach(g=>g.style.opacity='1');svg.querySelectorAll('[data-edge] path').forEach(p=>{p.style.stroke='#7c8c9c';p.style.strokeWidth='1.7'});$('status').textContent='全圖：121 個節點、128 條關係都在圖上。請搜尋或選一段關係放大閱讀。';}
function question(id){const q=questions.find(q=>q.id===id)||questions[0];$('question-copy').innerHTML=`<strong>${q.title}</strong><p>${q.text}</p><div class="choices">${q.routes.map(id=>`<button data-route="${id}">${routes.find(r=>r.id===id).title}</button>`).join('')}</div><p class="answer">${q.answer}</p>`;bindRoutes();document.querySelectorAll('[data-question]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.question===q.id));route(q.routes[0]);}
function bindRoutes(){document.querySelectorAll('[data-route]').forEach(b=>b.onclick=()=>route(b.dataset.route));}
async function start(){const [m,text]=await Promise.all([fetch('ER/INTEGRATED/er-model-v2.json').then(r=>r.json()),fetch('ER/INTEGRATED/fab-er-v2.svg').then(r=>r.text())]);const available=m.nodes.find(n=>n.id===m.mapping['2671:lot-eqp']);
if(available){available.labels=available.labels.map(t=>t==='預到'?'帶到':t);available.refs=available.refs.map(r=>({...r,labels:r.labels.map(t=>t==='預到'?'帶到':t)}));}
const contents=m.nodes.find(n=>n.id===m.mapping['2671:slot']);if(contents){contents.labels=contents.labels.map(t=>t==='在 Slot'?'內容物歷史':t);contents.refs=contents.refs.map(r=>({...r,labels:r.labels.map(t=>t==='在 Slot'?'內容物歷史':t)}));}for(const ref of ['2673:pd','2677:pd']){const n=m.nodes.find(n=>n.id===m.mapping[ref]);if(n)n.labels=n.labels[0]==='FRPD'?['PD（Process Definition）',...n.labels]:['PD（Process Definition）',...n.labels.slice(1)];}const dailySnapshot=m.nodes.find(n=>n.id===m.mapping['2675:wip-history']);if(dailySnapshot){dailySnapshot.labels=dailySnapshot.labels.map(t=>t.includes('星期一')?'每天07:20機群與KPI快照':t);dailySnapshot.refs=dailySnapshot.refs.map(r=>({...r,labels:r.labels.map(t=>t.includes('星期一')?'每天07:20機群與KPI快照':t)}));}model=m;window.ER_FOCUS.init(m,{selectNode});nodes=new Map(m.nodes.map(n=>[n.id,n]));edges=m.edges;const parsed=new DOMParser().parseFromString(text,'image/svg+xml');svg=document.importNode(parsed.documentElement,true);const historyGlyph=svg.getElementById(m.mapping['2671:slot']);if(historyGlyph){historyGlyph.querySelectorAll('text').forEach(t=>{if(t.textContent==='在 Slot')t.textContent='內容物歷史';});historyGlyph.setAttribute('aria-label','FOUP內容物歷史：各時間點的Wafer，Split／Merge進FOUP時更新');}const availableGlyph=svg.getElementById(m.mapping['2671:lot-eqp']);if(availableGlyph){availableGlyph.querySelectorAll('text').forEach(t=>{if(t.textContent==='預到')t.textContent='帶到';});availableGlyph.setAttribute('aria-label','帶到：Lot 在這個站點的可用機台');}
const dailyGlyph=svg.getElementById(m.mapping['2675:wip-history']);if(dailyGlyph){dailyGlyph.querySelectorAll('text').forEach(t=>{if(t.textContent.includes('星期一'))t.textContent='每天07:20機群與KPI快照';});dailyGlyph.setAttribute('aria-label','每天07:20機群與KPI快照 KER_WIP_Y_BTH');}$('canvas').replaceChildren(svg);svg.setAttribute('width','100%');svg.setAttribute('height','100%');allBox=svg.getAttribute('viewBox').split(/\s+/).map(Number);$('counts').textContent=`${m.nodes.length} 個可見節點 · ${m.edges.length} 條關係`;svg.querySelectorAll('[data-node]').forEach(g=>{g.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();selectNode(g.id)}})});$('routes').innerHTML=routes.map(r=>`<button data-route="${r.id}">${r.title}</button>`).join('');bindRoutes();$('questions').innerHTML=questions.map(q=>`<button data-question="${q.id}">${q.title}</button>`).join('');document.querySelectorAll('[data-question]').forEach(b=>b.onclick=()=>{history.replaceState(null,'','#'+b.dataset.question);question(b.dataset.question)});mode?question(location.hash.slice(1)):overview();if(new URLSearchParams(location.search).get('subject')==='wph')selectNode(model.mapping['2673:wph']);if(new URLSearchParams(location.search).get('subject')==='pd')selectNode(model.mapping['2673:pd']);if(new URLSearchParams(location.search).get('subject')==='future')selectNode(model.mapping['2673:future']);if(new URLSearchParams(location.search).get('subject')==='qtime')selectNode(model.mapping['2672:qtime']);if(new URLSearchParams(location.search).get('subject')==='lot-step')selectNode(model.mapping['2672:step']);if(new URLSearchParams(location.search).get('subject')==='predispatch')selectNode(model.mapping['2671:predispatch']);window.ER_ATLAS={teachingForNode,model,frameEntity,route,overview,selectNode,box,getView:()=>view.slice(),focusStep,getWalk:()=>walkIds.slice()};}
$('path-overview').onclick=()=>{fitIds(walkIds,true);$('status').textContent='本段全貌：用來辨識路徑結構；按沿線上一點／下一點回到可讀尺寸。'};$('step-prev').onclick=()=>focusStep(walkIndex-1);$('step-next').onclick=()=>focusStep(walkIndex+1);
$('overview').onclick=()=>{setView(allBox.slice());$('status').textContent='完整 ER 總覽；下方保留目前介紹。按「回目前主詞」恢復放大。'};$('focus-current').onclick=()=>{if(focusedSubject)focusSubject(focusedSubject)};$('core').onclick=()=>route('load');$('zoom-in').onclick=()=>zoom(.8);$('zoom-out').onclick=()=>zoom(1.25);
$('find').oninput=()=>{if(!model)return;const q=$('find').value.trim().toLowerCase();$('search-results').innerHTML=q?model.nodes.filter(n=>n.labels.some(s=>s.toLowerCase().includes(q))).slice(0,12).map(n=>`<button data-result="${n.id}">${n.labels.map(esc).join(' · ')}</button>`).join('')||'<p>沒有符合的節點</p>':'';document.querySelectorAll('[data-result]').forEach(b=>b.onclick=()=>{selectNode(b.dataset.result);$('search-results').innerHTML='';$('canvas').focus()})};
// Give tiny overview nodes a forgiving screen-space hit target.
function hitNode(e){const direct=e.target.closest('[data-node]');if(direct)return direct.id;
 let best=null,distance=11;
 svg.querySelectorAll('[data-node]').forEach(g=>{const b=g.getBoundingClientRect();const d=Math.hypot(Math.max(b.left-e.clientX,0,e.clientX-b.right),Math.max(b.top-e.clientY,0,e.clientY-b.bottom));if(d<distance){distance=d;best=g.id}});return best;
}
const canvas=$('canvas');canvas.addEventListener('wheel',e=>{if(!svg||!e.ctrlKey)return;e.preventDefault();const r=canvas.getBoundingClientRect();zoom(e.deltaY>0?1.1:1/1.1,(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height)},{passive:false});
canvas.addEventListener('pointerdown',e=>{if(!svg)return;e.preventDefault();moved=false;startNode=hitNode(e);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});canvas.setPointerCapture(e.pointerId);drag={x:e.clientX,y:e.clientY,v:view.slice()};if(pointers.size===2){const [a,b]=[...pointers.values()];pinch={distance:Math.hypot(a.x-b.x,a.y-b.y),v:view.slice()}}});
canvas.addEventListener('pointermove',e=>{if(!pointers.has(e.pointerId))return;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pointers.size===2&&pinch){const [a,b]=[...pointers.values()],f=pinch.distance/Math.hypot(a.x-b.x,a.y-b.y);setView([pinch.v[0]+pinch.v[2]*(1-f)/2,pinch.v[1]+pinch.v[3]*(1-f)/2,pinch.v[2]*f,pinch.v[3]*f]);moved=true}else if(drag){const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.hypot(dx,dy)>7)moved=true;if(!moved)return;setView([drag.v[0]-dx*drag.v[2]/canvas.clientWidth,drag.v[1]-dy*drag.v[3]/canvas.clientHeight,drag.v[2],drag.v[3]])}});
function end(e){if(e.type==='pointerup'&&!moved&&startNode)selectNode(startNode);pointers.delete(e.pointerId);pinch=null;drag=null;startNode=null;}canvas.addEventListener('pointerup',end);canvas.addEventListener('pointercancel',end);canvas.addEventListener('keydown',e=>{if(!svg)return;const k={ArrowLeft:[-.12,0],ArrowRight:[.12,0],ArrowUp:[0,-.12],ArrowDown:[0,.12]}[e.key];if(k){e.preventDefault();setView([view[0]+k[0]*view[2],view[1]+k[1]*view[3],view[2],view[3]])}});window.addEventListener('resize',()=>{if(svg){if(focusedSubject)focusSubject(focusedSubject);else setView(allBox.slice())}});let navigation;
function installNavigation(){
 const original={node:selectNode,route,entity:frameEntity,overview};
 navigation=window.createErNavigation({
  snapshot:()=>({view:view?.slice(),focusPage:window.ER_FOCUS.getState().page,walkIndex,walkFocused,scrollY:window.scrollY,detailsOpen:$('selection-details').open,dialogScroll:$('inspector-dialog').scrollTop}),
  restore:v=>{const fn=original[v.kind]||original.overview;fn(v.arg);if(v.walkFocused&&v.walkIndex!==undefined&&walkIds.length)focusStep(v.walkIndex);if(v.focusPage!==undefined)window.ER_FOCUS.setPage(v.focusPage);if(v.view)setView(v.view);if(v.detailsOpen!==undefined)$('selection-details').open=v.detailsOpen;requestAnimationFrame(()=>{window.scrollTo(0,v.scrollY||0);$('inspector-dialog').scrollTop=v.dialogScroll||0;});},
  home:()=>overview(),validNode:id=>nodes.has(id),validRoute:id=>routes.some(r=>r.id===id),validEntity:key=>['lot','carrier','equipment','flow','recipe'].includes(key)
 });
 selectNode=id=>navigation.perform('node',id,()=>original.node(id));
 route=id=>navigation.perform('route',id,()=>original.route(id));
 frameEntity=key=>navigation.perform('entity',key,()=>original.entity(key));
 overview=()=>navigation.perform('overview',undefined,()=>original.overview());
}
installNavigation();
start().then(()=>navigation.ready()).catch(e=>{$('loading')?$('loading').textContent='載入失敗：'+e.message:$('status').textContent='載入失敗：'+e.message;console.error(e)});
