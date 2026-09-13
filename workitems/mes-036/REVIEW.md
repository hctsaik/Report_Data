# MES-036 FOUP主詞的Lot裝載圖文

依使用者校正，FRLot_MtrlContnrs—FrlotMtrl—Frlot是FOUP/Lot装載關係，與FRCAST—FRCAST_LOT—FRLOT概念相同，此處以FOUP查詢。已更新兩material節點，撤回用途未確認的籠統說明，表與鍵保留不合併。
專屬桌面/手機圖在assets/mes-036：選F012→查晶圓歸屬→L023/L024。明示查詢方向、非事件順序；Lot為歸屬，不是實體盒子，颜色不表品質。一或多Lot均可，兩Lot為例。
最終使用專屬查詢圖和兩路徑文字對照，未重複嵌入25槽互動以避免把查詢重點淹沒；既有Lot/FOUP教學仍有25槽例。
兩生成圖已檢視，原輸出exec-61fa1951-7de6-4c32-9359-54835f31258f.png及exec-8f00ac65-18ce-4a79-be46-650451b3454d.png，提示主線見PLAN.md。
python workitems/mes-036/check.py通過，1440/390兩節點真實搜尋、圖文/放大/無JS error/溢出。手機頁面截圖已實看，證據tests/evidence/mes-036。使用者審閱pending，未自動評分；integrate.py一次性不可重跑。
