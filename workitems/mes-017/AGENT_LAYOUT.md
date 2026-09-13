# MES-017 Layout implementation

Use a source-derived subject root and readable relationship branches, preserving rectangles, diamonds, ellipses, complete source labels and edge identity. Four branches appear per page; explicit page controls expose every remaining branch. Labels reflow at the actual container width, and mobile uses vertical relation chains instead of shrinking desktop artwork. Recipe retains its full five-node configuration path to EQP. No Wafer entity or unsupported source edge is invented.

Implemented in er-focus.js and er-focus.css. Interface: init(model, {selectNode}), show(rootId), clear(), getState(). Root owns atlas integration and browser validation. SVG is deterministic native code suited to the requested ER graph; no raster teaching artwork was generated. Existing source SVG is unchanged.

Plan: extract actual relation branches, preserve Recipe chain, render responsive SVG, add pagination and enlargement, then validate integrated real pointer interaction and source edge provenance. Functionality is not a visual quality score or user approval.

## Actual prototype screenshot review

Viewed all ten `tests/evidence/mes-017/{1440,390}-{lot,carrier,equipment,flow,recipe}.png` images after integration. This review concerns those screenshots, not unseen later pages or later revisions. No numerical quality score assigned.

Confirmed visible: subject has a distinct fill and thicker colored border; source entity labels remain legible; each displayed relation has a diamond and real connected endpoint; desktop uses relation/entity rows and mobile reflows vertically; Recipe shows FRMRCP → SYSTEMKEY → FRMRCP_EQP → EQP_ID → FREQP without a fabricated shortcut, plus separate ER annotation.

Defects found and sent to integration owner:

- Both desktop and mobile equipment screenshots show the long `SIVIEW.CSFRPREDISPATCH` schema colliding with the lower diamond boundary. Diamond dimensions need text taper clearance, not just bounding-box containment.
- Four mobile branches produce approximately 1,400–1,500 px of panel height, putting branch pagination far below the root. Two branches per mobile page would shorten reading, but preserve useful initial endpoint variety: FOUP should initially show Lot and EQP, rather than Lot and Step history.
- FOUP, Lot and LR entities appear more than once for different source relationships. Add an explicit statement that these occurrences refer to the same entity; preserving multiple relations should not suggest duplicate tables.
- Parallel root rails run close together on the left. They remain visible and distinguishable in these screenshots, but are not an ideal visual for high-degree subjects; pagination limits this cost.

The Recipe mobile chain has no observed overlap and preserves the full relation/key path. Source correctness was separately checked by the semantic agent; this screenshot review does not itself prove all branches or pointer interaction.

## Revised screenshot review

Re-opened the refreshed `1440-equipment.png`, `390-equipment.png`, and `390-carrier.png` after the integration owner revised diamond geometry, branch priority and mobile pagination.

- Desktop EQP: the previously colliding `SIVIEW.CSFRPREDISPATCH` label now sits entirely inside a taller diamond with visible clearance from its slanted edges.
- Mobile EQP: first page now contains two branches (Lot and FOUP), with pagination above the graph. Labels remain legible and the subject is still distinct. The entire panel is about 1,067 px rather than about 1,457 px in the earlier screenshot.
- Mobile FOUP: first page now shows Lot and EQP, satisfying the intended initial entity context. The former Step-history branch no longer displaces equipment from the opening view.
- Both mobile screenshots explicitly explain that one entity can be displayed repeatedly for different relationships, and that this is not every indirect association.

Remaining evidence limit: the mobile predispatch diamond moved to page 2, which is not included in the refreshed first-page screenshot reviewed here. Its desktop fix is visually confirmed; this entry does not claim to have visually reviewed that mobile second page. No numerical score or user acceptance is inferred.

主 agent 補充（非 agent 自評）：最終已另拍並實看 tests/evidence/mes-017/390-equipment-page2.png，預派長表名保留全字且沒有碰斜邊，窄版仍會換行。
