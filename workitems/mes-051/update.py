from pathlib import Path
p=Path('er-atlas.html');p.write_text(p.read_text(encoding='utf-8').replace('er-topic-content.js?v=50','er-topic-content.js?v=51'),encoding='utf-8')
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-051 廠內定義補充\n\nBMIR：OHB 空時呼叫 RTD 計算下一批上架貨。Port UP有貨/LOST無貨。Lot R加工中/Q等待/H待確認/B長期暫置/E已出貨。KER_WIP_Y_BTH每天07:20機群與KPI快照（取代每週一）。FRPORT_UDATA撤下教學文字，原ER保留。文字已更新，尚未新增這些主題插圖。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
