# MES-039 Move 進機事件與兩種查法

依使用者定義，每次 Lot 與機台進機事件記一筆 Move。專屬桌面及手機圖文從進機事件集合分出每日廠區統計與按 Lot 查 DM_MOVE_STEP 站點歷程。重工再進機保留事件；說明 Move 不等於晶圓產出或理論最大產能。原來源完整表名及 Lot_id 保留，未假定 DM_MOVE_STEP 與來源同表。support.html 的連結教學同步進機定義。

發布 assets/mes-039/move-uses-v2.png 與 move-uses-mobile-v2.png。首版箭頭從單機出發造成統計來源不明，兩尺寸均修正為事件集合出發。圖中數字與站點為示例；生成圖及手機實際網頁截圖已目視檢查。

python workitems/mes-039/check.py 通過：四來源引用、真實搜尋選取、1440/390 圖文、放大正確資產、Move 路徑及無 JS 錯誤。證據 tests/evidence/mes-039。功能驗證不代替品質評分，使用者審閱 pending。integrate.py 為一次性腳本，不重跑。
