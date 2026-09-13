from pathlib import Path
p=Path('catalog.js');s=p.read_text(encoding='utf-8');s=s.replace("l('freshness.html','來源、時間與資料契約')", ",".join("l('freshness.html#%s','%s')"%(key,title) for key,title in [('architecture','來源架構與新鮮度'),('decision','按工作需求選來源'),('ai','異常後的資料時間'),('history','歷史與現在'),('join','欄位來源與時間對齊'),('contract','資料契約')]))
p.write_text(s,encoding='utf-8')
p=Path('site-shell.css');s=p.read_text(encoding='utf-8')+'\n.mes-unified #sidebar>.course-link{display:none!important}#mes-context details ol{padding-left:24px;margin:10px 0;max-width:600px}#mes-context details li{padding:5px 0}\n';p.write_text(s,encoding='utf-8')
p=Path('support.js');s=p.read_text(encoding='utf-8');s=s.replace('本輪未將它們畫成已確認的狀態圖。','Port 的 UP／LOST 則表示有貨／沒有貨，須依對象判讀。');p.write_text(s,encoding='utf-8')
print('Added all six freshness lessons to the shared sequence and refined confirmed status wording.')
