/* MES-017: redraw source relationships around a selected subject. */
(() => {
  'use strict';
  const NS='http://www.w3.org/2000/svg';
  let model, nodes, onSelect, root, branches=[], page=0;
  const $=id=>document.getElementById(id);
  const pageSize=()=>window.innerWidth<=950?2:4;
  const color={lot:'#176ac2',carrier:'#008775',equipment:'#b26018',flow:'#7756af',record:'#61748b',relation:'#657687'};
  function el(tag,attrs={},text){const n=document.createElementNS(NS,tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));if(text!==undefined)n.textContent=text;return n;}
  // User correction: the historical Step/FRCAST branch is not the Lot loading relation.
  // Keep the source model for audit; withdraw this branch from teaching subgraphs in both directions.
  function adjacent(id){const withdrawn=model.mapping['2672:cast-link'],predispatch=model.mapping['2671:predispatch'],carrier=model.mapping['2671:cast'];return model.edges.filter(e=>e.a!==withdrawn&&e.b!==withdrawn&&!([e.a,e.b].includes(predispatch)&&[e.a,e.b].includes(carrier))&&(e.a===id||e.b===id)).map(e=>({edge:e,id:e.a===id?e.b:e.a}));}
  function collect(id){
    const out=[];
    function walk(path,es){const last=path.at(-1),n=nodes.get(last);if(path.length>1&&(n.kind!=='diamond'||path.length>=5)){out.push({ids:path,edges:es});return;}const next=adjacent(last).filter(v=>!path.includes(v.id));if(!next.length&&path.length>1)out.push({ids:path,edges:es});next.forEach(v=>walk([...path,v.id],[...es,v.edge]));}
    walk([id],[]);
    if([model.mapping['2672:qtime'],model.mapping['2672:qtime-link']].includes(id)){
      const refs=id===model.mapping['2672:qtime']?['2672:qtime','2672:qtime-link','2672:step','2672:summary','2671:lot']:['2672:qtime-link','2672:step','2672:summary','2671:lot'];
      const ids=refs.map(ref=>model.mapping[ref]);
      const es=ids.slice(1).map((v,i)=>model.edges.find(e=>(e.a===ids[i]&&e.b===v)||(e.b===ids[i]&&e.a===v)));
      if(es.every(Boolean)){const i=out.findIndex(b=>b.ids[1]===ids[1]);if(i>=0)out.splice(i,1);out.unshift({ids,edges:es});}
    }

    // FOUP -> loading -> Lot -> Lot_id summary -> Step history: every edge exists in source.
    if(id===model.mapping['2671:cast']){
      const ids=['2671:cast','2671:cast-link','2671:lot','2672:summary','2672:step'].map(ref=>model.mapping[ref]);
      const es=ids.slice(1).map((v,i)=>model.edges.find(e=>(e.a===ids[i]&&e.b===v)||(e.b===ids[i]&&e.a===v)));
      if(es.every(Boolean)){const i=out.findIndex(b=>b.ids[1]===ids[1]&&b.ids.at(-1)===ids[2]);if(i>=0)out.splice(i,1);out.unshift({ids,edges:es});}
    }

    const refs=['2677:recipe','2677:recipe-key','2677:recipe-eqp','2677:eqp-id','2677:eqp'];
    const chain=refs.map(r=>model.mapping[r]);
    if(id===chain[0]&&chain.every(Boolean)){
      const es=chain.slice(1).map((v,i)=>model.edges.find(e=>(e.a===chain[i]&&e.b===v)||(e.b===chain[i]&&e.a===v)));
      if(es.every(Boolean)){const i=out.findIndex(b=>b.ids[1]===chain[1]);if(i>=0)out.splice(i,1);out.unshift({ids:chain,edges:es});}
    }
    const priority=(id===model.mapping['2671:cast']?['2671:cast-link','2671:location','2671:predispatch','2671:slot']:['2671:cast-link','2671:lot-eqp','2673:flow-link','2671:location','2671:predispatch','2671:slot','2673:lr-eqp-link','2674:chamber-link']).map(ref=>model.mapping[ref]);
    const rank=b=>Math.min(...b.ids.slice(1).map(v=>{const i=priority.indexOf(v);return i<0?99:i;}));
    if([model.mapping['2672:step'],model.mapping['2672:qtime'],model.mapping['2672:qtime-link']].includes(id))return out.sort((a,b)=>Number(b.ids.includes(model.mapping['2671:lot']))-Number(a.ids.includes(model.mapping['2671:lot'])));if(id===model.mapping['2671:predispatch']){const order=[model.mapping['2671:lot'],model.mapping['2671:eqp'],model.mapping['2671:cast']];return out.sort((a,b)=>order.indexOf(a.ids.at(-1))-order.indexOf(b.ids.at(-1)));}return out.sort((a,b)=>rank(a)-rank(b));
  }
  function wrap(text,width,font){const lines=[];let s='',size=0;for(const c of String(text)){const w=/[\u0000-\u00ff]/.test(c)?font*.57:font;if(size+w>width&&s){lines.push(s);s='';size=0;}s+=c;size+=w;}if(s)lines.push(s);return lines;}
  function nodeSpec(id,w){let n=nodes.get(id);if(root===model.mapping['2671:predispatch']&&id===model.mapping['2671:cast'])n={...n,labels:['FOUP（輔助關聯）',...n.labels.slice(1)]};const diamond=n.kind==='diamond';const inner=diamond?w*.62:w-24;const lines=n.labels.flatMap((s,i)=>wrap(s,inner,i?13:17).map(text=>({text,font:i?13:17})));let h=Math.max(diamond?92:66,lines.length*20+(diamond?38:24));if(diamond)for(let i=0;i<lines.length;i++){const l=lines[i],length=[...l.text].reduce((sum,c)=>sum+(/[\u0000-\u00ff]/.test(c)?l.font*.57:l.font),0);h=Math.max(h,2*(Math.abs(-(lines.length-1)*10+i*20)+l.font*.7+4)/(1-(length+12)/w));}return {id,n,w,h:Math.ceil(h),lines};}
  function drawNode(s,svg,x,y,isRoot=false){const g=el('g',{'data-focus-node':s.id,transform:`translate(${x},${y})`,tabindex:'0',role:'button','aria-label':`${s.n.labels.join(' / ')}${isRoot?'，目前主詞':'，改以此為主詞'}`});const c=color[s.n.category]||'#61748b';const attrs={fill:isRoot?'#e8f2ff':'#fff',stroke:c,'stroke-width':isRoot?3:1.8};if(s.n.kind==='diamond')g.append(el('polygon',{...attrs,points:`0,${-s.h/2} ${s.w/2},0 0,${s.h/2} ${-s.w/2},0`}));else if(s.n.kind==='circle')g.append(el('ellipse',{...attrs,rx:s.w/2,ry:s.h/2}));else g.append(el('rect',{...attrs,x:-s.w/2,y:-s.h/2,width:s.w,height:s.h,rx:7}));s.lines.forEach((l,i)=>g.append(el('text',{x:0,y:-(s.lines.length-1)*10+i*20+5,'text-anchor':'middle','font-size':l.font,'font-weight':i===0?'700':'400',fill:'#16354d'},l.text)));g.append(el('title',{},s.n.labels.join(' / ')));let pressed=false;g.addEventListener('pointerdown',()=>{pressed=true;});g.addEventListener('pointercancel',()=>{pressed=false;});g.addEventListener('click',e=>{if(pressed)onSelect(s.id);pressed=false;});g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();onSelect(s.id);}});svg.append(g);}
  function render(target,large=false){
    target.replaceChildren();if(!root)return;
    const width=Math.max(280,Math.floor(target.clientWidth||600)),mobile=width<510;
    const svg=el('svg',{width:'100%',role:'img','aria-label':`${nodes.get(root).labels[0]} 為主詞的關聯 ER`});
    const lines=el('g',{'class':'focus-lines'});svg.append(lines);
    const rootSpec=nodeSpec(root,Math.min(300,width-52)),rx=width/2,ry=rootSpec.h/2+24;
    const placements=[{s:rootSpec,x:rx,y:ry,root:true}];let y=ry+rootSpec.h/2+42;
    const visible=branches.slice(page*pageSize(),(page+1)*pageSize());
    visible.forEach((branch,index)=>{
      const count=branch.ids.length-1, colW=mobile?width-68:(width-78)/2;
      const list=branch.ids.slice(1).map(id=>nodeSpec(id,colW));
      let prev={x:rx,y:ry,s:rootSpec},bottom=y;
      list.forEach((s,i)=>{
        let x,cy;
        if(mobile){x=width/2;cy=y+s.h/2;y=cy+s.h/2+30;}
        else {x=i%2===0?36+colW/2:width-18-colW/2;if(i%2===0){const rowH=Math.max(s.h,list[i+1]?.h||0);cy=y+rowH/2;bottom=y+rowH+34;}else cy=placements.at(-1).y;if(i%2===1||i===count-1)y=bottom;}
        const next={s,x,y:cy};const e=branch.edges[i];let d;
        if(i===0){const rail=12+index*4;d=`M ${rx-rootSpec.w/2} ${ry} H ${rail} V ${cy} H ${x-s.w/2}`;}
        else if(!mobile&&i%2===1)d=`M ${prev.x+prev.s.w/2} ${prev.y} H ${x-s.w/2}`;
        else d=`M ${prev.x} ${prev.y+prev.s.h/2} V ${cy-s.h/2-15} H ${x} V ${cy-s.h/2}`;
        lines.append(el('path',{d,fill:'none',stroke:'#6c8598','stroke-width':e.provenance?2.8:1.8,'stroke-dasharray':e.provenance?'8 5':'none','data-edge-provenance':e.provenance||'source','data-focus-edge':e.id}));placements.push(next);prev=next;
      });
      y+=18;
    });
    if(!visible.length)y+=20;
    svg.setAttribute('viewBox',`0 0 ${width} ${Math.max(y,160)}`);svg.style.height=Math.max(y,160)+'px';placements.forEach(p=>drawNode(p.s,svg,p.x,p.y,p.root));target.append(svg);
  }
  function paint(){if(!root)return;const pages=Math.max(1,Math.ceil(branches.length/pageSize()));page=Math.min(page,pages-1);$('focus-title').textContent=nodes.get(root).labels[0]+' · 主詞關聯 ER';$('focus-note').textContent=branches.length?`以此主詞展開 ${branches.length} 條關係支線，目前第 ${page+1} / ${pages} 組關係。點相關節點可改換主詞。同一實體可重複顯示，以分開不同關係；此圖未展開所有間接關聯。`:'目前沒有可顯示的已確認關係支線。';if(nodes.get(root).refs.some(r=>r.node==='lot'))$('focus-note').append(' 原 ER 未獨立畫出 Wafer 實體；FOUP 內容物歷史仍記錄 Wafer。');if([model.mapping['2673:wph'],model.mapping['2673:wph-link']].includes(root))$('focus-note').append(' 業務定義：生管為機群訂定預期 WPH。下方是原資料關聯，不表示由 LR 定義個別機台的產出；請看專屬參考圖。');if(branches.some(b=>b.ids.includes(model.mapping['2671:lot-eqp'])))$('focus-note').append(' 「帶到」表示 Lot 在這個站點有可用機台，不是預計到達。');if(root===model.mapping['2671:slot']||branches.some(b=>b.ids.includes(model.mapping['2671:slot'])))$('focus-note').append(' 內容物歷史：記錄各時間點 FOUP 裡的 Wafer，每次 Split／Merge 進 FOUP 時更新。');if(root===model.mapping['2671:predispatch']||branches.some(b=>b.edges.some(e=>e.provenance)))$('focus-note').append(' 預派以 Lot 為主，由派工系統預先安排目標機台；FOUP 是輔助關聯。虛線為已確認的業務關係，不表示資料表 Join 鍵。');if(root===model.mapping['2672:step']||branches.some(b=>b.ids.includes(model.mapping['2672:step'])))$('focus-note').append(' Lot Step 歷史須對到 Lot；從 FOUP 查閱時保留裝載關係與中間的 Lot。');if([model.mapping['2672:qtime'],model.mapping['2672:qtime-link']].includes(root))$('focus-note').append(' 這是同一 Lot 的 Qtime 與站點歷史關聯；保留 Lot、Lot_id 及 Lot_ID／Ope_no 的來源路徑。');const more=$('focus-more');more.replaceChildren();if(pages>1){for(let p=0;p<pages;p++){const b=document.createElement('button');b.textContent=`第 ${p+1} 組：關係 ${p*pageSize()+1}–${Math.min(branches.length,(p+1)*pageSize())}`;b.setAttribute('aria-pressed',String(p===page));b.onclick=()=>{page=p;paint();};more.append(b);}}render($('focus-graph'));if($('focus-dialog')?.open)render($('focus-large'),true);}
  window.ER_FOCUS={
    refresh:paint,
    setPage(value){page=Math.max(0,Number(value)||0);paint();},
    init(m,options){model={...m,edges:[...m.edges,{id:'business-lot-predispatch',a:m.mapping['2671:lot'],b:m.mapping['2671:predispatch'],provenance:'user-confirmed-business',refs:[]}]};nodes=new Map(m.nodes.map(n=>[n.id,n]));
    for(const [ref,labels] of [['2672:step',['Lot Step 歷史','F12DM.DM_Lot_step_st']],['2673:wph',['機群 WPH 定義','F12DM.DM_TBL_IE_CTWPH']],['2673:wph-link',['WPH 定義對應']]]){const id=m.mapping[ref];if(nodes.has(id))nodes.set(id,{...nodes.get(id),labels});}
    onSelect=options.selectNode;const expand=$('focus-expand');if(expand)expand.onclick=()=>{if(!root)return;$('focus-dialog').showModal();render($('focus-large'),true);};let timer;window.addEventListener('resize',()=>{clearTimeout(timer);timer=setTimeout(()=>paint(),100);});},
    show(id){if(!nodes?.has(id))return;root=id;page=0;branches=collect(id);$('focus-panel').hidden=false;$('focus-expand').disabled=false;paint();},
    clear(){root=null;branches=[];if($('focus-panel'))$('focus-panel').hidden=false;if($('focus-graph'))$('focus-graph').replaceChildren();$('focus-title').textContent='選一個主詞，展開關聯';$('focus-note').textContent='點選上方 Lot、FOUP、EQP、Flow、Recipe，或直接點完整 ER 的節點。';$('focus-more').replaceChildren();$('focus-expand').disabled=true;if($('focus-dialog').open)$('focus-dialog').close();},
    getState(){return {root,page,branches:branches.map(b=>({ids:[...b.ids],edges:b.edges.map(e=>e.id),businessEdges:b.edges.filter(e=>e.provenance).map(e=>e.id)}))};}
  };
})();
