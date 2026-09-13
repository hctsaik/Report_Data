# MES-031 MCS傳送命令

依使用者廠內定義補充Macro command（E2E）與Micro command（各段軌道含每個轉彎處），說明依傳送命令／時間／位置追FOUP行蹤。

MCS兩節點獨立教材，不把MES傳送節點套入此層級。MCS路徑同步介紹。示意Macro M001為A→D；三個Micro為A→B、B→C、C→D，B/C轉彎；同FOUP F012在10:00–10:03四個假設紀錄位置可點選。SVG是精確概念路線，非實際軌道比例或即時資料。

區分命令目的地與已確認位置；到終點還需核對完成狀態。保留carrier_job_history@mcsdb／transfer_job_history@mcsdb、Carrier_id／transfer_job_id來源資訊，不推定兩表分別對應Macro或Micro，不編造實際SQL欄位。

驗證python workitems/mes-031/check.py通過：1440/390兩個MCS節點真實搜尋點選、四個時間事件、路徑入口、展開保持、MES分離、無JS error／溢出。MES-028導覽回歸通過。已實看390-trace.png，軌道轉彎、FOUP位置與選中時間一致。證據tests/evidence/mes-031；使用者審閱pending。integrate.py為一次性不可重跑。
