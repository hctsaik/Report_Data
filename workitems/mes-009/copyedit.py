from pathlib import Path
root=Path(__file__).resolve().parents[2]
for filename in ['advanced.js','workitems/mes-009/add_illustrations.py']:
    p=root/filename
    t=p.read_text(encoding='utf-8')
    for a,b in [('旧','舊'),('檢验','檢驗'),('完整图','完整圖'),('条件','條件'),('设备','設備'),('資格','資格'),('资格','資格'),('实际','實際'),('细節','細節')]:
        t=t.replace(a,b)
    p.write_text(t,encoding='utf-8')
