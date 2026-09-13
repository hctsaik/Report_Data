# MES-041 Stream 到站預估

依使用者確認，舊 Stream 功能透過 Flow 與 IE WPH 估算 Lot 後續各站到站時間，已由 LDS 取代。從一般 forecast 映射分離兩 Stream 引用，保留原 ER。說明站序、速率轉耗時與逐站累計；片數/WPH 僅用於解釋單位，不聲稱為實際完整算法，也不推定 LDS 沿用。

assets/mes-041/stream-arrival-v2.png 與 stream-arrival-mobile-v1.png 已發布。桌面首稿兩輸入箭頭均從 WPH 出發，並自行加入製程名稱，退回修正；最終圖兩輸入明示 Flow 站序與 WPH 耗時估算，移除多餘製程名稱。手機同樣雙輸入。圖、1440/390 實際頁面均已目視檢查；時鐘僅作概念圖示。小字可從放大入口閱讀，未自動評品質，使用者審閱 pending。

python workitems/mes-041/check.py 通過：兩 Stream 節點、搜尋真實點擊/觸控、兩尺寸圖文及放大、無 JS error；普通 forecast 不誤標 LDS。證據 tests/evidence/mes-041。integrate.py 一次性不重跑。
