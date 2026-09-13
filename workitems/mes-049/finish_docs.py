from pathlib import Path
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text('# MES-049 OHB\n\nOHB 為機台鄰近 FOUP 暫置架，遠端 Stocker 先搬至鄰近暫放以方便後續快速搬運。雙尺寸圖文及設定/狀況四引用已更新，BMIR 分離。讀 workitems/mes-049/REVIEW.md；驗證 python workitems/mes-049/check.py。使用者審閱 pending。\n\n'+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## MES-049 OHB\n機台附近簡易 FOUP 暫置架，Stocker/OHB/OHT角色分清。兩尺寸圖文實看與功能驗證通過。詳 workitems/mes-049/REVIEW.md。\n',encoding='utf-8')
p=Path('openspec/changes/er-subject-focus/spec.md');p.write_text(p.read_text(encoding='utf-8')+'\n- MES-049：OHB（Over Head Buffer）為機台附近簡易 FOUP 暫置架，方便從遠端倉儲預先就近暫放並於後續搬運；區分對應設定與狀況資料。\n',encoding='utf-8')
