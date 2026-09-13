# MES-030 Lot 與 Wafer 關係

依使用者補充：同FOUP可裝多Lot（不同Lot ID），也可單Lot25片；每片Wafer ID及Slot不同。更新Lot、FOUP與FRCAST_LOT裝載入口的說明，撤換這三類入口的通用實物照片，改為精確25槽的互動教學圖。

兩個獨立示例：F012單Lot L023／W001–W025；F012多Lot L023（Slot01–10）與L024（Slot11–25）。10+15分配為教學選例，不是廠內固定規則或一次Split/Merge前後。所有晶圓ID不同，25片不是Lot固定數量。
選晶圓同步顯示Lot ID、Wafer ID、FOUP ID、Slot No.；手機上方顯示完整身分，選中槽旁也有即時說明，避免反覆捲動對照。桌面雙欄，手機直向，右側展開維持目前示例。

圖為HTML/CSS精確位置示意，非實物比例；沒有新增未核對的Wafer資料表或Join。原始ER保留。清楚區分批次歸屬與容器位置。

`python workitems/mes-030/check.py`通過：1440／390，單/多Lot數量、25個唯一Wafer、槽位點選、兩情境切換、Lot/FOUP/關係/路徑入口、展開保持、離開主題清除、無JS error／溢出。`python workitems/mes-028/check.py`導覽回歸通過。
實際檢視桌面單Lot、手機多Lot截圖後補選中槽旁說明並重新擷取；證據tests/evidence/mes-030。
MES-025/026等舊檢查中「切回Lot必須空白topic-detail並顯示FOUP總覽照片」期望已被本輪要求取代，不能據此刪除新教材。品質未自動評分、使用者審閱pending。一次性integrate.py勿重跑。
