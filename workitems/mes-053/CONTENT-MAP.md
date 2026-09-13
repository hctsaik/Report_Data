# 現有內容與建議課綱對照

此為 MES-053 設計映射，尚未改動網站。單元編號依 [總建議第6節](DESIGN-RECOMMENDATIONS.md#6-建議課綱能力與先備先於檔案)。主歸屬不限制其他課引用；有主題或圖片不等於能力教學已完成。

## 現有頁面

| 入口 | 現有用途 | 建議歸屬及處理 |
|---|---|---|
| index.html | Fab／Wafer／FOUP／Slot／Lot、互動、自測 | 單元1；另建總覽，保留原錨點 |
| operations.html | 設備、搬送、配方、加工與六情境 | 拆入3、4及6；情境依先備重排 |
| flow.html | Flow到版本與十情境 | 基礎入2；例外入5、歷程與拆合批入6 |
| freshness.html | 來源架構、時間、資料契約與情境 | 1起即引入時間觀念，完整深化入8 |
| advanced.html | QTime、Future Hold、PART、Recipe、Flow教法比較 | 2/3/5；教法比較移導師資源 |
| support.html | CW、Sub Route、Move、MON/PM/EMS | 3/5/6；不維持增補雜項集合 |
| er-atlas.html | 完整ER、局部主詞、題目、專屬圖 | 共用資料參考與各單元局部入口 |
| integrated-map.html | 轉址 er-atlas | 保留 query/hash 相容性 |
| data-map.html | 七張原圖與導讀 | 來源參考，從整合ER可回查 |
| subject-er.html | 主詞及分支閱讀 | 先盤功能差異再整併；不另養一套定義 |
| ER/NEW/index.html | 原圖入口 | 原始來源保留，退出新手必經路線 |

## 主題 registry：逐項歸屬

執行時 `ER_TOPIC_CONTENT.topics` 共38項，以下全部對應；不等於全站只有38個概念，也不包含 ER內建主題及其他課的所有子題。refs為現有原圖識別，保留供稽核。

| topicId | 現有主題 | 主歸屬 | 原圖 refs | 處理 |
|---|---|---|---|---|
| `future` | Future Hold：先登記，到指定事件才攔截 | 5 | 2673:future、2673:future-link | 沿用定義與現有教材，補先備／任務／返回 |
| `lotstep` | Lot Step：查這一批的站點歷史 | 6 | 2672:summary、2672:step | 歷史對象與時間清楚；與現在狀態分開 |
| `contents` | FOUP 內容物歷史：那個時間裝了哪些 Wafer | 6 | 2671:slot | 歷史對象與時間清楚；與現在狀態分開 |
| `available` | 帶到：Lot 在這個站點有可用機台 | 3 | 2671:lot-eqp | 沿用定義與現有教材，補先備／任務／返回 |
| `load` | 裝載關係：Lot、Wafer 與 FOUP | 1 | 2671:cast-link、2676:cast-lot | 沿用定義與現有教材，補先備／任務／返回 |
| `move` | Move：每次進機一筆，按日看表現、按 Lot 查站點 | 6 | 2672:move、2672:move-link、2675:move-link | 沿用定義與現有教材，補先備／任務／返回 |
| `transfer` | 傳送歷史：presum 後的 FOUP 搬運資料 | 4 | 2672:mes-transfer、2672:transfer | 沿用定義與現有教材，補先備／任務／返回 |
| `prehistory` | 預派歷史：讓機台預先知道接下來的 Lot | 4 | 2672:predispatch、2672:pre-link | 沿用定義與現有教材，補先備／任務／返回 |
| `actions` | 批貨歷史：記錄每個 Lot 的各種動作 | 6 | 2672:all-actions、2672:history、2675:all-actions | 沿用定義與現有教材，補先備／任務／返回 |
| `wip` | WIP 快照：每天早上 07:20 的機群與 KPI | 8 | 2675:lot、2675:wip-link、2675:wip-history | 分別說明目前來源與KER_WIP_Y_BTH每日07:20；不暗示粒度相同 |
| `oee` | KER：最近一次更新與每小時歷史指標 | 8 | 2675:eqp-oee-link、2675:eqp-oee、2675:group-oee-link、2675:group-oee、2675:group-history-link、2675:group-history | 沿用定義與現有教材，補先備／任務／返回 |
| `chamber` | Chamber：機台內的加工腔體 | 3 | 2674:chamber-link、2674:chamber、2674:detail-link、2674:chamber-detail、2676:chamber | 沿用定義與現有教材，補先備／任務／返回 |
| `port` | Load Port：等待加工與完成後的暫置位置 | 3 | 2671:port-link、2671:port、2671:has、2674:port、2674:port-link、2676:port、2676:port-id | 沿用定義與現有教材，補先備／任務／返回 |
| `portdata` | Port 衍生設定（已撤下教學） | 撤下 | 2674:udata、2674:udata-link、2676:udata | 維持撤下；不重新加入課綱 |
| `portmode` | Port 模式：UP 有貨，LOST 沒有貨 | 4 | 2674:mode、2674:mode-link | 沿用定義與現有教材，補先備／任務／返回 |
| `location` | 載具與機台的位置關係 | 4 | 2671:location | 沿用定義與現有教材，補先備／任務／返回 |
| `bay` | EQP Bay：機台所在的 Fab 走道與管理單位 | 8 | 2674:bay、2674:bay-link、2677:bay、2677:location | 沿用定義與現有教材，補先備／任務／返回 |
| `eqpstatus` | 設備狀態：讀取機台與狀態時間 | 3 | 2674:eqp-history、2674:history-link、2675:status、2675:status-link、2677:status | 沿用定義與現有教材，補先備／任務／返回 |
| `group` | KER：機台與 Chamber 的分群對應 | 8 | 2675:eqp、2675:group-link、2675:chamber、2675:chamber-link | 沿用定義與現有教材，補先備／任務／返回 |
| `virtual` | KER：User 用 SQL 自訂虛擬 Tool Group | 8 | 2675:virtual、2675:virtual-link | 沿用定義與現有教材，補先備／任務／返回 |
| `stock` | Default STK：機台的預設 FOUP 倉儲 | 4 | 2674:default、2674:default-link | 沿用定義與現有教材，補先備／任務／返回 |
| `ohb` | OHB：機台附近的 FOUP 暫置架 | 4 | 2674:ohb-link、2674:ohb-eqp、2674:ohb-status-link、2674:ohb-status | 沿用定義與現有教材，補先備／任務／返回 |
| `part` | PART：產品對應 Flow，進版同步記錄 | 2 | 2673:part、2673:part-link | 沿用定義與現有教材，補先備／任務／返回 |
| `pd` | PD：Process Definition，站點的細部加工定義 | 3 | 2673:pd、2673:pd-eqp、2673:pd-eqp-link、2673:pd-link、2677:pd、2677:pd-key、2677:pd-eqp | 沿用定義與現有教材，補先備／任務／返回 |
| `recipegroup` | Recipe Group：彈性控制多台或單台機台的加工許可 | 3 | 2673:recipe、2673:recipe-link | 沿用定義與現有教材，補先備／任務／返回 |
| `producthold` | Product Hold：同產品的 Lot，到指定站點暫置 | 5 | 2673:product-hold、2673:hold-link | 沿用定義與現有教材，補先備／任務／返回 |
| `forecast` | 未來的 Flow：用 Flow 與 IE WPH 預估各站到站時間 | 7 | 2673:forecast、2673:forecast-link | 沿用定義與現有教材，補先備／任務／返回 |
| `stage` | Module → Stage → Step：從加工模組看到細部步驟 | 2 | 2673:stage、2673:stage-link | 沿用定義與現有教材，補先備／任務／返回 |
| `srts` | SRTS：Flow 站點的 Sampling rule 與抽測比例 | 5 | 2673:srts、2673:srts-link | 沿用定義與現有教材，補先備／任務／返回 |
| `material` | 以 FOUP 為主詞：查詢裝載的 Lot | 1 | 2671:material、2671:material-link | 沿用定義與現有教材，補先備／任務／返回 |
| `lotstatus` | Lot Process／Status：RQHBE 五種狀態 | 3 | 2676:status | 沿用定義與現有教材，補先備／任務／返回 |
| `mcs` | MCS 傳送歷史：Macro 與 Micro command | 4 | 2672:mcs-transfer、2672:mcs-history | 沿用定義與現有教材，補先備／任務／返回 |
| `stream` | Stream：Flow × IE WPH 預估到站 | 7 | 2673:stream、2673:stream-link | 標示已由LDS取代，留單元7歷史參考 |
| `owner` | 機群與課別：由機台查管理歸屬 | 8 | 2674:owner、2674:owner-link | 沿用定義與現有教材，補先備／任務／返回 |
| `bmir` | BMIR：OHB 空位時，呼叫 RTD 計算下一批貨 | 4 | 2674:bmir-link、2674:bmir | 沿用定義與現有教材，補先備／任務／返回 |
| `flowkey` | Lot 與 Flow：沿 Part／Mainpd_id 找流程 | 2 | 2673:flow-link | 沿用定義與現有教材，補先備／任務／返回 |
| `eqpkey` | EQP_ID：在這条資料路徑中識別機台 | 3 | 2676:eqp-id、2677:eqp-id | 沿用定義與現有教材，補先備／任務／返回 |
| `retired` | 原圖待校正關係：Lot 裝載與 Step 歷史須分清 | 來源參考 | 2672:cast-link | 原圖校正追溯，不作正確關係教學 |

## ER 內建與跨課概念

| 概念 | 主歸屬 | 注意 |
|---|---|---|
| Lot／carrier／Wafer／Slot | 1 | 沿用25槽與多Lot互動；不是38項registry的完整替代 |
| equipment | 3 | EQP、Port、Chamber角色；与設備狀態分清 |
| flow | 2 | 最小流程模型前移，保留版本語境 |
| recipe／LR／ER／Physical | 3 | 與PD相接，分層展開；ER縮寫依上下文明示 |
| predispatch | 4 | 與可用設備、到位及進機分開 |
| qtime | 5 | 明示計時起迄事件、Lot與站點 |
| wph | 7 | 預期產出標準；預測不是實績 |
| overview／source fallback | 0及來源參考 | 是導引及未知節點處理，不當作專屬內容覆蓋證明 |
| CW／MON／PM／Daily MON／EMS | 3、5支線 | 材料用途與設備條件，避免只因同在support而綁同章 |
| Rework／Sub Route | 5、6 | 路徑許可與實際事件分開 |
| Split／Merge | 6，1先教成員概念 | 保留Wafer譜系，不把換載具等同拆批 |
| Finished／本站完成／E出貨 | 3、6 | 明示完成範圍，不直接合併 |
| 來源新鮮度／晚到／混合時間Join／資料契約 | 8，前課漸進引入 | 每次查詢就問時點，不等資料章才提醒 |

## 遷移檢核

建議實作前建立機器可驗證的 lessonId/topicId/舊URL/新URL/先備/資產/來源對照，逐節而非只有逐HTML。此文件已覆蓋現有入口及38項registry的主歸屬；尚未提供所有旧錨點轉址契約，也未宣稱完成全量圖片品質稽核。

每次遷移核對：舊連結可達、專屬圖未錯配、有效文字和廠內確認一致、課程到ER再回來有脈絡、案例片數與時間範圍一致。未確認或原圖保留項必須有清楚狀態。
