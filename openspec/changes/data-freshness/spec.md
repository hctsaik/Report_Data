# 資料新鮮度教學（MES-007）

## MES-008 重製要求

六節各有與第一課風格對照的教學插畫，手機另排直向構圖；保留原有架構與三案例事實。圖後各一個可檢視資料變化的互動，以及改變條件的自測與有條件回饋。架構路徑選擇、資料來源／用途切換、事件涵蓋範圍、刷新不改上游時間與逐欄契約均須可操作。契約可下載JSON，明示示例、來源時間、loaded_at、queried_at與用途限制。驗證使用 tests/check_freshness_v2.py；MES-007是歷史基線，不用舊高分宣稱新版本合格。

依使用者提供的內部架構：MMDB為線上Source of Truth；一般工程師經Giga做查詢，需當下狀態時經TX。Reporting、Inline、TX是MMDB的分支；同Giga中Native通常<3分鐘，Mart约10分鐘但以實際契約為準。Inline未提供刷新條件，不賦予推測等級。

實作freshness.html六節：architecture、decision、ai、history、join、contract。三個互動例子使用A123：舊DEV與現在ETCH；昨日MoveOut與現在位置；同列Step和Hold的來源時間不同。共用時間語意區分source_data_time、loaded_at、queried_at。

验收：來源／用途切換改變回傳值與判斷；控制分支要求核准交易重驗；事件未收齊不能推論沒發生；整表刷新不能改變未更新上游欄位的來源時間；手機各分支標出源頭；契約全部欄位可讀；沒有真實DB連線。對照來源原文與逐頁評比見workitems/mes-007。

技術證據：tests/check_illustrated.py。作者評比與使用者認可分開記錄。
