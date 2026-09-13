from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=root/'freshness.js'
s=p.read_text(encoding='utf-8').replace('不满足','不滿足').replace('十分钟','十分鐘')
s=s.replace('r.map(c=>`<td>${c}</td>`)','r.map((c,i)=>`<td data-label="${head[i]}">${c}</td>`)')
s=s.replace('↓ 報表資料路徑','分支 A · MMDB → Reporting')
s=s.replace('↓ 另一條資料分支','分支 C · MMDB → Inline')
s=s.replace('↓ 透過交易服務取得線上狀態','分支 B · MMDB ↔ TX')
s=s.replace('<span class="branch-answer">可以</span>','<span class="branch-answer">三分鐘可接受</span>')
s=s.replace('<span class="branch-answer">不行</span>','<span class="branch-answer">三分鐘不可接受</span>')
p.write_text(s,encoding='utf-8')
p=root/'freshness.css'
s=p.read_text(encoding='utf-8')
s+='\n@media(max-width:700px){.architecture-branches>section{border-top:2px solid #a8c5db;padding-top:20px}.architecture-branches .path-label{font-weight:750;font-size:16px;text-align:left}.decision-pair>div{border-left:3px solid #a6c8de;padding-left:12px}.decision-pair .branch-answer:before{content:"條件：";font-size:15px}.table-scroll table{min-width:0}.table-scroll thead{display:none}.table-scroll tr{display:block;padding:12px 16px;border-top:3px solid #d2e2ef}.table-scroll tr:first-child{border-top:0}.table-scroll td{display:block;padding:8px 0;border:0;overflow-wrap:anywhere}.table-scroll td:before{content:attr(data-label);display:block;color:#366484;font-size:13px;font-weight:750;margin-bottom:3px}.table-scroll td:first-child{font-size:18px;font-weight:750}.table-scroll{overflow:visible}.history-arrow{font-size:0}.history-arrow:after{content:"↓ 經過其他站";font-size:16px}.join-arrows{font-size:0}.join-arrows:before{content:"↓ ";font-size:26px}.join-arrows span{font-size:16px}}\n'
p.write_text(s,encoding='utf-8')
