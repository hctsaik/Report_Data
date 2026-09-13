# MES-038 批貨歷史

使用者確認每Lot的Hold/進機Process/拆批等動作均記在FHOPEHS_S。actions兩關係及合併歷史節點同步圖文，保留Lot_ID上下文，區分各種動作與Move過站統計。
assets/mes-038桌面lot-history-v2.png、手機lot-history-mobile-v1.png。動作並列而非先後流程；Split示意4片分成2+2，沒有增加晶圓。首版晶圓堆數不一致、Hold容器內直立片退回，修正後發布。提示主線見PLAN，發布生成來源exec-68d1eb07-024f-4913-89c1-3775b5c91b9f.png與exec-8cefb873-6350-4600-a325-85058188c5b4.png。各生成圖及手機頁面已實看。
python workitems/mes-038/check.py通過：四來源引用（三實際節點）、1440/390真實搜尋、圖文與放大、無JS error。證據tests/evidence/mes-038，未自動評品質，使用者審閱pending。integrate.py一次性勿重跑。
