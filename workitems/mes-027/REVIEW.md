# MES-027 預派目標修正

使用者指出小圖「預派機台」右端的 FOUP 應是機台。原因是原始模型有預派—FOUP及預派—EQP兩条邊，遍歷時兩端都成為預派目標。

已在小圖鄰接關係中雙向撤下預派—FOUP；Lot 主詞只產生一條 Lot—預派—EQP 支線。預派主詞只顯示 Lot 與機台兩端。FOUP 仍透過正確 FRCAST_LOT 裝載關係連 Lot，沒有將 FRCAST 改名偽裝成設備表。原始模型及主 SVG 留作來源追溯。

驗證 `python workitems/mes-027/check.py` 通過：1440／390，真實搜尋點選 Lot、預派、FOUP、EQP 四個方向，檢查無錯誤支線、無重複預派目標、裝載關係保留、放大圖正確、無 JS error。桌面預派截圖已實際檢視，機台表為 Siview.freqp／EQP。證據 tests/evidence/mes-027。使用者審閱 pending。

前版 MES-023「預派根節點含三端」的舊期望已被本輪使用者校正取代；不以舊測試要求保留錯誤 FOUP 支線。快取版本 er-focus.js?v=27。
