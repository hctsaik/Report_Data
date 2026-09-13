from pathlib import Path
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-041 Stream 到站預估\n\nFlow 站序與 IE WPH 耗時估算的專屬圖文已更新，標明舊功能由 LDS 取代。Stream 與一般 forecast 映射分離。讀 workitems/mes-041/REVIEW.md；驗證 python workitems/mes-041/check.py。使用者審閱 pending。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## MES-041 Stream 到站時間\nFlow 與 IE WPH 雙輸入、累計到站與 LDS 替代註記。桌面首稿修正輸入箭頭與多餘製程名稱；最終兩尺寸圖及實際網頁實看，功能檢查通過，無自動品質評分。詳 workitems/mes-041/REVIEW.md。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n- MES-041：Stream 專屬圖文說明 Flow 站序、IE WPH 速率換算耗時、逐站預估到站，註明由 LDS 取代；一般 forecast 不套用替代註記。\n',encoding='utf-8')
