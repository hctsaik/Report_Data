from pathlib import Path
r=Path(__file__).resolve().parents[2]
for filename,prefix in {
'TEACHING_REVIEW_LOG.md':'''# MES-008｜新鮮度品質退回，重新製作

MES-007 新鮮度六頁及五張原生圖的高分與通過判斷撤回。使用者再次指出品質低落。第一課有實物→局部→記錄對應，舊新鮮度只有文字框、抽象關係與過量留白；功能測試沒有發現這種落差。已保存基線，製作前學習與六頁 brief 見 [MES-008 PLAN](workitems/mes-008/PLAN.md)。本輪改用現場／快照對照插畫、逐欄時間映射與可操作結果；手機另做閱讀構圖。先檢查 AI 原型再展開。MES-007 其他課仍未獲使用者驗收，本輪不改其內容。新鮮度製作中，未評分，user_acceptance: pending。

''',
'WORKITEMS.md':'''# 目前工作：MES-008

資料新鮮度六節重新製作；MES-007 新鮮度高分已撤回。基線、學習、brief 與驗證計畫：[workitems/mes-008/PLAN.md](workitems/mes-008/PLAN.md)。狀態：製作中；使用者未驗收。

''',
'AGENTS.md':'''# 最新接續：MES-008

先讀 workitems/mes-008/PLAN.md 及 TEACHING_REVIEW_LOG.md 最新段。使用者再次退回資料新鮮度，MES-007 新鮮度的頁面／圖像高分與通過判斷已撤回。MES-007 manifest 是歷史版本快照；本輪修改後不要求它與新 freshness 檔相同，不覆寫歷史 hash 掩蓋差異。新證據用 tests/evidence/mes-008。前三課本輪不改。沿用使用者重製授權，必須實際改網頁與圖，不只寫反省。新鮮度尚在製作，使用者審閱 pending。

'''
}.items():
    p=r/filename
    p.write_text(prefix+p.read_text(encoding='utf-8'),encoding='utf-8')
