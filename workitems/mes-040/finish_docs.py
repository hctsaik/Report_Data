from pathlib import Path
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-040 Product Hold\n\nPID 依產品與站點設定管制，同產品 Lot 各自到站暫置以便統一處理。專屬桌面／手機圖文已更新。讀 workitems/mes-040/REVIEW.md；驗證 python workitems/mes-040/check.py。使用者審閱 pending。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## MES-040 Product Hold\n產品與站點條件套用到同產品各 Lot 的到站事件。專屬雙尺寸圖文與頁面已實看，搜尋及放大驗證通過；未自動評品質。詳 workitems/mes-040/REVIEW.md。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n- MES-040：Product Hold 說明 PID 設定產品與站點條件，同產品 Lot 各自到站暫置、等待統一處理，保留來源 Lot_ID 關係與專屬雙尺寸插圖。\n',encoding='utf-8')
