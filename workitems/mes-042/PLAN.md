# MES-042 Lot forecast

依使用者確認，F12dm.dm_tbl_lot_forecast 使用 IE 站點 WPH 與 Flow 關係預估未來各站到站時間。製作專屬雙尺寸圖文，Lot 為主詞，Flow 站序與 WPH 耗時估算為兩個輸入，輸出每站預計到站時間。沒有確認此資料也被 LDS 取代，因此不沿用 Stream 的替代標記。

保留 Lot_ID／OPE_NO 原關係。無實際算法時不杜撰精確時間；示例明示，累計到目標站之前的耗時。更新 forecast 內容與資產版本；真實搜尋、兩來源、桌面手機及放大驗證並查看截圖。
