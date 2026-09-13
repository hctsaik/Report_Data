from pathlib import Path
for name,title,body in [('AGENTS.md','MES-039 Move 進機事件','每次 Lot 與機台進機記一筆；每日廠區統計與 DM_MOVE_STEP 按 Lot 追站點。專屬圖文與連結教學同步。讀 workitems/mes-039/REVIEW.md；驗證 python workitems/mes-039/check.py。'),('WORKITEMS.md','MES-039 Move 圖文','專屬圖文已更新，詳 workitems/mes-039/REVIEW.md。使用者審閱 pending。')]:
 p=Path(name);s=p.read_text(encoding='utf-8');p.write_text('# '+title+'\n\n'+body+'\n\n'+s.split('\n\n',2)[2],encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');s=p.read_text(encoding='utf-8').split('\n\n## MES-039 Move')[0];p.write_text(s+'\n\n## MES-039 Move\n進機事件集合分出每日統計與 Lot 站點查詢。兩尺寸修正箭頭來源；網頁驗證與目視檢查見 workitems/mes-039/REVIEW.md。使用者審閱 pending。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');s=p.read_text(encoding='utf-8');s='\n'.join(line for line in s.split('\n') if not line.startswith('- MES-039'));p.write_text(s+'\n- MES-039：Move 每次進機一筆，專屬圖文說明廠區每日統計及依 Lot 查 DM_MOVE_STEP 站點歷程。\n',encoding='utf-8')
