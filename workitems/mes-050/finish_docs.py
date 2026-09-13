from pathlib import Path
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-050 KER 圖文已更新\n\n依已確認定義製作分群/SQL/目前與歷史總覽，三主題十二引用同步。讀 workitems/mes-050/REVIEW.md；驗證 python workitems/mes-050/check.py。公式暫不處理，使用者審閱 pending。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('workitems/mes-050/KER-DEFINITIONS.md');p.write_text(p.read_text(encoding='utf-8')+'\n## 後續製作狀態\n使用者已另行授權產生圖文，網站更新與驗證見 REVIEW.md；上方「尚未製作」為當時定義確認階段紀錄。\n',encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## MES-050 KER\n依確認定義製作雙尺寸總覽，各主題專屬文字與來源。十二引用驗證通過，未自動評分。詳 workitems/mes-050/REVIEW.md。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n- MES-050：KER 圖文包含機台多重分群、Chamber 獨立分群、User SQL 虛擬群組、最近一次更新及每小時機台/機群歷史；本輪不展開指標公式。\n',encoding='utf-8')
