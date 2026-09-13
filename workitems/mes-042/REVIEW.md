# MES-042 未來的 Flow

使用者確認 Lot forecast 同樣透過 Flow 與 IE 站點 WPH 計算後續到站。已為 forecast 實體及關係製作專屬內容，保留 F12dm.dm_tbl_lot_forecast 與 Lot_ID／OPE_NO。未沿用僅適用前題 Stream 的 LDS 替代標記。

桌面 lot-forecast-v2.png 修正首稿累計文字及把 Lot 畫成設備的問題；手機 lot-forecast-mobile-v1.png 使用文件卡呈現批次。兩輸入明示 Flow 站序和 WPH 耗時估算。無虛構精確預測值；正文區分速率、耗時、預計到站、加工完成。生成圖與 1440/390 實際頁面截圖均已目視檢查，細字有放大入口；未自動評分，使用者審閱 pending。

python workitems/mes-042/check.py 通過：兩引用、搜尋點擊/觸控、雙尺寸資產與放大、無 JS error、不誤標 LDS。證據 tests/evidence/mes-042。integrate.py 一次性不重跑。
