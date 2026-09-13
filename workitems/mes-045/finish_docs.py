from pathlib import Path
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-045 SRTS 抽測規則\n\n使用者確認 SRTS 定義 Flow 站點 Sampling rule 與比例，例如 Part 抽檢30%。專屬雙尺寸圖文已更新，不臆測抽樣單位。讀 workitems/mes-045/REVIEW.md；驗證 python workitems/mes-045/check.py。使用者審閱 pending。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## MES-045 SRTS\nFlow 適用站點與 Part 抽測比例專屬圖文。手機修正多餘 CMM 設備類型，雙尺寸頁面實看及功能驗證通過。詳 workitems/mes-045/REVIEW.md。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n- MES-045：SRTS 定義 Flow 站點的 Sampling rule 與 Part 抽測比例，教學以30%示範；抽樣單位及選取方式依規則，不推定為每批晶圓比例。\n',encoding='utf-8')
