from pathlib import Path
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-042 未來的 Flow\n\nLot forecast 專屬圖文已補：Flow 站序加 IE WPH 耗時估算，逐站預計到站。未套用 Stream 的 LDS 替代標記。讀 workitems/mes-042/REVIEW.md；驗證 python workitems/mes-042/check.py。使用者審閱 pending。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## MES-042 Lot forecast\n專屬雙尺寸圖文，桌面修正累計文字及 Lot 物件表徵。兩尺寸網頁實看，搜尋、放大驗證通過；無自動品質評分。詳 workitems/mes-042/REVIEW.md。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n- MES-042：Lot forecast 圖文依 Flow 站序與 IE WPH 預估後續各站到站時間，保留 Lot_ID／OPE_NO 上下文，不沿用 Stream 的替代註記。\n',encoding='utf-8')
