from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
d=json.loads((root/'tests/evidence/mes-053/inventory.json').read_text(encoding='utf-8'))
groups={
 '1': 'load material',
 '2': 'part stage flowkey',
 '3': 'available chamber port eqpstatus pd recipegroup lotstatus eqpkey',
 '4': 'transfer prehistory portmode location stock ohb mcs bmir',
 '5': 'future producthold srts',
 '6': 'lotstep contents move actions',
 '7': 'forecast stream',
 '8': 'wip oee bay group virtual owner',
 '來源參考': 'retired',
 '撤下': 'portdata'
}
mapping={k:g for g,keys in groups.items() for k in keys.split()}
assert set(mapping)=={t['id'] for t in d['topics']}
text='''# 現有內容與建議課綱對照

此為 MES-053 設計映射，尚未改動網站。單元編號依 [總建議第6節](DESIGN-RECOMMENDATIONS.md#6-建議課綱能力與先備先於檔案)。主歸屬不限制其他課引用；有主題或圖片不等於能力教學已完成。

## 現有頁面

| 入口 | 現有用途 | 建議歸屬及處理 |
|---|---|---|
| index.html | Fab／Wafer／FOUP／Slot／Lot、互動、自測 | 單元1；另建總覽，保留原錨點 |
| operations.html | 設備、搬送、配方、加工與六情境 | 拆入3、4及6；情境依先備重排 |
| flow.html | Flow到版本與十情境 | 基礎入2；例外入5、歷程與拆合批入6 |
| freshness.html | 來源架構、時間、資料契約與情境 | 1起即引入時間觀念，完整深化入8 |
| advanced.html | QTime、Future Hold、PART、Recipe、Flow教法比較 | 2/3/5；教法比較移導師資源 |
| support.html | CW、Sub Route、Move、MON/PM/EMS | 3/5/6；不維持增補雜項集合 |
| er-atlas.html | 完整ER、局部主詞、題目、專屬圖 | 共用資料參考與各單元局部入口 |
| integrated-map.html | 轉址 er-atlas | 保留 query/hash 相容性 |
| data-map.html | 七張原圖與導讀 | 來源參考，從整合ER可回查 |
| subject-er.html | 主詞及分支閱讀 | 先盤功能差異再整併；不另養一套定義 |
| ER/NEW/index.html | 原圖入口 | 原始來源保留，退出新手必經路線 |

## 主題 registry：逐項歸屬

執行時 `ER_TOPIC_CONTENT.topics` 共38項，以下全部對應；不等於全站只有38個概念，也不包含 ER內建主題及其他課的所有子題。refs為現有原圖識別，保留供稽核。

| topicId | 現有主題 | 主歸屬 | 原圖 refs | 處理 |
|---|---|---|---|---|
'''
for t in d['topics']:
 k=t['id'];g=mapping[k]
 note='沿用定義與現有教材，補先備／任務／返回'
 if k=='stream':note='標示已由LDS取代，留單元7歷史參考'
 if k=='portdata':note='維持撤下；不重新加入課綱'
 if k=='retired':note='原圖校正追溯，不作正確關係教學'
 if k=='wip':note='分別說明目前來源與KER_WIP_Y_BTH每日07:20；不暗示粒度相同'
 if k in ['contents','lotstep']:note='歷史對象與時間清楚；與現在狀態分開'
 text+=f"| `{k}` | {t['title']} | {g} | {'、'.join(t['refs'])} | {note} |\n"
text+='''
## ER 內建與跨課概念

| 概念 | 主歸屬 | 注意 |
|---|---|---|
| Lot／carrier／Wafer／Slot | 1 | 沿用25槽與多Lot互動；不是38項registry的完整替代 |
| equipment | 3 | EQP、Port、Chamber角色；与設備狀態分清 |
| flow | 2 | 最小流程模型前移，保留版本語境 |
| recipe／LR／ER／Physical | 3 | 與PD相接，分層展開；ER縮寫依上下文明示 |
| predispatch | 4 | 與可用設備、到位及進機分開 |
| qtime | 5 | 明示計時起迄事件、Lot與站點 |
| wph | 7 | 預期產出標準；預測不是實績 |
| overview／source fallback | 0及來源參考 | 是導引及未知節點處理，不當作專屬內容覆蓋證明 |
| CW／MON／PM／Daily MON／EMS | 3、5支線 | 材料用途與設備條件，避免只因同在support而綁同章 |
| Rework／Sub Route | 5、6 | 路徑許可與實際事件分開 |
| Split／Merge | 6，1先教成員概念 | 保留Wafer譜系，不把換載具等同拆批 |
| Finished／本站完成／E出貨 | 3、6 | 明示完成範圍，不直接合併 |
| 來源新鮮度／晚到／混合時間Join／資料契約 | 8，前課漸進引入 | 每次查詢就問時點，不等資料章才提醒 |

## 遷移檢核

建議實作前建立機器可驗證的 lessonId/topicId/舊URL/新URL/先備/資產/來源對照，逐節而非只有逐HTML。此文件已覆蓋現有入口及38項registry的主歸屬；尚未提供所有旧錨點轉址契約，也未宣稱完成全量圖片品質稽核。

每次遷移核對：舊連結可達、專屬圖未錯配、有效文字和廠內確認一致、課程到ER再回來有脈絡、案例片數與時間範圍一致。未確認或原圖保留項必須有清楚狀態。
'''
(root/'workitems/mes-053/CONTENT-MAP.md').write_text(text,encoding='utf-8')
print('Mapped all 38 registered topics plus page and built-in concept families.')
