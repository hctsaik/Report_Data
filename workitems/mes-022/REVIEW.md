# MES-022 FOUP 內容物歷史

使用者確認 Siview.fhwlths 是 FOUP 內容物（Wafer）歷史：記錄各時間點這個 FOUP 放了什麼 Wafer，每次 Split／Merge 進 FOUP 時更新。撤回先前只以「在 Slot／晶圓槽位」解釋此表的說法。

計畫及修改：主圖顯示、小圖與維護中主題圖改成「內容物歷史」，原表名保留；節點說明與 slot 路徑說明補入時間及 Split／Merge 更新語意，七圖教學的表格說明一起修正。沒有推定 Split／Merge 是唯一寫入事件，沒有捏造 Wafer表、Join鍵或狀態快照。原始七圖及歷史 model 保存校正前來源；目前頁面載入時套用使用者校正。

原實物參考圖未修改，直接選內容物歷史節點時自動展開說明，圖說標明實物參考不是歷史紀錄或Split／Merge事件示例。讀歷史需指定時間，不能直接当現在內容。

驗證 workitems/mes-022/check.py；證據 tests/evidence/mes-022。使用者審閱pending。

最終1440／390測試PASS：內容物歷史標籤、時間／Wafer／Split／Merge說明、搜尋點選、路徑及先前帶到校正均正常，無JS錯誤。已實看手機history截圖，保留原LOT與FOUP連線作來源關聯，未自行改接不存在的Wafer表。
