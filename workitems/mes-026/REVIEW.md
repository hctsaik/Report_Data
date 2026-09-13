# MES-026 主詞介紹配對修正

使用者指出 QTime／Future Hold 等節點仍套用 FOUP 總覽。原因包含未知節點 fallback，以及 route() 的手動錯配。

已新增 er-topic-content.js 明確來源映射，121 個節點都有对应主題或原圖校正說明；18 條閱讀路徑同步修正。禁止未知節點回退 FOUP；未来新節點沒有教材時，以自身名稱、直接關係及待確認範圍說明，隱藏圖片和失效連結。

Future Hold 使用專屬桌面圖與新手機直向圖；QTime 保留自己的起算／停止事件圖文。其餘新增主題以專屬意義、閱讀步驟及判讀限制呈現，**不是每個主題都已新增插畫**。Lot／FOUP／EQP 明確對應的實物教材與全圖總覽保留。原圖待校正的 2672:cast-link 明示錯誤，不能當正確查詢路徑。

## 證據

- `python workitems/mes-026/check.py`：121 節點、18 路徑，無 console error。全部配對記錄在 tests/evidence/mes-026/teaching-audit.json。
- 1440／390：真實滑鼠／觸控點原 ER 的 Lot、FOUP、EQP、Flow、Recipe、Future Hold、QTime；拖曳不誤選。搜尋兩個 Future Hold 節點、QTime、OEE；圖片放大、手機 currentSrc、右側展開、切回 Lot 清除專屬文字均通過。
- 回歸 MES-020、023、025 通過。
- 舊 MES-016 檢查在拖曳後斷言舊總覽標題「完整 ER × 現場物件」失敗；目前既有標題是「完整 ER × 主詞聚焦」。沒有改舊測試或倒退標題；本輪 check.py 改以拖曳前後標題保持相同驗證，七類真實點擊於兩尺寸均通過。

實際檢視 Future Hold 桌面展開、手機說明及 OEE 桌面說明截圖。手機首版橫圖過小，重排直向後重新擷取並檢視，三階段文字可辨、同 Lot 與站點順序保持。QTime 功能回歸通过。未逐頁評教學分數，使用者審閱 pending，不能以121配對通過宣稱121份教材品質達標。

新圖：assets/mes-026/future-mobile-v1.png；來源參考 assets/mes-009/future.png。圖內為教學示例。生成工具 imagegen，原輸出 exec-e7fef55d-eddd-46f3-9f97-b8d0e2c7bdb5.png；提示摘要：三段直向，同 Lot L023，S20 登記 S50 進站前 Hold → S40 途中未觸發 → S50 進站前有效 Hold／等待覆核；白底藍框、具體現場、黃色 takeaway；不增加 QTime 計時或自動解除。桌面原圖未覆寫。

一次性 integrate.py 不可重跑。正式入口 er-atlas.html，快取版號26。
