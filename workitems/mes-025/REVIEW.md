# MES-025 Qtime與Lot教學

依使用者要求補Lot，並將不相關的FOUP位置參考換成Qtime介紹。

右圖保留完整來源鏈：Qtime歷史 — Qtime站點（Lot_ID／Ope_no）— Lot Step歷史 — 站點Summary（Lot_id）— Lot。直接選Qtime歷史或Qtime站點皆能看到Lot。新增subject=qtime入口，既有qtime路徑也延長到Lot。所有新增展示路徑均使用原始來源邊，沒有補猜Join鍵。

專屬教學：Qtime為同一Lot指定起訖事件間的時間限制；明示不一定只算排隊，可能跨站或以出站停止。讀歷史先核對Lot／站點、事件、時間及限值。示例30分鐘，10:00起算、10:20已用20分鐘、10:35停止則超時5分鐘；停止事件若是出站，進站不等於結束。數值標示為教學示例，依實際製程規則判讀，未補公司通用限值。

圖像：桌面沿用已檢視assets/mes-009/qtime.png；手機用內建imagegen基於該圖重排assets/mes-025/qtime-mobile-v1.png，提示保存prompt-mobile.txt。三段事件順序及同一Lot一致，手機圖明示10:30是時限、非已發生事件。連結advanced.html#qtime的互動教學。

驗證python workitems/mes-025/check.py，1440／390涵蓋兩個Qtime節點、每條来源邊、Lot存在、教學文字／計算、專屬圖與放大、預設展開、路徑、右側展開、切換Lot後清除專屬說明。證據tests/evidence/mes-025。使用者審閱pending，不借用功能PASS宣稱整套教學達標。
