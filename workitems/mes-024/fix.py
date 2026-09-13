"""Restore Lot context using existing source edges, not the withdrawn FOUP/Step shortcut."""
from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'er-focus.js';s=p.read_text(encoding='utf-8')
s=s.replace('walk([id],[]);',"""walk([id],[]);
    // FOUP -> loading -> Lot -> Lot_id summary -> Step history: every edge exists in source.
    if(id===model.mapping['2671:cast']){
      const ids=['2671:cast','2671:cast-link','2671:lot','2672:summary','2672:step'].map(ref=>model.mapping[ref]);
      const es=ids.slice(1).map((v,i)=>model.edges.find(e=>(e.a===ids[i]&&e.b===v)||(e.b===ids[i]&&e.a===v)));
      if(es.every(Boolean)){const i=out.findIndex(b=>b.ids[1]===ids[1]&&b.ids.at(-1)===ids[2]);if(i>=0)out.splice(i,1);out.unshift({ids,edges:es});}
    }
""")
s=s.replace("if(id===model.mapping['2671:predispatch'])", "if(id===model.mapping['2672:step'])return out.sort((a,b)=>Number(b.ids.includes(model.mapping['2671:lot']))-Number(a.ids.includes(model.mapping['2671:lot'])));if(id===model.mapping['2671:predispatch'])")
s=s.replace("[['2673:wph',['機群 WPH 定義'", "[['2672:step',['Lot Step 歷史','F12DM.DM_Lot_step_st']],['2673:wph',['機群 WPH 定義'")
s=s.replace("const more=$('focus-more');", "if(root===model.mapping['2672:step']||branches.some(b=>b.ids.includes(model.mapping['2672:step'])))$('focus-note').append(' Lot Step 歷史須對到 Lot；從 FOUP 查閱時保留裝載關係與中間的 Lot。');const more=$('focus-more');")
p.write_text(s,encoding='utf-8')
p=r/'er-atlas.js';s=p.read_text(encoding='utf-8')
s=s.replace('const routes=[',"const routes=[\n{id:'lot-step',title:'這個 Lot 的 Step 歷史',refs:['2671:lot','2672:summary','2672:step'],meaning:'Lot Step 歷史以 Lot 為對象。原圖透過「站點 Summary／Lot_id」連接 LOT（Siview.Frlot）與 F12DM.DM_Lot_step_st；從 FOUP 查這段資料時，還要經裝載關係找到 Lot，不能省略 Lot。'},")
s=s.replace("$('status').textContent='已定位：'+n.labels.join(' / ');", "if(id===model.mapping['2672:step']){$('selection-title').textContent='Lot Step 歷史';$('meaning').textContent='Lot Step 歷史以 Lot 為對象，透過原圖的「站點 Summary／Lot_id」與 LOT（Siview.Frlot）連接。查詢 FOUP 相關站點資料時，須保留中間的 Lot。';$('selection-details').open=true;}$('status').textContent='已定位：'+n.labels.join(' / ');")
s=s.replace("if(new URLSearchParams(location.search).get('subject')==='predispatch')", "if(new URLSearchParams(location.search).get('subject')==='lot-step')selectNode(model.mapping['2672:step']);if(new URLSearchParams(location.search).get('subject')==='predispatch')")
p.write_text(s,encoding='utf-8')
p=r/'er-atlas.html';s=p.read_text(encoding='utf-8').replace('er-atlas.js?v=23','er-atlas.js?v=24').replace('er-focus.js?v=23','er-focus.js?v=24');p.write_text(s,encoding='utf-8')
