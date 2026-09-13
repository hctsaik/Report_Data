from pathlib import Path
import json,html,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2];O=R/'ER/INTEGRATED';O.mkdir(exist_ok=True)
# Same topic is not an assertion that these are identical tables.
spec=[
('part','產品 Part','定義產品與對應路徑','FRPRODSPEC',0,0),
('flow','Flow／Stage','路徑、站點及分段定義','DM_Flow_step_Bt · Stage · SRTS',1,0),
('lr','LR 與設備對應','邏輯配方的配置線索','DM_Flow_LR_EQP_BT · Recipe Group',2,0),
('er','ER 與設備對應','設備配方配置；不是執行證據','FRMRCP · FRMRCP_EQP',3,0),
('pd','PD 與設備對應','製程定義關聯的候選設備','FRPD · FRPD_EQP',4,0),
('hold','Hold／Qtime','管制安排與時間限制的資料','Future Hold · Product Hold · Qtime',0,1),
('lot','Lot 生產批次','哪一批？製程狀態與歸屬','FRLOT · LOT Process Status',1,1),
('cast','FOUP／Slot／裝載','哪個盒子、哪個槽位、裝哪批','FRCAST · FRCAST_LOT · fhwlths',2,1),
('port','Port 交接位置','設備與載具交接的介面','FRPORT · FRPORT_UDATA · Port',3,1),
('eqp','EQP 設備','加工資源的主機身分','FREQP · EQP_ID',4,1),
('forecast','預派／預到／預估','計畫要去哪、預估何時到','Predispatch · Lot forecast · Stream',0,2),
('move','Move／全部動作','發生過什麼？重工另算過站','DM_Move_Step_bth · FHOPEHS_S',1,2),
('transfer','搬送歷史','載具如何被運送','MES／MCS Carrier history',2,2),
('chamber','Chamber 加工資源','設備內哪個資源、狀況如何','FRPRCRSC · FHCSCHS',3,2),
('state','設備現況／歷史','某時刻狀態；不等於期間比率','FREQP · FHESCHS · KER_EQP_STATUS',4,2),
('capacity','IE 產能定義','定義 WPH 的工程資料','DM_TBL_IE_CTWPH',0,3),
('wip','WIP／歷史快照','某時間點有哪些在製批次','KER_WIP_BT · KER_WIP_Y_BTH',1,3),
('groups','機群／虛擬群組','統計包含哪些設備與 Chamber','EQP_GRP · DYNAMIC_SQL',2,3),
('oee','機台／機群統計','一段期間的設備表現','OEE current／history',3,3),
('location','設備位置／儲位配置','Bay、Owner、STK、OHB 的線索','MFG_EQP_BAY_BT · OHB · BMIR',4,3)]
groups={k:dict(id=k,title=t,meaning=m,table=tb,col=c,row=r,refs=[]) for k,t,m,tb,c,r in spec}
assign={
'2671':{'cast':'material material-link slot cast-link cast','lot':'lot','port':'port-link port','eqp':'has eqp','forecast':'lot-eqp predispatch','location':'location'},
'2672':{'forecast':'predispatch pre-link','lot':'lot','move':'move move-link summary step all-actions history','cast':'cast cast-link','transfer':'mes-transfer transfer mcs-transfer mcs-history','hold':'qtime-link qtime'},
'2673':{'capacity':'wph wph-link','lr':'lr recipe lr-link recipe-link lr-eqp-link lr-eqp','pd':'pd-eqp pd-eqp-link pd pd-link','part':'part part-link','hold':'future future-link product-hold hold-link','lot':'lot','flow':'flow-link flow stage-link srts-link stage srts','forecast':'forecast-link stream-link forecast stream'},
'2674':{'port':'udata udata-link port mode mode-link port-link','location':'default default-link bay bay-link owner-link ohb-link owner ohb-eqp ohb-status-link ohb-status bmir-link bmir','state':'eqp-history history-link','eqp':'eqp','chamber':'chamber-link chamber detail-link chamber-detail'},
'2675':{'wip':'wip-history wip-link lot','move':'move move-link all-actions history','groups':'chamber-link chamber group-link eqp virtual-link virtual','state':'status-link status','oee':'eqp-oee-link eqp-oee group-oee-link group-oee group-history-link group-history'},
'2676':{'eqp':'eqp eqp-id','port':'port port-id udata','cast':'cast cast-lot','chamber':'chamber','lot':'lot status'},
'2677':{'pd':'pd pd-key pd-eqp','eqp':'eqp-id eqp','location':'bay location','er':'recipe recipe-key recipe-eqp er','lr':'lr','state':'status'}}
src=json.loads((R/'ER/NEW/transcription.json').read_text(encoding='utf-8'));ns={'s':'http://www.w3.org/2000/svg'};edges=[]
for d in src:
 name=d['name'];svg=ET.parse(R/f'ER/NEW/{name}.svg');nodes=svg.findall("s:g[@id='nodes']/s:g",ns)
 mapping={n:g for g,ids in assign[name].items() for n in ids.split()}
 assert set(mapping)=={n.get('id') for n in nodes},name
 for n in nodes:
  groups[mapping[n.get('id')]]['refs'].append(dict(source=name,node=n.get('id'),labels=[''.join(t.itertext()) for t in n.findall('s:text',ns)]))
 for e in d['edges']:edges.append(dict(source=name,a=e['a'],b=e['b'],groupA=mapping[e['a']],groupB=mapping[e['b']]))
data=dict(groups=list(groups.values()),sourceEdges=edges,notice='群組表示共同物理／業務主題，不等於同一張表；線為語意關係，不是 SQL Join。')
(O/'map.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
E=html.escape
W,H=2780,1780;cw,ch=450,235;xs=[55+545*i for i in range(5)];ys=[180+375*i for i in range(4)]
colors=['#356cb6','#087e83','#906238','#6452a3']
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"><title>Fab 資料與物理意義整合圖</title><desc>七張 ER 圖依二十個共同主題整合；主題不等於資料表合併，線條不是 SQL Join。</desc><style>text{{font-family:Microsoft JhengHei,Arial,sans-serif;fill:#15344f}}.edge{{fill:none;stroke:#9aafc2;stroke-width:3}}.edge-label{{font-size:18px;paint-order:stroke;stroke:white;stroke-width:8px;stroke-linejoin:round}}.node{{cursor:pointer}}</style><rect width="2780" height="1780" fill="#f5f8fc"/><text x="55" y="62" font-size="38" font-weight="bold">一座 Fab，同一批 Lot，多種資料視角</text><text x="55" y="106" font-size="23">上層是定義，中間是現場對象，下層是事件與統計。連線描述關係，不表示交易順序或可直接 Join。</text>']
# Explicitly selected teaching relationships; full original topology remains in map.json.
links=[('part','flow','產品對應流程'),('flow','lr','站點／LR'),('lr','er','配方關聯線索'),('er','pd','同看設備配置'),('flow','lot','Lot 套用定義'),('hold','lot','批次管制'),('lot','cast','裝載關係'),('cast','port','現場交接視角'),('port','eqp','設備的介面'),('pd','eqp','設備配置'),('lot','move','過站與動作'),('cast','transfer','載具搬送'),('eqp','state','現況與歷史'),('chamber','state','設備與資源分層'),('forecast','move','預估與事實比較'),('wip','groups','WIP 與機群'),('groups','oee','統計範圍'),('oee','location','統計與設備歸屬'),('state','location','狀態與位置分開')]
inference={('er','pd'),('cast','port'),('chamber','state'),('forecast','move'),('oee','location'),('state','location')}
for a,b,label in links:
 aa,bb=groups[a],groups[b];ax,ay=xs[aa['col']],ys[aa['row']];bx,by=xs[bb['col']],ys[bb['row']]
 if ay==by:
  x1,y1=ax+cw,ay+ch/2;x2,y2=bx,by+ch/2;tx=(x1+x2)/2;ty=y1-18
 else:
  x1,y1=ax+cw/2,ay+ch;x2,y2=bx+cw/2,by;tx=x1+12;ty=(y1+y2)/2
 dash=' stroke-dasharray="9 7"' if (a,b) in inference else ''
 label_markup=E(label) if ay!=by else E(label[:4])+f'<tspan x="{tx}" dy="23">{E(label[4:])}</tspan>'
 svg.append(f'<g class="relationship" data-a="{a}" data-b="{b}"><path class="edge" d="M{x1},{y1} L{x2},{y2}"{dash}/><text class="edge-label" x="{tx}" y="{ty}" text-anchor="middle">{label_markup}</text></g>')
for a,b,path,label,tx,ty,dashed in [
 ('capacity','lr','M55,1422 L22,1422 L22,465 L1370,465 L1370,415','IE WPH 與 LR 的定義關聯',850,450,False),
 ('forecast','lot','M505,1047 L552,1047 L552,672 L600,672','Lot 的預派／預估',540,865,False),
 ('lot','wip','M1050,672 L1095,672 L1095,1422 L1050,1422','同一批次的快照視角',1060,1230,True),
 ('eqp','chamber','M2455,790 L2455,850 L1915,850 L1915,930','設備下的 Chamber',2150,832,False)]:
 dash=' stroke-dasharray="9 7"' if dashed else ''
 svg.append(f'<g class="relationship" data-a="{a}" data-b="{b}"><path class="edge" d="{path}"{dash}/><text class="edge-label" x="{tx}" y="{ty}" text-anchor="middle">{label}</text></g>')
for g in groups.values():
 x,y=xs[g['col']],ys[g['row']];color=colors[g['row']]
 svg.append(f'<g id="{g["id"]}" class="node" tabindex="0" role="button" aria-label="{E(g["title"])}"><rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="18" fill="white" stroke="{color}" stroke-width="3"/><rect x="{x}" y="{y}" width="9" height="{ch}" rx="4" fill="{color}"/><text x="{x+25}" y="{y+58}" font-size="29" font-weight="bold">{E(g["title"])}</text><text x="{x+25}" y="{y+117}" font-size="22">{E(g["meaning"])}</text><text x="{x+25}" y="{y+176}" font-size="18">{E(g["table"])}</text></g>')
svg.append('<text x="55" y="1680" font-size="22">實線：原圖關係的主題摘要。虛線：教學比較／現場視角，不主張存在對應資料庫連線。</text><text x="55" y="1725" font-size="22">未在七圖完整交代：Wafer 逐片加工位置、Physical Recipe 執行紀錄、MON／EMS 放行條件、逐表 freshness。</text></svg>')
(O/'fab-integrated.svg').write_text('\n'.join(svg),encoding='utf-8')
print(len(data['groups']),'groups;',sum(len(g['refs']) for g in groups.values()),'original nodes;',len(edges),'original edges indexed')
