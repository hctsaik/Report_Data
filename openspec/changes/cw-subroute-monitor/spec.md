# CW、Sub Route、Move 與 MON／PM／EMS

## 已確認語義

- Monitor、Dummy、Seasoning 都納入本廠 CW；用途介紹不能取代實際適用規格，也不假設互斥。
- Sub Route 是 Lot 暫走另一條 Route，出去的原位置與返回位置一致。加量已確認是追加量測。
- Move 是以 Lot 為單位的過站事件；重工計入。不是晶圓數、搬運次數、不同 Lot 數。
- MON 是作業類型，監控設備／製程表現；PM 是預防性保養。
- Daily MON 逾期時，EMS（EQM Monitor System）阻擋生產加工。

## 教學行為

四節入口 support.html#cw、#subroute、#move、#monitor。每節具備情境插畫、原生互動、案例與自測；手機另排主線，圖片可放大。

Sub Route 模擬保留返回位置，直接回下一站會被拒絕；返回不自動過站。Move 模擬新重工事件加一、相同事件重送不新增。MON 模擬逾期、補做完成、結果接受與 EMS 更新的不同階段；PM 未完成或其他 Hold 不因監控通過而被清除。

不得假定 Daily MON 固定 24 小時、不假定 PM 每次必然觸發相同 seasoning、不得將 MON 完成直接視為 EMS 自動放行。所有控制僅在本機教學模型，不連接真實機台。

AAA 正式縮寫、AVL／Eff／Lost／Up 定義仍待使用者補充，本輪不補造。
