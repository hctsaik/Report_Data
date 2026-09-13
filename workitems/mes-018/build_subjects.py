"""Build faithful subject ER subsets. Safe to rerun; writes only subjects.json."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "ER/INTEGRATED/er-model-v2.json"
OUTPUT = ROOT / "ER/SUBJECTS/subjects.json"


def branch(key, title, relations, description):
    return {"key": key, "title": title, "refs": relations.split(), "description": description}


SPECS = [
    {
        "key": "lot", "title": "以 Lot 看裝載、設備安排與流程", "subject": "2671:lot",
        "description": "Lot 是生產批次。圖中同時保留 FOUP、EQP 與 Flow，從 Lot 的裝載、預到及流程定義理解資料。預到設備與 FOUP 所在設備可能是不同設備 ID，不能因共用 EQP 實體框便認定同台。",
        "core": "2671:cast-link 2671:lot-eqp 2673:flow-link 2671:location",
        "branches": [
            branch("loading", "裝載、Slot 與容器", "2671:cast-link 2671:slot 2671:material-link", "Lot 是批次、FOUP 是實體容器；裝載與 Slot 對應是不同關係。兩種容器資料表保持各自身分。"),
            branch("handoff", "Port 與設備交接", "2671:port-link 2671:has 2671:lot-eqp", "Lot 與 Port 的 EI 在關係、Port 所屬設備與 Lot 預到設備分別保留。不能直接解讀為 Lot 正在加工。"),
            branch("dispatch", "Lot 預派記錄", "2672:pre-link", "預派記錄是安排的紀錄；它不是設備實際加工紀錄。"),
            branch("control", "Product Hold 與 Future Hold", "2673:hold-link 2673:future-link", "Product Hold 與 Future Hold 是不同資料關係；Future Hold 不能直接當成已生效的當前 Hold。"),
            branch("history", "過站、站點與批貨歷史", "2672:move-link 2672:all-actions 2672:summary", "Move 是 Lot 過站事件，重工計入；不是 FOUP 搬送。MOVE 菱形原有三個端點，全部保留。"),
            branch("forecast", "未來 Flow 與到站預測", "2673:forecast-link 2673:stream-link", "預測未來站點與到站時間，不代表現在位置。來源未列 schema 的資料不與其他表合併。"),
            branch("flow", "Lot 的流程與 Stage 定義", "2673:flow-link 2673:stage-link", "沿 Lot 的 Part／Mainpd_id 找 Flow 定義，再沿原 Stage 定義關係看 Stage 與 Module 資料。")
        ]
    },
    {
        "key": "carrier", "title": "以 FOUP 看裝載、位置與搬送", "subject": "2671:cast",
        "description": "FOUP 是承載晶圓的實體容器。Lot 裝載、Slot 對應、所在設備及預派設備是不同關係；所在與預派也不保證是同一台設備。",
        "core": "2671:cast-link 2671:slot 2671:location 2671:predispatch",
        "branches": [
            branch("loading", "Lot 裝載與 Slot", "2671:cast-link 2671:slot", "同一 FOUP 可沿裝載與 Slot 兩種關係對應 Lot；保留兩個不同關係菱形。"),
            branch("location", "所在設備與預派設備", "2671:location 2671:predispatch", "FOUP 位於設備的資料與預派機台資料用途不同；設備 ID 需要分別確認。"),
            branch("transfer", "MES 與 MCS 搬送歷史", "2672:mes-transfer 2672:mcs-transfer", "搬送追蹤以 Carrier_id 等鍵連接；它是載具搬送歷史，不是 Lot Move 過站事件。"),
            branch("step-history", "FOUP 與 Lot 站點歷史", "2672:cast-link", "依原圖的 Lot 在 Foup 內關係連接站點歷史；歷史紀錄不等同於當前裝載狀態。"),
            branch("qtime", "站點歷史與 Qtime", "2672:cast-link 2672:qtime-link", "從 FOUP 關聯的站點歷史，再沿 Lot_ID／Ope_no 看 Qtime 歷史；不能把此鏈當作即時管制判定。")
        ]
    },
    {
        "key": "equipment", "title": "以 EQP 看交接位置與設備結構", "subject": "2671:eqp",
        "description": "EQP 是設備主詞，連到 FOUP 位置、Lot 預到、Port 與 Chamber。不同關係可能指向不同设备實例；本圖的設備框代表資料實體類型。",
        "core": "2671:lot-eqp 2671:location 2674:port-link 2674:chamber-link",
        "branches": [
            branch("handoff", "Lot、Port 與設備交接", "2671:has 2671:port-link 2671:lot-eqp", "Siview.Port 與 SIVIEW.FRPORT 是不同表，不合併。Lot 的 EI 在與預到關係也分別保留。"),
            branch("carrier", "FOUP 位置與預派", "2671:location 2671:predispatch", "設備可以是 FOUP 所在位置或預派目的地；兩種關係不表示同一設備 ID。"),
            branch("ports", "Load Port、細部與模式", "2674:port-link 2674:udata-link 2674:mode-link", "從 EQP 連到 FRPORT，再查看細部及模式；保留原鍵與關係端點。"),
            branch("chamber", "Chamber 與細部狀況", "2674:chamber-link 2674:detail-link", "Chamber 是設備內加工腔體；沿 eqp_id、procrsc_id 等原關係查看狀況及細部。"),
            branch("ownership", "機台位置、機群與課別", "2674:owner-link 2674:bay-link", "機台位置菱形有三個原端點，包含機群與課別；不能改成只有 EQP 與位置的兩端關係。"),
            branch("state-history", "機況歷史", "2674:history-link", "機況歷史可用於追蹤過去狀態；原圖未提供每表刷新契約，不能自行保證即時。"),
            branch("storage", "Default STK、OHB 與 BMIR", "2674:default-link 2674:ohb-link 2674:ohb-status-link 2674:bmir-link", "沿原 EQPSTKID、OHB_ID 關係查看設備儲位設定與 OHB 狀況；不連接身分未確認的其他設備來源。")
        ]
    },
    {
        "key": "flow", "title": "以 Flow 看 Lot、Stage 與製程對應", "subject": "2673:flow",
        "description": "此 Flow 表是步驟流程定義資料。Lot 經 Part／Mainpd_id 關聯流程，Stage／Module 與 LR 對應各有原關係；LR 與設備對應表不等同實際加工 Recipe 執行紀錄。",
        "core": "2673:flow-link 2673:stage-link 2673:lr-eqp-link",
        "branches": [
            branch("lot-part", "Lot 與 Part 定義", "2673:flow-link 2673:part-link", "Lot 關聯 Flow 與 Part 的 Mainpd_id 對映是不同原關係；不能憑教學概念新增捷徑。"),
            branch("stage", "Stage、Module 與抽測設定", "2673:stage-link 2673:srts-link", "Stage／Module 分組和 SRTS 抽測跳站設定各有資料來源。Flow 表包含步驟定義，但原圖沒有獨立 Step 實體，不能額外造節點。"),
            branch("logical-recipe", "LR 對映与 Recipe Group", "2673:lr-link 2673:lr-eqp-link 2673:recipe-link 2673:wph-link", "兩個 LCRECIPE_ID 關係原本分開，均保留。LR 對映設備、Recipe Group 與 WPH 定義都不是實際加工使用的 Physical Recipe 證據。"),
            branch("pd", "PD 與設備對應", "2673:pd-link 2673:pd-eqp-link", "沿站點 PD_ID 查看 Flow PD 與 PD_ID 對映機台資料；不與未列 schema 的 FRPD／FRPD_EQP 合併。")
        ]
    }
]


def build():
    raw = SOURCE.read_bytes()
    model = json.loads(raw)
    nodes = {n["id"]: n for n in model["nodes"]}
    edges = {e["id"]: e for e in model["edges"]}
    mapping = model["mapping"]

    def subset(subject, refs):
        relations = {mapping[ref] for ref in refs}
        assert all(nodes[r]["kind"] == "diamond" for r in relations)
        selected_edges = {e["id"] for e in edges.values() if e["a"] in relations or e["b"] in relations}
        selected_nodes = {subject}
        for eid in selected_edges:
            selected_nodes.update((edges[eid]["a"], edges[eid]["b"]))
        # Preserve direct ellipse attributes on included endpoints if present.
        for e in edges.values():
            if (e["a"] in selected_nodes and nodes[e["b"]]["kind"] == "circle") or (e["b"] in selected_nodes and nodes[e["a"]]["kind"] == "circle"):
                selected_edges.add(e["id"])
                selected_nodes.update((e["a"], e["b"]))
        for nid in selected_nodes:
            if nodes[nid]["kind"] == "diamond":
                assert {e["id"] for e in edges.values() if nid in (e["a"], e["b"])} <= selected_edges, f"Truncated relation: {nid}"
        reached = {subject}
        while True:
            old = len(reached)
            for eid in selected_edges:
                e = edges[eid]
                if e["a"] in reached or e["b"] in reached:
                    reached.update((e["a"], e["b"]))
            if len(reached) == old:
                break
        assert reached == selected_nodes, f"Disconnected view: {refs}"
        return {"nodes": sorted(selected_nodes), "edges": sorted(selected_edges), "relations": sorted(relations)}

    subjects = []
    node_views = {nid: [] for nid in nodes}
    edge_views = {eid: [] for eid in edges}
    for spec in SPECS:
        subject = mapping[spec["subject"]]
        item = {k: spec[k] for k in ("key", "title", "description")}
        item["subject"] = subject
        item["core"] = subset(subject, spec["core"].split())
        item["branches"] = []
        for b in spec["branches"]:
            item["branches"].append({k: b[k] for k in ("key", "title", "description")} | subset(subject, b["refs"]))
        all_edges = set(item["core"]["edges"])
        for view_key, view in [("core", item["core"])] + [(b["key"], b) for b in item["branches"]]:
            all_edges.update(view["edges"])
            for nid in view["nodes"]:
                node_views[nid].append(f"{item['key']}/{view_key}")
            for eid in view["edges"]:
                edge_views[eid].append(f"{item['key']}/{view_key}")
        direct = {e["id"] for e in edges.values() if subject in (e["a"], e["b"])}
        assert direct <= all_edges, f"Missing direct subject relationships: {spec['key']}: {direct - all_edges}"
        item["direct_relationship_count"] = len(direct)
        subjects.append(item)
    assert len(subjects[0]["core"]["nodes"]) == 8 and len(subjects[0]["core"]["edges"]) == 8
    document = {
        "version": 1,
        "model": "ER/INTEGRATED/er-model-v2.json",
        "model_sha256": hashlib.sha256(raw).hexdigest(),
        "subjects": subjects,
        "coverage": {
            "total_nodes": len(nodes), "total_edges": len(edges),
            "covered_nodes": sorted(n for n, views in node_views.items() if views),
            "covered_edges": sorted(e for e, views in edge_views.items() if views),
            "uncovered_nodes": sorted(n for n, views in node_views.items() if not views),
            "uncovered_edges": sorted(e for e, views in edge_views.items() if not views),
            "node_views": node_views, "edge_views": edge_views,
            "uncovered_access": "er-atlas.html?view=original",
            "note": "主題核心與分支不是全模型。未納入項目保留於完整 ER；未知 schema 的同名物件未合併、未假接。"
        }
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in subjects:
        print(item["key"], "core", len(item["core"]["nodes"]), len(item["core"]["edges"]), "branches", len(item["branches"]))
    print("coverage", len(document["coverage"]["covered_nodes"]), len(document["coverage"]["covered_edges"]))


if __name__ == "__main__":
    build()
