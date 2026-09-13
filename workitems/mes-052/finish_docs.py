from pathlib import Path

entry='''# MES-052 四主題八張教學圖

BMIR、Port UP／LOST、Lot RQHBE、KER_WIP_Y_BTH 每日07:20快照，已補專屬桌機／手機圖。每日快照路徑與執行時圖面標籤已修正，原始ER保留。FRPORT_UDATA維持撤下教學。讀 workitems/mes-052/REVIEW.md；驗證 python workitems/mes-052/check.py，KER回歸 python workitems/mes-050/check.py。證據 tests/evidence/mes-052；使用者審閱 pending。一次性 integrate.py、fix_snapshot.py、finish_docs.py 不重跑。

'''
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text(entry+p.read_text(encoding='utf-8'),encoding='utf-8')
for name in ['TEACHING_REVIEW_LOG.md','openspec/changes/er-subject-focus/spec.md']:
 p=Path(name);p.write_text(p.read_text(encoding='utf-8')+'\n\n'+entry,encoding='utf-8')
