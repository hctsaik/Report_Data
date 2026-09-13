from pathlib import Path
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-048 Default Stocker\n\n機台預設 Stocker（FOUP 倉儲）專屬雙尺寸圖文已更新，設定與位置/搬送分清。讀 workitems/mes-048/REVIEW.md；驗證 python workitems/mes-048/check.py。使用者審閱 pending。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## MES-048 Default STK\n機台→預設倉儲圖文，虛線表示對應設定，雙尺寸實看與功能驗證通過。詳 workitems/mes-048/REVIEW.md。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n- MES-048：Default STK 為機台預設 Stocker（FOUP 倉儲），圖文以設定對應呈現，不代表實際位置或搬送紀錄。\n',encoding='utf-8')
