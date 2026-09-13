"""Editable SVG transcription of ER/ORG photographs; no raster embedding."""
from pathlib import Path
from html import escape
import json

OUT = Path(__file__).resolve().parent
charts = []

class Diagram:
    def __init__(self, name, title, width, height):
        self.name,self.title,self.width,self.height=name,title,width,height
        self.nodes={}; self.edges=[]; self.notes=[]
        charts.append(self)
    def n(self,key,x,y,lines,kind='rect',blue=False,issue=None,w=300,h=None):
        self.nodes[key]=dict(id=key,x=x,y=y,lines=lines.split('|'),kind=kind,blue=blue,issue=issue,w=w,h=h or (170 if kind=='diamond' else 112))
        return key
    def d(self,key,x,y,lines,**kw): return self.n(key,x,y,lines,'diamond',**kw)
    def e(self,a,sa,b,sb,via=()): self.edges.append(dict(a=a,sa=sa,b=b,sb=sb,via=via))
    def anchor(self,key,side):
        n=self.nodes[key]; x,y=n['x'],n['y']; w,h=n['w'],n['h']
        return {'T':(x,y-h/2),'B':(x,y+h/2),'L':(x-w/2,y),'R':(x+w/2,y)}[side]
    def render(self):
        p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="title desc">',f'<title id="title">{escape(self.title)}</title>',f'<desc id="desc">依照片 {self.name}.jpg 重畫；矩形、菱形、圓形及無向連線保留。橘色標記為尚待核對的原圖文字。</desc>', '<style>text{font-family:"Microsoft JhengHei","Noto Sans TC",Arial,sans-serif;fill:#182635}.label{font-size:21px;font-weight:600}.detail{font-size:19px}.issue{fill:#a34c00;font-size:16px;font-weight:700}.edge{fill:none;stroke:#34485c;stroke-width:3;stroke-linejoin:round;stroke-linecap:round}.shape{stroke:#63798d;stroke-width:2;fill:white}</style>',f'<rect width="{self.width}" height="{self.height}" fill="white"/>',f'<text x="48" y="48" font-size="28" font-weight="700">{self.name} · {escape(self.title)}</text>', '<text x="48" y="82" font-size="17" fill="#52657a">原圖結構重繪 · 文字與線條均可編輯 · 橘色 U 編號請見待確認清單</text>','<g id="connections">']
        for i,e in enumerate(self.edges):
            pts=[self.anchor(e['a'],e['sa']),*e['via'],self.anchor(e['b'],e['sb'])]
            p.append(f'<polyline id="edge-{i+1}" class="edge" data-from="{e["a"]}" data-to="{e["b"]}" points="'+ ' '.join(f'{x},{y}' for x,y in pts)+'"/>')
        p.append('</g><g id="nodes">')
        for n in self.nodes.values():
            x,y,w,h=n['x'],n['y'],n['w'],n['h']; kind=n['kind']
            p.append(f'<g id="{n["id"]}" data-kind="{kind}" data-x="{x}" data-y="{y}" data-w="{w}" data-h="{h}">')
            style=' style="fill:#d4ebff;stroke:#2585c6;stroke-width:3"' if n['blue'] else ''
            if kind=='diamond': p.append(f'<polygon class="shape" points="{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}"{style}/>')
            elif kind=='circle': p.append(f'<ellipse class="shape" cx="{x}" cy="{y}" rx="{w/2}" ry="{h/2}"{style}/>')
            else: p.append(f'<rect class="shape" x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}"{style}/>')
            lines=n['lines']; start=y-(len(lines)-1)*14
            for j,line in enumerate(lines):
                p.append(f'<text class="{"label" if j==0 else "detail"}" x="{x}" y="{start+j*28}" text-anchor="middle" dominant-baseline="central">{escape(line)}</text>')
            if n['issue']:
                p.append(f'<rect x="{x+w/2-102}" y="{y-h/2-27}" width="102" height="24" rx="4" fill="#fff0d5"/><text class="issue" x="{x+w/2-51}" y="{y-h/2-10}" text-anchor="middle">{n["issue"]} 待確認</text>')
            p.append('</g>')
        p.append('</g>')
        for x,y,label in self.notes: p.append(f'<text x="{x}" y="{y}" font-size="17" fill="#68788a">{escape(label)}</text>')
        p.append('</svg>')
        return '\n'.join(p)

d=Diagram('2671','LOT、FOUP、Port 與機台',1800,1530)
d.n('material',600,180,'Foup|Siview.FRLot_MtrlContnrs',w=360)
d.d('material-link',600,390,'放在|Siview.FrlotMtrl',w=360)
d.n('lot',600,610,'LOT|Siview.Frlot',blue=True)
d.d('port-link',1050,610,'目在|Siview.Freqp_Lot',issue='U01',w=350)
d.n('port',1510,610,'Port|Siview.Port')
d.d('slot',220,860,'在 Slot|Siview.fhwlths',issue='U02',w=340)
d.d('cast-link',600,860,'放在|Siview.Frcast_lot',w=340)
d.d('lot-eqp',1050,860,'預到|Siview.Frlot_EQP',w=350)
d.d('has',1510,860,'有|eqp_id')
d.n('cast',600,1120,'Foup|Siview.Frcast')
d.d('location',1050,1120,'位於|eqp_id|Siview.CSFHDOPHS',w=390,h=190)
d.n('eqp',1510,1120,'機台|Siview.freqp')
d.d('predispatch',1050,1380,'預派機台|eqp_id|SIVIEW.CSFRPREDISPATCH',issue='U03',w=500,h=210)
d.e('material','B','material-link','T');d.e('material-link','B','lot','T')
d.e('lot','R','port-link','L');d.e('port-link','R','port','L')
d.e('lot','L','slot','T',[(220,610)]);d.e('slot','B','cast','L',[(220,1120)])
d.e('lot','B','cast-link','T');d.e('cast-link','B','cast','T')
d.e('lot','B','lot-eqp','T',[(600,720),(1050,720)])
d.e('port','B','has','T');d.e('has','B','eqp','T')
d.e('lot-eqp','B','eqp','T',[(1050,1010),(1510,1010)])
d.e('cast','R','location','L');d.e('location','R','eqp','L')
d.e('cast','R','predispatch','L',[(790,1120),(790,1380)])
d.e('predispatch','R','eqp','L',[(1320,1380),(1320,1120)])
d.notes.append((730,1005,'原圖獨立小字：siview.fhwlths（U02，未另接線）'))

d=Diagram('2672','LOT 歷史、Qtime 與搬送記錄',2800,1420)
d.n('predispatch',1000,200,'預派記錄|SIVIEW.CSFHPREDISP',w=350)
d.d('pre-link',1000,440,'預派機台|Lot_ID')
d.n('lot',1000,720,'LOT|Siview.Frlot',blue=True)
d.n('move',220,720,'MOVE 歷史|F12DM.DM_Move_Step_bth',w=360)
d.d('move-link',610,720,'機台 MOVE|Lot_id')
d.d('summary',1390,720,'站點 Summary|Lot_id')
d.n('step',1780,720,'Step 歷史|F12DM.DM_Lot_step_st',w=350)
d.d('all-actions',1000,1000,'貨所有動作|Lot_ID',issue='U04',w=350)
d.n('history',1000,1260,'批貨歷史|Siview.FHOPEHS_S',w=350)
d.n('cast',1780,200,'Foup|Siview.frcast')
d.d('cast-link',1780,440,'Lot 在 Foup 內|Siview.frcast',w=350)
d.d('mes-transfer',2180,200,'MES 傳送歷史|Carrier_id',w=340)
d.n('transfer',2580,200,'傳送歷史|Mfg_Carrier_te_ut',issue='U05',w=340)
d.d('mcs-transfer',2180,460,'MCS 傳送歷史|Carrier_id|transfer_job_id',w=360,h=190)
d.n('mcs-history',2580,460,'MCS 傳送歷史|carrier_job_history@mcsdb|transfer_job_history@mcsdb',w=390,h=140)
d.d('qtime-link',1780,1000,'Qtime 站點|Lot_ID|Ope_no',h=190)
d.n('qtime',1780,1260,'Qtime 歷史|F12DM.DM_Qrest_Hist_BTH',issue='U06',w=390)
for a,b in [('predispatch','pre-link'),('pre-link','lot'),('lot','all-actions'),('all-actions','history'),('cast','cast-link'),('cast-link','step'),('step','qtime-link'),('qtime-link','qtime')]:d.e(a,'B',b,'T')
for a,b in [('move','move-link'),('move-link','lot'),('lot','summary'),('summary','step'),('cast','mes-transfer'),('mes-transfer','transfer'),('mcs-transfer','mcs-history')]:d.e(a,'R',b,'L')
d.e('move-link','B','history','L',[(610,1260)])
d.e('cast','R','mcs-transfer','T',[(1980,200),(1980,335),(2180,335)])

d=Diagram('2673','LOT、Flow、Part、LR 與站點定義',2800,1830)
d.n('wph',1010,190,'IE 的 WPH 定義|F12DM.DM_TBL_IE_CTWPH',w=350)
d.d('wph-link',1010,420,'IE 的 WPH')
d.n('lr',1010,650,'LR 對映的機台|F12DM.DM_Flow_LR_EQP_BT',w=360)
d.n('pd-eqp',1430,190,'PD_ID 與機台|Siview.frpd_eqp')
d.d('pd-eqp-link',1430,420,'PD_ID 對映的機台',w=370)
d.n('pd',1430,650,'Flow PD|Siview.frpd')
d.n('part',1850,650,'PART 定義|Siview.frprodspec')
d.n('recipe',2270,650,'Recipe Group|Siview.CSFRRCPGRPST',issue='U07',w=360)
d.d('lr-link',1010,900,'LR 與機台|LCREIPE_ID',issue='U08',w=360)
d.d('pd-link',1430,900,'站點的 PD_ID',w=340)
d.d('part-link',1850,900,'PART 對映|Mainpd_id',w=340)
d.d('recipe-link',2270,900,'製程程式群組對照',issue='U09',w=360)
d.n('future',220,900,'未來的 Future Hold|Siview.frlot_futurehold',w=340)
d.d('future-link',620,900,'Future Hold|Lot_ID')
d.n('product-hold',220,1190,'Product Hold|Siview.CSFRPRHold',w=340)
d.d('hold-link',620,1190,'有 Prod Hold|Lot_ID')
d.n('lot',1020,1190,'LOT|Siview.frlot',blue=True)
d.d('flow-link',1430,1190,'Flow 定義|Part|Mainpd_id',h=190,w=340)
d.n('flow',1850,1190,'Flow|F12DM.DM_Flow_step_Bt',w=350)
d.d('lr-eqp-link',2270,1190,'LR 與 EQP_ID 對應|LCREIPE_ID',issue='U08',w=370)
d.n('lr-eqp',2640,1190,'LR 與機台對應關係|F12DM.DM_Flow_LR_EQP.BT',issue='U10',w=310,h=130)
d.d('forecast-link',620,1460,'未來的 Flow|Lot_ID|OPE_NO',h=190)
d.d('stream-link',1020,1460,'未來的各站|Lot_ID|OPE_NO',h=190)
d.n('forecast',620,1720,'未來的 Flow|F12dm.dm_tbl_lot_forecast',w=350)
d.n('stream',1020,1720,'Stream 到站時間|Stream_fcst_lot_st',w=340)
d.d('stage-link',1850,1460,'Stage 定義')
d.d('srts-link',2270,1460,'抽測跳站設定',issue='U11',w=340)
d.n('stage',1850,1720,'Stage 與 Module 定義|F12dm.dm_tbl_info_stage',w=350)
d.n('srts',2270,1720,'SRTS 設定|Siview.csfrsrts',w=340)
for a,b in [('wph','wph-link'),('wph-link','lr'),('pd-eqp','pd-eqp-link'),('pd-eqp-link','pd'),('lr','lr-link'),('pd','pd-link'),('part','part-link'),('recipe','recipe-link'),('forecast-link','forecast'),('stream-link','stream'),('stage-link','stage'),('srts-link','srts')]:d.e(a,'B',b,'T')
for a,b in [('future','future-link'),('product-hold','hold-link'),('hold-link','lot'),('lot','flow-link'),('flow-link','flow'),('flow','lr-eqp-link'),('lr-eqp-link','lr-eqp')]:d.e(a,'R',b,'L')
d.e('future-link','R','lot','T',[(805,900),(805,1080),(1020,1080)])
for a in ['lr-link','pd-link','part-link','recipe-link']:
    x=d.nodes[a]['x'];d.e(a,'B','flow','T',[(x,1050),(1850,1050)])
d.e('lot','B','stream-link','T')
d.e('lot','B','forecast-link','T',[(1020,1320),(620,1320)])
d.e('flow','B','stage-link','T')
d.e('flow','B','srts-link','T',[(1850,1320),(2270,1320)])

d=Diagram('2674','EQP、Load Port、Chamber 與 OHB',2350,1930)
d.n('udata',1050,190,'細部資料|SIVIEW.FRPORT_UDATA',w=360)
d.d('udata-link',1050,420,'有 L/P|D_THESYSTEMKEY',w=380)
d.n('port',1050,650,'機台 L/P|SIVIEW.FRPORT')
d.n('mode',220,650,'機台模式|SIVIEW.CSFRPORT_SUBMODE|SIVIEW.FHEMCHS',w=390,h=140)
d.d('mode-link',650,650,'機台模式|EQP_ID|PORT_ID',w=340,h=190)
d.n('default',1470,650,'機台的 Default STK|Siview.csfreqp_stk',w=340)
d.n('eqp-history',220,890,'機況歷史|SIVIEW.FHESCHS',w=350)
d.d('history-link',650,890,'機況歷史|EQP_ID')
d.d('port-link',1050,890,'有 L/P|EQP_ID')
d.d('default-link',1470,890,'Default STK|eqp_id')
d.n('bay',220,1140,'機台位置|MFG_EQP_BAY_BT',w=350)
d.d('bay-link',650,1140,'機台位置|EQP_ID')
d.n('eqp',1050,1140,'EQP|Siview.Freqp',blue=True)
d.d('chamber-link',1470,1140,'有 Chamber|eqp_id',w=340)
d.n('chamber',1890,1140,'Chamber 狀況|Siview.csfrprcrsc|SIVIEW.FHCSCHS',w=360,h=140)
d.d('owner-link',1050,1360,'機群與課別|EQP_ID',w=350)
d.d('ohb-link',1470,1360,'設定 OHB|EQPSTKID',w=340)
d.d('detail-link',1890,1360,'細部狀況|eqp_id|procrsc_id',w=340,h=190)
d.n('owner',1050,1580,'機群與課別|MFG_EQP_OWNER_BT',w=350)
d.n('ohb-eqp',1470,1580,'機群 OHB|Siview.csfrohb_eqp',w=340)
d.n('chamber-detail',1890,1580,'Chamber 細部|Siview.frprcrsc',w=340)
d.d('ohb-status-link',1470,1780,'OHB 狀況|OHB_ID',w=300,h=150)
# Lower branch extends canvas to keep every original object distinct.
d.height=2210
d.n('ohb-status',1470,2060,'OHB 狀況|Siview.csfrohb',w=320)
d.d('bmir-link',1870,2060,'設定 BMIR|OHB_ID',w=320,h=160)
d.n('bmir',2220,2060,'BMIR|SIVIEW.CSFROHB_CFG',w=250)
d.width=2400
for a,b in [('udata','udata-link'),('udata-link','port'),('port','port-link'),('port-link','eqp'),('default','default-link'),('eqp','owner-link'),('owner-link','owner'),('ohb-link','ohb-eqp'),('chamber','detail-link'),('detail-link','chamber-detail'),('ohb-eqp','ohb-status-link'),('ohb-status-link','ohb-status')]:d.e(a,'B',b,'T')
for a,b in [('mode','mode-link'),('mode-link','port'),('eqp-history','history-link'),('bay','bay-link'),('bay-link','eqp'),('eqp','chamber-link'),('chamber-link','chamber'),('ohb-status','bmir-link'),('bmir-link','bmir')]:d.e(a,'R',b,'L')
d.e('history-link','R','eqp','T',[(840,890),(840,1030),(1050,1030)])
d.e('default-link','L','eqp','T',[(1280,890),(1280,1030),(1050,1030)])
d.e('eqp','B','ohb-link','T',[(1050,1240),(1470,1240)])
d.e('bay-link','B','owner','L',[(650,1580)])

d=Diagram('2675','WIP、機群、機況與 OEE',2900,1570)
d.n('wip-history',1000,220,'一星期的七點二十分的 WIP|KER_WIP_Y_BTH',issue='U12',w=390)
d.d('wip-link',1000,450,'歷史 WIP|Lot_ID')
d.n('move',220,750,'MOVE 歷史|F12DM.DM_Move_Step_bth',w=360)
d.d('move-link',610,750,'機台 MOVE|Lot_id')
d.n('lot',1000,750,'LOT|KER_WIP_BT',blue=True)
d.d('chamber-link',1440,450,'機群與機台 Ch|EQP_GRP',w=350)
d.n('chamber',1870,450,'Chamber|ker_dm_sub_ch_eqp_grp_bt',w=360)
d.d('group-link',1440,750,'機群與機台|EQP_GRP',w=350)
d.n('eqp',1870,750,'機台|KER_EMP_EQP_GRP_CAP_UT',w=360)
d.d('virtual-link',2300,750,'屬於哪個虛擬群組|DYNAMIC_SQL',issue='U13',w=370)
d.n('virtual',2700,750,'虛擬 Group (*ALL)|KER_VR_EQP_GRP_DETAIL_BT',w=370)
d.d('all-actions',1000,1110,'貨所有動作|Lot_ID',issue='U04',w=340)
d.n('history',1000,1420,'批貨歷史|Siview.FHOPEHS_S',w=340)
d.d('status-link',1420,1110,'目前機況|EQP_ID')
d.n('status',1420,1420,'機台機況|KER_EQP_STATUS_BT',w=340)
d.d('eqp-oee-link',1840,1110,'機台歷史 OEE|EQP_ID')
d.n('eqp-oee',1840,1420,'機台 OEE 歷史|Ker_Eqp_Aaa_Oee_Ut',w=340)
d.d('group-oee-link',2260,1110,'機群目前 OEE|EQP_GRP',w=350)
d.n('group-oee',2260,1420,'機群目前 OEE|ker_dm_bt',w=340)
d.d('group-history-link',2680,1110,'機群歷史 OEE|EQP_ID',w=350)
d.n('group-history',2680,1420,'機群 OEE 歷史|Ker_Dm_Hourly_Bth',w=340)
for a,b in [('wip-history','wip-link'),('wip-link','lot'),('lot','all-actions'),('all-actions','history'),('status-link','status'),('eqp-oee-link','eqp-oee'),('group-oee-link','group-oee'),('group-history-link','group-history')]:d.e(a,'B',b,'T')
for a,b in [('move','move-link'),('move-link','lot'),('lot','group-link'),('group-link','eqp'),('chamber-link','chamber'),('eqp','virtual-link'),('virtual-link','virtual')]:d.e(a,'R',b,'L')
d.e('lot','R','chamber-link','B',[(1220,750),(1220,590),(1440,590)])
d.e('move-link','B','history','L',[(610,1420)])
for b in ['status-link','eqp-oee-link','group-oee-link','group-history-link']:
    x=d.nodes[b]['x'];d.e('eqp','B',b,'T',[(1870,930),(x,930)])

d=Diagram('2676','EQP、Port、Cast 與 LOT Process Status',1480,1520)
d.n('eqp',740,210,'EQP|FREQP')
d.d('eqp-id',740,450,'EQP_ID',w=300)
d.n('port',260,700,'PORT_ID|FRPORT')
d.n('cast',740,700,'CAST_ID|FRCAST')
d.n('chamber',1220,700,'CHAMBER ID|FRPRCRSC',w=330)
d.d('port-id',260,960,'EQP_ID')
d.d('cast-lot',740,960,'FRCAST_LOT')
d.n('udata',260,1210,'FRPORT_UDATA',w=330)
d.n('lot',740,1210,'FRLOT')
d.n('status',740,1410,'LOT Process|Status',kind='circle',w=210,h=150)
d.e('eqp','B','eqp-id','T')
for b in ['port','cast','chamber']:
    x=d.nodes[b]['x'];d.e('eqp-id','B',b,'T',[(740,590),(x,590)])
for a,b in [('port','port-id'),('port-id','udata'),('cast','cast-lot'),('cast-lot','lot'),('lot','status')]:d.e(a,'B',b,'T')

d=Diagram('2677','PD、ER、機台位置與狀態',2080,1440)
d.n('pd',240,220,'FRPD')
d.d('pd-key',670,220,'systemkey')
d.n('pd-eqp',1100,220,'MODULEPD_ID|FRPD_EQP',w=330)
d.d('eqp-id',1100,610,'EQP_ID')
d.n('bay',1540,460,'MFG_EQP_BAY_BT',w=330)
d.n('location',1920,460,'EQP|LOCATION|PHASE',kind='circle',w=240,h=200)
d.n('recipe',240,940,'FRMRCP')
d.d('recipe-key',670,940,'SYSTEMKEY')
d.n('recipe-eqp',1100,940,'FRMRCP_EQP',w=330)
d.n('eqp',1540,810,'FREQP',w=330)
d.n('status',1920,810,'EQP|STATUS',kind='circle',w=210,h=180)
d.n('er',240,1140,'ER',kind='circle',w=150,h=140)
d.n('lr',240,1340,'DM_FLOW_LR_EQP_BT',w=370)
for a,b in [('pd','pd-key'),('pd-key','pd-eqp'),('recipe','recipe-key'),('recipe-key','recipe-eqp'),('bay','location'),('eqp','status')]:d.e(a,'R',b,'L')
for a,b in [('pd-eqp','eqp-id'),('eqp-id','recipe-eqp'),('recipe','er'),('er','lr')]:d.e(a,'B',b,'T')
d.e('eqp-id','R','bay','L',[(1320,610),(1320,460)])
d.e('eqp-id','R','eqp','L',[(1320,610),(1320,810)])

def main():
    # User-confirmed corrections, 2026-09-13. Keep original transcription above traceable.
    resolved={f'U{i:02}' for i in range(1,14)}
    for diagram in charts:
        for node in diagram.nodes.values():
            node['lines']=[line.replace('LCREIPE_ID','LCRECIPE_ID').replace('一星期的七點二十分的 WIP','星期一的七點二十分的 WIP').replace('SIVIEW.CSFHPREDISP','Siview.CSFHPREDISP') for line in node['lines']]
            node['lines']=[{'目在':'EI 在','貨所有動作':'Lot 所有動作','F12DM.DM_Flow_LR_EQP.BT':'F12DM.DM_Flow_LR_EQP_BT'}.get(line,line) for line in node['lines']]
            if node['issue'] in resolved: node['issue']=None
        if diagram.name=='2671':
            diagram.notes=[(60,1500,'原圖獨立小字：siview.fhwlths（未另接線）')]
    for diagram in charts:
        svg=diagram.render().replace('橘色標記為尚待核對的原圖文字。','原先不清楚的文字已由使用者確認。').replace('橘色 U 編號請見待確認清單','原圖疑義文字已確認')
        (OUT/f'{diagram.name}.svg').write_text(svg,encoding='utf-8')
    data=[dict(name=d.name,title=d.title,width=d.width,height=d.height,nodes=list(d.nodes.values()),edges=d.edges,notes=d.notes) for d in charts]
    (OUT/'transcription.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Created 7 editable SVG diagrams.')

if __name__=='__main__': main()
