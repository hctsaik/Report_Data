# 方案 B：主詞置左、關係分組橫向展開

本文件是設計提案；沒有改網站、沒有畫成品，分數只能代表設計評估，不能沿用 MES-014 成品的 91 分。

## 概念

每個主題是一張由既有 ER 抽取的關係圖，不是依類別切開資料。Lot 主題仍包含 FOUP、EQP、Flow、Hold、History；唯一變更是視線从左邊 Lot 開始，沿原有線、菱形及鍵讀向右邊。分組標題只是排版背景，不是新實體，也不加入關係線。

矩形保留實體與表名；菱形保留關係與原表名／鍵；橢圓保留原屬性；連線沒有新箭頭或基數。Lot 藍、FOUP 綠、EQP 橙、Flow 紫固定跨圖一致。主詞用較厚外框及「本圖主詞」文字強調，不以把其他實體改成灰色表示不重要。

## Lot 具體布局

左欄是唯一的 `LOT / Siview.Frlot` 矩形，位於左側中間；中央為關係菱形；右欄為關係的完整終點。圖由上到下分成四段，各段共享同一個左側 Lot。每條線独立從 Lot 出發，不用沒有語意的共用匯流線。

| 排版段 | 原 ER 內容 | 保留的差別 |
| --- | --- | --- |
| 裝載與位置 | Lot — 放在 / Siview.Frcast_lot — FOUP / Siview.Frcast；Lot — 在 Slot / Siview.fhwlths — 同一 FOUP；Lot — 放在 / Siview.FrlotMtrl — Siview.FRLot_MtrlContnrs | 两条通向同一 FOUP 的菱形不能合併；另一種容器表不能假設同表 |
| 設備與預派 | Lot — EI 在 / Siview.Freqp_Lot — Port / Siview.Port；Lot — 預到 / Siview.Frlot_EQP — EQP / Siview.freqp；Lot — 預派機台 / Lot_ID — Siview.CSFHPREDISP | 預派／預到／實際位置不合成一條「在機台」關係；Port 到 EQP 如需展開，沿原 `has` 路徑追加 |
| Flow 與限制 | Lot — Flow 定義 / Part / Mainpd_id — F12DM.DM_Flow_step_Bt；Lot — Future Hold / Lot_ID — Siview.frlot_futurehold；Lot — 有 Prod Hold / Lot_ID — Siview.CSFRPRHold | Flow 定義與預測資料分開；Hold 存在不直接代表即刻不可加工 |
| 歷史與預測 | Lot 所有動作 / Lot_ID — Siview.FHOPEHS_S；機台 MOVE / Lot_id — F12DM.DM_Move_Step_bth；站點 Summary / Lot_id — F12DM.DM_Lot_step_st；未來 Flow / Lot_ID / OPE_NO — F12dm.dm_tbl_lot_forecast；未來各站 / Lot_ID / OPE_NO — Stream_fcst_lot_st | Move 不等於搬送；預測不等於當前位置；裸 schema 保持未確認 |

這張 Lot 主題不是只選三條漂亮的邊：以已确认主體 `SIVIEW.FRLOT` 的 14 條直接關係擴展到關係完整終點，程式讀取現有模型得到 28 節點、29 邊。它明確小於整張 121 節點／128 邊。這是候選範圍計數，之後製作須逐邊檢查，不能只用度數證明 ER 語意完整。

## 保持跨主題語意

同一 canonical node 可以同時顯示於不同主題，但仍是同一資料物件；每個主題內原則上一個畫面節點。FOUP 主題的主詞換成 `SIVIEW.FRCAST`，既有裝載關係讀回 Lot，另沿原位置／搬送關係讀到 EQP 或紀錄。EQP 主題以 `SIVIEW.FREQP` 為主詞，包含連回 Lot 的預到關係，以及 Port、Chamber、Recipe 對應等原路徑。Flow 主題以已知 Flow 表為主詞，連回 Lot 與 LR 對應。

相同 display label、但 schema 未知的 `FRLOT`／`FREQP` 不能併成已知主詞。未知來源可在同主題的「其他來源，對應未確認」區呈現獨立 ER 片段，不能畫一條虛構的 bridge。這也是各主詞主題只定義語意索引，不定義 SQL Join 的原因。

跨主題按鈕「以 EQP 為主詞看」保持被選 node／關係 ID；切換後高亮相同實體。完整總圖仍可回去對照。主題覆蓋清單記錄每個原節點、原邊落在哪些主題；允許重複，禁止全站遺漏。

## 教學與操作

桌面第一眼看整張主題 ER，至少看到 Lot、FOUP、EQP、Flow 同時存在。右側現場插圖跟隨點選；未提供專屬圖時明說是基礎參考，不假裝換圖。點選段落只突出原線，其餘仍可辨，不能再把主圖縮成主題卡。投影「逐段講解」提供已存在 ER 段落的局部放大，保留同一主詞與終點。

手機不能強求 28 個節點和完整表名塞滿 390 px。一開始提供主題全貌定位，正文提供四段可逐一放大閱讀；每段都含主詞、關係菱形、鍵與終點，不需要記憶畫面外的起點。若為閱讀重複畫 Lot，標「同一 Lot 的分段閱讀」，底層 canonical ID 不變，這個重複只發生於手機閱讀分段，不是假造第四個 Lot。

## 優點及取捨

- 左到右句子有共同起點，初學者最容易逐條讀出「Lot 與誰透過什麼資料有關」。平行關係易比較。
- 長表名、複合鍵在三欄布局較容易安排可讀寬度。
- 最大風險是主詞只有左邊一个，14 條出線跨整張高度，依然可能成為「梳子」般的密集圖；需要在 Lot 邊框分配獨立端點，不能用單一深色粗線混成有向流程。
- 28 節點主題全貌在一般螢幕仍無法保證所有表名清晰；必須逐段放大，不能以縮圖假稱可讀。若使用者希望同屏讀全部，A 的中心四象限可能比本案少滾動。
- 多段分組容易讓人誤認四種流程階段；分組標明「讀圖分類，非製程順序」，不加依序箭頭。

## 待交叉評估

依共同 DESIGN_REVIEW.md 五項：主詞清楚 24/25、ER 忠實 24/25、資訊負擔 13/20、跨圖一致 14/15、教學操作 11/15，合計設計估分 86/100。語意扣分為未知 schema 片段位置未定；資訊負擔主要扣在 14 條左側長出線及手機分段；教學扣在多段操作和右圖對應表仍待核對。這不代表已達交付品質。

交叉讀 A 後補充：上表「機台 MOVE / Lot_id」不是只接 Move 歷史的二端關係；該菱形還連 `Siview.FHOPEHS_S`，完整布局必須保留此第三端點與原線。所有菱形均依模型完整端點抽取，不能照表格簡寫重建圖。
