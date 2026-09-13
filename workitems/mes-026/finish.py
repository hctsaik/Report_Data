from pathlib import Path
intro='''# 最新接續：MES-026 主詞教材不可套 FOUP

已修節點與18閱讀路徑的配對，121節點明確映射；Future Hold／QTime各有專屬圖文，其他主題按語意介紹，未配對不得回退FOUP。Future Hold手機直向圖 assets/mes-026。讀 workitems/mes-026/REVIEW.md，驗證 python workitems/mes-026/check.py。品質未自動評分，使用者審閱pending；不是每個主題都有新插畫。一次性integrate.py不重跑。

'''
for name in ['AGENTS.md','WORKITEMS.md']:
 p=Path(name);p.write_text(intro+p.read_text(encoding='utf-8'),encoding='utf-8')
p=Path('TEACHING_REVIEW_LOG.md');p.write_text(p.read_text(encoding='utf-8')+'''

## MES-026｜全面移除不相關FOUP教材fallback

使用者指出多個主題借用FOUP。之前逐一修QTime等仍不足，根因在未知節點fallback和route手動錯配。改為明確來源映射，Future Hold與QTime分開教；其他主題各自解釋意義、步驟與限制。未知內容不虛構，沒有合適圖片不借別題補滿。121節點與18路徑配對檢查不代表每份教材品質通過。手機Future Hold實看橫圖過小，重排直向並重驗。詳workitems/mes-026/REVIEW.md；使用者審閱pending。
''',encoding='utf-8')
