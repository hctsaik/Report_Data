# MES-040 Product Hold 圖文

依使用者定義製作：產品問題由 PID 設定產品與站點條件；同產品 Lot 各自到站暫置，方便統一處理。以 P100、S20、L023/L024 為示例，沒有假造解除條件。原圖 Siview.CSFRPRHold／Lot_ID 關係保留。

桌面 product-hold-v1.png 與手機 product-hold-mobile-v1.png 均為專屬插畫；桌面兩次 S20 表示兩批各自到站的同一站點條件，右側結果不是繼續加工。手機同一 S20 攔住兩批。生成圖及 1440/390 實際頁面截圖已目視檢查；圖內小字可由放大入口閱讀，主標及案例身份可見。未自動評分，使用者審閱 pending。

python workitems/mes-040/check.py 通過：實體與關係節點內容、真實搜尋點擊／觸控、兩尺寸圖文、正確放大資產與無 JS 錯誤。證據 tests/evidence/mes-040。integrate.py 為一次性資產整合，不重跑。
