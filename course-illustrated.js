'use strict';
// Exact record logic remains in scenarios.js; the introductory illustration is a declared example.
const ILLUSTRATED = {
 port:{v:2,title:'同樣三片，為什麼不能放行？',captions:['先確認 F012 已到 ETCH03 的 LP1；到站只回答「盒子在哪裡」。','放大同一個 Slot 07，再看本次取得的晶圓身分。','W07 是批次預期，W99 是讀值；數量相同也不能消除身分差異。'],take:'片數相同，身分仍要逐槽核對。'},
 recipe:{v:1,title:'配方名稱相同，就能開工嗎？',captions:['L023 的工作要求是 S40、ETCH-DEMO v2，先從批次需求出發。','機台上的同名 v1 不符合這次要求；不能只比名稱。','找到 v2 才得到候選，仍須核對產品、站點與設備／腔體資格。'],take:'名稱相同，不代表版本與資格相同。'},
 chamber:{v:1,title:'晶圓怎麼從 FOUP 進入腔體？',captions:['在取片前，W06 放在 F012 的水平槽位中。','搬送臂取出同一片 W06；這是下一個時點，不是複製一片。','W06 進入 CH-A 後才開始本次加工；它的結果不能代表另外兩片。'],take:'一片加工完成，不等於整批完成。',crop:[[0,112,545,852],[554,112,1064,852],[1066,112,1536,852]]},
 state:{v:2,title:'設備 Ready，這批仍可能不能做',captions:['Ready 描述 ETCH03 的可用狀態。','Lot L023 另有 Q01、E02 兩項有效限制。','解除 Q01 只移除一個原因；E02 未解除，MES 開工請求仍不通過。'],take:'設備可用，不代表這批可以開工。'},
 handoff:{v:1,title:'三片回來了，資料也都到了嗎？',captions:['機台 Done 與三片返回，是現場完成的證據。','結果接收端仍缺 W08，必須保留「待收」，不能替它補 Pass。','Current 暫留 S40；資料補齊並完成 MES 交易，才移到 S50。'],take:'機台完成、資料齊全、過站成功是三件事。'},
 'operations-lab':{v:1,title:'跟著 F012，走一次現場搬送',captions:['從 Stocker 的暫存位置找到 F012。','下一個時點，OHT 搬送同一載具；Lot 與成員沒有因此改變。','停到設備 LP1 後，再核對身分與開工條件。'],take:'搬的是載具，追蹤的是批次與晶圓。'},
 stage:{v:2,title:'先看一段工作，再看每一站',captions:['準備：清洗表面，再形成薄膜；兩個 Step 合成一段目的。','圖形：微影建立圖形，再經蝕刻轉移；這段完成不等於整條路完成。','確認：在 S50 等待量測，最後以 S60 結案。結案是管理動作。'],take:'Step 是一站，Stage 是一段，Flow 是整條路徑。',crop:[[0,112,520,880],[524,112,1024,880],[1025,112,1536,880]]},
 step:{v:1,title:'同樣清洗，為什麼要記兩次？',captions:['CLEAN 是可重用的作業種類，圖中以清洗設備說明其工作。','較早的 S10 已完成；這份 Pass 屬於 S10 的那一次執行。','後來到 R10，仍要建立本次清洗結果；兩處名稱相同，不等於做過同一次工作。'],take:'作業可以重用，完成證據不能借用。',crop:[[8,116,677,853],[773,120,1532,467],[773,488,1532,853]]},
 'lot-flow':{v:3,title:'一份路線，兩批不同的旅程',captions:['F-DEMO v1 是共同的核准流程定義，規定站點與順序。','L023 的旅程指向 S40，成員 W06／W07／W08 放在 F012。','L024 另在 S10，成員 W21／W22 放在 F020；一批前進不會推動另一批。'],take:'共用流程定義，各批保有自己的進度。',crop:[[5,101,1530,421],[0,432,762,848],[766,432,1536,848]]},
 execution:{v:2,title:'加工完成，還要完成一次交接',captions:['在 S40 等待時，批次已到設備，但尚未加工。','開工後改變 RunState，Current 仍在 S40。','加工完成後收集本次結果，位置尚未推進。','MES 完成交易成功，才把 Current 推到 S50 等待。'],take:'加工改狀態，完成交易才推進位置。',crop:[[0,115,390,887],[390,115,772,887],[773,115,1156,887],[1157,115,1536,887]]},
 branching:{v:2,title:'先確認量測有效，再選下一步',captions:['量測要對到正確晶圓與特徵；圖中局部用來指出觀察的位置。','以線寬 98–102 nm 作假設範例：100 在內，105 超過；沒有值就不能判定。','有效合格才走 S60；不合格先 Hold，缺值先補查，不把未知當 Pass。'],take:'先看證據有效，再判斷下一步。',crop:[[0,108,486,827],[487,108,1049,827],[1050,108,1536,827]]},
 rework:{v:2,title:'重工回到原站，紀錄不倒帶',captions:['S50 第一次失敗，先保留 W08 的原始結果。','核准 RW-001 才進 R10 清洗；本例限制最多一次。','回到 S50 建立 Visit 2，結果仍待判；重工不保證改善，也不清掉第一次 Fail。'],take:'回到原站重測，保留第一次失敗。'},
 'split-merge':{v:1,title:'拆成兩批，晶圓沒有變多',captions:['左邊是拆批前的三片；拆批後父批只保留歷史。','活躍成員分為 A 的兩片與 B 的一片。框是管理分組，不是實際承載方式。','A 在 S50、B 在 R10，還不能合；同站後仍要核對版本、限制與成員。'],take:'分的是批次身分，晶圓沒有複製。'},
 versions:{v:1,title:'新版上線，舊批會自動換路嗎？',captions:['v1 的路徑與歷史保留；S40 後是 S50。','v2 在兩者之間增加 S45 檢查，發布只改變可用定義。','L023 需要批准與位置映射才遷移；本例由 v1/S50 轉到 v2/S45 補檢查。'],take:'發布新版本，不會自動搬動在製批次。'},
 'flow-lab':{v:2,title:'拿著這批的工作單，走一次流程',captions:['先認出 F012 與 L023；起點尚未執行，結果欄保持空白。','核對 P-DEMO 與核准的 F-DEMO v1，再建立流程參照。','每次作業累積自己的位置、結果與歷程；下方情境由你的操作推進。'],take:'看同一批的旅程，依證據決定下一步。'}
};
const MOBILE_ART={port:1,recipe:1,chamber:1,state:1,handoff:3,'operations-lab':1,stage:2,step:2,'lot-flow':3,execution:2,rework:1,'split-merge':1,versions:1,'flow-lab':1};
function illustration(id){
 const a=ILLUSTRATED[id],src=`assets/mes-v3/${id}-v${a.v}.png`;
 const crops=a.crop||[[0,105,512,890],[512,105,1030,890],[1030,105,1536,890]];
 const mobile=MOBILE_ART[id]?`<button class="open-art portrait-art" aria-label="放大直式插畫：${a.title}"><img src="assets/mes-v3/${id}-mobile-v${MOBILE_ART[id]}.png" alt="${a.title}。${a.captions.join(' ')}"></button>${a.captions.map((s,i)=>`<div class="illustrated-panel portrait-reading"><p><span>${i+1}</span>${s}</p></div>`).join('')}`:crops.map(([x,y,r,b],i)=>`<div class="illustrated-panel"><button class="open-art image-crop" aria-label="放大完整圖：${a.title}" style="aspect-ratio:${r-x}/${b-y}"><img src="${src}" alt="${a.captions[i]}" style="width:${1536/(r-x)*100}%;left:${-x/(r-x)*100}%;top:${-y/(b-y)*100}%"></button><p><span>${i+1}</span>${a.captions[i]}</p></div>`).join('');
 return `<figure class="lesson-illustration" data-art="${id}"><button class="open-art illustration-desktop" aria-label="放大完整圖：${a.title}"><img src="${src}" alt="${a.title}。${a.captions.join(' ')}"></button><div class="illustration-mobile"><h2>${a.title}</h2>${mobile}<p class="illustrated-take">${a.take}</p></div><figcaption>AI 生成教學示意；${id==='branching'?'線寬與門檻為假設數值，非實廠規格。':'物件比例、操作畫面與工作單為示意。'}<span>點圖可放大完整構圖</span></figcaption></figure><div class="illustration-reading">${a.captions.map((s,i)=>`<p><b>${String(i+1).padStart(2,'0')}</b>${s}</p>`).join('')}</div>`;
}
for(const key of ['operations','flow'])for(const lesson of COURSES[key].lessons){
 const id=lesson.id==='lab'?key+'-lab':lesson.id;
 if(!ILLUSTRATED[id])continue;
 const previousBody=lesson.body;
 lesson.body=()=>{
  const t=document.createElement('template');t.innerHTML=previousBody();
  const original=t.content.querySelector('.teaching-scene');
  if(original){const details=document.createElement('details');details.className='evidence-drill';details.innerHTML='<summary>展開資料對照與狀態練習</summary>';original.replaceWith(details);details.append(original);}
  const hero=illustration(id);
  return lesson.id==='lab'?`<details class="lab-introduction" open><summary>先看這個情境在現場代表什麼</summary>${hero}<button class="button primary" data-start-lab>開始操作情境 ↓</button></details>${t.innerHTML}`:hero+t.innerHTML;
 };
}
document.addEventListener('click',e=>{if(e.target.closest('[data-start-lab]')){document.querySelector('.lab-introduction').open=false;document.querySelector('#scenario-lab')?.scrollIntoView({block:'start'});}});
