/* Shared confirmed teaching content for ER and standalone topics. */
window.ER_TEACHING = (() => {
const teaching={
qtime:{title:'QTime：Lot 的製程時間限制',refs:['2672:qtime','2672:qtime-link'],color:'#7756af',image:'assets/mes-009/qtime.png',mobile:'assets/mes-025/qtime-mobile-v1.png',alt:'同一Lot的QTime教學示例：10:00起算、最大30分鐘，10:20已用20分鐘，10:30為本例最晚進站時間',caption:'教學示例：Lot L023 在10:00清洗出站起算，最大時限30分鐘，指定下一站進站為停止事件。本例10:30是截止時間，不是已發生的進站紀錄；實際事件與限值依製程規則。',meaning:'QTime 是同一 Lot 在指定起算事件與停止事件之間的時間限制，用來管控製程間隔。起訖可能是某站出站到指定站進站，也可能跨站或以出站停止；不能一律當成排隊時間，也不是整個 Lot 的總製造時間。',details:'<h3>怎麼讀 Qtime 歷史？</h3><p>先確認是哪個 Lot、哪個站點，再核對起算事件、停止事件、時間與允許間隔。依規則比較已用時間與限值，不能只看到歷史表就判定現在是否超時。</p><h3>同一 Lot 的教學示例</h3><p>假設最大時限 30 分鐘，10:00 起算：10:20 已用 20 分鐘，尚餘 10 分鐘；若指定停止事件在 10:35 才發生，已用 35 分鐘，超過本例限值 5 分鐘。</p><p>若停止事件是「出站」，只有「進站」還不算結束計時。Hold 不會自動重設；超時依廠內規則處理，不自行改時間。</p>',link:'advanced.html#qtime'},
predispatch:{title:'Lot 預派：派工系統預先安排目標機台',refs:['2671:predispatch'],color:'#b26018',image:'assets/mes-023/lot-predispatch-v1.png',mobile:'assets/mes-023/lot-predispatch-mobile-v1.png',alt:'Lot 生產批次交由派工系統預先安排目標機台，預派不表示已到站或已加工',caption:'主要對象是 Lot：派工系統預先安排這一批將被派到的機台。FOUP 是輔助關聯；圖為概念示意，不是實際派工結果或搬送紀錄。',meaning:'「預派機台／SIVIEW.CSFRPREDISPATCH」表示派工系統預先安排這個 Lot 將被派到的目標機台。Lot 是主要對象，FOUP 是輔助關聯。這和「帶到／FRLOT_EQP」表示本站可用機台不同，也不表示已到機台或已開始加工。',link:'#selection-details'},
wph:{title:'機群 WPH：生管訂定的預期產出',refs:['2673:wph','2673:wph-link'],color:'#7756af',image:'assets/mes-019/group-wph-v1.png',mobile:'assets/mes-019/group-wph-mobile-v1.png',alt:'生產管理部門訂定機群 WPH，表示該機群每小時的預期晶圓產出量',caption:'每個機群的 WPH 由公司生產管理部門定義，單位為片／小時，是預期產出效率的標準。圖中機台與晶圓數量僅為示意；實際產出另查生產紀錄。',meaning:'依廠內定義：生產管理部門為每個機群訂定 WPH（wafer per hour），也就是預期每小時晶圓產出量。這是機群的預期產出標準，不是個別機台的實測值，也不是百分比。',link:'#selection-details'},
overview:{image:'examples/fab-physical-data-v01.png',alt:'機台、FOUP、Slot、Wafer 與 Lot 資料對照',caption:'左側是現場，右側是資料。Lot 是生產批次；FOUP 是承載晶圓的實體容器。',link:'index.html#fab'},
lot:{title:'Lot：生產批次',refs:['2671:lot','2676:lot'],color:'#176ac2',image:'examples/fab-physical-data-v01.png',alt:'現場物件與右側 Lot L023 的資料對照',caption:'看右側 lot_id = L023：Lot 將這批晶圓組織成生產與追蹤單位。',meaning:'藍框標出 Lot 資料實體。Lot 本身不是盒子；沿著「放在」關係，才會找到承載它的 FOUP。不同 schema 證據的節點仍各自保留。',link:'index.html#lot'},
carrier:{title:'FOUP：承載晶圓的容器',refs:['2671:cast','2676:cast'],color:'#008775',image:'examples/fab-physical-data-v01.png',alt:'FOUP F012 內的 Slot 07 與 Wafer W07',caption:'看中間剖面：FOUP 內有 Slot，晶圓放在對應位置。',meaning:'綠框標出 FOUP 資料實體。FRCAST 描述載具，FRCAST_LOT 表達與 Lot 的裝載關係；兩者不是同一個物件。',link:'index.html#foup'},
equipment:{title:'EQP：執行作業的設備',refs:['2671:eqp','2676:eqp','2677:eqp'],color:'#b26018',image:'examples/fab-physical-data-v01.png',alt:'FOUP F012 放在 ETCH-03 設備的 LP1',caption:'看左側 ETCH-03 與 LP1：設備、Port、FOUP 有不同身分。',meaning:'橘框標出 EQP 資料實體。設備可與 Port、Chamber、派工及 Recipe 配置相連；「預派」不能直接證明載具已經到達。',link:'operations.html#port'},
flow:{title:'Flow：批次遵循的製程路徑',refs:['2673:flow'],color:'#7756af',image:'assets/mes-v3/stage-v2.png',alt:'三個 Stage、六個 Step，以及目前在 S50 的 Lot',caption:'整條是 Flow；每段是 Stage；每一站是 Step。Lot 有自己的執行進度。',meaning:'紫框標出 Flow 資料對象。從 Lot 的 Part／Mainpd_id 關係找到流程定義，再區分「路徑如何定義」與「這批目前走到哪裡」。',link:'flow.html#stage'},
recipe:{title:'Recipe：從邏輯要求到設備配置',refs:['2673:lr-eqp','2677:recipe'],color:'#7756af',image:'assets/mes-009/recipes.png',alt:'LR、ER 與實際加工 Physical Recipe 的教學對照',caption:'示意值用來理解三層概念；實際名稱與映射仍以廠內定義為準。',meaning:'紫框分別指出 LR 與 ER 相關資料。ER 連線呈現配置關係；要知道某批實際用了哪個 Physical Recipe，還需要該次執行紀錄及版本證據。',link:'advanced.html#recipes'}
};
Object.assign(teaching, window.ER_TOPIC_CONTENT.topics);
for(const key of ['lot','carrier','load'])Object.assign(teaching[key],{
 title:key==='lot'?'Lot 與 Wafer：同一批中的不同晶圓':key==='carrier'?'FOUP 內容物：Lot、Wafer 與 Slot':'裝載關係：Lot、Wafer 與 FOUP',
 meaning:window.ER_LOT_WAFER.description,details:window.ER_LOT_WAFER.details.replace('對照上方 ER','對照 ER 關係').replace('下方是教學用的內容物示例','互動圖是教學用的內容物示例'),
 image:undefined,mobile:undefined,link:undefined
});

teaching.source={title:'來源關係說明',color:'#52728e'};
return teaching;
})();
