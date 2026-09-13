from pathlib import Path
entry='''# MES-054 全站課程架構已實作

入口learning.html；index無錨點轉總覽，旧教材錨點相容。共用catalog十單元/三路線、五現場任務、獨立topic與ER共用定義、統一site-shell導航/來源返回/前後教材/進度。讀workitems/mes-054/REVIEW.md及TEST-REPORT.md。檢查workitems/mes-054/check.py、check_lab.py、check_journeys.py、check_topics.py、check_persistence.py。原ER保留，FRPORT_UDATA不回課綱，Stream歷史註記。244頁面操作、132情境狀態、92主題視圖已驗證；真人學習效果與使用者審閱pending。一次性integrate/refine/extract/finish腳本不重跑。

'''
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text(entry+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n'+entry+'本輪以共用課綱串聯既有圖文，而非再增加孤立圖槽。實作、工具驗證與真人成效分開；缺少真人樣本不影響完成已授權的網站調整，也不能因此假稱試教通過。\n',encoding='utf-8')
p=Path('openspec/changes/mes-learning-architecture/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n## MES054驗證\n\n以上網站能力已實作，證據與限制見workitems/mes-054/REVIEW.md。真人試讀/課程時數未實測；技術與操作驗證不代替學習成效。\n',encoding='utf-8')
