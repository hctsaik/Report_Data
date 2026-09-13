# MES-048 Default Stocker

使用者確認每台機台有預設 Stocker（FOUP 倉儲）。stock 兩引用已更新專屬圖文，保留 Siview.csfreqp_stk／eqp_id。設定關係與實際位置、搬送事件分清。

發布 assets/mes-048/default-stocker-v1.png 與 default-stocker-mobile-v1.png，EQP-A 對應 STK-01，倉儲內多個 FOUP，虛線表示預設對應。生成圖、1440/390 網頁已目視檢查，細字可由放大入口閱讀。未自動品質評分，使用者審閱 pending。

python workitems/mes-048/check.py 通過：兩引用、搜尋點擊/觸控、雙尺寸圖文與放大、無 JS error。證據 tests/evidence/mes-048。integrate.py 一次性不重跑。
