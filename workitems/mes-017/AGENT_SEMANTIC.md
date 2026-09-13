# MES-017 語意設計審查

本報告依 ER/INTEGRATED/er-model-v2.json、er-atlas.js、MES-015／016 REVIEW 查核。屬於來源及設計審查，不代表瀏覽器操作或視覺驗收已通過。

## 決策

右圖以所選 canonical entity 為中心重新排版。保留實體、關係菱形、關係表、鍵與來源邊；右图不是既有全圖裁切，也不是現場插圖。所有 ref 必須經 model.mapping 解到既有節點，顯示邊必須存在於 model.edges。

同名不同 schema 不合併。2671/2672/2673:lot 共用 t_cfc81de70314；2671/2672:cast 共用 t_55072ef91a15；2671/2674:eqp 共用 t_7f282520afb8。2676、2677 未指定 schema 的同名節點仍是獨立來源物件。主詞按鈕採主要來源，其他框選位置應按實際點選節點另建小圖。

## 五類核心路徑

以下每列路徑中的未重複 source 前綴沿用該列第一個 ref。應保留入選節點間所有真實來源邊，不能只保留方便畫圖的一條。

| 主詞 | 核心來源路徑 |
| --- | --- |
| Lot | 2671:lot → cast-link → cast；lot → slot → cast；lot → lot-eqp → eqp；lot → port-link → port → has → eqp |
| FOUP | 2671:cast → cast-link → lot；cast → slot → lot；cast → location → eqp；cast → predispatch → eqp |
| EQP | 2671:eqp → lot-eqp → lot；eqp → location → cast；eqp → predispatch → cast；eqp → has → port；2674:eqp → chamber-link → chamber → detail-link → chamber-detail |
| Flow | 2673:flow → flow-link → lot；flow → lr-eqp-link → lr-eqp；flow → lr-link → lr；flow → pd-link → pd；flow → part-link → part；flow → stage-link → stage |
| Recipe | 2677:recipe → recipe-key → recipe-eqp → eqp-id → eqp |

Flow 擴充包含 flow → srts-link → srts 及 flow → recipe-link → recipe。此 recipe 是 Recipe Group，不是 2677 的 FRMRCP。2673:lr 與 lr-eqp 是同一 canonical 節點，但兩個關係菱形仍須保留。

## 不可誤導的邊界

- 來源沒有 Wafer entity。若教學需要晶圓，可以另外明示教學補充，不可捏造來源 ER 的 Wafer 節點、表名或連線。
- FOUP 所在位置、預派工、Lot 預派工、Slot 是不同關係；不能改成不帶名稱的線，更不能推論正在加工。
- Recipe 需要通過 FRMRCP_EQP 這個矩形中介表繼續到 EQP_ID 與設備。固定兩條原始邊的遍歷會過早停止。
- 2677:eqp-id 是連接 pd-eqp、recipe-eqp、bay、eqp 的 junction；保留菱形，不能捏造任意兩端的直接外鍵關係。
- Siview.Port 與 SIVIEW.FRPORT 不合併。KER_WIP_BT 與 Siview.FRLOT 也不合併。
- LR／ER 配置不等於某批 Lot 實際使用的 Physical Recipe。
- 核心模式應明示是聚焦子圖，其他直接關聯可展開；避免把顯示上限誤呈現為完整資料模型。

## 靜態驗證建議

1. 五個核心集合每個 ref 都可解析；每個指定相鄰 pair 都是來源真實邊。
2. 每個輸出節點 id 都存在於 model.nodes，每條輸出邊 id／端點皆與 model.edges 一致；不產生 Wafer 假表。
3. 每張子圖連通，中心存在；所有輸出邊的兩端均在子圖內；source refs 與 labels 沿用原模型。
4. Lot 核心至少含 FRLOT、FRCAST、FREQP、Port，且 cast-link／slot、location／predispatch 等並行語意不被合併。
5. Recipe 核心含完整五節點鏈及四条真實邊；同名且未知 schema 的 secondary roots 維持不同 id。
6. 全部 121 個來源節點可生成合法聚焦圖；特殊 circle／diamond 點選不得被無依據映射成 Lot。

上述檢查只驗證來源完整性；需要真實 mouse／touch 點擊加桌面與手機截圖才能驗證網站互動和可讀性。

## 實作來源審查

已讀取新 er-focus.js，並以 Node VM 直接執行實際 collect 函式，針對 121 個來源節點逐一檢查所有輸出路徑的中心、節點／邊數及相鄰端點。共 431 次來源邊出現均與 model.edges 對應，未發現假造節點或假邊。五類支線數：Lot 15、FOUP 7、EQP 12、Flow 8、Recipe 2；Recipe 保留 recipe → recipe-key → recipe-eqp → eqp-id → eqp 的四邊完整鏈。這是資料層靜態驗證，不是瀏覽器證據。

現行實作選擇「以中心展開關係支線、每頁四條」，而非把所有入選節點的所有關係合成單一 induced subgraph。一般支線遇到第一個非菱形節點即停止；進一步關係由讀者點該節點切換主詞，Recipe 則明確補完整設備鏈。因此 Lot 圖可能有 FOUP 與 EQP，但不會同時顯示 FOUP → 所在位置 → EQP，不能宣稱右圖保留這些端點之間的每條來源邊。

同一 canonical entity 可能因不同支線重複繪出（例如 Lot 的 FOUP 裝載與 Slot 支線、Flow 的兩條 LR 支線）。建議在圖說標示「同一實體可在不同支線重複出現」，以免讀者誤認為兩個不同資料物件。主詞頁列出支線數及分頁，沒有把四條畫成全部關聯。
