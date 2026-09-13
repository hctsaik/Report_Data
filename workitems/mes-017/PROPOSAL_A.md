# 提案 A：主詞中心、完整關係分支

狀態：設計討論，未改網站；以下是從現有 er-model-v2.json 實際拓樸計算的範圍，不是完成圖面或成品品質評分。

## 畫法

Lot、EQP、FOUP、Flow 各有獨立主題 ER。主詞置中，維持既有實體色彩，額外用較厚框、較大中文名稱及「本圖主詞」標記；其他實體保留原色，不改成主詞的顏色。全部矩形、關係菱形、鍵及原連線仍可讀。

每張以「中心實體 → 原關係菱形 → 該菱形所有端點」為最小完整範圍。左右可按教學閱讀區塊排版，但區塊標題不成為資料實體、不加推測的箭頭。例如 Lot 左側放裝載／現場位置，右側放製程與管制，下方放歷史。若同一 FOUP 連兩個菱形，只有一個 FOUP 節點，兩條關係都保留。

## 四張具體範圍

| 主詞 | canonical ID | 直接關係數 | 關係閉包節點／邊 | 圖內相關實體 |
|---|---|---:|---:|---|
| Lot | t_cfc81de70314 | 14 | 28／29 | FOUP、Port、EQP、Flow、預派記錄、批貨歷史、Move、Step summary、Hold、Forecast |
| FOUP | t_55072ef91a15 | 7 | 13／14 | Lot、EQP、Step 歷史、MES／MCS 搬送歷史 |
| EQP | t_7f282520afb8 | 11 | 22／23 | Lot、FOUP、兩種 Port 表、Chamber、位置、課別、機況歷史、STK、OHB |
| Flow | t_d4d030ed08a4 | 8 | 16／16 | Lot、LR 機台對映、PD、Part、Recipe Group、Stage／Module、SRTS |

Lot 的 14 個完整分支：

1. 放在 / Siview.FrlotMtrl → Siview.FRLot_MtrlContnrs。
2. EI 在 / Siview.Freqp_Lot → Siview.Port。
3. 在 Slot / Siview.fhwlths → Siview.Frcast。
4. 放在 / Siview.Frcast_lot → 同一 Siview.Frcast。
5. 預到 / Siview.Frlot_EQP → Siview.freqp。
6. 預派機台 / Lot_ID → Siview.CSFHPREDISP。
7. Lot 所有動作 / Lot_ID → Siview.FHOPEHS_S。
8. 機台 MOVE / Lot_id → F12DM.DM_Move_Step_bth **以及** Siview.FHOPEHS_S，原菱形有三個端點，不能退化成二端關係。
9. 站點 Summary / Lot_id → F12DM.DM_Lot_step_st。
10. 有 Prod Hold / Lot_ID → Siview.CSFRPRHold。
11. Flow 定義 / Part / Mainpd_id → F12DM.DM_Flow_step_Bt。
12. Future Hold / Lot_ID → Siview.frlot_futurehold。
13. 未來的各站 / Lot_ID / OPE_NO → Stream_fcst_lot_st。
14. 未來的 Flow / Lot_ID / OPE_NO → F12dm.dm_tbl_lot_forecast。

因此「Lot 圖中有 EQP、FOUP、Flow，主詞仍是 Lot」不需造新關係，即可直接從原圖成立。點 EQP 提供「以 EQP 為主詞查看」入口，換圖時相同 canonical ID 有可追蹤標記。

## 抽取及完整性規則

- 抽取來自 canonical node ID 與 edge ID 白名單，不能用標籤相似度、顏色、表名後半段重新合併。
- 每個納入的菱形必須保留全部原始端點、鍵與原邊；非二元關係也完整。跨圖同節點是同一身分的重現，不是假裝新表。
- 四張主題 ER 不是原完整圖的全部分割。尚未收進主詞直接關係的二階詳細資料，以明示的延伸入口到完整大圖或延伸主題；不得宣称四張等於所有 121 節點與 128 邊皆已展示。
- 顯示各圖範圍清單與未納入清單；完整大圖、七張來源圖保留為核對入口。四張間共有關係允許重複，不能為了分割唯一歸屬而切斷關係。
- 未列 schema 的 FRLOT/FREQP/FRCAST 等節點不併入已列 schema 的主詞；若未證實與主詞有原線，列為獨立延伸示例，不能以虛線假連接。
- Flow 的 LR 對映資料不直接畫成實際加工 Physical Recipe 或機台執行證據；Port 表名不同也不合併。
- 納入的端點如有原始 ellipse 屬性亦應附上；上述四中心直接閉包未碰到 ellipse，其他延伸仍須此規則。

## 主要優點與缺點

優點：規則最容易重現與稽核、主詞完整直接關係不漏、符合真 ER、切換四主詞不會改變語意。Lot 和 EQP 不會被隔離成互斥圖。

缺點：Lot 仍有 28 節點、14 菱形，EQP 有 22 節點；直接塞進右側還有教學圖的視窗，恐怕仍會縮小至不可讀。中心多條線的放射布局易交叉，必須以分區正交排線；只靠此方案並不能保證初學者容易看懂。對完整教學而言「全部直接關係一屏」與「閱讀清晰」衝突，可能應採另一提案的預設核心分支＋完整延伸模式，但隱藏範圍必須明示。

## 評分原則

交叉評分依本輪共同 DESIGN_REVIEW.md：主詞清楚 25／ER 忠實 25／資訊負擔 20／跨圖一致 15／教學操作 15。MES-014 成品量表只作之後製作驗收的要求參考，本輪沒有成品，不能當已繪製圖面無遺漏的證據。可讀性與操作尚無實作截圖，僅能做預期風險評估，不給成品通過結論。
