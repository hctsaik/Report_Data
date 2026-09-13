'use strict';
const courseKey=document.body.dataset.course;
const course=COURSES[courseKey];
const $=s=>document.querySelector(s);
const engines=new Map();
let lessonIndex=0,activeScenario=SCENARIOS[courseKey][0].id;
const esc=value=>String(value??'—').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
$('#course-root').innerHTML=`<header class="topbar"><a class="brand" href="index.html"><b>M</b><span><small>MES LEARNING LAB</small>從現場認識資料</span></a><div class="course-tabs"><a href="index.html">01 基本物件</a><a href="operations.html" ${courseKey==='operations'?'aria-current="page"':''}>02 設備與現場</a><a href="flow.html" ${courseKey==='flow'?'aria-current="page"':''}>03 Flow 與 Lot</a></div><button class="button mobile-menu" id="menu-toggle" aria-expanded="false" aria-controls="sidebar">課程目錄</button></header><div class="shell"><aside id="sidebar"><p class="eyebrow">${course.label} · ${course.short}</p><h2 class="sidebar-title">${course.title}</h2><nav aria-label="本課章節">${course.lessons.map((l,i)=>`<a href="#${l.id}" data-lesson="${l.id}"><span>${String(i+1).padStart(2,'0')}</span><div>${l.nav}<small>${l.sub}</small></div></a>`).join('')}</nav><div class="aside-foot"><p>先讀概念，再操作情境。<br>每個練習都可重設與比較。</p><a href="index.html">第一部分 · 基本物件</a><br><a href="operations.html">第二部分 · 設備現場</a><br><a href="flow.html">第三部分 · Flow 深入</a></div></aside><main id="content" tabindex="-1"><div class="crumb">MES 入門教學 ／ ${course.label}</div><div class="page-meta"><span class="pill">${course.short}</span><span id="progress"></span></div><div id="lesson-container"></div><div class="footer-nav"><button class="button" id="previous">← 上一段</button><span id="footer-progress"></span><button class="button primary" id="next">下一段 →</button></div><p class="page-foot"><a href="${course.next}">${course.nextText} →</a></p>${sources}</main></div><dialog id="image-dialog" aria-label="完整教學圖"><div class="dialog-bar"><span>完整教學圖</span><button class="button" id="zoom-toggle">原始尺寸</button><button class="button" id="close-dialog">關閉 ×</button></div><div class="zoom-view"><img id="zoom-image" alt="放大的教學示意圖"></div></dialog>`;
function closeMenu(){$('#sidebar').classList.remove('open');$('#menu-toggle').setAttribute('aria-expanded','false');}
$('#menu-toggle').addEventListener('click',()=>{const open=$('#sidebar').classList.toggle('open');$('#menu-toggle').setAttribute('aria-expanded',String(open));});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu();});
function showLesson(focus=false){
 let [id,query]=location.hash.slice(1).split('?');
 const params=new URLSearchParams(query||'');
 // Keep all previously delivered scenario links usable after the complete rewrite.
 if(SCENARIOS[courseKey].some(s=>s.id===id)&&!course.lessons.some(l=>l.id===id)){activeScenario=id;id='lab';}
 if(params.get('case')&&SCENARIOS[courseKey].some(s=>s.id===params.get('case')))activeScenario=params.get('case');
 lessonIndex=Math.max(0,course.lessons.findIndex(l=>l.id===id));const lesson=course.lessons[lessonIndex];
 $('#lesson-container').innerHTML=`<article class="lesson" id="${lesson.id}"><h1>${lesson.title}</h1><p class="lead">${lesson.lead}</p><div class="lesson-body">${lesson.body()}</div></article>`;
 document.title=`${lesson.nav}｜${course.label} MES 教學`;
 $('[id=progress]').textContent=`${String(lessonIndex+1).padStart(2,'0')} / ${course.lessons.length}`;
 $('#footer-progress').textContent=`${lessonIndex+1} / ${course.lessons.length} · ${lesson.nav}`;
 document.querySelectorAll('[data-lesson]').forEach(a=>{if(a.dataset.lesson===lesson.id)a.setAttribute('aria-current','step');else a.removeAttribute('aria-current');});
 $('#previous').disabled=lessonIndex===0;
 $('#next').textContent=lessonIndex===course.lessons.length-1?'回到本課開頭 ↺':'下一段 →';
 closeMenu();
 if(lesson.id==='lab')renderLab();
 document.querySelectorAll('.open-art').forEach(button=>button.addEventListener('click',()=>{const src=button.querySelector('img').currentSrc||button.dataset.src;$('#zoom-image').src=src;$('#zoom-image').alt=button.querySelector('img').alt;$('.zoom-view').classList.remove('native');$('#zoom-toggle').textContent='原始尺寸';$('#image-dialog').showModal();}));
 if(focus){$('#content').focus({preventScroll:true});window.scrollTo({top:0,behavior:'instant'});}
}
$('#previous').addEventListener('click',()=>{if(lessonIndex>0)location.hash=course.lessons[lessonIndex-1].id;});
$('#next').addEventListener('click',()=>{location.hash=course.lessons[(lessonIndex+1)%course.lessons.length].id;});
window.addEventListener('hashchange',()=>showLesson(true));
$('#close-dialog').addEventListener('click',()=>$('#image-dialog').close());
$('#zoom-toggle').addEventListener('click',()=>{const on=$('.zoom-view').classList.toggle('native');$('#zoom-toggle').textContent=on?'符合視窗':'原始尺寸';});
function getEngine(){if(!engines.has(activeScenario))engines.set(activeScenario,new ScenarioEngine(SCENARIOS[courseKey].find(s=>s.id===activeScenario)));return engines.get(activeScenario);}
function renderLab(){
 const e=getEngine(),s=e.state,n=e.node;
 const nav=SCENARIOS[courseKey].map(c=>`<button type="button" data-scenario="${c.id}" aria-pressed="${c.id===activeScenario}">${c.title}<small>${c.sub}</small></button>`).join('');
 $('#scenario-lab').innerHTML=`<div class="lab-head"><p class="subtle">${SCENARIOS[courseKey].length} 個獨立情境 · 點選情境切換，保留各自進度</p><button class="button" id="reset-scenario">重設此情境 ↺</button></div><div class="lab-grid"><div class="scenario-nav" role="group" aria-label="選擇情境">${nav}</div><section class="sim" aria-label="情境操作"><div class="article"><p class="eyebrow">${course.label} · 情境練習</p><h2 class="sim-title">${e.scenario.title}</h2><p class="scenario-context">${e.scenario.context}</p><h3 id="scenario-prompt" tabindex="-1">${n.prompt}</h3><div id="sim-state">${stateView(s)}</div><div class="actions" aria-label="可執行動作">${n.actions.map((a,i)=>`<button type="button" data-action="${i}">${a.label}</button>`).join('')}</div><div class="feedback ${e.kind}" role="status" aria-live="polite" aria-atomic="true" id="scenario-feedback">${esc(e.feedback)}</div>${n.lesson?`<div class="takeaway"><span>${n.lesson}</span></div>`:''}${!n.actions.length?'<p class="end-note">✓ 本條路徑已走完。可以重設比較其他選擇，或切換情境。</p>':''}<details open><summary>事件紀錄（${e.events.length}）</summary><ol class="event-log">${e.events.map(event=>`<li><strong>${{start:'起點',accept:'事件',reject:'拒絕'}[event.kind]}</strong> · ${esc(event.text)}</li>`).join('')}</ol></details></div></section></div>`;
 $('#reset-scenario').addEventListener('click',()=>{getEngine().reset();renderLab();$('#scenario-prompt').focus({preventScroll:true});});
 document.querySelectorAll('[data-scenario]').forEach(b=>b.addEventListener('click',()=>{activeScenario=b.dataset.scenario;history.replaceState(null,'',`#lab?case=${activeScenario}`);renderLab();$('#scenario-prompt').focus({preventScroll:true});if(innerWidth<1150)$('#scenario-prompt').scrollIntoView({block:'start',behavior:'smooth'});}));
 document.querySelectorAll('[data-action]').forEach(b=>b.addEventListener('click',()=>{getEngine().act(Number(b.dataset.action));const y=window.scrollY;renderLab();$('#scenario-feedback').setAttribute('tabindex','-1');$('#scenario-feedback').focus({preventScroll:true});window.scrollTo({top:y,behavior:'instant'});}));
}
function stateView(s){
 let rows=[['Lot',esc(s.lot)],['Flow 版本',esc(s.flow)],['目前作業位置',esc(s.current)],['執行狀態',esc(s.status)],['載具位置',esc(s.location)],['Hold 原因',s.hold.length?s.hold.map(esc).join('／'):'無']];
 if(courseKey==='operations')rows.push(['配方',esc(s.recipe)]);
 if(s.count)rows.push(['本次已完成',esc(s.count)]);
 if(s.qtime!==undefined)rows.push(['S20完成→S30開始',`${s.qtime} 分鐘／上限30分鐘（教學設定）`]);
 if(s.visits)rows.push(['已保存的 visit',esc(s.visits)]);
 if(s.otherLot)rows.push(['另一批的獨立狀態',esc(s.otherLot)]);
 if(s.migration)rows.push(['版本遷移紀錄',esc(s.migration)]);
 if(s.genealogy)rows.push(['批次譜系',esc(s.genealogy)]);
 if(s.scan)rows.push(['本次讀值（不覆寫預期）',s.scan.map(esc).join(' ／ ')]);
 if(s.missing)rows.push(['缺少資料',esc(s.missing)]);
 if(courseKey==='flow'&&!s.lots){const index=STEPS.findIndex(x=>x.id===s.current);let next=s.current==='R10'?'S50 複測':s.current==='S45'?'S50 量測':index>=0&&index<5?`${STEPS[index+1].id} ${STEPS[index+1].name}`:s.current==='S60'?'全部驗證完成後結案':'—';if(s.flow.endsWith('v2')&&s.current==='S40')next='S45 新增檢查';rows.push(['完成本次作業後的正常去向',s.hold.length?'Hold 待處置；尚不允許推進':next]);}
 let result=record(rows);
 if(courseKey==='operations'){
  result+=`<div class="state-visual"><div><span class="process-banner">${activeScenario==='reconcile'?'F012 · 預期槽位':'F012 · 槽位快照'}</span><div class="wafer-stack">${Object.entries(s.slots).map(([slot,id])=>`<div><span class="wafer">${esc(id||'空')}</span><small>Slot ${esc(slot)}</small></div>`).join('')}</div></div><div><span class="process-banner">CH-A</span><div class="wafer-stack">${s.chamber?`<span class="wafer active">${esc(s.chamber)}</span>`:'<span>空 · 無晶圓</span>'}</div><small>此圖只顯示本例追蹤的3個槽位</small></div></div>`;
 }else if(s.lots){
  result+=`<div class="two" style="margin-top:20px">${s.lots.map(l=>`<div class="branch-node"><h3>${esc(l.id)}</h3><p>F-DEMO v1 · ${esc(l.current)} · Queued</p><div class="wafer-stack">${l.wafers.map(w=>`<span class="wafer">${esc(w)}</span>`).join('')}</div></div>`).join('')}</div><p class="subtle">兩個活躍子批合計3片；父批保留譜系，不重複計數。</p>`;
 }else{
  const routeOpen=document.querySelector('.route-details')?.open??(innerWidth>560);
  result+=`<details class="route-details" ${routeOpen?'open':''}><summary>完整 Flow · 查看階段與位置</summary>${flowMap(s.current,s.done,'',s.lot,s.flow)}</details>`;
  if(s.current==='R10')result+=`<div class="branch-node review"><h3>● L023 在重工支線 R10 · CLEAN</h3><p>核准返回點：S50。主線的 S10 完成紀錄維持不變。</p></div>`;
  if(s.current==='S45')result+=`<div class="branch-node"><h3>v2 新增 S45 · 檢查</h3><p>目前位置已在上方 Stage C 中顯示：S40 → <strong>S45</strong> → S50。原 v1 的歷程仍保留。</p></div>`;
  if(s.current==='結束')result+='<p class="completion">✓ Stage A、B、C 都完成；L023 Finished。</p>';
 }
 return labScene(s,courseKey,activeScenario,getEngine().node.lesson||getEngine().node.prompt)+`<details class="lab-details"><summary>查看完整欄位與原始位置紀錄</summary>${result}</details>`;
}
showLesson();
