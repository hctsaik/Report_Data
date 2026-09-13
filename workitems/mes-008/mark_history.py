from pathlib import Path
r=Path(__file__).resolve().parents[2]
p=r/'workitems/mes-007/REVIEW.md'
p.write_text('''# 狀態更新：資料新鮮度評分已撤回

使用者在MES-008再次指出資料新鮮度品質低落。本檔下方新鮮度六頁與五張原生圖的高分／通過判斷均已撤回，只保留歷史；新版與退回理由見 [MES-008 REVIEW](../mes-008/REVIEW.md)。原始未加此狀態的檔案已保存到 [MES-008 baseline](../mes-008/baseline/REVIEW.md)，供歷史hash核對。其他課的作者評比不代表使用者認可。

'''+p.read_text(encoding='utf-8'),encoding='utf-8')
p=r/'AGENTS.md'
s=p.read_text(encoding='utf-8').replace('目前版本 MES-007：','歷史版本 MES-007：').replace('MES-007證據檢查執行 `python tools/verify_mes007_evidence.py`；','歷史MES-007證據檢查為 `python tools/verify_mes007_evidence.py`，不適用MES-008的新鮮度檔案；')
p.write_text(s,encoding='utf-8')
