# MES-023 Lot 預派與專屬示意圖

使用者明確要求預派關係增加 Lot：派工系統預先將這個 Lot 派到機台，FOUP 不是主要重點。已在右側預派關聯圖加入 Lot，Lot／EQP 優先，FOUP 標示輔助關聯；手机第一頁先顯示 Lot 與 EQP。

新增邊 business-lot-predispatch 是使用者確認的業務關係，以虛線及獨立 provenance 呈現，不冒充原圖中的資料表 Join。原模型／SVG仍保留，沒有推定新鍵、基數或資料欄位。主圖路徑仍可追到既有來源，右圖則補業務含義。先前「帶到／FRLOT_EQP＝本站可用機台」保持不變。

內建imagegen重製三段實物示意：Lot（批次卡與晶圓）→ 派工系統預先安排 → 預派目標機台。FOUP不作主視覺，黃色重點明示不代表已到站或加工。桌面 lot-predispatch-v1.png、手機 lot-predispatch-mobile-v1.png 保存於 assets/mes-023；prompt.txt 與 prompt-mobile.txt 保存產圖提示。圖片為概念示意，不包含真實派工數據；晶圓數量不代表實際Lot規模。

入口 er-atlas.html?subject=predispatch。直接選預派節點與選預派路徑都自動展開專屬圖與說明。既有Lot/WPH等圖仍各自使用原有映射。

驗證 python workitems/mes-023/check.py：1440／390均PASS；Lot/EQP優先、輔助FOUP、虛線標記、新圖與放大、右側展開、真實mouse/touch切主詞、全部121根的來源邊與唯一業務補充邊核對，以及帶到／內容物歷史／WPH回歸。無JS錯誤。已實看桌面graph及手機illustration截圖，並檢視兩張生成圖文字與主線。

先前MES-017僅允許原始來源邊的假設不適用本次使用者明確補充；驗證依provenance區分，不能刪除標記來讓舊測試通過。使用者審閱pending，未自評整套教材達標。
