# MES-047 機群與課別

依使用者說明 MFG_EQP_OWNER_BT 可查設備管理單位、機群及廠商資訊。owner 兩引用從通用 group 映射分出，避免套用到 Chamber 群組的其他來源。原 EQP_ID 關係保留。

assets/mes-047/eqp-owner-v1.png 與 eqp-owner-mobile-v1.png 使用同一 EQP-A/B、G01、設備一課示例，廠商甲為設備資訊另列。兩圖與 1440/390 頁面已目視檢查，機台及管理資訊一致；細字可由放大入口閱讀。未自動品質評分，使用者審閱 pending。

python workitems/mes-047/check.py 通過：兩引用、真實搜尋點擊/觸控、雙尺寸圖文與放大、無 JS error。證據 tests/evidence/mes-047。integrate.py 一次性不重跑。
