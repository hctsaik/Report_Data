'use strict';

const steps = ['fab', 'wafer', 'foup', 'slot', 'lot', 'explore', 'check'];
const labels = ['先走進 Fab', 'Wafer', 'FOUP', 'Slot', 'Lot', '動手對照', '自測'];
const $ = (selector) => document.querySelector(selector);
let currentStep = 0;
let transferred = false;
let selectedWafer = 'W07';
let selectedSlot = 7;
const members = ['W06', 'W07', 'W08'];

function readStep() {
  const hash = location.hash.slice(1);
  // Accept the familiar Vision AI style URL as well as readable chapter links.
  const slide = Number(new URLSearchParams(hash).get('slide'));
  return steps.includes(hash) ? steps.indexOf(hash) : Number.isInteger(slide) && slide >= 1 && slide <= steps.length ? slide - 1 : 0;
}

function showStep(moveFocus = false) {
  currentStep = readStep();
  document.querySelectorAll('.lesson').forEach((section, index) => { section.hidden = index !== currentStep; });
  document.querySelectorAll('[data-step]').forEach((link, index) => {
    if (index === currentStep) link.setAttribute('aria-current', 'step');
    else link.removeAttribute('aria-current');
  });
  $('#step-count').textContent = `${String(currentStep + 1).padStart(2, '0')} / 07`;
  $('#footer-label').textContent = labels[currentStep];
  $('#previous').disabled = currentStep === 0;
  $('#next').textContent = currentStep === steps.length - 1 ? '回到互動範例 →' : `下一段：${labels[currentStep + 1]} →`;
  $('#sidebar').classList.remove('open');
  $('#menu-toggle').setAttribute('aria-expanded', 'false');
  document.title = `${labels[currentStep]}｜Fab 的四個基本角色`;
  if (moveFocus) { $('#content').focus({preventScroll: true}); window.scrollTo({top: 0, behavior: 'instant'}); }
}

$('#previous').addEventListener('click', () => { if (currentStep > 0) location.hash = steps[currentStep - 1]; });
$('#next').addEventListener('click', () => { location.hash = currentStep === steps.length - 1 ? 'explore' : steps[currentStep + 1]; });
window.addEventListener('hashchange', () => showStep(true));
$('#menu-toggle').addEventListener('click', () => {
  const isOpen = $('#sidebar').classList.toggle('open');
  $('#menu-toggle').setAttribute('aria-expanded', String(isOpen));
});
document.querySelectorAll('[data-step]').forEach(link => link.addEventListener('click', () => {
  if (link.dataset.step === steps[currentStep]) showStep(true);
}));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && $('#sidebar').classList.contains('open')) {
    $('#sidebar').classList.remove('open'); $('#menu-toggle').setAttribute('aria-expanded', 'false'); $('#menu-toggle').focus();
  }
});

function snapshot() {
  const first = transferred ? 2 : 6;
  return { foup: transferred ? 'F018' : 'F012', lot: 'L023', first,
    wafers: members.map((id, index) => ({id, slot: first + index})) };
}

function renderExplorer() {
  const data = snapshot();
  if (selectedWafer) selectedSlot = data.wafers.find(wafer => wafer.id === selectedWafer).slot;
  $('#pod-id').textContent = data.foup;
  const slots = $('#slots');
  slots.replaceChildren();
  for (let slot = data.first + 3; slot >= data.first - 1; slot--) {
    const wafer = data.wafers.find(item => item.slot === slot);
    const chosen = selectedSlot === slot;
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'slot-button'; button.dataset.slot = String(slot);
    button.setAttribute('aria-pressed', String(chosen));
    button.setAttribute('aria-label', `${data.foup} Slot ${String(slot).padStart(2, '0')}，${wafer ? `Wafer ${wafer.id}` : '空槽位'}`);
    // All interpolated values are controlled lesson data, never user input.
    button.innerHTML = `<span>Slot ${String(slot).padStart(2, '0')}</span><span class="${wafer ? 'slot-wafer' : 'empty-label'}">${wafer ? wafer.id : '空槽位'}</span><span class="selected-label">${chosen ? '已選' : ''}</span>`;
    button.addEventListener('click', () => {
      selectedWafer = wafer ? wafer.id : null; selectedSlot = slot;
      renderExplorer(); $(`[data-slot="${slot}"]`).focus({preventScroll: true});
    });
    slots.append(button);
  }
  const slotNumber = String(selectedSlot).padStart(2, '0');
  $('#quick-selection').textContent = selectedWafer ? `${selectedWafer} · ${data.foup}／Slot ${slotNumber} · Lot ${data.lot}` : `${data.foup}／Slot ${slotNumber} · 空槽位，無晶圓或批次`;
  $('#record-title').textContent = selectedWafer ? `Wafer ${selectedWafer}` : `Slot ${slotNumber} · 空槽位`;
  $('#selection-sentence').textContent = selectedWafer ? `${selectedWafer} 現在位於 ${data.foup} 的 Slot ${slotNumber}。` : `${data.foup} 的 Slot ${slotNumber} 目前沒有晶圓。`;
  $('#value-wafer').textContent = selectedWafer || '—';
  $('#value-foup').textContent = data.foup;
  $('#value-slot').textContent = slotNumber;
  $('#value-lot').textContent = selectedWafer ? data.lot : '—';
  $('#record-explanation').textContent = selectedWafer ? '藍底兩列描述位置；Wafer 是晶圓身分，Lot 是批次歸屬。' : 'Slot 是位置，即使沒有晶圓仍然存在。空槽不對應任何 Wafer 或 Lot。';
  $('#transfer').disabled = transferred;
  $('#transfer').textContent = transferred ? '已移到 F018' : '模擬整批換到 F018 →';
}

$('#transfer').addEventListener('click', () => {
  const before = snapshot();
  transferred = true;
  // After moving the lot, follow a physical wafer. An empty slot is not moved.
  const wasEmpty = !selectedWafer;
  if (wasEmpty) selectedWafer = 'W07';
  renderExplorer();
  const oldSlot = before.wafers.find(wafer => wafer.id === selectedWafer).slot;
  $('#transfer-result').textContent = `${wasEmpty ? '空槽位不會被搬走；現在追蹤 W07。' : ''}整批 3 片已移到 F018。${selectedWafer}：F012／${String(oldSlot).padStart(2, '0')} → F018／${String(selectedSlot).padStart(2, '0')}；Wafer 身分與 Lot L023 保持不變。F012 原來的 06、07、08 已空出。`;
  $('#reset').focus({preventScroll: true});
});
$('#reset').addEventListener('click', () => {
  transferred = false; selectedWafer = 'W07'; selectedSlot = 7; renderExplorer();
  $('#transfer-result').textContent = '已重設：W07 位於 F012／07，屬於 L023。';
});

const quizKeys = {
  location: {answer: 'foup', correct: '答對了。每個 FOUP 都可能有 Slot 03；FOUP 編號＋Slot 編號才能指出盒內的位置。', wrong: '再想一下：不同盒子裡都可能有 Slot 03。Lot 說的是批次歸屬，晶圓直徑說的是尺寸，都無法指出哪個盒子。'},
  move: {answer: 'position', correct: '答對了。位置由 F012／07 變成 F018／03；晶圓仍是 W07，批次仍是 L023。', wrong: '請對照搬動前後：改變的是 F012→F018、07→03；W07 和 L023 都保留。單純換位置不必改晶圓身分與批次。'},
  empty: {answer: 'exists', correct: '答對了。Slot 是盒子裡的放置位置；空槽仍有 FOUP 與 Slot 編號，只是沒有 Wafer 與 Lot 可對應。', wrong: '再看看位置與物件的差別：晶圓移走後，盒子的支撐位置仍在，因此 Slot 存在，只是目前空著。'}
};
const quizResults = new Map();
document.querySelectorAll('.quiz').forEach(quiz => {
  quiz.querySelectorAll('.answer').forEach(button => button.addEventListener('click', () => {
    const key = quizKeys[quiz.dataset.quiz];
    const correct = button.dataset.answer === key.answer;
    quizResults.set(quiz.dataset.quiz, correct);
    quiz.querySelectorAll('.answer').forEach(answer => { answer.classList.remove('chosen', 'correct'); answer.setAttribute('aria-pressed', String(answer === button)); });
    button.classList.add(correct ? 'correct' : 'chosen');
    const feedback = quiz.querySelector('.feedback'); feedback.hidden = false;
    feedback.classList.toggle('success', correct); feedback.textContent = correct ? key.correct : key.wrong;
    const count = [...quizResults.values()].filter(Boolean).length;
    $('#quiz-summary').textContent = `已答對 ${count} / 3 題。${count === 3 ? '現在試著用自己的話，說出 W07 的身分、位置與歸屬。' : '可重新選擇；重點是看懂判斷理由。'}`;
  }));
});

const dialog = $('#image-dialog');
let opener = null;
document.querySelectorAll('[data-zoom]').forEach(button => button.addEventListener('click', () => {
  opener = button; $('.zoom-viewport').classList.remove('native'); $('#zoom-size').textContent = '原始尺寸';
  dialog.showModal(); $('#close-dialog').focus();
}));
$('#close-dialog').addEventListener('click', () => dialog.close());
$('#zoom-size').addEventListener('click', () => {
  const native = $('.zoom-viewport').classList.toggle('native');
  $('#zoom-size').textContent = native ? '適合視窗' : '原始尺寸';
});
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
dialog.addEventListener('close', () => { if (opener) opener.focus({preventScroll: true}); });
renderExplorer();
showStep();
