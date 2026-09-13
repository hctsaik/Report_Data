/* Illustrative event trace, not an MCS schema or live tracking feed. */
window.ER_MCS = {
 mount(){
  const host=document.getElementById('mcs-command-demo');if(!host)return;
  const stops=[{name:'起點 A',time:'10:00',x:70,y:65},{name:'轉彎 B',time:'10:01',x:320,y:65},{name:'轉彎 C',time:'10:02',x:320,y:235},{name:'終點 D',time:'10:03',x:70,y:235}];
  let selected=0;
  function paint(){const s=stops[selected],next=stops[selected+1];
   host.innerHTML='<section class="mcs-demo" aria-label="MCS 巨觀與微觀命令示例"><h3>同一個 FOUP F012，從 A 搬到 D</h3><p>教學示例：以下時間、位置與命令編號均為假設，線路非實際軌道比例。</p><div class="mcs-macro"><strong>Macro command M001｜E2E</strong><p>起點 A ─────────→ 終點 D</p><span>描述整趟搬運的起終點；下方展開同一趟的 Micro command。</span></div><svg viewBox="0 0 390 310" role="img" aria-label="微觀路徑由起點 A 經轉彎 B、轉彎 C 到終點 D，目前紀錄位置 '+s.name+'"><defs><marker id="mcs-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7Z" fill="#39749c"/></marker></defs>'+stops.slice(1).map((p,i)=>{const a=stops[i];return '<path d="M'+a.x+' '+a.y+' L'+p.x+' '+p.y+'" fill="none" stroke="'+(i<selected?'#146fc0':'#a6b7c5')+'" stroke-width="5" marker-end="url(#mcs-arrow)"/>';}).join('')+'<text x="190" y="42" text-anchor="middle">Micro μ01：A → B</text><text x="304" y="140" text-anchor="end">μ02：B → C</text><text x="190" y="280" text-anchor="middle">Micro μ03：C → D</text>'+stops.map((p,i)=>'<circle cx="'+p.x+'" cy="'+p.y+'" r="10" fill="'+(i===selected?'#ffcc62':'#fff')+'" stroke="#176ac2" stroke-width="3"/><text x="'+p.x+'" y="'+(p.y===65?93:215)+'" text-anchor="middle">'+p.name+'</text>').join('')+'<rect x="'+(s.x-30)+'" y="'+(s.y-44)+'" width="60" height="24" rx="4" fill="#008775"/><text x="'+s.x+'" y="'+(s.y-27)+'" text-anchor="middle" fill="white">F012</text></svg><div class="mcs-events" role="group" aria-label="依時間查看位置紀錄">'+stops.map((p,i)=>'<button type="button" data-mcs-event="'+i+'" aria-pressed="'+(selected===i)+'">'+p.time+'<br>'+p.name+'</button>').join('')+'</div><div class="mcs-event-detail" aria-live="polite"><strong>'+s.time+'｜FOUP F012</strong><p>此筆示例紀錄位置：<b>'+s.name+'</b></p><p>'+(next?'下一段命令：'+s.name+' → '+next.name+'；要確認何時到達，請看 '+next.time+' 的下一筆位置紀錄。':'此筆示例記錄已到終點 D；整趟命令是否完成，仍須核對命令完成狀態。')+'</p></div><p class="topic-takeaway">Macro 看整趟起終點；Micro 追每段軌道移動。把時間、位置與命令狀態合起來，才能回查 FOUP 的行蹤。</p></section>';
   host.querySelectorAll('[data-mcs-event]').forEach(b=>b.onclick=()=>{selected=Number(b.dataset.mcsEvent);paint();host.querySelector('[data-mcs-event="'+selected+'"]').focus({preventScroll:true});});
  }
  paint();
 }
};
