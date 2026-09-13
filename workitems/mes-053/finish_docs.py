from pathlib import Path
entry='''# MES-053 全站架構四角色審查

使用者要求 Multi-agent 以新手工程師、Data Scientist、現場工程師、導師完整審查網站並寫Markdown。已完成，主文件 workitems/mes-053/DESIGN-RECOMMENDATIONS.md，逐項映射 CONTENT-MAP.md，四份ROLE報告及REVIEW.md。十入口雙尺寸載入，代表首屏實看；課末循環與ER返回往返實測見 tests/evidence/mes-053。建議循序/任務/ER三入口共用內容，先做Lot未進機原型。本輪只審查與文件，網站未重構，真人學習效果未驗證。設計審閱pending，不把建議當實作完成；一次性finish_docs.py不重跑。

'''
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text(entry+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md')
p.write_text(p.read_text(encoding='utf-8')+'\n\n'+entry+'觀察：內容增補與導覽注入造成課綱不連貫。原則：審查最終呈現，分清課程順序、瀏覽歷程與ER逐點路徑；主題覆蓋不能代替能力覆蓋。下一輪驗證：使用同一個跨課任務測深連結、來源返回、狀態恢復及學員解釋。\n',encoding='utf-8')
