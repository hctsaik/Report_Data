/* Topic presentation uses exactly the same confirmed registry as the ER inspector. */
(async()=>{
 const get=id=>document.getElementById(id),params=new URLSearchParams(location.search);
 const key=params.get('topic')||'lot',topics=window.ER_TEACHING,t=topics[key];
 if(!t||['overview','source'].includes(key)){
  get('topic-title').textContent='找不到這個主題';get('topic-meaning').textContent='請回學習中心選擇主題，或到 ER 搜尋資料名稱。';get('topic-references').hidden=true;return;
 }
 document.title=t.title+'｜MES 主題教學';document.body.dataset.topic=key;
 get('topic-title').textContent=t.title;get('topic-meaning').textContent=t.meaning||'';
 const retired=['retired','portdata'].includes(key);
 if(retired)get('topic-status').textContent='此項保留原始來源與撤下原因，不列入學習課程。';
 get('topic-detail').innerHTML=t.details||'';
 window.ER_LOT_WAFER.mount();window.ER_MCS.mount();
 if(t.image){get('topic-figure').hidden=false;get('topic-image').src=t.image;get('topic-image').alt=t.alt||t.title;get('topic-mobile').srcset=t.mobile||t.image;get('topic-caption').textContent=t.caption||'';
  get('topic-enlarge').onclick=()=>{get('topic-large').src=get('topic-image').currentSrc;get('topic-large').alt=t.alt||t.title;get('topic-large-caption').textContent=t.caption||'';get('topic-dialog').showModal();};
 }
 if(t.link&&!t.link.startsWith('#')){get('topic-extended').hidden=false;get('topic-extended').href=t.link;}
 const addLink=(host,label,href)=>{const a=document.createElement('a');a.textContent=label;a.href=href;host.append(a);return a;};
 const unit=window.MES_CATALOG?.topicUnits?.[key];
 if(unit&&!retired){const n=Array.isArray(unit)?unit[0]:unit;const number=typeof n==='object'?(n.id||n.unit):n;addLink(get('topic-context'),'回單元 '+number,'learning.html?unit='+encodeURIComponent(number));addLink(get('topic-next'),'回單元 '+number+'，繼續學習','learning.html?unit='+encodeURIComponent(number));}
 else addLink(get('topic-context'),'學習中心','learning.html');
 addLink(get('topic-next'),'所有學習單元','learning.html');
 try{
  const response=await fetch('ER/INTEGRATED/er-model-v2.json');if(!response.ok)throw Error('ER source unavailable');const model=await response.json();
  for(const ref of t.refs||[]){const id=model.mapping[ref],node=model.nodes.find(n=>n.id===id);if(!node)continue;
   const li=document.createElement('li');addLink(li,'在 ER 查看：'+node.labels.join('／'),'er-atlas.html?view=original&erNode='+encodeURIComponent(id));
   const small=document.createElement('small');small.textContent='來源 '+ref+' · ';addLink(small,'開啟原圖','data-map.html?view=original#'+ref.split(':')[0]);li.append(small);get('topic-refs').append(li);
  }
  if(!get('topic-refs').children.length)get('topic-references').hidden=true;
 }catch(error){get('topic-refs').textContent='ER 來源暫時無法載入，請回 ER 資料參考重試。';}
})();
