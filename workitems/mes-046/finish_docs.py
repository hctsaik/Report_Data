from pathlib import Path
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-046 PART 與 Flow 版本\n\n產品/PART 對應 Flow，進版時同步記錄版本資訊。專屬雙尺寸圖文已更新。讀 workitems/mes-046/REVIEW.md；驗證 python workitems/mes-046/check.py。使用者審閱 pending。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## MES-046 PART\n產品流程對應及進版記錄專屬图文。首稿移除未授權基數/進版內容假設，雙尺寸實看與功能驗證通過。詳 workitems/mes-046/REVIEW.md。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n- MES-046：PART 對應產品的 Flow/Route，以 Mainpd_id 對照來源；Flow 進版時 PART 同步記錄版本資訊，不推定在製 Lot 自動切版。\n',encoding='utf-8')
