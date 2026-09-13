from pathlib import Path
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-043 Recipe Group\n\n群組包含可做類似加工的機台，依產品/加工條件切換多台或單台加工許可。專屬雙尺寸圖文已更新。讀 workitems/mes-043/REVIEW.md；驗證 python workitems/mes-043/check.py。使用者審閱 pending。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## MES-043 Recipe Group\n補足機台群及多台/單台許可控制，雙尺寸圖與網頁實看，功能驗證通過。未自動評分。詳 workitems/mes-043/REVIEW.md。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n- MES-043：Recipe Group 圖文包含機台群、依產品或加工條件控制多台/單台許可，区分設備能力與當前許可，不推定控制優先權。\n',encoding='utf-8')
