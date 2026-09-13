# MES055：指定頁面的圖文與閱讀版面

本輪修正使用者列出的 12 個不同頁面。location 的兩個網址是同一主題；material 作為第 13 個參考對照頁。已實作，使用者審閱仍待確認，不以功能測試代替美感或學習效果評分。

## 完成內容

- index 的 FOUP／Slot／Lot／Explore 改為寬單欄，移除這四頁的舊側欄與重複課末導覽，使用共同課程前後頁與回單元入口。
- FOUP、Slot、Lot 各有實物圖。Explore 先看實物對照，再操作既有槽位、空槽、整批換盒與重設。
- load 採用 material 的實物與裝載關係圖。25 槽練習改為使用者展開，避免初次閱讀先面對長清單；所有槽位仍可操作。
- flowkey、available、eqpstatus、eqpkey、location、lotstep、contents 各補專屬圖片與三段案例說明；獨立 topic 與 ER 共用更新。
- 新增 10 張正式圖片於 assets/mes-055；material 原圖未改。

## 逐頁核對

| 頁面 | 教學焦點與實際修正 | 桌面／手機 |
|---|---|---|
| index#foup | 容器 F012 與晶圓 W07；門體改為取下 | 已看圖文 |
| index#slot | F012＋07 才是位置；局部三片與空槽 | 已看圖文 |
| index#lot | 三片晶圓共同歸屬 L023；補充單批25片、多批共盒 | 已看圖文 |
| index#explore | 實物→控制面板→位置與身分；保留換盒操作 | 已看圖文、操作檢查 |
| topic load | 實物裝載圖先行，25槽練習可展開 | 已看折疊頁、操作檢查 |
| topic flowkey | Lot→Part→Flow與版本；定義與足跡分開 | 已看圖文 |
| topic available | 兩台候選設備；可用／預派／實際加工區分 | 已看圖文 |
| topic eqpstatus | 同機台兩個時間；加工在Chamber，Port語境分開 | 已看圖文 |
| topic eqpkey | 同設備識別跨資料；多筆關係不等於多台設備 | 已看圖文 |
| topic location | FOUP在Port與Chamber內加工分開 | 已看圖文 |
| topic lotstep | S40→S50→S40；保留再次經過與時間 | 已看圖文 |
| topic contents | 同FOUP兩時間的Wafer名單；Split／Merge更新 | 已看圖文 |
| topic material | 使用者指定參考，原資產保留 | 參考對照 |

圖片與頁面不填自動品質分數。方形主圖在桌面為 988–1036 px 寬、手機為 334–338 px 寬；細字可放大，重要解釋另有 HTML 文字。load 與 material 手機使用原有直式圖。

## 退回的圖稿

設備狀態初稿錯把加工畫進 FOUP，已棄用並以真空腔體剖面重做。FOUP／Slot 初稿有側開鉸鏈門，Lot 初稿槽位順序反向，已修正後才更新正式圖片。資產来源見 assets.json；初稿不部署。

## 驗證與證據

- `python workitems/mes-055/audit.py after`：13頁×桌面1440／手機390，共26視圖；每張圖 currentSrc、CSS寬高、載入狀態及文字見 tests/evidence/mes-055/after/audit.json。before 保留原版對照。
- `python workitems/mes-055/check.py`：149項通過，覆蓋圖片、說明、放大、回單元與前後教材入口、無橫向溢出、無JS錯誤、裝載情境、換盒、空槽及ER共用內容。
- `python workitems/mes-055/regression.py`：92個主題視圖通過，包含共用定義、图片、放大、Lot／MCS互動及ER載入。輸出到本輪目錄，不覆寫MES054歷史截圖。這是功能回歸，不表示重新評估全站美感。

原圖關係、schema、資料鍵未修改。教學ID與時間皆示例；沒有推定未確認的SQL Join條件、Chamber可用性或指標公式。既有失效mesFrom值不當作有效返回紀錄，仍可由回單元及課程順序離開頁面。
