# MES-034 EQP Bay走道與管理單位

依使用者定義，EQP Bay為機台位於Fab哪條走道，供線上查位置及所屬管理單位。四個Bay來源節點補專屬圖文，強調實體位置與管理歸屬分開，不推定同走道必同單位。
桌面/手機圖：assets/mes-034/eqp-bay-v1.png、eqp-bay-mobile-v1.png。三段查機台→找走道→確認單位；ETCH-03/B12/設備管理A組明示教學假設。保留原ER表與註記，不臆測PHASE與管理單位欄位。
imagegen提示見PLAN主線；兩張生成圖均實看，手機直向。來源exec-0185114a-c1b7-4a3e-b049-ff969fafeccb.png與exec-5c62311d-2f2d-4e8a-9378-43332a211819.png。
python workitems/mes-034/check.py通過：四來源、1440/390圖文/真實搜尋/放大、無JS error或溢出；手機頁面截圖已檢視，證據tests/evidence/mes-034。未自動評品質，使用者審閱pending。一次性integrate.py不重跑。
