/* Exact, illustrative 25-slot records. No inferred schema or live factory data. */
window.ER_LOT_WAFER = (() => {
 const description='Lot 是晶圓的生產批次歸屬，Wafer 是每一片晶圓。同一個 FOUP 可以裝不同 Lot ID 的晶圓，也可以只裝一個 Lot 的 25 片晶圓；每片都有不同的 Wafer ID，放在不同的 Slot。FOUP 是容器，Slot 是容器內的位置，不能把一個 FOUP 當成一個 Lot。';
 const details='<h3>先分清楚四種身分</h3><p><strong>Lot ID</strong> 回答晶圓屬於哪一批；<strong>Wafer ID</strong> 辨識是哪一片；<strong>FOUP ID</strong> 辨識容器；<strong>Slot No.</strong> 表示它在這個容器內的位置。</p><div id="lot-wafer-demo"></div><p class="topic-takeaway">同一個 FOUP，可以有多個 Lot；同一個 Lot，可以有多片不同 Wafer。批次歸屬與槽位位置要分開看。</p><h3>對照上方 ER</h3><p>FRCAST_LOT 連接 FOUP 與 Lot 的裝載關係。這條線本身沒有列出每片 Wafer ID 和 Slot，不能把它當成完整的晶圓位置清單。下方是教學用的內容物示例，原圖未獨立畫出的 Wafer 不冒充新增的資料表。</p><p>查過去某個時間 FOUP 裡有哪些 Wafer，則要看內容物歷史；Split／Merge 進 FOUP 時會更新。25 片是這裡的單一 Lot 示例，不代表所有 Lot 都固定有 25 片。</p>';
 function mount(){
  const host=document.getElementById('lot-wafer-demo');if(!host)return;
  let scenario='single',selected=7;
  function records(){return Array.from({length:25},(_,i)=>({slot:String(i+1).padStart(2,'0'),wafer:'W'+String(i+1).padStart(3,'0'),lot:scenario==='single'||i<10?'L023':'L024'}));}
  function paint(){
   const rows=records(),r=rows[selected-1];
   host.innerHTML='<section class="lot-wafer-example" aria-label="Lot 與 Wafer 裝載示例"><h3>同一個 FOUP，兩種裝載情況</h3><p>以下是兩個獨立的教學示例，不是即時資料，也不表示一次 Split／Merge 的前後紀錄。</p><div class="lot-wafer-switch" role="group" aria-label="切換裝載示例"><button type="button" data-lw-mode="single" aria-pressed="'+(scenario==='single')+'">單一 Lot：25 片</button><button type="button" data-lw-mode="multiple" aria-pressed="'+(scenario==='multiple')+'">多個 Lot：10 ＋ 15 片</button></div><p class="lot-wafer-summary" role="status">'+(scenario==='single'?'FOUP F012：Lot L023，共 25 片不同 Wafer。':'FOUP F012：Lot L023 有 10 片，Lot L024 有 15 片；兩批共用這個容器。')+'</p><div class="lot-wafer-layout"><div class="lot-wafer-container"><div class="foup-handle" aria-hidden="true"></div><h4>FOUP F012</h4><p class="slot-heading">Slot　／　Wafer ID　／　Lot ID</p><div class="wafer-slots">'+rows.map((v,i)=>'<button type="button" class="wafer-slot '+(v.lot==='L023'?'lot-a':'lot-b')+'" data-lw-slot="'+(i+1)+'" aria-pressed="'+(selected===i+1)+'" aria-label="Slot '+v.slot+'，Wafer '+v.wafer+'，Lot '+v.lot+'"><span>'+v.slot+'</span><span class="wafer-disc">'+v.wafer+'</span><span>'+v.lot+'</span></button>').join('')+'</div><p class="slot-caption">槽位內容示意，非實物比例；點選一片查看歸屬。</p></div><div class="wafer-record" aria-live="polite"><h4>這一片的身分與位置</h4><dl><dt>Wafer ID</dt><dd>'+r.wafer+'</dd><dt>Lot ID</dt><dd>'+r.lot+'</dd><dt>FOUP ID</dt><dd>F012</dd><dt>Slot No.</dt><dd>'+r.slot+'</dd></dl><p><strong>'+r.wafer+'</strong> 屬於 <strong>'+r.lot+'</strong>，放在 <strong>F012 的 Slot '+r.slot+'</strong>。</p><p>'+(scenario==='single'?'25 片的 Lot ID 相同，但 Wafer ID 與 Slot No. 各不相同。':'Slot 01–10 屬於 L023，Slot 11–25 屬於 L024；Lot ID 不同，FOUP ID 仍相同。')+'</p><p class="wafer-record-hint">Slot 編號只在這個 FOUP 的上下文中表示位置，不能代替 Wafer ID。</p></div></div></section>';
   const inline=document.createElement('p');inline.className='wafer-inline-detail';inline.textContent=r.wafer+' 屬於 '+r.lot+'；位置：F012／Slot '+r.slot;host.querySelector('[data-lw-slot="'+selected+'"]').after(inline);
   host.querySelectorAll('[data-lw-mode]').forEach(b=>b.onclick=()=>{scenario=b.dataset.lwMode;paint();host.querySelector('[data-lw-mode="'+scenario+'"]').focus({preventScroll:true});});
   host.querySelectorAll('[data-lw-slot]').forEach(b=>b.onclick=()=>{selected=Number(b.dataset.lwSlot);paint();host.querySelector('[data-lw-slot="'+selected+'"]').focus({preventScroll:true});});
  }
  paint();
 }
 return {description,details,mount};
})();
