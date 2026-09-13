from pathlib import Path
r=Path(__file__).resolve().parents[2]
changes={
 'integrated-map.js':{'CSFRPREDISPATCH 是 FOUP 預派線索':'CSFRPREDISPATCH 表示派工系統預先安排 Lot 的目標機台'},
 'data-map.js':{'FOUP 已預派 ETCH-03':'Lot 已被派工系統預派 ETCH-03','原圖標「預派機台」及 eqp_id，對應安排的目標。':'表示派工系統預先安排 Lot 的目標機台；Lot 是主要對象，FOUP 是輔助關聯。'},
 'ER/SUBJECTS/subjects.json':{'FOUP 位置與預派':'FOUP 位置與 Lot 預派','設備可以是 FOUP 所在位置或預派目的地；兩種關係不表示同一設備 ID。':'設備可以是 FOUP 所在位置或 Lot 被派工系統預派的目標；兩種關係不表示同一設備 ID。','FOUP 位於設備的資料與預派機台資料用途不同；设备 ID 需要分別確認。':'FOUP 位置與 Lot 預派機台資料用途不同；設備 ID 需要分別確認。'}
}
for file,replacements in changes.items():
 p=r/file;s=p.read_text(encoding='utf-8')
 for a,b in replacements.items():s=s.replace(a,b)
 p.write_text(s,encoding='utf-8')
for file,prefix in {
 'AGENTS.md':'# 最新接續：MES-023 Lot預派機台\n\n使用者確認預派以Lot為主要對象，派工系統預先安排目標機台，FOUP輔助。右側加入Lot業務虛線（非已確認Join），Lot/EQP优先；專屬桌面／手機圖在assets/mes-023。入口er-atlas.html?subject=predispatch。測試python workitems/mes-023/check.py，讀REVIEW。不要以舊來源邊唯一規則刪除使用者已確認的業務邊；須保留provenance。\n\n',
 'WORKITEMS.md':'# 最新工作：MES-023 Lot預派\n\n右側新增Lot業務關聯，重製桌面／手機派工示意圖，主要對象Lot，FOUP輔助。桌面手機驗證通過，詳workitems/mes-023/REVIEW.md。\n\n'
}.items():
 p=r/file;p.write_text(prefix+p.read_text(encoding='utf-8'),encoding='utf-8')
p=r/'TEACHING_REVIEW_LOG.md';p.write_text(p.read_text(encoding='utf-8')+'\n## MES-023｜派工主詞是Lot\n\n使用者指出CSFRPREDISPATCH需加入Lot，派工系統預派的是Lot，FOUP輔助。以明示業務虛線补主詞，不猜SQL鍵；示意圖重製為Lot→派工系統→預派目標，區分本站可用、預先安排及實際到站／加工。\n',encoding='utf-8')
p=r/'openspec/changes/er-subject-focus/spec.md';p.write_text(p.read_text(encoding='utf-8')+'\n- MES-023 使用者補充：預派圖 MUST 包含Lot及EQP為主要關聯、FOUP為輔助。Lot—預派機台連線作已確認業務補充，以虛線及provenance明示，MUST NOT 冒充原始來源邊或已驗證Join鍵。專屬圖解釋派工系統預先安排Lot目標機台，不表示已到站或加工。\n',encoding='utf-8')
