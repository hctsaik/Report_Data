# Fab 基礎與現場情境：MES 入門教學

為只有最基本 Fab 知識的讀者製作的兩課教材。第一課認識 Wafer、FOUP、Slot、Lot；第二課介紹設備、流程與狀態，並提供四個互動情境。

## 開啟

直接用瀏覽器開啟 `index.html` 即可，無需安裝套件或連線。也可以在本目錄執行：

```powershell
python -m http.server 4175 --bind 127.0.0.1
```

再開啟 <http://127.0.0.1:4175/>。`#explore` 可直接進入互動，`#check` 是理解自測。

第二課：<http://127.0.0.1:4175/operations.html>，也可直接開啟本機 `operations.html`。第一課的目錄與頁尾都有第二課入口，兩課可互相返回。

## 第二課與四個情境

基本介紹：Tool／Equipment、Load Port、Chamber、Route／Step、Recipe、AMHS／OHT／Stocker，以及加工／Hold 狀態。Track-in／Track-out 在流程的補充說明中介紹，不把管理事件一律等同載具實體移動。

| 入口 | 操作與學習重點 |
|---|---|
| `operations.html#arrival` | 選目的設備與 Port，觀察暫存、搬送途中、已到達；目的地不符就不派送 |
| `operations.html#run` | 選配方及版本，逐片 W06→W07→W08 加工、回槽；三片完成才算本站完成 |
| `operations.html#hold` | 設備空閒但 Lot 被 Hold；模擬複核解除，位置保持不變 |
| `operations.html#reconcile` | 預期／讀取槽位比對；少一片與身分不符都不能直接放行，重新讀取會撤銷舊判斷 |

每個情境獨立起始、可重設；切換章節可保留本次網頁內的操作，再次載入會回到初始狀態。情境沒有連接任何真實設備、MES 或批准程序。

第二課沿用 L023、F012、W06／W07／W08 與 06／07／08。第一課的換載具操作不會改變第二課的獨立初始值。新增 R-DEMO、S10／S20／S30、ETCH-DEMO／v2、STK-01、OHT-01、ETCH-03／LP1／CH-A 皆為教學假設；不提供實際加工參數，也不是完整設備機構圖。

## 教學內容

1. Fab 情境與 MES 的基本角色。
2. Wafer：一片晶圓與晶粒的差別。
3. FOUP：裝載晶圓的實體載具。
4. Slot：特定 FOUP 內的放置位置，包含空槽。
5. Lot：生產批次及其晶圓成員。
6. 選取晶圓與空槽，對照資料；模擬整批換載具與重設。
7. 三個情境自測，提供正誤原因與重答。

大圖支援放大、原始尺寸捲動、Escape 關閉。手機另行重排主線，目錄可展開。所有按鈕可用鍵盤操作。

## 範例契約

所有編號、成員與搬動都是教學假設。L023 的 W06/W07/W08 起初在 F012 的 06/07/08；模擬整批換到 F018 的 02/03/04，Wafer 與 Lot 保持不變。初始空槽是 05/09，搬動後呈現新載具的空槽 01/05。畫面只顯示局部五槽，不代表 FOUP 全容量；操作不連接 MES，也不模擬實際設備安全程序。

原實物圖 `examples/fab-physical-data-v01.png` 是既有 AI 生成示意，不是現場照片；圖為搬動前固定快照，不會因互動而變動。HTML/CSS 圖形描述教學關係，不作設備尺寸或槽位方向規格。來源連結集中於頁面最後一段；閱讀方式參考使用者指定的 Vision AI DefectFill 頁面。

## 維護與驗證

- `index.html`：教材、章節與來源。
- `styles.css`：桌面與手機樣式、原生物件示意。
- `app.js`：導覽、狀態模型、互動、自測、圖像放大。
- `operations.html`：第二課教材、四個情境、詞彙與來源。
- `operations.js`：第二課導覽與四組獨立狀態；原生設備示意。
- `operations.css`：第二課設備／搬送／製程與核對圖，含手機重排。
- `WORKITEMS.md`：計畫、範圍、驗收與接續。
- `TEACHING_REVIEW_LOG.md`：本輪檢查與審閱狀態。

開發驗證需要 Python Playwright 及 Chromium：

```powershell
python -X utf8 tests/check_lesson.py
python -X utf8 tests/check_operations.py
```

第二課測試的 HTTP 檢查需要先啟動 4175 預覽。結果與 1440／390／360 像素寬截圖存於 `tests/evidence/`；第二課另有 900／768 寬版面檢查，證據在 `tests/evidence/operations-v01/`。這些是技術／視覺審閱證據；不代表真人學習成效或使用者驗收。網站尚未公開發布。
