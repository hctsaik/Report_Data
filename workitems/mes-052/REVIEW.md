# MES-052 四主題圖文補齊

已更新 er-atlas.html 教學：BMIR、Port UP／LOST、Lot RQHBE、每日 07:20 機群 KPI 快照。每主題各有桌機與手機專屬圖，共八張，位於 assets/mes-052。

## 語意與修正

- BMIR：OHB 空位觸發 RTD 計算下一批貨；使用高架暫置架，選貨結果與實際搬送分開。退回草稿的地面架與錯誤因果箭頭。
- Port：同一 LP1 有 FOUP 為 UP，沒有貨為 LOST。手機圖移除可能混淆的機台狀態面板。
- Lot：R 加工中、Q 等待加工、H 待確認、B 長期暫置、E 已出貨；並列呈現，不畫固定轉換順序。移除草稿未經確認的生命週期結束敘述。
- KER_WIP_Y_BTH：每天早上 07:20 保存機群狀況與 KPI。圖上沒有虛構指標值或公式。路徑及執行時 ER 標籤同步改為每日；原始 ER 檔保留。
- FRPORT_UDATA 保持撤下教學。四主題的教材標題使用確認後的主題名稱，原始來源名稱仍可追溯。

## 驗證

`python workitems/mes-052/check.py` 通過：八個相關來源、四主題在 1440／390 viewport 的實際搜尋點選、專屬圖載入、放大、標題與每日快照文字、無 JavaScript 錯誤。

`python workitems/mes-050/check.py` 通過既有 KER 教學回歸檢查。

逐一查看四主題桌機與手機截圖，共八張，位於 tests/evidence/mes-052。主要圖文完整可讀，沒有借用通用 FOUP 圖。截圖核對後修正教材標題並重新產生證據。圖片為教學示例，非實際廠內資料。未提供量化品質評分，使用者審閱 pending。
