# MES-014 獨立覆核：完整性與安全合併

Reviewer：merge_rules agent；2026-09-13。依本輪製作前固定 ER_REVIEW_RUBRIC.md。此為重畫後覆核，不引用上輪摘要當完成證據。

## 實際覆核範圍

讀取 ER/NEW/transcription.json 全七圖，逐項對照 ER/NEW/2671.svg 至 2677.svg 的文字；再對照 ER/INTEGRATED/er-model-v1.json 及 fab-er-v1.svg 的節點、文字、形狀類別、邊端點。另讀 er-atlas.html/js 與 verification.json。實看本輪 fab-er-v1.png、load-1440.png、recipe-390.png；沒有把這三張當成所有視覺狀態皆已人工評分。

## 完整性：35 / 35

- 原始 128 個節點逐一可透過 mapping 找到唯一 canonical node，且該 node 實際存在於 SVG，不只是 JSON。
- 128 條原始邊逐條用 source/index 找到對應，再查 canonical 端點與 SVG data-a/data-b，一致，無漏邊或多出無來源邊。
- 所有原始 labels 與 refs 一致；原七張 SVG 亦實際含有 transcription 的文字。整合 SVG 長表名有換行，將連續 text 拼合後，128 個節點的所有原始文字均可找到；沒有將換行誤報為遺漏。
- 128 原始節點合為 119 個可見節點；8 組合併共減少 9 個節點。SIVIEW.FRLOT 合三個出現位置，其餘合併各兩個。
- 原矩形、菱形、圓形類別保留；未觀察到箭頭／額外主題摘要盒取代 ER。

## 語意正確：22 / 25（網站修正前）

安全合併覆核通過：SIVIEW.FRLOT、SIVIEW.FRCAST、SIVIEW.FREQP、F12DM.DM_MOVE_STEP_BTH、SIVIEW.FHOPEHS_S、F12DM.DM_FLOW_LR_EQP_BT、MFG_EQP_BAY_BT、FREQP。完整名只作大小寫正規化；未列 schema 的 FREQP 與 SIVIEW.FREQP 分開。SYSTEMKEY、EQP_ID 菱形未按同名全域合併。FRCAST_LOT 保留原菱形與表名，沒有抹去中介關係。FRLOT 與 KER_WIP_BT、預派與位於、LR 配置與實際 Physical Recipe 的差別有保留。

發現必修網站語意缺陷：er-atlas.js 的 inspect(ids) 在每兩項間都插入「— 原圖連線 —」，但 selectNode 的 ids 可能是一個分支／星狀鄰接集合，不是連續路徑。以點選 2676:eqp-id 為例，程式會列：

`EQP_ID → FREQP → FRPORT → FRCAST → FRPRCRSC`

逐項以 canonical edge 集合檢查，只有第一對存在，其餘三對均無原始邊。SVG 本身仍正確；錯誤發生在右側「這一段關係」閱讀清單。這會讓學員以為不同資料表直接相連。固定 routes 目前是線形因此未觸發，點節點或搜尋才觸發。

建議 inspect 接受真實 edge 列表，以「端點 A — 關係 — 端點 B」或分支樹展示；不要把鄰接節點清單串成偽路徑。修正後須針對 EQP_ID 三分支及高 degree 節點驗證。此項依 rubric 憑空關係的否決精神，修正前不建議整體交付。

## 可讀性、教學操作：不提供完整分數

只實看上述三張畫面。桌面 load 聚焦可清楚看到 Lot、裝載關係、FOUP；手機 recipe 聚焦圖內文字很小，頁下清單較可讀，但這不能替代完整手機互動驗證。總覽確實是結構索引，不應宣稱縮圖內每個表名都可直接閱讀。節點遮擋／曲線穿越、全部 17 段與 5 題之視覺品質留由另位 reviewer 覆核，未以自動 PASS 代替人工評分。

## 結論

圖面資料完整性成立，合併規則保守且可追溯。現時網站的分支關係清單存在具體語意錯誤，須修正後再決定是否交付。本覆核不給總分，不以 35/35 完整性推論整體品質達標或使用者驗收。

## V2 定向複核（保留上方 V1 原判斷）

覆核新版 er-model-v2.json、fab-er-v2.svg 及 er-atlas.js，另以 Python Playwright 直接開啟目前 4175 的 er-atlas.html；沒有只相信作者驗證結果。

- 重新逐項比對 128 個來源節點的 mapping、refs、類別及 SVG 可見文字；128 條來源邊的來源編號、端點與實際 SVG 元素全部一致，零差異。
- 現有 121 個 canonical nodes。六組合併均為完整帶 schema 同名表；原 V1 的無 schema FREQP 及 MFG_EQP_BAY_BT 已依來源拆開。保守拆分沒有丟失關係或製造跨圖 Join。
- 原圖独立小字 siview.fhwlths 已記入 sourceNotes，並由 inspector 顯示相關來源註記，不加上一條原圖不存在的線。
- 直接在桌面 1440 與手機 390 瀏覽器，各對全部 121 個節點呼叫 selectNode，檢查所有 .edge-pair 的兩端皆有實際 model edge，並檢查 getWalk 每一對連續節點皆為實際 edge：兩個尺寸均零錯誤。
- 實際派送 Enter 鍵事件到 2676:eqp-id SVG 節點，取得九步 DFS 路線：hub → FREQP → hub → FRPORT → hub → FRCAST → hub → FRPRCRSC → hub。再點下一點確認標示推進。每次轉向都回到真正的共同 hub，V1 的偽路徑問題已修正。
- inspect 現在按真實邊輸出配對，不再把分支資料硬串成線形關係。沿線閱讀的前後步屬於瀏覽動作，原圖仍沒有製程方向箭頭。

V2 定向評分：完整性 **35/35**；語意正確 **25/25**。此處滿分僅表示本 reviewer 覆核的兩項在本版具完整可反查證據，沒有推論實際資料庫 schema、逐表 freshness 或 SQL Join 已經驗證。V1 發現的網站語意否決項解除。

仍不給整體總分：完整手機／桌面視覺可讀性、曲線穿越及全部教學狀態由其他 reviewer 評估。此次未新增全畫面視覺審美評分，也未宣稱使用者已驗收。
