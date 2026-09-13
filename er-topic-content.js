/* Explicit source references, never colour/category inference. */
window.ER_TOPIC_CONTENT = (() => {
 const topics = {};
 function add(key, refs, title, meaning, steps, takeaway, link) {
  topics[key] = {refs:refs.split(' '), title, meaning, color:'#52728e',
   details:'<h3>'+title+'</h3><ol class="topic-reading">'+steps.map(s=>'<li>'+s+'</li>').join('')+'</ol><p class="topic-takeaway">'+takeaway+'</p>', link};
 }
 add('future','2673:future 2673:future-link','Future Hold：先登記，到指定事件才攔截',
  'Future Hold 是對 Lot 預先登記的管制條件。當這個 Lot 到達指定站點與觸發事件時，才依規則形成有效 Hold；登記存在不代表現在已被 Hold。',
  ['教學示例：Lot L023 在 S20 登記「S50 進站前 Hold」。','經過 S40 時，尚未到達這筆預約的觸發點；其他加工條件仍須滿足。','到 S50 的指定進站事件時攔截，等待覆核；解除這筆 Hold 後，仍須檢查其他管制。'],
  'Future Hold 看「指定事件是否到達」；QTime 看「起訖事件間經過多久」。兩者要分開判讀。','advanced.html#future-hold');
 Object.assign(topics.future,{image:'assets/mes-009/future.png',alt:'Lot L023 在 S20 登記、經 S40、到 S50 進站前觸發 Future Hold 的教學示例',caption:'教學示例：先登記 → 尚未觸發 → 指定事件攔截。實際站點、進出站事件與解除條件依廠內規則。'});
 add('lotstep','2672:summary 2672:step','Lot Step：查這一批的站點歷史',
  'Lot Step 歷史以 Lot 為主詞。先確認是哪一批，再對照它的站點紀錄；來源以站點 Summary／Lot_id 連接 LOT 與 F12DM.DM_Lot_step_st。',
  ['確認 Lot：同一個 FOUP 可能在不同時間承載不同批次。','查這個 Lot 的站點紀錄，對照站點與紀錄時間。','若有重工或重複經過同站，須區分事件，不把同站名當成同一次加工。'],
  '用 Lot 串起歷程；FOUP 只能提供載具上下文。');
 add('contents','2671:slot','FOUP 內容物歷史：那個時間裝了哪些 Wafer',
  'Siview.fhwlths 記錄 FOUP 內容物（Wafer）的歷史：在什麼時間點，這個 FOUP 放了哪些 Wafer。每次 Split／Merge 進 FOUP 時更新。',
  ['先選 FOUP 和要回查的時間。','找該時間點的 Wafer 內容物紀錄。','對照 Split／Merge 前後的內容物變化，追查晶圓的批次歸屬。'],
  '歷史內容物須帶時間查詢，不能當成目前槽位快照。');
 add('available','2671:lot-eqp','帶到：Lot 在這個站點有可用機台',
  'Siview.Frlot_EQP 表示這個 Lot 在目前站點有可用機台的關係。',
  ['先確認 Lot 所在站點。','查該站點對這批 Lot 的可用機台集合。','派工系統再安排目標；是否已到機台或開工，另查實際事件。'],
  '本站可用、預先派工、實際加工，是三個不同問題。');
 add('load','2671:cast-link 2676:cast-lot','Lot 與 FOUP：生產批次和載具的裝載關係',
  'FRCAST_LOT 連接 Lot 與 FOUP。Lot 表示生產批次，FOUP 是承載晶圓的實體容器。',
  ['以 Lot 找目前相關載具。','沿 FRCAST_LOT 讀取裝載關係，再找 FOUP。','回查過去裝了哪些 Wafer 時，改查帶時間的內容物歷史。'],
  '裝載關係要連到 Lot 和 FOUP 兩端。');
 add('move','2672:move 2672:move-link 2675:move-link','Move：Lot 的過站事件',
  'F12DM.DM_Move_Step_bth 是 Lot 的 Move 歷史。Move 計算 Lot 過站事件，重工過站也計入；FOUP 搬運次數不能代替 Move 次數。',
  ['確認 Lot 與查詢期間。','逐筆辨識過站事件，重工返回同站後再次過站仍須保留。','連接其他歷史資料後，檢查是否把同一事件重複計數。'],
  '搬了一次載具，不代表完成一次過站。','support.html#move');
 add('transfer','2672:mes-transfer 2672:transfer 2672:mcs-transfer 2672:mcs-history','載具傳送歷史：追查搬運工作',
  '傳送歷史以 Carrier 為主詞。MES 傳送紀錄與 MCS 工作歷史是不同資料來源；MCS 關係列出 Carrier_id 與 transfer_job_id。',
  ['確認是哪個載具和哪段時間。','以來源提供的載具／工作識別追查搬運工作。','對照工作事件及設備位置；需要 Lot 過站結果時，另查 Move。'],
  '傳送工作、實際到位、Lot 過站須各自有紀錄支持。');
 add('prehistory','2672:predispatch 2672:pre-link','預派歷史：回查 Lot 當時被安排到哪裡',
  'Siview.CSFHPREDISP 保存預派歷史，來源以 Lot_ID 關係連接 Lot。它描述派工安排的歷程。',
  ['指定 Lot 及回查時間。','讀取當時的預派紀錄，區分不同次安排。','若要知道最後在哪台加工，對照實際加工紀錄。'],
  '歷史預派目標不能直接當成實際加工機台。');
 add('actions','2672:all-actions 2672:history 2675:all-actions','Lot 動作歷史：追查批次發生的事件',
  'Siview.FHOPEHS_S 由 Lot_ID 關係連回批次，提供 Lot 動作／過貨歷史的查詢上下文。',
  ['選定 Lot 和時間範圍。','依事件種類與時間閱讀歷程。','計算 Move 時，要先確認哪些事件符合過站定義，不能把所有動作都算入。'],
  '同一 Lot 可以有多筆不同動作；事件種類要先分清。');
 add('wip','2675:lot 2675:wip-link 2675:wip-history','WIP：在製批次與固定時間快照',
  'KER_WIP_BT 是此來源的 Lot／WIP 資料；KER_WIP_Y_BTH 每天早上 07:20 保存機群狀況與 KPI 快照。',
  ['先選現在的在製資料，或某次歷史快照。','確認快照時間，再看該時間點有哪些 Lot。','跨期間比較時使用一致時間基準，不把歷史快照當成現在庫存。'],
  'WIP 回答某時點的在製狀況；Move 回答期間發生的過站事件。');
 add('oee','2675:eqp-oee-link 2675:eqp-oee 2675:group-oee-link 2675:group-oee 2675:group-history-link 2675:group-history','OEE 資料：先分機台、機群與統計期間',
  '此來源分別列出機台 OEE 歷史、機群目前 OEE 與機群歷史資料。必須配合各自的關聯鍵與統計期間閱讀。',
  ['先看選的是機台還是機群，不混用 EQP_ID 與 EQP_GRP。','對齐統計時間與資料更新時間，再比較數值。','廠內已確認：UP 是正在加工、Lost 是閒置、AVL 是期間 Availability 比率；Eff 公式及 AVL 分子分母尚待確認。'],
  '即時狀態、期間比率與生產管理定義的 WPH 不能互相代替。');
 add('chamber','2674:chamber-link 2674:chamber 2674:detail-link 2674:chamber-detail 2676:chamber','Chamber：機台內的加工腔體',
  'Chamber 是設備內的加工資源。來源將機台、Chamber 狀況與 Chamber 細部資料分開，不能只由整台機台的狀態推定每個腔體都可用。',
  ['先確認 EQP，再辨認該台的 Chamber。','對照腔體識別與細部資料；來源列出 eqp_id／procrsc_id 關係。','判斷可用性時讀取該腔體的狀態與時間。'],
  '機台與腔體是不同層級，狀態也要分開查。','operations.html#chamber');
 Object.assign(topics.chamber,{image:'assets/mes-v3/chamber-v1.png',mobile:'assets/mes-v3/chamber-mobile-v1.png',alt:'同一片 Wafer W06 從 FOUP 取出、經搬送手臂、進入 CH-A 加工腔體的三個連續時點',caption:'單片加工教學示例：同一片 W06 從 FOUP 交接到 CH-A。三格是不同時點；進入腔體的是晶圓，不是整個 FOUP。一片的加工結果不能代表整個 Lot。'});
 topics.chamber.details+='<h3>Chamber 是什麼？</h3><p>Tool／EQP 是整台設備；Chamber 是其中執行製程的腔體。設備可以有多個腔體，晶圓經設備內部交接進入適用的腔體加工。實際結構與加工方式依設備而異，不能把所有機台都想成相同的單片設備。</p><h3>為什麼要查腔體自己的狀態？</h3><p>教學示例：同一台 ETCH-03 的 CH-A 正在加工 W06，CH-B 處於維護狀態。只看到整台設備正在運作，仍無法推定 CH-B 能接工作；需要對照指定腔體的狀態、時間及適用條件。</p><h3>這張 ER 怎麼讀？</h3><p>先用 eqp_id 確認機台；Chamber 狀況節點列出 Siview.csfrprcrsc／SIVIEW.FHCSCHS，細部資料則沿 eqp_id／procrsc_id 連到 Siview.frprcrsc。保留設備與腔體識別的上下文；各狀態碼、時間欄位及表的詳細用途須依內部字典確認。</p><h3>腔體空了，Lot 就完成了嗎？</h3><p>不一定。單片加工時，兩片之間腔體可以暫時沒有晶圓，但同一 Lot 還可能有其他片等待加工。要逐片核對 Wafer 的結果，再確認這批在本站的完成條件。</p><p><a href="operations.html#tool">先讀：設備、交接位置與腔體的關係 →</a></p>';
 add('port','2671:port-link 2671:port 2671:has 2674:port 2674:port-link 2676:port 2676:port-id','Port：設備與載具的交接位置',
  'Port 是設備的交接位置。先以 EQP 識別機台，再辨認 Port；Lot 與 Port 的來源關係列出 FREQP_LOT。',
  ['確認設備是哪一台。','在該設備下辨認 Port，不能只憑 LP1 等局部名稱跨機台合併。','需要了解當下裝載或作業狀態時，再對照該時間的紀錄。'],
  'Port 是位置；載具在位置上，也不等於 Lot 已開工。','operations.html#port');
 add('portdata','2674:udata 2674:udata-link 2676:udata','Port 細部資料：沿位置識別讀取補充資訊',
  'FRPORT_UDATA 是 Port 的細部資料；已列 schema 的來源透過 D_THESYSTEMKEY 連接 Port。',
  ['先辨認設備與 Port。','沿來源的 D_THESYSTEMKEY 關係讀取细部資料。','個別欄位的用途須依內部字典確認，不能從 UDATA 名称猜值。'],
  '同名表未列 schema 時，保留來源差異。');
 add('portmode','2674:mode 2674:mode-link','Port 模式：位置上的作業設定與紀錄',
  '來源以 EQP_ID／PORT_ID 連到機台模式，並列出 CSFRPORT_SUBMODE 與 FHEMCHS。',
  ['鎖定機台和 Port。','對照模式資料與其時間上下文。','模式代碼的允許行為要查廠內定義，不直接等同「可以加工」。'],
  '位置、模式與加工狀態須分開閱讀。');
 add('location','2671:location','載具與機台的位置關係',
  'Siview.CSFHDOPHS 以 eqp_id 表達 FOUP 與設備的位置關聯。',
  ['辨认 FOUP 與相關設備。','核對資料時間，確認是在查現在還是歷史位置。','要判斷已加工，仍需該 Lot 的加工事件。'],
  '位置關係本身不證明晶圓正在加工。');
 add('bay','2674:bay 2674:bay-link 2677:bay 2677:location','設備位置：查 EQP 所屬區域',
  'MFG_EQP_BAY_BT 提供設備位置的對照上下文；來源包含 EQP／LOCATION／PHASE 註記。',
  ['先辨認 EQP。','查設備對應的位置或區域資料。','追查晶圓在哪裡時，還需載具與位置紀錄，不能由設備區域直接反推 Lot。'],
  '設備所在區域與某批 Lot 的當前位置是不同問題。');
 add('eqpstatus','2674:eqp-history 2674:history-link 2675:status 2675:status-link 2677:status','設備狀態：讀取機台與狀態時間',
  '來源分別包含設備狀況歷史與目前狀況資料。閱讀狀態必須帶上設備識別及紀錄時間。',
  ['確認 EQP_ID。','分清目前狀況或某時刻的歷史狀况。','UP 代表正在加工；要算期間 Availability，需另外確認期間與計算口徑。'],
  '單一時刻的狀態不能代表整段期間效率。');
 add('group','2675:eqp 2675:group-link 2675:chamber 2675:chamber-link','機群：把設備或腔體依管理關係組織起來',
  '來源保留機群／課別、機群與機台、機群與 Chamber 等不同對應資料。EQP_GRP 表達群組層級。',
  ['先確認要查機群、機台還是腔體。','沿對應關係找群組成員，不把群組名稱當成單台設備。','套用機群 WPH 或彙總資料前，核對群組範圍與資料時間。'],
  '同一機群的預期產出定義與個別機台的實際狀態分開閱讀。');
 add('virtual','2675:virtual 2675:virtual-link','虛擬 Group：讀取群組成員的定義',
  'KER_VR_EQP_GRP_DETAIL_BT 是虛擬 Group 明細，來源以 DYNAMIC_SQL 標示成員判定關係。',
  ['選定虛擬 Group。','核對成員定義及其查詢條件。','統計前確認當次納入哪些設備；不能只凭 *ALL 字樣推定固定範圍。'],
  '虛擬群組的範圍須由實際定義確認。');
 add('stock','2674:default 2674:default-link','Default STK：設備的預設儲位關聯',
  'Siview.csfreqp_stk 透過 eqp_id 連接設備與 Default STK 設定。',
  ['找到設備。','沿設定關係確認預設 STK。','回查實際搬運目的地時，核對搬運工作紀錄。'],
  '預設設定不等於某一次載具已到達的位置。');
 add('ohb','2674:ohb-link 2674:ohb-eqp 2674:ohb-status-link 2674:ohb-status 2674:bmir-link 2674:bmir','OHB／BMIR：設備關聯、狀況與設定分開查',
  '此來源將 OHB 的設備對應、OHB 狀況及 BMIR 設定分開，以 EQPSTKID／OHB_ID 等關係串接。',
  ['先從設備關係找到對應的 OHB。','以 OHB_ID 對照狀況資料。','BMIR 的具體廠內含義與設定值尚需字典確認，不能從圖名推定搬運或放行結果。'],
  '設定資料和狀況資料用途不同，原圖關係不代表事件順序。');
 add('part','2673:part 2673:part-link','Part：產品定義與流程的對照',
  'Siview.frprodspec 保存 PART 定義；來源以 Mainpd_id 對應 Flow 相關資料。',
  ['辨認 Lot 所帶的 Part。','依 Part／Mainpd_id 關係找對應流程定義。','同時核對版本與適用範圍；Part 及 RouteId 的廠內細部字典仍須確認。'],
  '產品／流程定義與 Lot 實際走到哪站是不同資料。','advanced.html#part');
 add('pd','2673:pd 2673:pd-eqp 2673:pd-eqp-link 2673:pd-link 2677:pd 2677:pd-key 2677:pd-eqp','PD：Process Definition，站點的細部加工定義',
  'PD 是 Process Definition，也就是每一站的細部加工定義。可以把它理解為：這個站點裡面會使用的 Recipe（加工配方）與 Tool（機台）的關係。先找到站點，再透過 PD 理解這一站怎麼加工。',
  ['找站點：在 Flow 中確認要讀哪一站，再對照該站的 PD_ID。','讀 PD：理解該站的細部加工定義，以及其中 Recipe 與 Tool 的對應；PD 本身是定義，不是某批 Lot 的加工紀錄。','對照實際執行：要知道某批 Lot 這次到底用了哪台 Tool、哪支 Recipe，仍須查看該次執行紀錄。'],
  'PD 定義這一站怎麼加工；實際用了什麼，要看執行紀錄。','#selection-details');
 Object.assign(topics.pd,{image:'assets/mes-029/pd-definition-v2.png',mobile:'assets/mes-029/pd-definition-mobile-v1.png',alt:'站點 S20 透過 PD-A 理解 Recipe R-A 與 Tool ETCH-03 的加工定義關係；教學示例',caption:'教學示例：站點 S20 → PD-A → Recipe R-A 與 Tool ETCH-03。這是定義關係的概念示意，並非實際配置或 Lot 加工紀錄。'});
 topics.pd.details+='<h3>對照上方資料關係</h3><p>Flow 的站點以 PD_ID 對應 Process Definition；Siview.frpd 是圖中的 PD 資料，Siview.frpd_eqp 表達 PD 與機台的對應。另一來源以 SYSTEMKEY 串接 FRPD／FRPD_EQP，須保留各自的來源上下文。</p><p>Recipe 與 Tool 的業務概念依本次廠內定義說明；上方 ER 保留已提供的表與鍵，不因概念示意就新增未核對的 Recipe 資料表連線。</p>';
 add('recipegroup','2673:recipe 2673:recipe-link','Recipe Group：查看程式群組的對應',
  'Siview.CSFRRCPGRPST 是來源中的 Recipe Group 資料，連接群組對應的上下文。',
  ['先確認要查群組定義或單一 Recipe。','沿來源的群組關係讀取對應。','某批實際用了哪支 Recipe，需要另外核對執行紀錄及版本。'],
  '群組對應不能代替實際加工配方的證據。');
 add('producthold','2673:product-hold 2673:hold-link','Product Hold：沿 Lot 關係檢查產品管制',
  'Siview.CSFRPRHold 是 Product Hold 資料，來源以 Lot_ID 關係連回 Lot。它與 Future Hold 分列為不同管制資料。',
  ['確認是哪個 Lot 及對應產品。','查適用的管制條件、原因與有效狀態。','判斷能否放行時一併核對其他有效管制，不能只看這張表是否有紀錄。'],
  'Product Hold、Future Hold 與 QTime 要各自判讀。');
 add('forecast','2673:forecast 2673:forecast-link','未來站點與到站時間：讀取 Lot 的預測',
  'Lot forecast 與 Stream 到站時間透過 Lot_ID／OPE_NO 關係串接 Lot 和站點，提供未來流程的預估上下文。',
  ['指定 Lot 與要看的站點。','分清預測時間和實際事件時間，並核對預測更新時間。','要確認已到站或 QTime 是否超時時，使用實際對應事件。'],
  '預測到站不等於實際已到站。');
 add('stage','2673:stage 2673:stage-link','Stage／Module：流程中的分段定義',
  'F12dm.dm_tbl_info_stage 保存 Stage 與 Module 定義；來源將其與 Flow 連接。',
  ['先看整條 Flow。','依定義辨认站點所屬 Stage／Module。','再以 Lot 的站點資料定位進度，不能把段落定義當成加工紀錄。'],
  'Flow 是路線，Stage 是分段，Lot 進度要查實際站點。','flow.html#stage');
 add('srts','2673:srts 2673:srts-link','SRTS：流程相關設定',
  'Siview.csfrsrts 是來源中與 Flow 相連的 SRTS 設定資料；圖上標註設定關係。',
  ['先確認關聯的 Flow。','核對 SRTS 實際設定及適用範圍。','縮寫、欄位與規則作用須依廠內字典確認，不能由名稱猜出派工結果。'],
  '先讀設定的適用範圍，再對照執行結果。');
 add('material','2671:material 2671:material-link','物料容器關係：沿 Lot 查對應資料',
  '來源以 Siview.FrlotMtrl 關係連接 Lot 與 Siview.FRLot_MtrlContnrs；此容器資料與 FRCAST 分開保留。',
  ['先確認 Lot。','沿 FrlotMtrl 找物料容器對應。','物料容器的具體用途與欄位須核對內部字典，不能因顯示名稱同為 Foup 就合併表。'],
  '名稱相似不代表資料對象相同。');
 add('lotstatus','2676:status','Lot Process／Status：批次的作業狀態',
  '此節點是 Lot Process／Status 的概念註記，用來區分批次的作業狀態與裝載位置。',
  ['辨认 Lot。','查批次的作業狀態及時間。','需判斷開工或完成時，核對相應事件，而不是只看 FOUP 位置。'],
  '這是概念註記，原圖未給出一張可直接查詢的狀態表。');
 // MCS has its own confirmed command hierarchy; MES transfer stays separate.
 topics.transfer.refs=['2672:mes-transfer','2672:transfer'];
 add('mcs','2672:mcs-transfer 2672:mcs-history','MCS 傳送歷史：Macro 與 Micro command',
  'MCS 傳送命令分為 Macro command（巨觀命令）與 Micro command（微觀命令）。Macro 描述起點到終點的 E2E 搬運；Micro 展開沿途的細部移動，連軌道上的每個轉彎處都會定義。透過傳送命令及其時間、位置紀錄，可以回查同一個 FOUP 在什麼時候、所在何處，以及往哪裡移動。',
  ['先找 FOUP：依 Carrier_id 和要查的時間範圍，辨認這個載具的傳送工作。','看 Macro：確認這趟 E2E 搬運的起點與終點，避免把多趟工作混在一起。','展開 Micro：沿工作識別與關聯，按時間讀取各段軌道移動、轉彎位置與狀態，重建 FOUP 的移動過程。'],
  '命令告訴你要往哪裡；配合事件時間、位置與執行狀態，才能確認何時到了哪裡。');
 topics.mcs.details+='<table class="mcs-comparison"><thead><tr><th>層級</th><th>閱讀重點</th></tr></thead><tbody><tr><th>Macro command<br>巨觀</th><td>整趟 E2E：FOUP 從哪裡搬到哪裡。</td></tr><tr><th>Micro command<br>微觀</th><td>沿途每段移動與轉彎點：何時經過哪裡、下一段往哪裡。</td></tr></tbody></table><div id="mcs-command-demo"></div><h3>對照上方 MCS 歷史資料</h3><p>圖中列出 carrier_job_history@mcsdb、transfer_job_history@mcsdb，並以 Carrier_id／transfer_job_id 連回 FOUP。這些資料提供傳送工作的查詢上下文；兩張表如何分配 Macro／Micro 記錄、實際時間與位置欄位名稱，仍須依內部資料字典核對。</p><p>回查時要區分已發出、執行中、完成或其他狀態。尚未完成的命令目的地，不當成已觀測到的位置；載具傳送也不等於 Lot 的 Move 過站事件。</p>';
 Object.assign(topics.transfer,{
  title:'傳送歷史：presum 後的 FOUP 搬運資料',
  meaning:'MFG_Carrier_Te_Ut 是經 presum 的傳送資料；MCS 則是原始的傳送歷史。兩者概念相近，都是沿 FOUP 的搬運工作，查詢它在什麼時間、位於哪裡、移動到哪裡；閱讀時要分清原始紀錄與 presum 後的資料層次。',
  details:'<h3>MFG_Carrier_Te_Ut：看 presum 後的傳送</h3><p>先依 Carrier_id 確認 FOUP，再選要查的時間範圍，讀取 presum 後保留的傳送資訊。這裡的重點仍是同一個載具的搬運過程，並不是 Lot 的加工過站。</p><h3>和 MCS 原始歷史有什麼不同？</h3><p>MCS 原始歷史提供傳送命令的追查上下文，包括 Macro 的 E2E 與 Micro 的沿途移動。MFG_Carrier_Te_Ut 已經過 presum，不能直接假設每筆原始命令、每個轉彎細節都仍逐筆保留。</p><p>presum 的分組方式、保留欄位與更新時點須依內部規則確認；這裡不把 presum 自行解釋為固定筆數的加總，也不推定它和原始紀錄是一對一。</p><p class="topic-takeaway">查同一個 FOUP 的傳送，先辨認目前讀的是原始歷史，還是 presum 後的資料。</p>'
 });
 topics.mcs.meaning='MCS 是原始的傳送歷史；MFG_Carrier_Te_Ut 則是經 presum 的傳送資料。兩者都追查 FOUP 搬運，但資料層次不同。'+topics.mcs.meaning;
 topics.mcs.details='<h3>你現在看的是原始 MCS 歷史</h3><p>從同一個 FOUP 的工作與事件追查原始傳送过程。與 MFG_Carrier_Te_Ut 的 presum 資料相比，這裡著重命令、細部路徑、事件時間與位置的對照；presum 實際保留什麼，須另看其規則。</p>'+topics.mcs.details;
 for(const key of ['transfer','mcs'])Object.assign(topics[key],{image:'assets/mes-033/transfer-history-v1.png',mobile:'assets/mes-033/transfer-history-mobile-v1.png',alt:'FOUP F012 搬運形成 MCS 原始傳送歷史，並以 presum 整理資料層次對照 MFG_Carrier_Te_Ut 的概念示意',caption:key==='transfer'?'看圖右側（手機下方）：MFG_Carrier_Te_Ut 是 presum 後的傳送資料。保留的時間、位置與細節依 presum 規則；箭頭表示概念整理關係，不是已核對的 SQL 處理流程。':'看圖中間：MCS 是原始傳送歷史，Macro 看 E2E，Micro 追沿途各段與轉彎；右側對照 presum 後的資料。FOUP F012 為概念示例。'});
 Object.assign(topics.bay,{
  title:'EQP Bay：機台所在的 Fab 走道與管理單位',
  meaning:'EQP Bay 指機台放在 Fab 的哪一條 Bay，也就是哪一個走道。線上查詢時，可用機台識別找到所在位置，以及機台所屬的管理單位，方便找到設備並確認由誰管理。',
  details:'<h3>Bay 是機台所在的走道</h3><p>先辨認機台 EQP，再查它位於 Fab 的哪條 Bay。Bay 表達實體位置；管理單位表達負責歸屬，兩者應分開閱讀，不能只憑同一條走道就推定全部機台由同一單位管理。</p><h3>線上怎麼查？</h3><ol class="topic-reading"><li>輸入或選擇機台 ID，確認要找的是哪一台設備。</li><li>讀取 Bay／位置資訊，找到設備所在的走道。</li><li>確認這台機台的所屬管理單位，再依現場作業需要聯繫或查閱。</li></ol><h3>同一台機台的教學示例</h3><p>查 ETCH-03，結果顯示它位於 Bay B12，所屬管理單位為「設備管理 A 組」。這些名稱皆為示例，不是實際廠區配置。</p><p class="topic-takeaway">查機台，找到走道，也找到負責單位。</p><h3>對照上方資料關係</h3><p>MFG_EQP_BAY_BT 是圖中的設備位置資料；EQP／LOCATION／PHASE 是原圖保留的註記。管理單位的實際欄位與資料對應、PHASE 的廠內含義仍須依字典確認，不從名稱自行補成楼層、製程階段或管理單位。</p>',
  image:'assets/mes-034/eqp-bay-v1.png',mobile:'assets/mes-034/eqp-bay-mobile-v1.png',
  alt:'查詢機台 ETCH-03，找到 Fab 的 Bay B12 走道，再確認所屬設備管理 A 組的教學示例',
  caption:'同一台機台的查詢主線：EQP → Bay 走道 → 所屬管理單位。ETCH-03、Bay B12、設備管理 A 組均為示例，非實際廠區配置。'
 });
 Object.assign(topics.port,{
  title:'Load Port：等待加工與完成後的暫置位置',
  meaning:'Load Port 是機台前端的載具交接與暫置位置。載有 Wafer 的 FOUP 可以停在這裡等待加工；加工完成、晶圓返回 FOUP 後，也可暫置在這裡等待 OHT 搬離。放在平台上的是 FOUP，晶圓則在 FOUP 內。',
  details:'<h3>看懂圖中的四個角色</h3><ul><li><strong>機台／EQP：</strong>執行加工的設備，Load Port 是它的交接位置。</li><li><strong>OHT：</strong>沿上方軌道搬送 FOUP，送到 Load Port 或從這裡取走載具。</li><li><strong>Load Port：</strong>承接並暫置 FOUP，供等待加工或加工後等待搬離。</li><li><strong>Wafer：</strong>FOUP 裡的晶圓，加工時由設備內部交接；OHT 不直接搬裸晶圓。</li></ul><h3>同一個位置，可能在等不同的事</h3><ol class="topic-reading"><li>OHT 將 F012 送到機台 ETCH-03 的 LP1。</li><li>加工前，F012 停在 LP1 等待加工；Wafer W07 是容器內其中一片晶圓。</li><li>加工後，晶圓返回 FOUP，F012 仍可停在 LP1，等待 OHT 搬離。</li></ol><p>這是同一個載具在三個不同時點的教學示例；圖中略去設備內部加工過程。</p><p class="topic-takeaway">看到 FOUP 停在 Load Port，還要查作業狀態，才能分清正在等加工，還是已加工等待搬離。</p><h3>對照上方 ER</h3><p>先確認 EQP，再識別它的 Port。原圖以 eqp_id 連接機台，並以 Siview.Freqp_Lot 表達 Lot 與 Port 的相關上下文。Port 位置、FOUP 裝載與 Lot 作業狀態須分開閱讀；不能只憑位置推定加工已完成。</p>',
  image:'assets/mes-035/load-port-v1.png',mobile:'assets/mes-035/load-port-mobile-v1.png',
  alt:'機台 ETCH-03 的 Load Port LP1 承接 OHT 搬來的 FOUP F012；局部放大顯示內部 Wafer W07，對照等待加工與加工後等待搬離',
  caption:'同一載具的三個時點：OHT 送達 → Load Port 等待加工 → 加工後等待搬離。晶圓在 FOUP 裡；機台、LP1、F012、W07 均為教學示例。'
 });
 Object.assign(topics.material,{
  title:'以 FOUP 為主詞：查詢裝載的 Lot',
  meaning:'這裡也是 Lot 與 FOUP 的裝載關係，只是查詢主詞是 FOUP：先選一個 FOUP，再找出其中晶圓所屬的 Lot。FRLot_MtrlContnrs、FrlotMtrl、Frlot 這條路徑，與 FRCAST、FRCAST_LOT、FRLOT 表達相同的裝載概念。',
  details:'<h3>從 FOUP 出發怎麼讀？</h3><ol class="topic-reading"><li>先選要查的 FOUP，例如 F012。</li><li>沿「放在」的裝載關係，找出與這個 FOUP 關聯的 Lot。</li><li>讀取 Lot ID；同一個 FOUP 可裝一個 Lot，也可以有不同 Lot 的晶圓。</li></ol><h3>兩條路徑，相同裝載概念</h3><p>本圖：<strong>Siview.FRLot_MtrlContnrs → Siview.FrlotMtrl → Siview.Frlot</strong>。</p><p>另一組：<strong>FRCAST → FRCAST_LOT → FRLOT</strong>。</p><p>兩者都是連接 FOUP 與 Lot；這裡特別從 FOUP 查詢。概念相同不代表資料表、欄位或查詢條件可以直接互換，仍保留各自來源。</p><h3>Lot 是晶圓的歸屬，不是另一個容器</h3><p>示例中，F012 內的部分晶圓屬於 L023，另一部分屬於 L024，所以查到兩個 Lot。圖中顏色只區分批次歸屬，不表示品質或加工狀態；並不是在 FOUP 裡放兩個叫 Lot 的盒子。</p><p>如果要逐片確認，還要對照 Wafer ID 與所在 Slot。查歷史裝載時也要帶時間，不能把某次結果當成所有時間都不變的關係。</p><p class="topic-takeaway">從 FOUP 出發，找出其中晶圓所屬的 Lot。</p>',
  image:'assets/mes-036/foup-query-lot-v1.png',mobile:'assets/mes-036/foup-query-lot-mobile-v1.png',
  alt:'從 FOUP F012 查裝載關係，找到晶圓所屬 Lot L023 與 L024 的查詢示例',
  caption:'查詢示例：FOUP F012 → 裝載關係 → Lot L023／L024。箭頭表示查詢閱讀方向，不是搬運或 Split／Merge 事件；可查到一個或多個 Lot。'
 });
 Object.assign(topics.prehistory,{
  title:'預派歷史：讓機台預先知道接下來的 Lot',
  meaning:'在機台真正執行以前，派工系統會先產生預派，讓機台預先知道接下來預計加工的 Lot 是誰。Siview.CSFHPREDISP 保存預派歷史，來源以 Lot_ID 關係連接 Lot，供回查當時的派工安排。預派存在不代表已經開工。',
  details:'<h3>預派發生在實際加工之前</h3><ol class="topic-reading"><li>派工系統先安排預計加工的 Lot 與目標機台。</li><li>機台透過預派，預先知道接下來預計執行哪個 Lot。</li><li>之後可查 CSFHPREDISP 的歷史，了解當時曾做過的預派安排。</li></ol><h3>同一個 Lot 的教學示例</h3><p>派工系統將 Lot L023 預派到 ETCH-03，機台因此先知道接下來預計加工 L023；此時仍是預先安排，圖中明示尚未開工。L023 與 ETCH-03 均為示例。</p><h3>如何讀預派歷史？</h3><p>先確認 Lot_ID 與查詢時間，再對照當時的預派安排。要確認最後是否在該機台開工、何時開始或完成，仍需查看實際執行紀錄；不能把曾經預派當成最後一定執行。</p><p class="topic-takeaway">預派讓機台先知道下一個 Lot；是否開工另查執行紀錄。</p><p>上方 ER 保留 CSFHPREDISP 與 Lot_ID 的来源關係；下方圖表示業務概念，不額外推定資料表鍵或通知機制的技術細節。</p>',
  image:'assets/mes-037/predispatch-history-v2.png',mobile:'assets/mes-037/predispatch-history-mobile-v1.png',
  alt:'派工系統將 Lot L023 預派到 ETCH-03，機台先知道但尚未開工，再以 CSFHPREDISP 回查預派安排的示例',
  caption:'預派安排 → 機台預先得知 → 回查安排歷史。圖中是預先安排的概念示例，不是已開工或完成的加工紀錄。'
 });
 Object.assign(topics.actions,{
  title:'批貨歷史：記錄每個 Lot 的各種動作',
  meaning:'Siview.FHOPEHS_S 是批貨歷史，記錄每一個 Lot 發生的動作，包含 Hold、進機 Process、拆批 Split 等。以 Lot_ID 連回 Lot，可以回查這批曾發生哪些事情；它不只是加工過站的紀錄。',
  details:'<h3>哪些動作會留下紀錄？</h3><ul><li><strong>Hold：</strong>Lot 被管制的動作。</li><li><strong>進機 Process：</strong>Lot 進入機台加工相關的動作。</li><li><strong>拆批 Split：</strong>批次拆分的動作，追查晶圓批次歸屬的變化。</li><li><strong>其他 Lot 動作：</strong>依實際發生的作業留下歷史。</li></ul><p>這些是動作種類，不是每個 Lot 一定依序經歷的流程；不能把 Hold → Process → Split 當成固定順序。</p><h3>怎麼回查一批的經過？</h3><ol class="topic-reading"><li>先以 Lot_ID 指定批次，再選要查的時間範圍。</li><li>按紀錄時間閱讀各種動作，核對動作種類與相關內容。</li><li>追查拆批時，配合實際的批次關聯資料辨認涉及的 Lot 與 Wafer，不只看目前批次名稱。</li></ol><h3>批貨歷史與 Move 有什麼差別？</h3><p>批貨歷史涵蓋各種 Lot 動作；Move 著重加工過站事件。統計 Move 前必須選出符合定義的事件，不能把 Hold、Split 等所有歷史筆數都算成過站次數。</p><p class="topic-takeaway">批貨歷史記錄 Lot 的各種動作，不只加工過站。</p><p>上方保留 FHOPEHS_S 與 Lot_ID 的來源關係；實際動作代碼、時間欄位與內容格式依內部字典核對。圖中是教學分類示例，不是真實歷史紀錄。</p>',
  image:'assets/mes-038/lot-history-v2.png',mobile:'assets/mes-038/lot-history-mobile-v1.png',
  alt:'以 Lot L023 查批貨歷史，Hold、進機 Process、拆批 Split 及其他動作都會留下紀錄，動作種類非先後順序',
  caption:'Lot 動作分類示例：Hold、Process、Split 等記入批貨歷史。拆批圖只是晶圓重新分組的示意，片數不增加；圖中的種類排列不是事件時間順序。'
 });
 Object.assign(topics.move,{
  title:'Move：每次進機一筆，按日看表現、按 Lot 查站點',
  meaning:'依廠內定義，Move 計算 Lot 過站事件：只要機台與 Lot 發生一次進機事件，就記錄一筆。可按廠區與日期統計，觀察每天的製造表現；也可查 DM_MOVE_STEP，追蹤這個 Lot 經過哪些站點。',
  details:'<h3>一筆 Move 怎麼產生？</h3><p>Lot 與機台每發生一次進機事件就記一筆。同一 Lot 經過不同站點，或重工再發生進機事件，都可能產生新的 Move；統計的是事件，不是不同 Lot 的個數，也不是 Wafer 片數或 FOUP 搬運次數。</p><h3>用途一：看廠區每日製造表現</h3><p>以同一廠區、相同日期切分方式，統計當天符合定義的進機事件筆數，觀察每日製造能力的表現。比較時要維持一致的廠區範圍、日界線及事件口徑，避免 Join 造成同一事件重複計數。</p><p>Move 是實際作業量的觀察指標，不直接等於完成的晶圓數、良品數或理論最大產能。已記進機，也不能單憑這筆就推定加工完成。</p><h3>用途二：按 Lot 查經過哪些站點</h3><p>查 DM_MOVE_STEP 時，先選 Lot 與時間範圍，再依事件時間讀站點經過歷程；同一站若再次進機，要保留這次事件，不能只取不重複站名而丟掉重工歷程。</p><p>本圖來源完整名稱為 F12DM.DM_Move_Step_bth，以 Lot_id 連回 Lot。DM_MOVE_STEP 沿用本次查詢用語；實際物件名稱與欄位以內部字典確認。</p><p class="topic-takeaway">每次進機記一筆；按日看表現，按 Lot 追站點。</p>',
  image:'assets/mes-039/move-uses-v2.png',mobile:'assets/mes-039/move-uses-mobile-v2.png',
  alt:'Lot進機事件集合分別用於廠區每日Move統計與DM_MOVE_STEP按Lot追查站點的兩種用途',
  caption:'兩條查詢路徑都從進機事件集合出發：按廠區／日期統計，或按 Lot 回查站點。圖表高低、L023及S10／S20／S30均為示例，非實際產量與流程。'
 });
 Object.assign(topics.producthold,{
  title:'Product Hold：同產品的 Lot，到指定站點暫置',
  meaning:'當產品（Product）有問題時，產品工程師（PID）設定 Product Hold，讓屬於該產品的 Lot 各自到達指定站點時被攔住、暫置，方便後續統一處理。',
  details:'<h3>PID 設定的是產品與站點條件</h3><p>產品發生問題，需要對同產品的各批貨採取一致的處理時，PID 可設定 Product Hold：指定要管制的 Product，以及要暫置的站點。</p><h3>各批 Lot 到站時，套用同一條管制</h3><p>例如 Product P100 在 S20 站點受到管制。Lot L023 和 L024 都屬於 P100，因此各自走到 S20 時，都會被 Product Hold 攔住。兩批不必同時到站，也不必是相同的 Lot ID。</p><p>判讀時要同時看「Lot 屬於哪個 Product」與「是否到達指定站點」。這項設定是依產品條件管制符合的 Lot，不是把全廠所有產品都暫置。</p><h3>暫置後，方便統一處理</h3><p>PID 可確認受影響且已暫置的 Lot，統一評估後續處理。圖中的暫置狀態不代表已完成處置；後續如何解除或繼續加工，依實際處理決定。</p><h3>如何對照這張 ER？</h3><p>Siview.CSFRPRHold 保存 Product Hold 資料，來源以 Lot_ID 關係連回 Siview.Frlot。這條線協助讀者對照受到管制的 Lot；產品與站點是本次說明的業務條件，未在此假造來源未列出的欄位或 Join。</p><p class="topic-takeaway">以 Product 設定條件，讓符合的 Lot 到指定站點暫置，等待統一處理。</p>',
  image:'assets/mes-040/product-hold-v1.png',mobile:'assets/mes-040/product-hold-mobile-v1.png',
  alt:'PID設定Product P100於S20暫置，所屬Lot L023與L024各自到站被Product Hold攔住，等待統一處理',
  caption:'P100、S20、L023 與 L024 為教學示例。圖中兩批各自到站時受到相同管制；右側／下方呈現暫置結果的檢視，不表示已解除管制或繼續加工。'
 });
 add('stream','2673:stream 2673:stream-link','Stream：Flow × IE WPH 預估到站',
  'Stream 舊功能依 Lot 的 Flow 與 IE 站點 WPH，估算後續各站的預計到站時間；此功能已由 LDS 取代。Flow 提供站點先後，WPH 提供加工速率，兩者共同支援到站時間推估。',[], 'Flow 決定先後，WPH 支援耗時估算。');
 Object.assign(topics.stream,{
  details:'<h3>先用 Flow 找出後續站點</h3><p>從 Lot 目前的流程位置出發，沿著它所屬的 Flow，找出接下來會經過哪些站點及順序。教學例以 L023 目前在 S10，後續經 S20、S30 說明；實際站序依該批 Flow。</p><h3>IE WPH 提供各站的加工速率</h3><p>WPH 是 wafer per hour（每小時晶圓片數），代表預期加工速率。將 Flow 站點對應到適用的 IE WPH，再搭配批量等條件，作為估算加工耗時的依據。</p><p>只為理解單位時，可把「片數 ÷ WPH」看成簡化加工小時數；它不是完整的到站預測公式。等待、搬送及其他耗時是否納入、如何估算，須依系統實際算法，不能只用 WPH 推定。</p><h3>沿 Flow 累計，推估每一站何時到達</h3><p>概念上，以基準時間加上到達目標站前的累計耗時，得到預計到站時間。推估 S20 要看抵達 S20 前的路段；推估更後面的 S30，則累計到 S30 前的各段。若目前站已加工一部分，也要依當前進度估算剩餘時間，不能重算整站。</p><p>因此 Flow 決定要累計哪些站與路段，WPH 支援其中加工耗時的估算。到站時間是預測值，不代表已到站，也不是該站的加工完成時間。</p><h3>舊資料與目前功能</h3><p><strong>此功能已由 LDS 取代。</strong>這裡保留 Stream 的歷史概念，協助理解資料關係；不推定 LDS 採用相同算法。原圖 Stream_fcst_lot_st 透過 Lot_ID／OPE_NO 對照 Lot 與未來站點，圖文補充 Flow 和 IE WPH 的業務計算關係，不新增未確認的資料表 Join。</p><p class="topic-takeaway">Flow 決定站點先後，WPH 支援耗時估算，沿途累計預計到站時間。</p>',
  image:'assets/mes-041/stream-arrival-v2.png',mobile:'assets/mes-041/stream-arrival-mobile-v1.png',
  alt:'Lot L023依Flow的S10到S20到S30站序，結合IE WPH估算耗時，累計後續各站預計到站時間；Stream舊功能已由LDS取代',
  caption:'Flow 站序與 WPH 耗時估算共同構成預測依據。L023、S10／S20／S30 為概念示例，時鐘不是實際預測值；實際算法及其他耗時依系統定義。'
 });
 Object.assign(topics.forecast,{
  title:'未來的 Flow：用 Flow 與 IE WPH 預估各站到站時間',
  meaning:'F12dm.dm_tbl_lot_forecast 描述 Lot 未來各站的預計到站時間。依這批貨的 Flow 找後續站點順序，結合 IE 站點 WPH 估算耗時，再逐站推算預計到站時間。',
  details:'<h3>Flow：這批貨接下來經過哪些站？</h3><p>先確認 Lot 目前的流程位置，再沿它的 Flow 找出後續站點。以 L023 目前在 S10、後續走 S20 與 S30 為例，Flow 提供站點先後，讓預測知道要累計哪些路段。</p><h3>IE WPH：各站加工預計需要多久？</h3><p>將 Flow 站點對應到適用的 IE WPH。WPH 是 wafer per hour（每小時晶圓片數），提供預期加工速率；搭配批量等條件，可作為各段加工耗時的估算依據。</p><p>「片數 ÷ WPH」只用來理解簡化加工耗時的單位，不代表完整預測算法。等待、搬送等其他耗時及目前站的剩餘加工時間，如何納入須依系統實際定義。</p><h3>沿站序累計，產生各站預計到站時間</h3><p>概念上，以基準時間加上到達目標站前的累計耗時，推算該站的預計到站時間。S20 看抵達 S20 前的耗時；S30 再累計到 S30 前的各段，形成同一 Lot 的未來到站清單。</p><p>這份清單是預測，不表示 Lot 已經到站，也不是目標站的加工完成紀錄。查詢時要對照預測更新時間與 Lot 當前進度。</p><h3>對照原圖的 Lot 與站點關係</h3><p>來源 F12dm.dm_tbl_lot_forecast 透過 Lot_ID／OPE_NO 對照 Lot 與未來站點。以 Lot 找這批貨，再沿站序讀各站的預計到站時間。Flow 與 IE WPH 是使用者確認的計算概念，實際欄位與資料表連接依內部定義。</p><p class="topic-takeaway">Flow 決定先後，WPH 支援估時，Lot 串起未來各站的預計到站時間。</p>',
  image:'assets/mes-042/lot-forecast-v2.png',mobile:'assets/mes-042/lot-forecast-mobile-v1.png',
  alt:'Lot L023沿Flow的S10至S20至S30站序，結合IE WPH耗時估算，推算未來各站的預計到站時間',
  caption:'L023 與 S10／S20／S30 為教學示例。Flow 站序和 WPH 耗時估算共同支援到站預測；圖中未填入實際預測值，實際算法與其他耗時依系統定義。'
 });
 Object.assign(topics.recipegroup,{
  title:'Recipe Group：彈性控制多台或單台機台的加工許可',
  meaning:'Recipe Group 包含一群能執行特定類似加工的機台。製造端可依加工條件，例如特定產品，切換多台或單台機台是否允許進行這類加工，增加製造控制的彈性。',
  details:'<h3>群組裡也包含機台</h3><p>Recipe Group 不只是程式名稱的集合，也包含能執行這類加工的機台。先理解這一群機台具備相近的加工能力，再看目前允許哪些機台執行指定加工。</p><h3>有能力加工，還要看是否允許</h3><p>針對特定產品或加工類別，可以透過這項功能調整機台的加工許可。例如同一群 EQP-A、EQP-B、EQP-C 都能執行這類加工，但對產品 P100 的加工類別 R，可以暫時不允許其中部分機台執行。</p><h3>多台控制與單台控制</h3><p>多台控制示例：對上述條件，EQP-A 與 EQP-B 暫不允許，EQP-C 允許。單台控制示例：只有 EQP-B 暫不允許，EQP-A 與 EQP-C 允許。兩個案例是獨立設定情境，並非先後操作，也不表示群組與個別設定的覆蓋優先權。</p><p>需要調整時，可以依製造需求開啟或關閉多台或單台的許可，讓可執行機台的範圍更有彈性。這裡的開關是該加工條件的允許狀態，不是機台電源，也不能由此推定整台設備對所有加工都停用。</p><h3>如何對照原圖？</h3><p>Siview.CSFRRCPGRPST 是 Recipe Group 資料，原圖透過「製程程式群組對照」連接 Flow（F12DM.DM_Flow_step_Bt）。教學圖補上機台群與加工許可的業務概念；實際機台對應欄位、控制規則及優先權仍依內部設定，未新增未確認的資料表連接。</p><p class="topic-takeaway">依加工條件，彈性控制多台或單台機台的加工許可。</p>',
  image:'assets/mes-043/recipe-group-v1.png',mobile:'assets/mes-043/recipe-group-mobile-v1.png',
  alt:'Recipe Group包含EQP-A、EQP-B、EQP-C三台可執行類似加工的機台，依產品P100加工類別R比較多台與單台加工許可控制',
  caption:'P100、R 與 EQP-A／B／C 為教學示例。兩個獨立情境顯示多台或單台的加工許可，不代表設備電源、實際生產狀態或設定優先權。'
 });
 Object.assign(topics.stage,{
  title:'Module → Stage → Step：從加工模組看到細部步驟',
  meaning:'Module 是像黃光這樣的加工模組；一個 Module 裡包含多個 Stage，每個 Stage 再包含細部加工步驟 Step。F12dm.dm_tbl_info_stage 保存 Stage 與 Module 定義，與 Flow 對照後可理解各站的分段與歸屬。',
  details:'<h3>Module：看一類加工模組</h3><p>依廠內定義，Module 可以是「黃光」這樣的加工模組。完成這個模組的加工，需要經過多個 Stage，而不是只做單一站點。</p><h3>Stage：模組內的流程分段</h3><p>一個 Module 包含多個 Stage。每個 Stage 代表其中一段加工流程，內部再由多個細部 Step 組成。圖中用黃光 Module 包含 Stage A、Stage B 說明層級。</p><h3>Step：細部加工步驟</h3><p>Stage A 內的 S10、S20，以及 Stage B 內的 S30、S40，代表細部加工步驟。這些名稱與站序僅為教學示例，不是實際黃光製程設定。Flow 提供流程路線，Module／Stage 定義則協助辨認站點所屬的模組與分段。</p><h3>從 Lot 的 Step 往上找</h3><p>例如 L023 目前在 S30，依定義可找到它屬於 Stage B，再往上找到黃光 Module。如此可以在單站、分段與加工模組三種尺度理解這批貨目前的位置。</p><p>分段定義本身不是加工紀錄。要知道 Lot 實際走到哪個 Step，仍要查這批貨的當前站點或歷史紀錄。</p><h3>原圖的資料關係</h3><p>F12dm.dm_tbl_info_stage 保存 Stage 與 Module 定義，原图透過 Stage 定義連到 Flow（F12DM.DM_Flow_step_Bt）。教學圖呈現使用者確認的 Module 包含 Stage、Stage 包含 Step 層級；實際分段名稱與對應以廠內資料為準。</p><p class="topic-takeaway">Module 看加工模組，Stage 看流程分段，Step 看細部步驟。</p>',
  image:'assets/mes-044/module-stage-step-v2.png',mobile:'assets/mes-044/module-stage-step-mobile-v2.png',
  alt:'黃光Module包含Stage A及Stage B，各Stage包含細部Step；Lot L023目前S30對照Stage B與黃光Module',
  caption:'Module → Stage → Step 為廠內確認的包含層級。Stage A／B 與 S10～S40 為示例；Lot 歸屬箭頭表示查詢對照，非加工移動。'
 });
 Object.assign(topics.srts,{
  title:'SRTS：Flow 站點的 Sampling rule 與抽測比例',
  meaning:'SRTS 用來定義 Flow 中哪些站點設有 Sampling rule，以及適用的抽測比例。例如針對某個 Part，在指定量測站設定 30% 抽測，依規則選取量測對象。',
  details:'<h3>先看 Flow：哪些站點有抽測規則？</h3><p>沿 Flow 找到設有 Sampling rule 的站點，確認規則適用在哪個量測環節。圖中以 S10 → S20 → S30 為例，S20 是設定抽測規則的量測站。</p><h3>再看 Part：這個站要抽多少？</h3><p>例如 Part P100 在 S20 的抽測比例設定為 30%。閱讀規則時，要把 Part、適用站點與比例一起看，不能只看到 30% 就套用到所有站點或其他 Part。</p><h3>30% 的對象與選取方式，依規則定義</h3><p>抽測比例決定適用範圍內要抽檢的量測比例。實際抽樣單位、計算範圍與選取方式，須依規則設定確認；本例不將它直接解釋成每批固定抽 30% 的晶圓，也不假定按 Lot 抽樣或採隨機選取。</p><p>系統依適用規則選取量測對象後執行抽測。設定資料本身不代表已完成量測；要看實際抽了哪些對象及結果，需再查執行與量測紀錄。</p><h3>如何對照原圖？</h3><p>Siview.csfrsrts 與 Flow（F12DM.DM_Flow_step_Bt）透過原圖的「抽測跳站設定」關係連接。此處重點是使用者確認的站點 Sampling rule 與比例；未被選取的對象如何走後續流程，依實際規則，不單憑比例推定一律跳站。</p><p class="topic-takeaway">先找 Flow 的適用站點，再看 Part 的 Sampling rule 與抽測比例。</p>',
  image:'assets/mes-045/srts-sampling-v1.png',mobile:'assets/mes-045/srts-sampling-mobile-v2.png',
  alt:'Flow的S20量測站設定Part P100抽測30%，依Sampling rule選取量測對象',
  caption:'P100、S20 與 30% 為教學示例。抽樣單位與選取方式依規則定義；圖中設定不是實際量測結果。'
 });
 Object.assign(topics.part,{
  title:'PART：產品對應 Flow，進版同步記錄',
  meaning:'PART 定義可查出產品（Product／PART）使用的加工 Flow，也就是此處所說的 Route／mainpd_id 流程對應。Flow 進版時，PART 也同步記錄進版資訊，讓製造依適用的正確版本與加工順序執行。',
  details:'<h3>這個產品使用哪條 Flow？</h3><p>從產品的 PART 定義出發，找到它對應的加工流程。Flow 描述要經過哪些站點及其先後；此處 Route 與 mainpd_id 是使用者提供的相關流程稱呼與識別方式。</p><h3>Flow 進版，PART 也記錄進版資訊</h3><p>當加工流程進版，PART 會同步記錄對應的版本資訊。圖中以同一個 PART P100 示範：進版前對照 Flow V1，進版後記錄對應 Flow V2，讓產品與流程版本的資訊維持一致。</p><h3>目的：使用正確加工流程與順序</h3><p>製造時不只要知道產品名稱，也要確認對應的 Flow 與適用版本，才能依正確的站點內容與順序執行。進版實際修改哪些站點或設定，依流程定義；圖中 V1／V2 僅用來解釋版本對應。</p><p>在製 Lot 如何適用新版或保留原版，仍依實際切版規則，不能只憑 PART 的新版資訊就推定所有在製批次立即切換。</p><h3>如何對照原圖？</h3><p>Siview.frprodspec 保存 PART 定義，原圖以 Mainpd_id 對應 Flow（F12DM.DM_Flow_step_Bt）。查詢時把產品、流程識別與版本資訊一起對照；實際版本欄位與同步方式依內部定義，本例不假定版本一定編在 Mainpd_id 裡。</p><p class="topic-takeaway">PART 連結產品與 Flow，進版資訊同步，製造依正確流程與站序。</p>',
  image:'assets/mes-046/part-flow-version-v2.png',mobile:'assets/mes-046/part-flow-version-mobile-v1.png',
  alt:'PART P100透過Mainpd_id對照Flow；Flow從V1進版V2時PART同步記錄版本，供製造依正確流程與站序執行',
  caption:'P100、V1／V2 與站點為教學示例；版本標記不是實際欄位值。在製 Lot 的版本適用依實際規則。'
 });
 add('owner','2674:owner 2674:owner-link','機群與課別：由機台查管理歸屬',
  'MFG_EQP_OWNER_BT 提供機群／課別與機群／機台的管理對照。透過 EQP_ID，可以查詢機台所屬的管理單位、機群名稱與廠商名稱等資訊。',[], '由機台查機群、管理單位與廠商資訊。');
 Object.assign(topics.owner,{
  details:'<h3>先確認要查哪一台機台</h3><p>從 EQP_ID 出發，確認要查詢的設備，再查它的機群與管理資訊。例子以 EQP-A、EQP-B 表示兩台機台，名稱皆為教學示意。</p><h3>機台、機群與課別如何對照？</h3><p>圖中 EQP-A 與 EQP-B 同屬機群 G01，並由設備一課管理。透過這份資料，可以知道機台屬於哪一個機群，以及對應哪個單位或課別負責管理；實際對應以廠內資料為準。</p><h3>一次看懂設備的管理資訊</h3><p>查 EQP-A 時，可對照機群名稱 G01、管理單位設備一課與廠商名稱廠商甲。機群協助組織設備，管理單位說明負責歸屬，廠商名稱則提供設備廠商資訊，三者各有用途。</p><p>這是管理資料的查詢關係，不表示加工先後，也不代表機台目前的加工許可或運轉狀態。</p><h3>對照原圖</h3><p>MFG_EQP_OWNER_BT 透過 EQP_ID 連到機台 Siview.freqp。由此閱讀管理歸屬與設備資訊；實際欄位名稱及有效對應依內部資料定義。</p><p class="topic-takeaway">從機台找到所屬機群、管理單位與廠商資訊。</p>',
  image:'assets/mes-047/eqp-owner-v1.png',mobile:'assets/mes-047/eqp-owner-mobile-v1.png',
  alt:'EQP-A及EQP-B同屬機群G01並由設備一課管理，EQP-A查詢結果包含機群管理單位及廠商甲',
  caption:'EQP-A／B、G01、設備一課與廠商甲均為教學示例。箭頭表示管理歸屬與查詢對照，非加工順序。'
 });
 Object.assign(topics.stock,{
  title:'Default STK：機台的預設 FOUP 倉儲',
  meaning:'每一台機台有其預設的 Stocker（FOUP 倉儲）。Siview.csfreqp_stk 透過 eqp_id 對照機台，讓讀者查詢這台設備預設對應哪一個 Stocker。',
  details:'<h3>Stocker 是什麼？</h3><p>Stocker 是存放 FOUP 的倉儲。圖中以倉儲內放置多個 FOUP，呈現它與加工機台的不同用途；STK 是這裡使用的 Stocker 簡稱。</p><h3>每台機台的預設對應</h3><p>依廠內定義，每台機台都有預設的 Stocker。例子中機台 EQP-A 的預設倉儲是 STK-01，查這台設備的設定，就能知道這個對應。</p><h3>如何閱讀這份設定？</h3><p>先確認機台 eqp_id，再查看它對應的 Default STK，最後辨認該 Stocker。圖上的虛線表示預設設定關係，不是 FOUP 正在移動的路徑。</p><p>預設 Stocker 不代表某個 FOUP 此刻已在該倉儲，也不證明已發生搬送。若要確認實際位置或搬送歷程，應另外查 FOUP 位置及傳送紀錄。</p><h3>對照原圖</h3><p>Siview.csfreqp_stk 透過 eqp_id 連接機台 Siview.freqp，表示機台與預設 Stocker 的設定對照。圖中名稱為教學示例；實際倉儲識別與設定以廠內資料為準。</p><p class="topic-takeaway">查機台設定，就知道它預設的 Stocker（FOUP 倉儲）。</p>',
  image:'assets/mes-048/default-stocker-v1.png',mobile:'assets/mes-048/default-stocker-mobile-v1.png',
  alt:'機台EQP-A透過預設設定對應Stocker STK-01，Stocker倉儲內存放多個FOUP',
  caption:'EQP-A、STK-01 與倉儲外觀均為教學示例。虛線表示預設對應，不代表 FOUP 目前位置或已搬送。'
 });
 topics.bmir={...topics.ohb,refs:['2674:bmir-link','2674:bmir']};
 Object.assign(topics.ohb,{
  refs:['2674:ohb-link','2674:ohb-eqp','2674:ohb-status-link','2674:ohb-status'],
  title:'OHB：機台附近的 FOUP 暫置架',
  meaning:'OHB（Over Head Buffer）是機台鄰近的簡易 FOUP 暫置架。當 Stocker 距離機台較遠時，可先把 FOUP 放到附近 OHB，方便後續需要加工時快速就近搬運。',
  details:'<h3>為什麼機台附近需要 OHB？</h3><p>Stocker 是 FOUP 倉儲，但有時距離機台較遠。若到需要加工時才從遠端 Stocker 取貨，搬運可能耗費較久；先把 FOUP 暫放在機台附近的 OHB，可縮短後續取貨的路程。</p><h3>OHB 是暫置架</h3><p>OHB 是 Over Head Buffer，用來在機台附近暫時放置 FOUP。圖中畫成高架的簡易架子，FOUP 放在架子上，等待後續搬到機台。</p><p>OHB 負責暫置；圖中的 OHT 則是沿軌道搬運 FOUP 的車。需要時，由搬送設備把 FOUP 送到機台 Load Port。圖示僅說明用途，實際搬送安排依現場系統。</p><h3>先查對應，再查狀況</h3><p>Siview.csfrohb_eqp 記錄機台與 OHB 的對應，原圖以 EQPSTKID 關係連到機台。沿 OHB_ID 可再對照 Siview.csfrohb 的 OHB 狀況資料。</p><p>設定資料幫助找到對應架子；狀況資料則要搭配當時紀錄判讀。不能只因機台設定了 OHB，就推定某個 FOUP 已在架上或已搬送完成。</p><p class="topic-takeaway">FOUP 先暫放鄰近 OHB，方便後續就近搬到機台。</p>',
  image:'assets/mes-049/ohb-near-tool-v1.png',mobile:'assets/mes-049/ohb-near-tool-mobile-v1.png',
  alt:'遠端Stocker的FOUP先暫放機台附近OHB架子，後續由OHT就近搬到機台Load Port',
  caption:'位置、架子外觀與路徑為概念示意，非實際搬送紀錄或時間保證。OHB 是暫置架，OHT 是搬運車。'
 });
 const kerIntro='<p>KER 是 Key EQP Report，用來管理機台與機群的報表資料，方便線上查詢 AVL、EFF、LOST 等指標。本次聚焦資料關係與時間，不展開公式或彙總算法。</p>';
 const kerTime='<h3>目前與歷史分開讀</h3><ul><li>ker_dm_bt：機群目前指標，指最近一次更新；以 EQP_GRP 關聯。</li><li>Ker_Dm_Hourly_Bth：每小時的機群歷史指標。</li><li>Ker_Eqp_Aaa_Oee_Ut：機台歷史指標，也是一小時一次。</li></ul><p>最近一次更新不直接等於當日累計；每小時一次也不能單憑名稱推定各指標的計算窗口。比較前先確認對象、成員及資料時間。</p>';
 Object.assign(topics.group,{
  title:'KER：機台與 Chamber 的分群對應',
  meaning:'KER（Key EQP Report）管理機台與機群報表。KER_EMP_EQP_GRP_CAP_UT 記錄機台在機群的對應；同一機台可同時屬於多個機群，Chamber 也能獨立分群。',
  details:kerIntro+'<h3>同一機台可同時屬於多個機群</h3><p>KER_EMP_EQP_GRP_CAP_UT 的資料代表機台在某個機群的對應。例子中 EQP-A 同時對應 G1 與 G2；不能把機群當成互斥分類，也不能跨群直接加總就視為不重複機台。</p><h3>Chamber 可獨立分群</h3><p>ker_dm_sub_ch_eqp_grp_bt 支援 Chamber 分群。同一機台內 CH-1 與 CH-2 可以分別屬於 C1 與 C2，不必跟整台機台使用相同分群。</p>'+kerTime
 });
 Object.assign(topics.virtual,{
  title:'KER：User 用 SQL 自訂虛擬 Tool Group',
  meaning:'KER（Key EQP Report）的 KER_VR_EQP_GRP_DETAIL_BT 讓 User 自行用 SQL 定義 Tool Group；DYNAMIC_SQL 表達群組成員的判定關係。',
  details:kerIntro+'<h3>依報表需求定義機群</h3><p>User 可用 SQL 條件選出要看的機台，形成虛擬 Tool Group。閱讀 KER_VR_EQP_GRP_DETAIL_BT 時，重點是使用者實際定義的條件，以及選出了哪些設備。</p><p>虛擬分群是報表成員定義，不代表搬動機台或修改加工許可。同一設備可能出現在不同群組；查報表前應核對成員範圍。SQL 執行及更新時機依系統實作。</p>'+kerTime
 });
 Object.assign(topics.oee,{
  title:'KER：最近一次更新與每小時歷史指標',
  meaning:'KER（Key EQP Report）提供 AVL、EFF、LOST 等指標。機群目前資料是最近一次更新；機群歷史與機台歷史皆每小時一次，需分清對象與資料時間。',
  details:kerIntro+kerTime+'<h3>對照 ER 的鍵與來源</h3><p>機群目前 OEE 的 EQP_GRP 是刻意設計，保留此關係。機台歷史依來源 EQP_ID 閱讀；機群歷史原圖的連線也保留，不將未確認的連線自行改寫。</p><p>單台目前機況 KER_EQP_STATUS_BT 是另一類狀況資料，不能當成機群期間比率。AVL、EFF、LOST 本輪僅介紹為報表指標項目，公式與彙總方式暫不處理。</p>'
 });
 for(const key of ['group','virtual','oee']) Object.assign(topics[key],{
  image:'assets/mes-050/ker-overview-v1.png',mobile:'assets/mes-050/ker-overview-mobile-v1.png',
  alt:'KER機台多重分群、Chamber獨立分群、User SQL虛擬機群及最近更新與每小時歷史指標總覽',
  caption:'KER 關係總覽：機台與群名為教學示例，連線表示分群或查詢。AVL／EFF／LOST 僅列項目，沒有實際數值或公式。'
 });
 Object.assign(topics.bmir,{
  title:'BMIR：OHB 空位時，呼叫 RTD 計算下一批貨',
  meaning:'當 OHB 空的時候，BMIR 會呼叫 RTD，計算下一批應該放到 OHB 的貨。',
  details:'<h3>觸發：OHB 空了</h3><p>依廠內定義，OHB 空的時候會呼叫 RTD，計算接下來應該選哪一批貨放到 OHB，作為後續補貨安排的依據。</p><h3>選貨與搬送分開看</h3><p>RTD 計算下一批貨，不代表貨已放上架；實際到位需再對照搬送與 OHB 狀況。RTD 的選貨條件、呼叫頻率與其他細節依系統設定。</p>',image:undefined,mobile:undefined
 });
 Object.assign(topics.portmode,{
  title:'Port 模式：UP 有貨，LOST 沒有貨',
  meaning:'Port 的 UP／LOST 表示 Port 上是否有貨：UP 為有貨，LOST 為沒有貨。這裡要依 Port 的語境判讀。',
  details:'<h3>Port 上有沒有貨？</h3><ul><li>UP：Port 上已經有貨。</li><li>LOST：Port 上沒有貨。</li></ul><p>Port 有貨不等於 Lot 已進機加工；機台的 UP／LOST 也有不同語境，不能直接把機台狀態定義套到 Port。</p>'
 });
 Object.assign(topics.lotstatus,{
  title:'Lot Process／Status：RQHBE 五種狀態',
  meaning:'Lot 常見狀態 RQHBE：R 加工中、Q 等待加工、H 暫置待確認、B 長期間暫置、E 已出貨。',
  details:'<h3>依廠內定義閱讀 Lot 狀態</h3><ul><li>R — Run（In process）：加工中。</li><li>Q — Waiting for Process：等待加工。</li><li>H — Hold for check：暫置等待檢查或確認。</li><li>B — Bank：長期間暫置。</li><li>E — End of Process：已出貨。</li></ul><p>這是五種狀態的意義，不是固定先後流程。E 依本廠定義代表已出貨，不只表示完成某一站；H 與 B 則要分清待確認與長期暫置。</p>'
 });
 Object.assign(topics.wip,{
  title:'WIP 快照：每天早上 07:20 的機群與 KPI',
  meaning:'KER_WIP_Y_BTH 每天早上 07:20 保存一版快照，記錄當時的機群狀況與相關 KPI，例如 AVAIL、EFF。',
  details:'<h3>每天固定時間拍一版</h3><p>KER_WIP_Y_BTH 在每天早上 07:20 保存當時的機群狀況及相關 KPI，方便回看固定時點的資料。這是每日快照，不是每週一。</p><h3>快照與現在不同</h3><p>快照代表該日 07:20 保存的狀況，不代表目前即時狀況。AVAIL、EFF 等指標的計算期間不能單由拍照時間推定；公式與彙總方式本輪不展開。</p><p>KER_WIP_BT 與歷史快照為不同來源，原圖關係保留，實際查詢粒度及鍵依資料定義。</p>'
 });
 Object.assign(topics.portdata,{title:'Port 衍生設定（已撤下教學）',meaning:'FRPORT_UDATA 是 Port 的衍生設定；依使用者要求不列入教學介紹。',details:'',image:undefined,mobile:undefined,link:undefined});
 const supplementalArt={
  bmir:['bmir-v3.png','bmir-mobile-v1.png','OHB空了呼叫RTD，計算下一批Lot L023，等待後續搬送安排','OHB 是高架暫置架；選貨結果並非已搬送或已上架。Lot L023 為教學示例。'],
  portmode:['port-occupancy-v1.png','port-occupancy-mobile-v2.png','同一EQP-A的LP1有FOUP時為UP，沒有FOUP時為LOST','同一 Port 的兩種示例，非狀態轉換順序；Port 有貨不表示 Lot 已加工。'],
  lotstatus:['lot-rqhbe-v2.png','lot-rqhbe-mobile-v1.png','Lot R加工中Q等待加工H待確認B長期暫置E已出貨五種獨立狀態','依廠內定義並列五種狀態；插畫為情境示例，沒有固定狀態轉換順序。'],
  wip:['daily-snapshot-v1.png','daily-snapshot-mobile-v1.png','每天早上07:20保存機群狀況及AVAIL EFF等KPI，按日期回看版本','每日 07:20 為確認的保存時點；第1～3天為示例，沒有填入實際 KPI 值。']
 };
 for(const [key,[desktop,mobile,alt,caption]] of Object.entries(supplementalArt))Object.assign(topics[key],{image:'assets/mes-052/'+desktop,mobile:'assets/mes-052/'+mobile,alt,caption});
 topics.future.mobile='assets/mes-026/future-mobile-v1.png';
 add('flowkey','2673:flow-link','Lot 與 Flow：沿 Part／Mainpd_id 找流程',
  '這個關係把 Lot 連到 Flow 定義，原圖列出的對應是 Part／Mainpd_id。',
  ['先確認 Lot 所屬 Part。','沿 Part／Mainpd_id 找對應 Flow。','想知道已走到哪站時，再查這批的站點歷史。'],
  '流程定義描述路線；站點歷史記錄這批的經過。','flow.html#stage');
 add('eqpkey','2676:eqp-id 2677:eqp-id','EQP_ID：在這条資料路徑中識別機台',
  'EQP_ID 是設備識別的關係註記。來源 2676 用於設備組成關係；來源 2677 用於 PD／Recipe 到設備的對應。',
  ['先看目前選中的 EQP_ID 屬於哪張來源圖。','沿相連的設備或對應表閱讀，保持這條路徑的上下文。','同名 EQP_ID 註記不能單憑名稱合併，也不能自行推定主鍵或關係基數。'],
  '識別欄位要和它連接的資料對象一起讀。');
 add('retired','2672:cast-link','原圖待校正關係：Lot 裝載與 Step 歷史須分清',
  '這個原圖節點以 FRCAST 標示「Lot 在 Foup 內」並連到 Step，已由使用者指出語意不正確；右側教學關聯已撤下這條支線。',
  ['查裝載：Lot — FRCAST_LOT — FOUP。','查 Lot Step：Lot — 站點 Summary／Lot_id — Step 歷史。','此節點僅保留原圖追溯，不能拿來當作正確的裝載或站點查詢路徑。'],
  '裝載關係的表是 FRCAST_LOT；Step 歷史的主詞是 Lot。');
 return {topics, routeKeys:{'lot-step':'lotstep',load:'load',slot:'contents',location:'location',predispatch:'predispatch','lot-pre':'available',port:'port',flow:'flow',lr:'recipe',pd:'pd',recipe:'recipe',chamber:'chamber',hold:'future',move:'move',transfer:'mcs',qtime:'qtime',wip:'wip',oee:'oee'}};
})();
