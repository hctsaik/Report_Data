# 原圖文字確認紀錄（已全部確認）

2026-09-13：使用者分兩輪確認全部 13 項疑義。**目前沒有待確認文字，圖上橘色標記已全部移除。** 下表僅保留原暫讀作為校字歷史，並非現行待辦。

第二輪已套用：U01 →「EI 在」；U04 →「Lot 所有動作」（2672、2675）；U09 →「製程程式群組對照」；U10 → `F12DM.DM_Flow_LR_EQP_BT`；U11 →「抽測跳站設定」。

已套用：`Siview.fhwlths`、`SIVIEW.CSFRPREDISPATCH`、`Siview.CSFHPREDISP`、`Mfg_Carrier_te_ut`、`F12DM.DM_Qrest_Hist_BTH`、`LCRECIPE_ID`、`Siview.CSFRRCPGRPST`、「星期一的七點二十分的 WIP」、「屬於哪個虛擬群組」。其中 WIP 原暫讀「一星期」已更正；LR 原暫讀 `LCREIPE_ID` 已更正。

| 編號 | 原圖／位置 | 暫讀文字 | 不確定處 |
|---|---|---|---|
| U01 | 2671，LOT 與 Port 間菱形標題 | 目在 | 第一字不清楚，未依意思改成「目前在」。 |
| U02 | 2671，左下「在 Slot」及中央游離小字 | Siview.fhwlths | h／w／l 字形靠得很近；獨立小字保留，未自行接線。 |
| U03 | 2671，最下「預派機台」 | SIVIEW.CSFRPREDISPATCH | 原圖分成 CSFRPREDIS、PATCH 兩行；完整拼字待確認。2672 寫 CSFHPREDISP，未混為一表。 |
| U04 | 2672 與 2675，LOT 下方菱形 | 貨所有動作 | 開頭字與底線重疊，可能缺字；保留暫讀。 |
| U05 | 2672，右上「傳送歷史」表 | Mfg_Carrier_te_ut | te 字形不完全確定。 |
| U06 | 2672，右下「Qtime 歷史」表 | F12DM.DM_Qrest_Hist_BTH | Qrest 的字形待核對。 |
| U07 | 2673，Recipe Group 表 | Siview.CSFRRCPGRPST | 連續 R／C／P 與底線重疊，請確認完整名稱。 |
| U08 | 2673，LR 與機台及右側對應菱形 | LCREIPE_ID | 原圖看似此拼字；沒有擅改成 LCRECIPE_ID。 |
| U09 | 2673，Recipe Group 下方菱形 | 製程程式群組對照 | 標題後半與斜線重疊，完整中文待核對。 |
| U10 | 2673，最右「LR 與機台對應關係」表 | F12DM.DM_Flow_LR_EQP.BT | 尾端跨行，EQP 與 BT 間看似句點；左上另一處用 _BT，未自行統一。 |
| U11 | 2673，SRTS 設定上方菱形 | 抽測跳站設定 | 前段字形被斜線與底線干擾。 |
| U12 | 2675，最上方 WIP 表標題 | 一星期的七點二十分的 WIP | 「七」字及整句含義待確認，不據此新增排程規則。 |
| U13 | 2675，最右側 DYNAMIC_SQL 菱形標題 | 屬於哪個虛擬群組 | 中文標題部分筆畫與邊線重疊。 |

2676、2677 未發現無法辨讀的文字。所有資料表名稱是照片轉錄，尚未連接資料庫驗證。原圖未標示的 schema、關聯方向、1:N 基數與缺失欄位均未補寫。
