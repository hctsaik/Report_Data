# MES-008：資料新鮮度重新製作

使用者再次指出新鮮度品質低落；沿用已授權製作，不另加批准步驟。範圍 freshness.html 的 architecture、decision、ai、history、join、contract 六節。前三課不改。

## 基線與撤回

baseline/ 保存啟用的 HTML/CSS/JS、MES-007 REVIEW 與 manifest。MES-007 新鮮度頁面 92–96 分、原生圖 93–95 分不再作通過依據；原始檔保留歷史。功能測試結果不撤回，但只能證明介面功能。

實看 examples/fab-physical-data-v01.png 與 tests/evidence/mes-007/freshness-architecture-1440-art.png。第一課有設備、可追蹤放大、記錄一一對應；新鮮度主圖僅方塊加術語，Inline 下方大量空白，最重要的時間落差沒有對應現場。這是上輪已知問題未落實修正，不是再調顏色可解決。

## 製作前學習

1. 用同一 Lot 的現場位置、帶時間的來源快照、工程決定建立視覺證據。架構與精確數值使用原生標註，工作情境使用影像生成；工具選擇不構成品質證據。
2. 每節主圖只講一個問題，3–4 個主要節點；主圖後讓讀者操作一個變數，看資料／決策是否改變。參考資料另外收進可展開區，不堆成第二張文字海報。
3. 手機使用可獨立閱讀的直向圖，不把寬圖縮至文字不可讀；按真實頁面截圖重新判讀。
4. 先做 AI 案例原型並檢查全部文字、Lot 身分、來源與時間，再展開其餘。不以清晰的 PNG 或功能 PASS 直接給高分。

## 有效規則與來源

CLAUDE.md、IMAGE_STYLE_GUIDE.md、TEACHING_WEBPAGE_GUIDE.md、TEACHING_SCORING_RUBRIC.md v1.0、TEACHING_REVIEW_LOG.md；teaching-review-cycle G0–G6 與 imagegen。原文 workitems/mes-007/source-freshness.txt 與 openspec/changes/data-freshness/spec.md。內部延遲為使用者給的通常值，不是外部通用 SLA。

## 分項 brief（生成前）

共同受眾：Fab 初學工程師。共同風格：實看第一課的白底、實物／記錄相連、深藍短標題、唯一淡黃 #FFF4CC 結論。短標籤繁中。圖為假設教學示意，不是實際 MES 畫面或 AI 實測；不添加人像、機器人或裝飾設備。桌面約 1050px 圖寬，手機約 320px；分別檢視。

| 頁／版型／節點 | 核心理解與工作問題 | 輸入、固定身分、方法與改變 | 可見證據與下一步 | 構圖、關係、必要字數／風險 |
|---|---|---|---|---|
| ai / D / 3 | AI 發現異常後，舊 Step 會引導錯誤決策 | 同一 A123；10:01 查詢固定；現場 ETCH，Mart DEV@09:51、Native ETCH@10:00 | 現場設備與兩份帶時間記錄對照，10 與 1 分鐘差；監看驗時間、控制 TX 重驗 | 左現場、右同入口上下快照；線是快照對應不是流程；原型先製作，確認 Lot 不是 FOUP ID |
| architecture / C / 3 | Giga 是入口，不能用入口推斷 freshness | MMDB → Reporting → Giga 的 Native / Mart；另分 Inline 與 TX；Mart 多來源整理 | 同 Giga 視窗兩種來源與兩種時間，追來源路徑；當下要求經 TX | 來源／處理路徑／查詢輸出三區；資料箭頭不得把 TX 接到 Reporting；Inline 不猜延遲 |
| decision / D / 3 | 容許延遲取決於你要做的事 | 同 A123，昨日統計／允許3分監看／當下控制三需求 | 聚合歷史、目前位置快照、交易重驗各可見；按需求選 Mart / Native / TX | 三種工作對照而非三個名詞框；RT2/1/0 不畫成品質排行榜；只有通常延遲 |
| history / D / 3 | 歷史事件不等於目前位置，缺紀錄還要看收齊沒 | 昨日14:20 DEV Move Out 與今日10:01 ETCH；事件保留；涵蓋14:00時尚未收錄 | 事件帳本、Lot前進、當下快照；回答經過或現在，未收齊不得答沒經過 | 同一 A123 的旅程與帳本相連；圖中昨天／今天明確，不能把昨日14:20誤畫今日未來 |
| join / C / 3 | 重新載入不能讓上游舊欄位变新 | A123 Step ETCH@10:00 與 Hold N@09:51 合併；loaded_at 10:00→10:01 | 兩條來源線逐欄對應到一列；刷新章變新、Hold來源章不變；不可據此認定當下無Hold | 來源／合併／刷新對照；資料時間與表載入時間用不同標籤，線不交叉；不捏造真實Hold狀態 |
| contract / C / 3 | 把來源時間與用途一起交給下一位工程師 | 同一 LOT_PROCESS_SUMMARY，來源時間不明→逐欄lineage→有條件用途 | 有來源欄的資料契約與可追查時間；分析可用，控制要核准交易 | 查詢記錄／契約放大／接手動作；不得把填契約自動當成即時，名稱明示示例 |

驗證：六頁桌面／手機、所有互動狀態、圖片載入與放大、鍵盤、HTTP／disk 一致、原文架構與時間演算。逐頁逐圖證據另記 REVIEW.md；作者評比、技術驗證、使用者審閱分開。user_acceptance: pending。

## 實作與驗證結果

六節、12張主圖（六桌面／六手機）、六互動區、六題18項回饋及契約下載已接回網頁。先經AI原型，再逐張檢查與修正。桌面1440、平板800、手機360共18版面及190操作通過；手機實看發現過小標籤後再重製兩圖並重跑。見 REVIEW.md、review.json、evidence-manifest.json。使用者審閱pending，沒有真人學習測試。
