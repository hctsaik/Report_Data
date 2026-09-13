# MES-049 OHB

依使用者定義，OHB 為機台附近簡易 FOUP 暫置架，遠端 Stocker 取貨較久時先就近暫放，方便後續搬運。四 OHB 引用更新；BMIR 保留原內容獨立映射，未套用未確認定義。

assets/mes-049/ohb-near-tool-v1.png 與 ohb-near-tool-mobile-v1.png 已發布。OHB 畫固定架，OHT 畫搬運車，Stocker 畫倉儲；路徑是概念，不是已執行事件。兩圖及 1440/390 實際頁面已目視檢查，細字可放大閱讀；未自動品質評分，使用者審閱 pending。

python workitems/mes-049/check.py 通過：四引用、搜尋點擊/觸控、兩尺寸及放大、無 JS error。證據 tests/evidence/mes-049。integrate.py 一次性不重跑。
