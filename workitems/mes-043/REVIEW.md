# MES-043 Recipe Group

依使用者定義补上群組內機台角色與加工許可控制。專屬雙尺寸圖文顯示三台可做類似加工的機台，以及對同一產品/加工條件的多台與單台獨立控制情境。明確區分能力與許可、許可與電源；不推定控制優先權或實際 Join。

發布 assets/mes-043/recipe-group-v1.png 和 recipe-group-mobile-v1.png。生成圖與 1440/390 頁面已目視檢查，兩案例的機台 ID 與許可一致、沒有先後箭頭。圖內細字可由放大入口閱讀，未自動評品質，使用者審閱 pending。

python workitems/mes-043/check.py 通過：群組實體與關係引用、真實搜尋點擊/觸控、雙尺寸圖文與放大、無 JS error。證據 tests/evidence/mes-043。integrate.py 一次性不重跑。
