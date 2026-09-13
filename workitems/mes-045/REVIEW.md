# MES-045 SRTS 抽測規則

使用者確認 Flow 適用站點與 Sampling rule 比例，例如每 Part 30% 抽檢。srts 兩引用專屬圖文已更新，呈現 Flow 站點、Part 與30%設定、依規則量測。未臆測抽樣單位或跳站算法。

發布 assets/mes-045/srts-sampling-v1.png、srts-sampling-mobile-v2.png。手機首版自行添加 CMM，已重製為半導體量測設備並去除該標籤。兩圖及 1440/390 網頁截圖已實看，比例及 Part 一致；細字可由放大入口閱讀。未自動品質評分，使用者審閱 pending。

python workitems/mes-045/check.py 通過：兩引用、搜尋點擊/觸控、雙尺寸圖文及放大、無 JS error。證據 tests/evidence/mes-045。integrate.py 一次性不重跑。
