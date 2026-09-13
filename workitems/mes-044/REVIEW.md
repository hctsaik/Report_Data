# MES-044 Module／Stage／Step

使用者本輪確認：Module 如黃光，包含多個 Stage，各 Stage 包含細部 Step。此定義取代 PLAN 初稿的未確認狀態。依此重製雙尺寸圖文，原先未定義 Module 的草圖不發布。

最終 assets/mes-044/module-stage-step-v2.png 與 module-stage-step-mobile-v2.png 使用三層巢狀框；Lot S30 往上查 Stage B 與黃光 Module。站名為示例，不當成實際黃光步驟。生成圖及 1440/390 網頁截圖已實看，包含層級與 Lot 對照一致。未自動品質評分，使用者審閱 pending。

python workitems/mes-044/check.py 通過：實體/關係引用、搜尋點擊/觸控、雙尺寸與放大、無 JS error。證據 tests/evidence/mes-044。integrate.py 一次性不重跑。
