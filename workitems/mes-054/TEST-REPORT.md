# MES-054 功能與教材一致性驗證

日期：2026-09-13。功能測試已執行；下列通過代表實際瀏覽器操作與載入檢查，不代表真人學習效果。

## 實際結果

| 程式 | 結果 | 實際證據 |
|---|---|---|
| `python workitems/mes-054/check.py` | 244/244 通過 | `tests/evidence/mes-054/verification.json`；228 次頁面/深鏈載入，另含首頁轉址、ER 五類實點與鍵盤操作 |
| `python workitems/mes-054/check_lab.py` | 132 個可達情境狀態通過 | `tests/evidence/mes-054/lab/states.json` 及同目錄每狀態截圖；六個設備情境與十個 Flow 情境，桌機/手機 |
| `python workitems/mes-054/check_journeys.py` | 12 條往返/保存檢查通過 | `tests/evidence/mes-054/journeys.json`；兩尺寸各六項流程 |
| `python workitems/mes-054/capture_views.py` | 已產生代表首屏與修正後 Flow 終點證據 | `tests/evidence/mes-054/views`；首頁、單元3、任務、PART 主題各兩尺寸，另有 Flow 終點 |

所有新主題入口、十單元、五任務、三角色路線、導師入口、catalog 的閱讀深鏈與代表舊入口已載入檢查；無 JavaScript 錯誤、資產 HTTP 錯誤、破圖或大於 2px 的整頁水平溢出。圖內可滾动區域不被誤當整頁溢出。

實際往返包含：mainpd_id 搜尋 → PART → 圖片放大/Escape → ER 對應節點 → 原主題 → 搜尋來源；任務改寫對象/時間 → Lot 狀態主題 → 返回保持輸入；operations/flow/freshness 的下一步按新課綱前進；單元瀏覽不自動答題，作答後重新整理仍保存結果。

首次全面執行有 16 個測試假設失敗，已修正後完整重跑：同頁 hash 跳轉不會產生新的 HTTP response；Lot/FOUP 採互動圖後不以舊圖片標題檢查選取；鍵盤啟動頁面連結會重載且焦點可回 body。最終檢查分別驗證同文件導航、實際選中主題、連結目標 URL，沒有降低圖片/錯誤/溢出檢查。

## 範圍

- `check.py`：首頁相容转址、十單元、獨立主題全集、任務深鏈、舊教材入口；桌機 1440 與手機 390；頁面錯誤、HTTP/圖片載入、整頁溢出；ER 五類節點真實滑鼠/觸控點選；鍵盤導覽。
- `check_lab.py`：設備六情境與 Flow 十情境，對每個可到達節點從起點以真實按鈕重播，留存實際可見狀態與截圖。此項為操作/版面證據，不代表逐張圖片已通過教學品質評分。
- 已補驗：課末往下一步、任務/課程 → 主題 → ER → 返回來源、搜尋與圖片放大、瀏覽紀錄不自動視為作答。

## 舊內容一致性發現（已回報主實作者）

| 位置 | 原文字/風險 | 修正方向 |
|---|---|---|
| `data-map.js` WIP 案例 | 星期一 07:20；以在製批次描述 KER_WIP_Y_BTH | 每天 07:20 機群狀況與 KPI 快照；不自行推定 KER_WIP_BT 頻率 |
| `course.js`、`course-remake.js`、`scenarios.js` Flow 結束 | Finished 未顯式區分實際 Lot E | 限定本教學路徑完成，並明示不是 Lot E 已出貨 |
| `support.js` Move | 「過站成立」容易與完成後推進混淆 | 明示本廠每次 Lot 進機記一筆；保留去重示例及未知真實事件鍵 |
| `support.js` 末段 | AVL/Eff/Lost/Up 全列未確認 | AVL 期間 Availability、機台 Lost 閒置/UP 加工已確認；保留 EFF 公式與彙總等未知 |
| `freshness.js` 末頁 | 回到開頭循環 | 新導覽接續下一單元，重讀另列 |
| `advanced.js` QTime Move In/Out | 事件詞與 Move KPI 同名語境風險 | 保留規則示例的起訖事件，不用全域替換把 QTime 規則誤改 |

## 證據邊界

已實看首頁、單元3、任務與 PART 主題的代表桌機/手機首屏，以及修改後手機 Flow 終點。可讀文字、來源與操作未見遮擋；手機首頁標題末字換行曾回報主實作者作細化。全部 132 狀態均已實際以按鈕到達並留圖，但未逐張人工評分；不能用這些截圖數宣稱所有教學插圖品質達標。

不將自動測試通過當成真人試讀成功。新入口與功能的可操作性、資料語意一致性、實際學習成效分開記錄；沒有看過的截圖不填品質分數。原圖/SVG/schema 未在本測試工作中改動。
