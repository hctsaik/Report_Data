# MES-050 KER 圖文

依 KER-DEFINITIONS.md 使用者確認內容製作，group/virtual/oee 三主題共用 KER 專屬雙尺寸總覽，各自提供分群、SQL 定義或時間層級的文字與來源表。十二來源引用已覆盖。機群目前 EQP_GRP 保留；不改歷史原線、不展開公式。

assets/mes-050/ker-overview-v1.png、ker-overview-mobile-v1.png 呈現多重分群、Chamber 獨立分群、User SQL、目前與每小時歷史。生成圖及手機頁面實看，指標圖示僅項目，不是數值。使用者審閱 pending，未自動品質評分。

python workitems/mes-050/check.py 通過：十二引用、桌面手機搜尋點擊/觸控、雙尺寸與放大、無 JS error。證據 tests/evidence/mes-050。integrate.py 一次性不重跑。
