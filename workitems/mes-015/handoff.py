from pathlib import Path
p=Path('AGENTS.md');s=p.read_text(encoding='utf-8');s=s[s.index('# 最新接續：MES-014'):]
p.write_text('''# 最新接續：MES-015 全圖框選與教學對照

入口維持 integrated-map.html?view=original，轉址 er-atlas.html。初始完整 ER；框選 Lot／FOUP／EQP／Flow／Recipe 主要位置，保留全部線，旁邊同步教學插圖。讀 workitems/mes-015/REVIEW.md。驗證 python workitems/mes-015/check.py。任意節點不可直接以顏色分類推斷教學圖；明確映射，否則顯示基礎參考。原 SVG 不變。使用者審閱 pending。

'''+s,encoding='utf-8')
