# 主詞關聯小圖

- MES-038：FHOPEHS_S MUST 介紹為每Lot所有動作歷史，含Hold/進機Process/拆批；分類圖不表示必然順序，所有歷史筆數不得當Move數量。

- MES-037：CSFHPREDISP教材 MUST 表達機台執行前的預派安排，讓機台先知道接下來Lot並能回查歷史；不得將預派存在當開工或最終必執行。

- MES-036：FRLot_MtrlContnrs—FrlotMtrl—Frlot MUST 教為FOUP主詞查Lot的裝載關係，與FRCAST—FRCAST_LOT—FRLOT相同業務概念；不得以概念相同推定資料表可直接互換。

- MES-035：Port教材 MUST 說明等待加工與加工後等待搬離的暫置用途，圖示機台/OHT/Wafer/Load Port；OHT搬FOUP，晶圓不直接放平台，位置不推定加工完成。

- MES-034：EQP Bay MUST 解釋為機台所在Fab走道，供查位置及所屬管理單位；不得由走道推同一管理歸屬或臆測PHASE欄位含義。

- MES-033：MFG_Carrier_Te_Ut MUST 解釋為presum過的傳送資料，MCS為原始傳送歷史；兩者以FOUP搬運為共同概念，各自補圖文，不推定presum演算法或保留所有原始細節。

- MES-031：MCS教材 MUST 分Macro E2E與Micro各段軌道/轉彎命令，用同FOUP時間位置說明追查；命令目的地不得視為已確認到達，兩歷史表的層級對應不得臆測。

- MES-030：Lot/FOUP/裝載教材 MUST 分清Lot歸屬與Wafer身分及Slot位置；展示同FOUP多Lot與單Lot25片兩個例子，不能推定FOUP與Lot一對一，也不能把25片視為所有Lot固定數量。教學Wafer示意不冒充原ER新增資料表。

- MES-029：PD MUST 依使用者定義解釋為Process Definition，每站細部加工定義與Recipe／Tool關係；專屬教材 MUST 區分定義與實際執行。不可從業務概念新增未核對的資料表Join。

- MES-028：主詞／路徑／框選切換 MUST 提供歷程返回與全圖出口，恢復關係組、逐點位置、縮放與閱讀狀態。最近瀏覽路徑 MUST 明示為瀏覽歷程，不當成資料階層。放大圖返回與關閉 MUST 分開。教材／來源跨頁 MUST 提供返回原ER主詞入口；無來源上下文不得假造上一頁。

- MES-027 使用者校正：預派的目標 MUST 是 EQP；小圖 MUST 雙向撤下預派—FOUP 直接支線。Lot 主詞 MUST 呈現 Lot—預派—EQP；FOUP 透過 FRCAST_LOT 連接 Lot。此條取代 MES-023 將 FOUP 直接呈現在預派根節點下的做法，來源模型保留追溯。

- MES-026：節點與閱讀路徑的介紹 MUST 明確按來源引用配對；不得以顏色、未匹配 fallback 或不相關路徑自動套用 FOUP 總覽。QTime 與 Future Hold MUST 各自介紹，切換時清除上一主題圖文。未確認內部字典 MUST 明示限制；沒有合適插圖時隱藏插圖，不借別題填空。手機 Future Hold 使用直向圖。

- 在完整 ER 選 Lot、FOUP、EQP、Flow、Recipe、任意節點或搜尋結果時，旁邊 MUST 按所選實體重新排版關聯 ER。
- 小圖 MUST 保留來源實體、關係菱形／鍵與真實連線，不推定 PK/FK、基數、事件方向。
- 概念入口 MUST 使用明確主要來源；同名但未知 schema 節點不可默默合併。
- Recipe MUST 可讀到 SYSTEMKEY、FRMRCP_EQP、EQP_ID 與 FREQP 完整配置鏈。
- 多分支 MAY 分頁，但 MUST 明示範圍與其餘分支入口；不得宣稱已包含所有間接關係。
- 小圖節點 MUST 能切換主詞。手機 MUST 另排可讀圖形，提供放大檢視。
- 清除選取 MUST 清除小圖；左側完整原 SVG 與既有路徑入口保留。
- 驗證 MUST 包含真實滑鼠／觸控與每個主詞的桌面／手機證據。功能檢查不等於品質分數或使用者核准。

- MES-018 使用者校正：主詞小圖 MUST 撤下 2672:cast-link 的 Step 歷史支線，Lot 裝載 MUST 使用 2671:lot — 2671:cast-link（Siview.Frcast_lot）— 2671:cast。不得僅因歷史來源有邊就認定其教學語意正確。

- MES-020：右側 MUST 提供整區展開，包含圖與說明；收回或Escape MUST 還原側欄並保留主詞、分頁及原說明收合狀態。既有單圖放大可在展開區內操作。

- MES-023 使用者補充：預派圖 MUST 包含Lot及EQP為主要關聯、FOUP為輔助。Lot—預派機台連線作已確認業務補充，以虛線及provenance明示，MUST NOT 冒充原始來源邊或已驗證Join鍵。專屬圖解釋派工系統預先安排Lot目標機台，不表示已到站或加工。


- MES-039：Move 每次進機一筆，專屬圖文說明廠區每日統計及依 Lot 查 DM_MOVE_STEP 站點歷程。

- MES-040：Product Hold 說明 PID 設定產品與站點條件，同產品 Lot 各自到站暫置、等待統一處理，保留來源 Lot_ID 關係與專屬雙尺寸插圖。

- MES-041：Stream 專屬圖文說明 Flow 站序、IE WPH 速率換算耗時、逐站預估到站，註明由 LDS 取代；一般 forecast 不套用替代註記。

- MES-042：Lot forecast 圖文依 Flow 站序與 IE WPH 預估後續各站到站時間，保留 Lot_ID／OPE_NO 上下文，不沿用 Stream 的替代註記。

- MES-043：Recipe Group 圖文包含機台群、依產品或加工條件控制多台/單台許可，区分設備能力與當前許可，不推定控制優先權。

- MES-044：Module（如黃光）包含多個 Stage，每個 Stage 包含細部 Step；專屬圖文用巢狀框表示，Lot 依目前 Step 對照 Stage 與 Module。

- MES-045：SRTS 定義 Flow 站點的 Sampling rule 與 Part 抽測比例，教學以30%示範；抽樣單位及選取方式依規則，不推定為每批晶圓比例。

- MES-046：PART 對應產品的 Flow/Route，以 Mainpd_id 對照來源；Flow 進版時 PART 同步記錄版本資訊，不推定在製 Lot 自動切版。

- MES-047：MFG_EQP_OWNER_BT 透過 EQP_ID 查機台管理單位、機群名稱與廠商資訊；專屬圖文區分管理歸屬與廠商。

- MES-048：Default STK 為機台預設 Stocker（FOUP 倉儲），圖文以設定對應呈現，不代表實際位置或搬送紀錄。

- MES-049：OHB（Over Head Buffer）為機台附近簡易 FOUP 暫置架，方便從遠端倉儲預先就近暫放並於後續搬運；區分對應設定與狀況資料。

- MES-050：KER 圖文包含機台多重分群、Chamber 獨立分群、User SQL 虛擬群組、最近一次更新及每小時機台/機群歷史；本輪不展開指標公式。


# MES-052 四主題八張教學圖

BMIR、Port UP／LOST、Lot RQHBE、KER_WIP_Y_BTH 每日07:20快照，已補專屬桌機／手機圖。每日快照路徑與執行時圖面標籤已修正，原始ER保留。FRPORT_UDATA維持撤下教學。讀 workitems/mes-052/REVIEW.md；驗證 python workitems/mes-052/check.py，KER回歸 python workitems/mes-050/check.py。證據 tests/evidence/mes-052；使用者審閱 pending。一次性 integrate.py、fix_snapshot.py、finish_docs.py 不重跑。

