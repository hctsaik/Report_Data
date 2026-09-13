# MES-037 預派歷史圖文

CSFHPREDISP及Lot_ID預派關係兩節點補專屬圖文。使用者確認預派在機台執行前產生，讓機台先知道接下來Lot。正文分安排/預知/歷史回查，預派不當成開工或最後一定執行。
新桌面predispatch-history-v2.png與手機predispatch-history-mobile-v1.png位於assets/mes-037。三段同L023/ETCH-03，示例非真實紀錄。首版多出設備品牌未發布，修正版移除後生成手機版。三張生成結果均已檢视；發布來源exec-754c486f-effb-45ce-a617-a800ad07847a.png及exec-18a5b207-5edd-4434-8b9c-7fdb7261102c.png，提示概念見PLAN。
python workitems/mes-037/check.py通過：兩來源、1440/390真實搜尋選取、圖文與放大，無JS error。手機頁面已實看，證據tests/evidence/mes-037。使用者審閱pending，未自動評分；integrate.py不可重跑。
