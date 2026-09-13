# MES-014：重畫、Multi-agent 評分與修正

## 最終交付 v2

- 網站：`er-atlas.html?view=original`／`?view=questions`。原本`integrated-map.html`自動轉到新版，保留mode與題目。
- 大圖：`ER/INTEGRATED/fab-er-v2.svg`；模型與來源對照：`er-model-v2.json`。
- 七張原圖128節點／128邊，全部映到實際SVG；六組確定表識別合併後121節點，128條線。
- 中性灰菱形保留關係或鍵；彩色矩形保留實體／資料對象；橢圓保留概念／屬性註記。主圖沒有來源圖號、主題摘要盒或教學推論線。
- 原本網站首頁及第二／三部分側欄入口可達，保留七張原圖與逐圖教材。

## Multi-agent：確實在重畫後審查

量表在製作前固定於`ER_REVIEW_RUBRIC.md`：完整性35、語意25、可讀性25、教學操作15。這是ER任務專用，不改歷史AI模型量表。

| 審閱者 | v1 | v2 | 驗證與限制 |
|---|---|---|---|
| merge_rules 完整性 | 完整35/35、語意22/25；未全評總分 | 完整35/35、語意25/25；不補未評總分 | 獨立逐項核對128原節點文字與128邊到SVG；桌面手機逐一選121節點，所有配對與DFS步驟為真實邊 |
| er_critic 語意／教學 | 77/100，退回 | 91/100：34+24+20+13 | 獨立來源核對、拆除不明裸表合併、色彩分類、手機逐一定位121節點無文字水平越界；長關係需逐點 |
| er_layout 可讀性／操作 | 78/100，退回 | 91/100：32+23+22+14 | 實看桌面手機與五條路徑每個節點；90%逐點約18px；直接點圖、上一下一點、鍵盤平移、CDP模擬雙指縮放通過 |

完整獨立報告：[完整性](AGENT_COMPLETENESS.md)、[語意](AGENT_SEMANTICS.md)、[可讀性](AGENT_VISUAL.md)。未把三份評分平均掩蓋缺口；專項審閱者沒有檢查的項目不填假總分。

## v1 → v2 實際修正

1. 初稿完整fit使手機最小只有約2–8px、Move只有13%比例；改為低於80%就切90%沿線閱讀，有「本段全貌」及上一／下一點。所有座標固定、不另造局部圖。
2. 點星狀分支時，inspect把鄰接集合錯列成線形路徑；改為每一條真實edge的兩端配對，巡覽用DFS沿實際邊往返。agent再次全量验证。
3. 兩組未列schema的同名FREQP與MFG_EQP_BAY_BT存在識別疑義；拆回獨立節點，119→121，不再把保守判斷當已確認同表。
4. Hold／forecast／stream按同一紀錄類別用灰色，不因字串含Lot或Flow而誤上核心色。
5. 橢圓的圖例與點選解說改為概念／屬性註記，不直接当欄位或資料表。來源獨立fhwlths小字也保留在展開說明。

第一個原型使用原圖Lot／FOUP／EQP核心，先比較實際渲染；neato/fdp布局空間過大，採dot階層布局與固定位置逐點閱讀。布局由[Graphviz官方工具](https://graphviz.org/download/)產生，下載SHA-256核對後在本地使用，沒有用影像模型猜文字。

## 實際檢查

`python tests/check_er_atlas.py`為目前v2檢查：來源128節點／128邊、實際SVG文字／端點、121節點、未確認同表不合併、七張原圖hash不變；17條路徑×1440/390、5題×兩寬度、每個配對真實邊、聚焦比例下限、搜尋、縮放與鍵盤平移。結果在`tests/evidence/mes-014/v2/verification.json`。

`python workitems/mes-014/geometry_audit.py`：沿128條SVG線每6座標單位取樣，沒有穿過無關節點的填滿區域；文字不超出shape水平範圍。取樣不是形式化曲線證明。`geometry.json`保留結果。

`python workitems/mes-014/check_entry.py`：從原網站兩個側欄進入新版、旧URL保留問題模式、橢圓點選說明。

父agent實看v1原型、完整圖與初版長路徑，修正後看v2手機load／Move與桌面Flow；完整視覺範圍另由er_layout報告限定。不是只用DOM通過宣稱實圖已看。

## 實際限制與狀態

可以交付使用者審閱；不是使用者已驗收。全圖密集，長邊兩端仍需逐點切換或平移，手機不宣稱一屏讀完；框線色只輔助辨認，文字與形狀仍是必要線索。沒有真實MES查詢、Join基數或控制權限驗證，沒有憑空補Physical Recipe執行資料。未知schema需保留分開。

維護：`build_er.py`可重新生成v2；`connect.py`、`refine_v2.py`、`final_touch.py`是一次性修改，不要重跑。`tests/check_er_atlas.py`已升為v2正式檢查，v1在baseline。v1圖、截圖與低分保留，不覆寫成通過證據。
