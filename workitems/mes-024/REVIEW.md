# MES-024 Lot Step 必須包含 Lot

使用者指出FOUP/Step圖沒有Lot，Lot Step應包含Lot。來源核對：2671:lot — 2672:summary（站點Summary／Lot_id）— 2672:step全部已有原始邊，不需新增推測業務邊。

改動：Lot Step根優先顯示Lot關係，標題改Lot Step歷史；FOUP首條裝載路徑延伸為FOUP — FRCAST_LOT — Lot — 站點Summary — Step歷史，保留中間Lot。沒有恢復MES-018撤下的2672:cast-link假捷徑。新增「這個Lot的Step歷史」路徑入口及subject=lot-step直達。

驗證workitems/mes-024/check.py，證據tests/evidence/mes-024。桌面／手機確認Lot存在、來源每邊成立、FOUP完整鏈、撤回支線仍不出現。使用者審閱pending。
