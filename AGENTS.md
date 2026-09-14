# MES-057 ER 頁面重製

主詞與搜尋集中、總圖提前顯示、圖例/來源說明收合、解說快速跳轉。一般ER不再誤歸單元8，questions仍保留。343回歸及23專項通過，證據tests/evidence/mes-057；讀workitems/mes-057/REVIEW.md。原SVG/JSON未變。使用者審閱pending，不宣稱品質分數。

# MES-056 ER上下版面

所有ER介紹採上總圖／下關聯與教學，選主詞自動放大置中；全圖按鈕保留介紹，回目前主詞恢復聚焦。手機不倒序。沿線點選也同步下圖。觸控pointerup時不可立即捲頁，避免相容click誤觸工具列。讀workitems/mes-056/REVIEW.md；check.py共343項通過，證據tests/evidence/mes-056。原SVG/JSON不變；implement.py與sync_walk.py為一次性工具，不重跑。使用者審閱pending。

# MES-055 指定頁面視覺與解說補強

已重整 index#foup/#slot/#lot/#explore、topic load，補 flowkey/available/eqpstatus/eqpkey/location/lotstep/contents 專屬圖文。參考 material；10張新圖在 assets/mes-055。lesson-refresh 與 topic-refresh 為本輪入口，後者須在 er-teaching-base 後、topic/er-atlas 前載入。load 互動需先展開 refresh-lab。讀 workitems/mes-055/REVIEW.md；檢查 check.py、audit.py、regression.py。149項功能檢查通過，26視圖證據位於 tests/evidence/mes-055。使用者審閱 pending，不宣稱品質分數。

# MES-054 全站課程架構已實作

入口learning.html；index無錨點轉總覽，旧教材錨點相容。共用catalog十單元/三路線、五現場任務、獨立topic與ER共用定義、統一site-shell導航/來源返回/前後教材/進度。讀workitems/mes-054/REVIEW.md及TEST-REPORT.md。檢查workitems/mes-054/check.py、check_lab.py、check_journeys.py、check_topics.py、check_persistence.py。原ER保留，FRPORT_UDATA不回課綱，Stream歷史註記。244頁面操作、132情境狀態、92主題視圖已驗證；真人學習效果與使用者審閱pending。一次性integrate/refine/extract/finish腳本不重跑。

# MES-053 全站架構四角色審查

使用者要求 Multi-agent 以新手工程師、Data Scientist、現場工程師、導師完整審查網站並寫Markdown。已完成，主文件 workitems/mes-053/DESIGN-RECOMMENDATIONS.md，逐項映射 CONTENT-MAP.md，四份ROLE報告及REVIEW.md。十入口雙尺寸載入，代表首屏實看；課末循環與ER返回往返實測見 tests/evidence/mes-053。建議循序/任務/ER三入口共用內容，先做Lot未進機原型。本輪只審查與文件，網站未重構，真人學習效果未驗證。設計審閱pending，不把建議當實作完成；一次性finish_docs.py不重跑。

# MES-052 四主題八張教學圖

BMIR、Port UP／LOST、Lot RQHBE、KER_WIP_Y_BTH 每日07:20快照，已補專屬桌機／手機圖。每日快照路徑與執行時圖面標籤已修正，原始ER保留。FRPORT_UDATA維持撤下教學。讀 workitems/mes-052/REVIEW.md；驗證 python workitems/mes-052/check.py，KER回歸 python workitems/mes-050/check.py。證據 tests/evidence/mes-052；使用者審閱 pending。一次性 integrate.py、fix_snapshot.py、finish_docs.py 不重跑。

# MES-051 廠內定義補充

BMIR：OHB 空時呼叫 RTD 計算下一批上架貨。Port UP有貨/LOST無貨。Lot R加工中/Q等待/H待確認/B長期暫置/E已出貨。KER_WIP_Y_BTH每天07:20機群與KPI快照（取代每週一）。FRPORT_UDATA撤下教學文字，原ER保留。文字已更新，尚未新增這些主題插圖。

# MES-050 KER 圖文已更新

依已確認定義製作分群/SQL/目前與歷史總覽，三主題十二引用同步。讀 workitems/mes-050/REVIEW.md；驗證 python workitems/mes-050/check.py。公式暫不處理，使用者審閱 pending。

# MES-050 KER 定義確認

使用者已確認 KER 多重機群對應、Chamber 獨立分群、User SQL 虛擬分群、最近一次更新與每小時歷史。先讀 workitems/mes-050/KER-DEFINITIONS.md。EFF 公式及彙總方式使用者指示先不處理；本輪僅記錄，未製作圖文或修改網站。

# MES-049 OHB

OHB 為機台鄰近 FOUP 暫置架，遠端 Stocker 先搬至鄰近暫放以方便後續快速搬運。雙尺寸圖文及設定/狀況四引用已更新，BMIR 分離。讀 workitems/mes-049/REVIEW.md；驗證 python workitems/mes-049/check.py。使用者審閱 pending。

# MES-048 Default Stocker

機台預設 Stocker（FOUP 倉儲）專屬雙尺寸圖文已更新，設定與位置/搬送分清。讀 workitems/mes-048/REVIEW.md；驗證 python workitems/mes-048/check.py。使用者審閱 pending。

# MES-047 機群與課別

MFG_EQP_OWNER_BT 專屬圖文已補：由機台查機群、管理單位及廠商名稱。owner 映射與一般 group 分開。讀 workitems/mes-047/REVIEW.md；驗證 python workitems/mes-047/check.py。使用者審閱 pending。

# MES-046 PART 與 Flow 版本

產品/PART 對應 Flow，進版時同步記錄版本資訊。專屬雙尺寸圖文已更新。讀 workitems/mes-046/REVIEW.md；驗證 python workitems/mes-046/check.py。使用者審閱 pending。

# MES-045 SRTS 抽測規則

使用者確認 SRTS 定義 Flow 站點 Sampling rule 與比例，例如 Part 抽檢30%。專屬雙尺寸圖文已更新，不臆測抽樣單位。讀 workitems/mes-045/REVIEW.md；驗證 python workitems/mes-045/check.py。使用者審閱 pending。

# MES-044 Module／Stage／Step

使用者確認 Module 如黃光，包含多個 Stage，每個 Stage 包含細部 Step。雙尺寸圖文及 Lot 歸屬對照已更新。讀 workitems/mes-044/REVIEW.md；驗證 python workitems/mes-044/check.py。使用者審閱 pending。

# MES-043 Recipe Group

群組包含可做類似加工的機台，依產品/加工條件切換多台或單台加工許可。專屬雙尺寸圖文已更新。讀 workitems/mes-043/REVIEW.md；驗證 python workitems/mes-043/check.py。使用者審閱 pending。

# MES-042 未來的 Flow

Lot forecast 專屬圖文已補：Flow 站序加 IE WPH 耗時估算，逐站預計到站。未套用 Stream 的 LDS 替代標記。讀 workitems/mes-042/REVIEW.md；驗證 python workitems/mes-042/check.py。使用者審閱 pending。

# MES-041 Stream 到站預估

Flow 站序與 IE WPH 耗時估算的專屬圖文已更新，標明舊功能由 LDS 取代。Stream 與一般 forecast 映射分離。讀 workitems/mes-041/REVIEW.md；驗證 python workitems/mes-041/check.py。使用者審閱 pending。

# MES-040 Product Hold

PID 依產品與站點設定管制，同產品 Lot 各自到站暫置以便統一處理。專屬桌面／手機圖文已更新。讀 workitems/mes-040/REVIEW.md；驗證 python workitems/mes-040/check.py。使用者審閱 pending。

# MES-039 Move 進機事件

每次 Lot 與機台進機記一筆；每日廠區統計與 DM_MOVE_STEP 按 Lot 追站點。專屬圖文與連結教學同步。讀 workitems/mes-039/REVIEW.md；驗證 python workitems/mes-039/check.py。

# 最新接續：MES-038 批貨歷史

FHOPEHS_S依使用者確認記錄每Lot所有動作，含Hold/進機Process/拆批。actions專屬圖文在assets/mes-038，並列非事件順序，不把全部動作算Move。讀workitems/mes-038/REVIEW.md，驗證python workitems/mes-038/check.py。

# 最新接續：MES-037 預派歷史

CSFHPREDISP兩節點補專屬圖文：實際執行前派工系統產生預派，讓機台先知道下一Lot，預派不等於開工。assets/mes-037，詳workitems/mes-037/REVIEW.md，驗證python workitems/mes-037/check.py。

# 最新接續：MES-036 FOUP查Lot

使用者确认FRLot_MtrlContnrs—FrlotMtrl—Frlot與FRCAST—FRCAST_LOT—FRLOT裝載概念相同，此處FOUP為查詢主詞。兩material節點專屬圖文更新，不推表可互換。讀workitems/mes-036/REVIEW.md，驗證python workitems/mes-036/check.py。

# 最新接續：MES-035 Load Port暫置

Port依使用者定義為等待加工/加工後暫置；載FOUP、晶圓在FOUP內。七來源與路徑補機台/OHT/Wafer/Load Port專屬圖文，assets/mes-035。讀workitems/mes-035/REVIEW.md，驗證python workitems/mes-035/check.py。

# 最新接續：MES-034 EQP Bay走道

EQP Bay是機台所在Fab走道，供查位置與管理單位（使用者確認）。四Bay來源專屬圖文在assets/mes-034，PHASE與欄位對應不猜測。讀workitems/mes-034/REVIEW.md，驗證python workitems/mes-034/check.py。

# 最新接續：MES-033 原始/presum傳送

MFG_Carrier_Te_Ut為presum過的傳送，MCS為原始歷史（使用者確認）。四傳送節點補專屬比較插圖及各自說明，assets/mes-033。MCS互動保留，不推定presum算法。讀workitems/mes-033/REVIEW.md，驗證python workitems/mes-033/check.py。

# 最新接續：MES-032 Chamber完整教材

Chamber五來源補operations.html#chamber與#tool入口，既有桌面/手機專屬圖及腔體狀態/細部/逐片說明。讀workitems/mes-032/REVIEW.md，驗證python workitems/mes-032/check.py。

# 最新接續：MES-031 MCS Macro/Micro

使用者定義Macro為E2E，Micro細至各軌道轉彎處。MCS專屬說明與四時間位置互動圖已更新，MES傳送不混用；不推定兩個MCS表分別等於巨觀/微觀。讀workitems/mes-031/REVIEW.md，驗證python workitems/mes-031/check.py。

# 最新接續：MES-030 Lot與Wafer

使用者確認同FOUP可多Lot，也可單Lot25片，每片不同Wafer ID/Slot。Lot/FOUP/裝載三入口改專屬25槽互動示例，er-lot-wafer.js/css。讀workitems/mes-030/REVIEW.md，驗證python workitems/mes-030/check.py。旧測試要求Lot通用照片/空白topic-detail已過時，不重跑integrate.py。

# 最新接續：MES-029 PD Process Definition

使用者確認PD為每站細部加工定義，理解為站內Recipe與Tool關係。七PD節點與路徑已補專屬圖文，圖在assets/mes-029。讀workitems/mes-029/REVIEW.md，驗證python workitems/mes-029/check.py。不能再將PD全名列未確認，不能推定實際執行或額外Join。

# 最新接續：MES-028 閱讀歷程返回

Multi-agent審查後新增er-navigation.js、er-return.js。右側/放大圖可返回，保留主詞、關係組、逐點/縮放；七主要教材頁帶返回ER來源。讀workitems/mes-028/REVIEW.md及MULTI_AGENT_REVIEW.md，驗證python workitems/mes-028/check.py。不要重跑一次性integrate.py。使用者審閱pending。

# 最新接續：MES-027 預派目標是機台

小圖已撤下預派—FOUP直接支線，Lot—預派—EQP唯一目標；FOUP經裝載關係連Lot。來源模型不改名。詳workitems/mes-027/REVIEW.md，驗證python workitems/mes-027/check.py。此校正取代MES-023預派三端舊期望。

# 最新接續：MES-026 主詞教材不可套 FOUP

已修節點與18閱讀路徑的配對，121節點明確映射；Future Hold／QTime各有專屬圖文，其他主題按語意介紹，未配對不得回退FOUP。Future Hold手機直向圖 assets/mes-026。讀 workitems/mes-026/REVIEW.md，驗證 python workitems/mes-026/check.py。品質未自動評分，使用者審閱pending；不是每個主題都有新插畫。一次性integrate.py不重跑。

# 最新接續：MES-025 Qtime與Lot

Qtime/站點節點已接完整原來源鏈到Lot：Qtime—Qtime站點—LotStep—Summary—Lot。專屬Qtime說明與桌面/手機圖替換FOUP位置圖，明示30分鐘為示例，附起訖事件/歷史判讀及advanced.html#qtime入口。入口er-atlas.html?subject=qtime。驗證python workitems/mes-025/check.py；讀REVIEW。

# 最新接續：MES-024 Lot Step包含Lot

Lot Step歷史首要關聯為Lot—站點Summary/Lot_id—Step歷史，全部是原始來源邊。FOUP圖保留裝載→Lot→Summary→Step完整鏈，不恢復已撤下2672:cast-link。新增subject=lot-step入口。讀workitems/mes-024/REVIEW.md；驗證python workitems/mes-024/check.py。

# 最新接續：MES-023 Lot預派機台

使用者確認預派以Lot為主要對象，派工系統預先安排目標機台，FOUP輔助。右側加入Lot業務虛線（非已確認Join），Lot/EQP优先；專屬桌面／手機圖在assets/mes-023。入口er-atlas.html?subject=predispatch。測試python workitems/mes-023/check.py，讀REVIEW。不要以舊來源邊唯一規則刪除使用者已確認的業務邊；須保留provenance。

# 最新接續：MES-022 FOUP內容物歷史

使用者確認Siview.fhwlths記錄FOUP在各時間點放了哪些Wafer，每次Split／Merge進FOUP時更新。不是單純在Slot的目前位置。主圖、小圖、路徑與說明已校正，詳workitems/mes-022/REVIEW.md；驗證python workitems/mes-022/check.py。原來源校正前文字保留稽核。

# 最新接續：MES-021 帶到／可用機台

使用者校正2671:lot-eqp不是預到而是帶到，代表Lot在這個站點有可用機台。不得再解釋預派、预計到達或已開始加工。主圖顯示、小圖、路徑解釋及主題頁已更新；原始來源檔保存校正前文字供稽核。讀workitems/mes-021/REVIEW.md；驗證python workitems/mes-021/check.py。

# 最新接續：MES-020 展開右側

右側頂部新增展開整區按鈕，圖與說明共同進入大視窗，收回或Escape返回；保留主詞與分頁。實作inspector-expand.js，驗證python workitems/mes-020/check.py。詳workitems/mes-020/REVIEW.md；證據tests/evidence/mes-020。

# 最新接續：MES-019 機群 WPH

已依使用者確認：WPH由生產管理部門為每個機群定義，表示預期每小時晶圓產出量。不是個別機台實測或百分比。新專屬參考圖在assets/mes-019，桌面／手機各一；2673:wph和wph-link明確映射。入口er-atlas.html?view=original&subject=wph。讀workitems/mes-019/REVIEW.md；驗證python workitems/mes-019/check.py。舊來源IE文字不自行展開，原model保留來源。

# 最新接續：MES-018 裝載關係校正

使用者否定 FOUP — Lot在Foup內/Siview.frcast — Step歷史支線；主詞小圖已雙向撤下2672:cast-link。正確裝載是Lot — 放在/Siview.Frcast_lot — FOUP（2671）。原始SVG/model保留稽核，不能把來源存在當教學正確。讀workitems/mes-018/REVIEW.md；驗證python workitems/mes-018/check.py；新證據tests/evidence/mes-018。

# 最新接續：MES-017 主詞關聯小圖

選主詞後右側重排真正關聯 ER，原圖維持全圖定位。讀 workitems/mes-017/REVIEW.md、AGENT_SEMANTIC.md、AGENT_LAYOUT.md。驗證 python workitems/mes-017/check.py 與 regression.py；證據 tests/evidence/mes-017。來源沒有 Wafer，不補造；同一 entity 可在不同支線重複呈現，桌面四支線／手機兩支線。手機觸控重排後的相容 click 不得二次誤選。原 SVG/model 不改；使用者審閱 pending。一次性 integrate.py/refine.py 不重跑。

# 最新接續：MES-016 ER 直接點擊與右圖同步

使用者指出點 ER 圖右圖沒有更新。已用真實 mouse/touch 測試五類節點，增加小節點命中容差、避免點擊微移變成拖曳，右图同步選取名稱與圖面焦點。不能只用 ER_ATLAS.selectNode() 測試宣稱點擊有效。驗證 python workitems/mes-016/check.py，證據 tests/evidence/mes-016。閱讀 workitems/mes-016/REVIEW.md。一次性 fix.py/finish.py 不重跑。

# 最新接續：MES-015 全圖框選與教學對照

入口維持 integrated-map.html?view=original，轉址 er-atlas.html。初始完整 ER；框選 Lot／FOUP／EQP／Flow／Recipe 主要位置，保留全部線，旁邊同步教學插圖。讀 workitems/mes-015/REVIEW.md。驗證 python workitems/mes-015/check.py。任意節點不可直接以顏色分類推斷教學圖；明確映射，否則顯示基礎參考。原 SVG 不變。使用者審閱 pending。

# 最新接續：MES-014 v2 整合 ER

使用者要求重畫並畫後Multi-agent評分，已完成兩輪。er-atlas.html及ER/INTEGRATED/fab-er-v2.svg是新主圖；integrated-map.html保留舊入口轉址。來源128節點／128邊映到121實際節點／128線，六組已列schema同表合併。未知schema不合併；關係菱形與鍵完整，沒有20主題卡。固定色彩圖例、長路徑90%逐點閱讀。先讀workitems/mes-014/REVIEW.md及三份AGENT報告。v1語意77／視覺78退回；v2兩位均91，專項完整35/35語意25/25，使用者審閱pending。測試python tests/check_er_atlas.py。不要重跑一次性refine/connect/final_touch腳本。主圖不放來源編號。

# 最新接續：MES-013 設計審查

使用者指出20主題卡失去ER概念，明確要求Multi-agent思考畫法。三位agent已只讀審查；結論見 workitems/mes-013/MULTI_AGENT_DESIGN.md。本輪未修改網站。MES-012是語意摘要，未滿足整合ER要求；下一版保留具體實體、關係菱形、關係表與鍵，合併經核對的重複資料對象；題目只高亮同一張ER的既有路徑。先驗中央Lot／FOUP／EQP片段，不能再用20主題卡替代ER。原圖編號只放詳情，不回到主圖。

# 最新接續：MES-012

使用者要求跨七張圖整合，不能再一張圖等於一課。入口 integrated-map.html，SVG與索引在 ER/INTEGRATED。20共同主題，128原節點／128原連線可追溯；大圖是語意摘要，不是逐節點完整SQL ER。先讀 workitems/mes-012/CONTENT.md、REVIEW.md。驗證 python tests/check_integrated_map.py；五個跨圖題目與原圖／聚焦雙入口。原七張圖不變。course.js 的 aside-foot 是使用者實際找入口的位置，必須一起維護。使用者審閱pending。

# 最新接續：MES-011

七張已校字 ER 圖已整合到 data-map.html，七節各兩案例，含逐點讀圖、聚焦、縮放及原圖連結。先讀 workitems/mes-011/REVIEW.md。驗證 python tests/check_data_map.py；七張 SVG 原檔 hash 保持不變。不要重跑 integrate.py、refine.py 等一次性修改工具。使用者審閱 pending，不宣稱品質評分達標。最新廠內定義：AVL 是期間 Availability 比率、Lost 是閒置、UP 是正在加工；Eff 公式、AVL 分子分母仍未確認。此段取代下方舊段落中這三項「未確認」的狀態。

# 最新接續：MES-010

已新增 support.html 四節：CW、Sub Route（加量＝追加量測，回原站）、Move（Lot 過站事件，重工計入）、MON／PM／Daily MON／EMS。先讀 workitems/mes-010/CONTENT.md、PLAN.md、REVIEW.md。驗證 python tests/check_support.py：154項通過。使用者驗收 pending；AAA 及 AVL／Eff／Lost／Up 定義未確認。advanced.html 僅新增入口，其餘既有前端以歷史 hash 核對。舊 manifest 不再代表本輪修改後的共用文件，不覆寫歷史證據。

# 最新接續：MES-009

本輪新增 advanced.html：QTime、Future Hold、Part／RouteId、LR／ER／Physical，以及原版＋三種 Flow 候選。先讀 workitems/mes-009/PLAN.md、CONTENT.md、REVIEW.md。檢查 python tests/check_advanced.py（90項）。使用者選版 pending，Part／LR／ER 的內部字典 pending；頁面已明示教學假設。新圖 assets/mes-009，原 stage-v2.png 保留。MES-008 入口與新鮮度資產未改，root 共用文件新增內容後，其旧 manifest 不再代表當前全部文件。不得重跑舊生成器覆蓋新內容。

# 最新接續：MES-008

先讀 workitems/mes-008/PLAN.md 及 TEACHING_REVIEW_LOG.md 最新段。使用者再次退回資料新鮮度，MES-007 新鮮度的頁面／圖像高分與通過判斷已撤回。MES-007 manifest 是歷史版本快照；本輪修改後不要求它與新 freshness 檔相同，不覆寫歷史 hash 掩蓋差異。新證據用 tests/evidence/mes-008。前三課本輪不改。沿用使用者重製授權，必須實際改網頁與圖，不只寫反省。MES-008六節與12張主圖已更新，逐頁評比見 workitems/mes-008/REVIEW.md、review.json。驗證 python tests/check_freshness_v2.py；封存一致性 python tools/verify_mes008_evidence.py。使用者審閱 pending。

# MES 教學製作的接續規則

先讀 CLAUDE.md、IMAGE_STYLE_GUIDE.md、TEACHING_WEBPAGE_GUIDE.md、TEACHING_SCORING_RUBRIC.md、TEACHING_REVIEW_LOG.md 與 WORKITEMS.md 最新段落。

歷史版本 MES-007：使用者授權重製15頁並新增資料新鮮度。先讀 workitems/mes-007/PLAN.md、REVIEW.md 與 evidence-manifest.json。新主插畫在 assets/mes-v3；freshness.html 為第四課。MES-004品質通過已撤回，不作完成依據；MES-006為歷史比較基準。MES-007使用者審閱仍 pending。

使用者第二次指出品質失敗。不得再以部分圖片評分或功能 PASS 宣稱整批教學完成。每個指定 URL 是獨立驗收單位；lab 還須覆蓋全部情境的可見狀態。每頁與每張主圖分開記錄實際桌面／手機證據、分項分數、缺口、修正。未看寫未評估，不能自動填分。

歷史MES-007證據檢查為 `python tools/verify_mes007_evidence.py`，不適用MES-008的新鮮度檔案；它只查範圍、資產與證據一致，不自動評品質，不代表使用者核准。舊 MES-004 validator 不適用新版本。任何共享渲染程式改動後，舊截圖須重驗，不能繼續使用過時證據。
