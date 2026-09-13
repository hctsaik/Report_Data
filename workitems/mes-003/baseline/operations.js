'use strict';

// Every exercise owns an independent state, so replaying one cannot alter another.
const chapterIds = ['tool', 'port', 'chamber', 'process', 'transport', 'state', 'arrival', 'run', 'hold', 'reconcile'];
const chapterNames = ['Tool / Equipment', 'Load Port', 'Chamber', 'Route・Step・Recipe', '搬送與暫存', '加工與 Hold 狀態', '情境 A：搬送停靠', '情境 B：配方與加工', '情境 C：Hold 複核', '情境 D：槽位核對'];
const one = selector => document.querySelector(selector);
let chapterIndex = 0;

function closeMenu() { one('#sidebar').classList.remove('open'); one('#menu-toggle').setAttribute('aria-expanded', 'false'); }
function showChapter(focus = false) {
  const requested = location.hash.slice(1);
  chapterIndex = chapterIds.includes(requested) ? chapterIds.indexOf(requested) : 0;
  document.querySelectorAll('.lesson').forEach((section, index) => { section.hidden = index !== chapterIndex; });
  document.querySelectorAll('[data-step]').forEach(link => {
    if (link.dataset.step === chapterIds[chapterIndex]) link.setAttribute('aria-current', 'step');
    else link.removeAttribute('aria-current');
  });
  one('#step-count').textContent = `${String(chapterIndex + 1).padStart(2, '0')} / 10`;
  one('#footer-label').textContent = chapterNames[chapterIndex];
  one('#previous').disabled = chapterIndex === 0;
  one('#next').textContent = chapterIndex === chapterIds.length - 1 ? '重新挑戰情境 A →' : `下一段：${chapterNames[chapterIndex + 1]} →`;
  document.title = `${chapterNames[chapterIndex]}｜設備、流程與現場情境`;
  closeMenu();
  if (focus) { one('#content').focus({preventScroll: true}); window.scrollTo({top: 0, behavior: 'instant'}); }
}
window.addEventListener('hashchange', () => {
  if (location.hash === '#content') { one('#content').focus(); return; }
  showChapter(true);
});
one('#previous').addEventListener('click', () => { if (chapterIndex > 0) location.hash = chapterIds[chapterIndex - 1]; });
one('#next').addEventListener('click', () => { location.hash = chapterIndex === chapterIds.length - 1 ? 'arrival' : chapterIds[chapterIndex + 1]; });
one('#menu-toggle').addEventListener('click', () => {
  const open = one('#sidebar').classList.toggle('open'); one('#menu-toggle').setAttribute('aria-expanded', String(open));
});
document.querySelectorAll('[data-step]').forEach(link => link.addEventListener('click', () => {
  if (link.dataset.step === chapterIds[chapterIndex]) showChapter(true);
}));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && one('#sidebar').classList.contains('open')) { closeMenu(); one('#menu-toggle').focus(); }
});

// These diagrams are DOM-native so the visible labels and live data stay exact.
document.querySelectorAll('[data-machine]').forEach(host => {
  const inside = host.dataset.machine === 'chamber';
  host.innerHTML = `<div class="machine-shell"><div class="machine-name">Tool ETCH-03</div><div class="machine-interior"><div class="mini-chamber">Chamber CH-A${inside ? '<span class="mini-wafer">W07</span>' : ''}</div><div class="mini-chamber">Chamber CH-B</div></div>${inside ? '<div class="machine-movement">↑ W07 從原槽位移入 CH-A</div>' : ''}<div class="machine-ports"><div class="machine-port"><div class="small-foup">F012</div><strong>Load Port LP1</strong></div><div class="machine-port"><span>無載具</span><strong>Load Port LP2</strong></div></div></div><p class="machine-caption">設備外形與內部配置為教學剖面示意${inside ? '；此刻 F012 的 Slot 07 已空出。' : '，非特定機型結構圖。'}</p>`;
});

function feedback(selector, message, kind = '') {
  const element = one(selector); element.textContent = message;
  element.classList.remove('problem', 'success'); if (kind) element.classList.add(kind);
}

let arrivalPhase = 0;
const arrivalLocations = ['STK-01 暫存位置', 'OHT-01 搬送途中', 'ETCH-03／LP1'];
function renderArrival() {
  const locations = [
    {name: 'Stocker STK-01', detail: '出發位置'},
    {name: 'OHT-01', detail: '運送載具的車輛'},
    {name: 'ETCH-03／LP1', detail: '已核對的目的位置'}
  ];
  one('#arrival-scene').innerHTML = locations.map((place, index) => `<div class="arrival-place ${arrivalPhase === index ? 'active' : ''}"><h2>${place.name}</h2><div class="carrier-space">${arrivalPhase === index ? '<div class="small-foup">F012</div>' : '<span class="placeholder">此刻 F012 不在這裡</span>'}</div><small>${place.detail}</small></div>`).join('');
  one('#arrival-location').textContent = `F012 目前位置：${arrivalLocations[arrivalPhase]}。W07 仍在 F012／07，屬於 L023。`;
  one('#destination').disabled = arrivalPhase > 0;
  one('#arrival-next').disabled = arrivalPhase === 2;
  one('#arrival-next').textContent = ['核對目的地並派送', '模擬完成交接，確認到達', '已停靠，尚未開始加工'][arrivalPhase];
}
one('#arrival-next').addEventListener('click', () => {
  if (arrivalPhase === 2) return;
  if (arrivalPhase === 0 && one('#destination').value !== 'ETCH-03/LP1') {
    feedback('#arrival-feedback', '目的地不符合本次任務。要求的是 ETCH-03／LP1；設備或 Port 任一不同都不能派送。F012 仍在 STK-01。', 'problem'); return;
  }
  arrivalPhase++;
  renderArrival();
  feedback('#arrival-feedback', arrivalPhase === 1 ? '已派送，F012 正在 OHT-01 上。目的地仍是 ETCH-03／LP1，但不能先把目前位置寫成已到達。' : '交接完成，F012 已停靠 ETCH-03／LP1；三片晶圓仍在原槽位。這個事件只完成搬送，S20 蝕刻尚未開始。', 'success');
  if (arrivalPhase === 2) one('#arrival-reset').focus({preventScroll: true});
});
one('#arrival-reset').addEventListener('click', () => {
  arrivalPhase = 0; one('#destination').value = 'ETCH-03/LP1'; renderArrival();
  feedback('#arrival-feedback', '已重設。F012 在 STK-01，目的地要求 ETCH-03／LP1；可以再試設備或 Port 不符的選項。');
});

const runMembers = [{id: 'W06', slot: '06'}, {id: 'W07', slot: '07'}, {id: 'W08', slot: '08'}];
let completedWafers = 0;
let processing = false;
let runEvents = [];
function renderRun() {
  one('#run-slots').innerHTML = [...runMembers].reverse().map(member => {
    const index = runMembers.indexOf(member);
    const inChamber = processing && index === completedWafers;
    return `<div class="run-slot"><span>Slot ${member.slot}<small>${inChamber ? '本片在 CH-A' : index < completedWafers ? '本站已完成' : '本站未完成'}</small></span>${inChamber ? '<span class="vacant">空槽位</span>' : `<span class="mini-wafer">${member.id}</span>`}</div>`;
  }).join('');
  one('#chamber-wafer').innerHTML = processing ? `<span class="mini-wafer">${runMembers[completedWafers].id}</span>` : '<span class="empty-chamber">目前無晶圓</span>';
  one('#chamber-state').textContent = processing ? 'Processing · 加工中' : 'Idle · 待機';
  one('#run-progress').textContent = `本站完成 ${completedWafers} / 3 片`;
  one('#run-lot-state').textContent = completedWafers === 3 ? 'L023 · S20 完成，待進 S30 量測' : `Lot L023 · ${processing || completedWafers > 0 ? 'Processing' : 'Ready'}`;
  one('#recipe-choice').disabled = processing || completedWafers > 0;
  one('#run-next').disabled = completedWafers === 3;
  one('#run-next').textContent = completedWafers === 3 ? '本站已完成' : processing ? `模擬 ${runMembers[completedWafers].id} 完成並回槽` : `核對並開始 ${runMembers[completedWafers].id}`;
  const history = one('#run-history'); history.replaceChildren();
  for (const text of runEvents) { const li = document.createElement('li'); li.textContent = text; history.append(li); }
}
one('#run-next').addEventListener('click', () => {
  if (completedWafers === 3) return;
  if (!processing && one('#recipe-choice').value !== 'ETCH-DEMO/v2') {
    feedback('#run-feedback', '配方或版本不符合本課 S20 的指定條件。必須核對 ETCH-DEMO／v2；尚未開始加工，三片仍保持本情境的目前位置。', 'problem'); return;
  }
  const member = runMembers[completedWafers];
  if (!processing) {
    processing = true;
    runEvents.push(`${member.id}：從 F012／${member.slot} 移入 ETCH-03／CH-A，使用 ETCH-DEMO／v2。`);
    feedback('#run-feedback', `${member.id} 正在 CH-A 加工，原 Slot ${member.slot} 已空出。FOUP 仍在 LP1；Lot 仍為 L023。按完成後再看它回到原槽位。`, 'success');
  } else {
    processing = false; completedWafers++;
    runEvents.push(`${member.id}：本站完成，回到 F012／${member.slot}。`);
    feedback('#run-feedback', completedWafers === 3 ? '三片都已完成 S20 並回到原槽位，這一站才算完成。下一步 S30 量測尚未執行，不代表整個 Route 已完成。' : `${member.id} 已完成並回槽。目前只有 ${completedWafers}／3 片完成；L023 在本站的作業尚未全部完成，請繼續下一片。`, 'success');
  }
  renderRun(); if (completedWafers === 3) one('#run-reset').focus({preventScroll: true});
});
one('#run-reset').addEventListener('click', () => {
  completedWafers = 0; processing = false; runEvents = []; one('#recipe-choice').value = 'ETCH-DEMO/v2'; renderRun();
  feedback('#run-feedback', '已重設：三片都在 F012 原槽位，CH-A 空閒，S20 尚未開始。可以再試錯誤配方或另一版本。');
});

let holdReleased = false;
function renderHold() {
  one('#hold-status').textContent = holdReleased ? 'Ready · 本例允許準備開工' : 'Hold · 暫停';
  one('#hold-status').classList.toggle('amber', !holdReleased); one('#hold-status').classList.toggle('good', holdReleased);
  one('#hold-permission').textContent = holdReleased ? '本次 Hold 已解除，仍需其他開工條件' : '不可開始下一站';
}
one('#hold-start').addEventListener('click', () => {
  feedback('#hold-feedback', holdReleased ? '本次 Hold 已依模擬複核結果解除。可以進行其他開工確認，但此按鈕只檢查資格，不啟動加工。W07 仍在 F012／07。' : '不可開工。ETCH-03 雖然 Idle，L023 仍是 Hold；請先取得符合條件的複核結果。不要因設備有空就忽略批次管制。', holdReleased ? 'success' : 'problem');
});
one('#hold-apply').addEventListener('click', () => {
  const decision = one('#review-choice').value;
  holdReleased = decision === 'approved';
  one('#hold-review').textContent = decision === 'approved' ? '已確認符合條件，允許解除' : decision === 'more' ? '需要更多資料，尚未允許解除' : '尚未完成';
  renderHold();
  feedback('#hold-feedback', holdReleased ? '模擬複核允許解除，本次 Hold 已解除。改變的是作業管制狀態，沒有搬動 F012，也沒有改變 W07 的 Lot L023。' : '目前複核仍未允許解除，L023 維持 Hold；身分與位置不變。', holdReleased ? 'success' : 'problem');
});
one('#hold-reset').addEventListener('click', () => {
  holdReleased = false; one('#review-choice').value = 'pending'; one('#hold-review').textContent = '尚未確認'; renderHold();
  feedback('#hold-feedback', '已重設：L023 是 Hold，設備 Idle，W07 仍在 F012／07。先試著檢查能否開工。');
});

let scanMode = 'missing';
function observedMap() { return ['W06', scanMode === 'missing' ? null : scanMode === 'wrong' ? 'W99' : 'W07', 'W08']; }
function renderMap() {
  const observed = observedMap();
  one('#map-count').textContent = `預期 3 片／讀取 ${observed.filter(Boolean).length} 片`;
  one('#map-count').classList.toggle('amber', scanMode !== 'matched');
  one('#map-count').classList.toggle('good', scanMode === 'matched');
  one('#map-rows').innerHTML = runMembers.map((expected, index) => {
    const matches = expected.id === observed[index];
    return `<div class="map-row ${matches ? '' : 'problem'}" role="row"><span role="cell">${expected.slot}</span><span role="cell"><span class="mini-wafer">${expected.id}</span></span><span role="cell">${observed[index] ? `<span class="mini-wafer">${observed[index]}</span>` : '空槽'}</span><span role="cell">${matches ? '相符' : observed[index] ? '身分不同' : '缺少讀取'}</span></div>`;
  }).join('');
}
one('#scan-apply').addEventListener('click', () => {
  scanMode = one('#scan-choice').value; renderMap();
  one('#map-decision').textContent = '核對狀態：資料已更新，需重新核對；尚未放行';
  feedback('#map-feedback', scanMode === 'matched' ? '這次讀取三片與位置均符合預期。現在再按核對，確認本情境的槽位條件。' : scanMode === 'wrong' ? '這次也讀到三片，但 Slot 07 是 W99，預期應為 W07。片數一致仍有身分差異。' : 'Slot 07 又讀為空槽。原本的放行判斷不能沿用，需依這次結果重新核對。');
});
one('#map-validate').addEventListener('click', () => {
  const observed = observedMap();
  const match = runMembers.every((member, index) => member.id === observed[index]);
  one('#map-decision').textContent = match ? '核對狀態：三片身分與槽位相符，可進行下一項開工確認' : '核對狀態：不相符，暫不放行，等待核對';
  feedback('#map-feedback', match ? '本次三個槽位都與預期相符，通過這一項核對；還不能把它當成所有開工條件都通過。預期的 W06／W07／W08 沒有被改寫。' : 'Slot 07 的讀取與預期不同，暫不放行。先核對實物與資料來源，不直接把預期 W07 刪除或改成 W99，也不推論是晶圓品質不良。', match ? 'success' : 'problem');
});
one('#map-reset').addEventListener('click', () => {
  scanMode = 'missing'; one('#scan-choice').value = 'missing'; renderMap();
  one('#map-decision').textContent = '核對狀態：待確認，尚未放行';
  feedback('#map-feedback', '已重設：預期三片，本次讀取兩片，Slot 07 顯示空槽。');
});

renderArrival(); renderRun(); renderHold(); renderMap(); showChapter();
