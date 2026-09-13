# MES-029 PD Process Definition

使用者確認：PD 是 Process Definition，每一站的細部加工定義，可理解為站點內使用的 Recipe 與 Tool 關係。
更新 PD 七個來源節點與路徑的介紹，FRPD 顯示名稱補上全名，保留各來源表與鍵，不虛構 SQL Join。
使用 imagegen 技能製作專屬教學圖，不借用其他主題圖。

## 插圖 preflight

目標：讀者能從站點找到 PD，理解加工定義中的 Recipe／Tool 對應，與實際執行分開。
C 因果故事：站點 → PD → Recipe 與 Tool；三個主要視覺節點。
參考現有 Future Hold 教材白底、藍框、具體 fab 場景與黃色 takeaway；採桌面16:9與手機直向版本。
例示站點 S20、PD-A、Recipe R-A、Tool ETCH-03 均為教學示例，不是廠內正式配置。
黃色結語：PD 定義這一站怎麼加工；實際用了什麼，要看執行紀錄。
圖僅示意業務概念，不能把 Recipe／Tool 連線宣稱為已驗證的資料表 Join。

驗證七PD節點、路徑入口、桌面手機圖片及圖文切換；原圖模型保留。
