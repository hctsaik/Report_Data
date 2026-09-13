# MES-028 閱讀導航與返回

右側新增「返回：上一個檢視名稱」、「回到 ER 全圖」及可點選的最近瀏覽路徑。放大關聯圖內也有返回，關閉按鈕明示回圖與說明；關係分頁改稱第N組。

切換主詞、路徑或框選時保存主詞／模式、關係分組、逐點位置、原圖viewBox、捲動及說明開合。相同檢視不重複入歷史，frameEntity內部overview不多入一筆。與瀏覽器上一頁／下一頁及重新整理同步；直接深連結沒有假上一頁，可回全圖。

從ER到index、operations、flow、advanced、support、data-map、freshness保留來源；目的頁提供「返回ER：主詞」。跨頁返回帶回原歷程，仍能繼續返回上一主詞。跨頁狀態限目前瀏覽器session；無儲存權限時不宣稱跨頁精確恢復。

## 驗證

`python workitems/mes-028/check.py` 通過，1440／390：
- WPH點LR再返回，圖文同步。
- Lot第2組點另一主詞再返回，恢復組別及viewBox。
- 右側展開→單圖放大→切換→返回；Escape逐層關閉。
- QTime教材往返保留主詞及歷程；browser forward、reload、back保留組別。
- QTime路徑逐點→預派→返回，恢復逐點位置與縮放。
- 無JS error／橫向溢出。

回歸MES-026全121節點／18路徑、MES-027預派四方向均通過。跨頁agent另測七頁手機。手機導航實際截圖已檢視，返回與全圖可見，瀏覽路徑分行；證據tests/evidence/mes-028。Multi-agent報告見MULTI_AGENT_REVIEW.md。

未為全站所有舊版頁面做逐頁品質評分；本輪涵蓋現行ER及七個主要目的頁。使用者審閱pending。一次性integrate.py勿重跑。
