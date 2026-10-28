---
name: classic-adaptation
description: Runbook for producing the complete adaptation package of one Shanhaijing sub-classic (子經) — station mileage grid, per-entity mappings, adaptation report, sentence-level analysis document and SVG map — from a confirmed initialization anchor. Use when adapting any single 子經 of the Five Mountain Classics.
---

# 子經適配 runbook

以西次三經包（`projects/shanhaijing/data/derived/era/adaptation/xici3-*`）為工作範例。任何子經的適配按本 runbook 執行，產物結構與命名保持一致。

## 基礎判斷約束（每階段必守）

靜態形狀優先／禁止因果倒置／古代通用詞義／文化斷層保持未知／統一推論順序（原文 → 靜態形狀與物理特徵 → 古代通用詞義 → 同時代候選 → 對稱評估 → 可信度與未知項）。動態流向僅作無方向連接；現代水流、後世地名、傳播鏈缺失、現代狹窄分類不得單獨否決。語義判斷全部由 LLM 產生；代碼只做算術展開、結構保存與覆蓋核對。

**名稱永不作錨（發起人 2026-10-23 裁定）**：成書在前、後世命名在後——任何與現實地名相同的文本名（包括汾水、管涔山、太室少室、洞庭、岷山等中原名）一律只標記「後世借名方向」，不得作為錨點或證據。錨定與映射的證據順序固定為：**① 水系拓扑（無方向連接、分水嶺、共享水體、多水匯流格局）→ ② 山勢走向（里程鏈方位與相對位置）→ ③ 人文風物（動植物物產、禮制、造像、生業描述）**。名稱重合只能作為旁證標記與借名案例記錄。

## 輸入

- `data/derived/working-text.jsonl`：條目原文與次序。
- `data/derived/era/profiles.jsonl`：腿程方位、里程合計、地形與物產概貌。
- `data/derived/kg/nodes.jsonl`、`edges.jsonl`：實體節點與關係（覆蓋核對基準）。
- `data/derived/era/anchors.jsonl`：初始化錨點。
- 已完成的前序子經適配包：鏈條校準依據（西山經之首→二→三→四為順序擴展，彼此不重疊）。
- `reference/shanhaijing/text/06–18`：海內/海外/大荒跨卷證據引文來源。

## 執行步驟

1. **錨點確認**：與項目發起人確認本子經的初始化錨點（未確認、無證據優先權）。多錨點可聯合校準。
2. **里程鏈展開**（代碼，純算術）：從原文解析腿程方位與里數，以錨點為原點按 0.35/0.385/0.42 km/里 三檔展開站點坐標 → `<slug>-station-grid.jsonl`。記錄 stated 總里數 vs 腿程合計差異。
3. **逐實體映射**（LLM）：全部 MTN/WAT/LND 及次級地物（望點、宮囿、門戶等），**零遺漏**——以 KG 節點按條目前綴核對覆蓋。每實體：主候選＋對立候選（≥2 大區，窗口期存在）、屬性逐項比較、演化邏輯（改道/消亡/萎縮/沼澤化/運河遺址/性狀改變）、跨卷證據（逐字引文＋出處 ID）、可信度、衝突與未知項 → `<slug>-mappings.jsonl`。全部 `proposed_pending_review`。
   - **山體必附現實山名（發起人 2026-10-23 裁定）**：每個 MTN 實體的主候選除區域方向外，必須給出可核驗的現代山體名稱（山脈/山嶺/山峰，如「伏牛山·老鴉岔堖」），寫入 `modern_mountain` 字段；只有方向性擬合而無法落到具體山體時，填「未定位——僅區域方向」並列入未知項，**不得編造山名**。水體同理給現代河/湖名（`modern_water`），遺址/消亡水體給最後可考的地理單元名。現實名稱是映射結果的表述，**不是證據**——證據順序仍為水系拓扑→山勢走向→人文風物。
4. **適配報告**：方法、里程核算表、全站映射總表、水系統配置、跨卷證據彙編、演化邏輯摘要、衝突與未知、宏觀範圍修正（如有）、待審清單 → `<slug>-adaptation.md`。
5. **逐句文檔**：每條目按固定四段式——原文引錄／逐句全要素展開（引用 KG 節點 ID）／時代映射表（4000–1000 BCE 坐標、考古-古生物分類、存續狀態）／4D 交叉驗證（地理相對屬性、人文、風物、歷史演化、跨卷證據）→ `<slug>-sentence-analysis.md`。文末附機器核對用節點引用索引。
   - **時代映射表零遺漏（發起人 2026-10-23 裁定）**：該條目 KG 節點（含 §2 展開的全部山水人文風物——MTN/WAT/LND/CRE/PLA/MIN/PER/OBJ/AST/CLIM/POL）**全部**在時代映射表有行，機器核對（按 `first_entry` 前綴）不得有缺。基準動物/否定記錄/兆象/祀物亦入行——無現實映射者標「依附本站／framework」；判讀文字一律取自已核准的 mappings.jsonl 或 §2 展開文本，**不得生成碎片文本**。
   - **配套零遺漏**：`<slug>-mappings.jsonl` 必須覆蓋本子經全部 MTN/WAT/LND 節點（含否定水文記錄與泛稱水體——否定/泛稱以 `period_state:"n/a"` 或低置信記）；CRE/PLA/MIN/PER 以文檔表格承載，不入 mappings.jsonl。
6. **SVG 地圖**：由 `atlas-renderer` 依 `specs/<slug>-map.json`（spec 為唯一事實源；底圖/假想特徵/注記全入 spec）＋ `<slug>-station-grid.jsonl` 渲染 → `<slug>-map.svg`；算術網格與擬合走廊大幅背離時用 spec 的 `fit_coords`（僅繪圖覆蓋）並記 variant。概要圖（每經一張＋五臧總體一張）由 `render_overview_map.py` 依 `specs/<name>-overview.json` 生成。
7. **findings**：覆蓋缺口（缺節點）、同名異水/異地衝突、原文內部差異記入 `projects/shanhaijing/findings/`。

## 命名與位置

- 產物置於 `projects/shanhaijing/data/derived/era/adaptation/`。
- slug 規則：`xici3`＝西次三經；西次四經＝`xici4`，南次二經＝`nanci2`，中次五經＝`zhongci5`，以此類推。

## 校驗（交付前必過）

- 全部 JSONL 逐行 `json.loads` 通過。
- 覆蓋核對：該子經全部 KG 節點在 mappings 或逐句文檔中被引用（腳本比對，uncited 必須為空）。
- 地圖：XML 解析通過＋文本溢出審計（無文本越過地圖/面板邊界）＋瀏覽器或柵格化目檢。
- `git diff --check` 通過；每任務完成即提交。

## 鏈條校準規則

- 里程與方位是硬約束：若錨點＋里程鏈推出的範圍與先前宏觀估計衝突，**以里程為準並向發起人明示修正**，不得靜默更改。
- **嚴格走向校準（發起人 2026-10-29 裁定，adapt-beici3-3 首用）**：語義站位（fit_coords）必須使**每一腿**的實際方位落在經文方位容差錐內（八方位 ±22.5°；北腿整體可作 NNW 緩漂但單腿不得越出容差錐）——站位間不得出現違背經文走向的折返/橫跳（如經文「南」而圖上向東北）。校準程序：①以純地理指紋錨（資源/物種/地形，無名稱成分）定關鍵站；②前向/後向逐腿推進選址；③數值檢驗每腿實際方位與實距，輸出逐腿實測比（實距km/文本里數）；④方位無法兩全的站點記校勘存疑（不為錨點強行附會）；⑤分段里程比值（保真/壓縮/拉伸）寫入適配報告 §1。走向指**經文的走向**（腿程方位），不是山勢走向。
- 共享水體是跨山/跨經錨點：同名水體出現在多站時，優先檢驗「同一水體」與「同名異水」兩種假說，衝突標記 pending，不在本層裁決。
- 同名地物（如積石、恒山、湯谷）若與後世中國地名相同，記為後世借名方向（因果倒置警示），不得反證。
