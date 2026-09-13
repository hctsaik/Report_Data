# MES-046 PART 流程版本

使用者確認產品/PART 對應 Flow（Route/mainpd_id），Flow 進版時 PART 同步記錄版本資訊以維持加工流程正確。兩引用專屬圖文已更新，保留原表及 Mainpd_id。不推定在製 Lot 自動全部切版或版本欄位格式。

發布 assets/mes-046/part-flow-version-v2.png 及 part-flow-version-mobile-v1.png。桌面首稿自行補成版本文件更新而站序不需調整，已修正為進版內容依實際定義，並移除一對一基數措辭。兩圖、1440/390 網頁均目視檢查，P100 的 V1/V2 對應一致，細字有放大入口。無自動品質評分，使用者審閱 pending。

python workitems/mes-046/check.py 通過：兩引用、搜尋點擊/觸控、兩尺寸及放大、無 JS error。證據 tests/evidence/mes-046。integrate.py 一次性不重跑。
