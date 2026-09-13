(() => {
 const captions={foup:'FOUP 是容器，晶圓是內容物。圖為開門概念示意，僅呈現部分晶圓；實際門體由設備交接機構處理。',slot:'局部槽位示例：先找到 F012，再找到 Slot 07；W07 是晶圓身分。',lot:'此圖僅示三片晶圓。同一 Lot 也可以有 25 片，每片有不同 Wafer ID；一個 FOUP 也可以裝多個 Lot。'};
 for(const key of Object.keys(captions)){
  const panel=document.querySelector(`#${key} .teaching-panel`);
  const figure=document.createElement('figure');figure.className='refresh-figure';
  figure.innerHTML=`<a href="assets/mes-055/${key}.png" target="_blank" rel="noopener" aria-label="放大 ${key} 教學圖"><img src="assets/mes-055/${key}.png" alt="${captions[key]}"></a><figcaption>${captions[key]} <a href="assets/mes-055/${key}.png" target="_blank" rel="noopener">放大教學圖 ↗</a></figcaption>`;
  panel.replaceWith(figure);
 }
 const intro=document.createElement('div');intro.className='refresh-exercise-intro';intro.innerHTML='<h2>動手找 W07，再移動它</h2><p>先選有晶圓的槽位，讀取 Wafer、FOUP、Slot 與 Lot。再按移動，觀察位置改變後，哪些身分仍相同。</p><a href="topic.html?topic=material">先看 FOUP 與 Lot 的實物對照 →</a>';
 const reference=document.createElement('figure');reference.className='refresh-figure';reference.innerHTML='<a href="assets/mes-055/slot.png" target="_blank" rel="noopener"><img src="assets/mes-055/slot.png" alt="實物對照：FOUP F012 內 Slot 07 的晶圓 W07"></a><figcaption>先看實物中的身分與位置，再用下方控制面板練習。<a href="assets/mes-055/slot.png" target="_blank" rel="noopener">放大教學圖 ↗</a></figcaption>';
 document.querySelector('#explore .explorer').before(reference,intro);
 const update=()=>document.body.classList.toggle('refresh-basic',['slot','foup','lot','explore'].includes(location.hash.slice(1)));
 update();window.addEventListener('hashchange',update);
})();
