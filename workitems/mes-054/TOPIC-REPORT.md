# MES-054 獨立主題教材

## 變更

- 新增 `topic.html?topic=<key>`、`topic.js`、`topic.css`，46 個既有主題可直接閱讀。`retired` 與 `portdata` 保留撤下原因，不列入課程。
- 將原 `er-atlas.js` 中的基礎教學定義移至 `er-teaching-base.js`。獨立頁與 ER 檢視器共享同一組基礎與 topic registry，沒有複製另一套廠內定義。
- 主題頁提供所屬單元、返回學習、桌機／手機專屬圖與原尺寸放大、延伸教材、每個來源 reference 的 ER 深連結與原圖入口。
- Lot、FOUP、裝載仍使用同一份 25 槽互動模組；MCS 保留四個時間位置事件互動，沒有拿靜態 FOUP 圖代替。
- 原「上方 ER」「下方示例」改為與頁面位置無關的說法；其餘沿用已確認的教材內容。

## 驗證

`python workitems/mes-054/check_topics.py`：92 個主題頁（46 × 1440／390）通過。檢查共用標題與定義一致、每張圖片實際載入、放大使用正確 responsive 圖、Lot 情境切換及第25槽歸屬、MCS終點事件、無橫向溢出、ER 能載入。

`python workitems/mes-052/check.py`：四主題、八引用、雙尺寸搜尋及放大回歸通過。

截圖：`tests/evidence/mes-054/topics/`。人工實看 Lot 桌面與 QTime 手機代表頁，文字、互動與圖片可讀；其他頁有機械驗證與截圖，未逐頁人工評分。不用功能 PASS 宣稱全部插圖品質或真人學習效果已驗收。

全站 shell 與 catalog 整合後已重跑 `check_topics.py`，92 頁全部通過並刷新截圖；另以 `check_topic_shell.py` 實際點擊 QTime → ER → 返回 QTime → 單元5，在桌機／手機均通過，確認頁首課程位置、頁尾前後教材与單元一致。實看整合後 QTime 桌面與 MCS 手機全頁，未見遮擋或橫向溢出。整體課綱驗證由主代理處理；使用者審閱 pending。

`extract_teaching.py` 為已執行的一次性搬移腳本，不重跑。
