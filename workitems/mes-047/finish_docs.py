from pathlib import Path
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-047 機群與課別\n\nMFG_EQP_OWNER_BT 專屬圖文已補：由機台查機群、管理單位及廠商名稱。owner 映射與一般 group 分開。讀 workitems/mes-047/REVIEW.md；驗證 python workitems/mes-047/check.py。使用者審閱 pending。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## MES-047 機群與課別\n由機台查管理歸屬及廠商資訊，雙尺寸實看與功能驗證通過。詳 workitems/mes-047/REVIEW.md。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n- MES-047：MFG_EQP_OWNER_BT 透過 EQP_ID 查機台管理單位、機群名稱與廠商資訊；專屬圖文區分管理歸屬與廠商。\n',encoding='utf-8')
