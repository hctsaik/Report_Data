from pathlib import Path
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-044 Module／Stage／Step\n\n使用者確認 Module 如黃光，包含多個 Stage，每個 Stage 包含細部 Step。雙尺寸圖文及 Lot 歸屬對照已更新。讀 workitems/mes-044/REVIEW.md；驗證 python workitems/mes-044/check.py。使用者審閱 pending。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('workitems/mes-044/PLAN.md');p.write_text(p.read_text(encoding='utf-8')+'\n## 使用者澄清後的最終計畫\nModule 為黃光等加工模組，包含多個 Stage，每個 Stage 包含細部 Step。此定義取代上方未確認假設；雙尺寸均重畫三層包含框與 Lot 歸屬查詢。\n',encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## MES-044 Module 層級確認\n使用者補充 Module 包含 Stage、Stage 包含 Step，兩尺寸重新生成，不發布未確認版。實際頁面實看與功能驗證通過。詳 workitems/mes-044/REVIEW.md。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n- MES-044：Module（如黃光）包含多個 Stage，每個 Stage 包含細部 Step；專屬圖文用巢狀框表示，Lot 依目前 Step 對照 Stage 與 Module。\n',encoding='utf-8')
