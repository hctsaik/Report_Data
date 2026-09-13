# MES-029 PD 定義與專屬教材

依使用者廠內定義：PD = Process Definition，每一站的細部加工定義，可以理解為站點會使用的 Recipe 與 Tool 關係。

已更新七個 PD 來源節點及 PD 路徑的介紹。FRPD 的顯示名稱補上 Process Definition；來源資料表／鍵保留，沒有推定 Recipe Join 或把定義當成 Lot 的實際執行。

新增桌面 assets/mes-029/pd-definition-v2.png、手機 pd-definition-mobile-v1.png。讀圖為站點 S20 → PD-A → Recipe R-A／Tool ETCH-03，均明示教學示例。第一版圖自行添加加工參數，未發布；修正版移除參數與額外站點名稱後再製手機版。三張生成結果已檢視，僅後兩張使用。

生成提示主線：三段白底藍框、實際fab形象，站點→PD→Recipe與Tool，黃色結語「PD定義這一站怎麼加工；實際用了什麼，要看執行紀錄」。修正版明確刪除化學品、壓力、功率、時間等未授權數值；手機依修正版直向重排。原始輸出exec-20a6974a-e943-4f2a-b395-b2132eeb7c1b.png、exec-dcc27f7a-e340-4c9c-83b0-daeb852ea151.png。

驗證 `python workitems/mes-029/check.py`：七個節點、路徑、桌面／手機圖片及放大、真實搜尋點選、切回Lot清除、無JS error／溢出通過。MES-028導覽回歸通過。
實際檢視390說明及1440關聯圖，PD全名與表名可讀，手機三段直向圖正常。證據tests/evidence/mes-029。不宣稱品質分數或使用者驗收。
一次性integrate.py不重跑。
