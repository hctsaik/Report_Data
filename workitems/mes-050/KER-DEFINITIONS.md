# KER 廠內定義確認

本輪為使用者回答關係問題的紀錄；尚未製作新圖文或修改網站。以下定義作為後續教學依據，不由表名推導 SQL 實作。

- KER = Key EQP Report。用來管理機台與機群的報表，提供 AVL、EFF、LOST 等指標。
- KER_EMP_EQP_GRP_CAP_UT：資料代表機台在某個機群的對應。同一機台可以同時屬於多個機群。
- ker_dm_sub_ch_eqp_grp_bt：Chamber 可以獨立分群，同一機台的不同 Chamber 可以屬於不同機群。
- KER_VR_EQP_GRP_DETAIL_BT：User 可自行用 SQL 分 tool group；DYNAMIC_SQL 用於理解使用者定義的虛擬分群。不假定條件執行時機或快取行為。
- ker_dm_bt：「目前」指最近一次更新，不直接等同當班或當日累計；時間窗及公式未確認。
- Ker_Dm_Hourly_Bth：每小時的機群指標。
- Ker_Eqp_Aaa_Oee_Ut：機台歷史指標，也是一小時一次。
- 「機群目前 OEE」以 EQP_GRP 關聯是刻意設計，保留此關係。
- 使用者指示指標如何彙總與 EFF 廠內定義先不用管；不追加公式、不假設加總或平均。

範圍界線：使用者未另確認「機群歷史 OEE」連線 EQP_ID 是否需更正，因此不將目前 OEE 的 EQP_GRP 確認套用至歷史連線。

## 後續製作狀態
使用者已另行授權產生圖文，網站更新與驗證見 REVIEW.md；上方「尚未製作」為當時定義確認階段紀錄。
