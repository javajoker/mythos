# 山海經 Web App — 技術規格

> 版本 0.1（2026-10-26）。對齊 PRD/UIUX 0.1。

## 1. 技術選型

- **純靜態站**：無後端、無構建框架依賴——Vanilla HTML/CSS/JS + SVG。可離線打開（file://）與任意靜態託管。
- 地圖：項目自產 SVG（子經/補丁/概要）＋首頁自研 SVG 世界視圖（數據自 `era/adaptation/` 導出為精簡 JSON，前端用 SVG 渲染＋自寫 pan/zoom，不引 Leaflet/瓦片——離線約束）。
- 無 npm 構建要求；如需開發服務器，`python3 -m http.server` 即可。

## 2. 數據管線（導出器 → 靜態 JSON）

新增工具 `tools/shj/webapp_export.py`（冪等，只讀不改寫源數據）：

| 輸出 | 來源 | 內容 |
|---|---|---|
| `webapp/data/graph.json` | kg/nodes+edges+attributes | 節點（id/類型/名/首出條目）、邊（REL:FW＋山經水系）、屬性（era.candidate/state、讀法、賦義） |
| `webapp/data/entries.json` | working-text + draft-v2 | 869 條目：原文、白話解讀、未決項、配圖引用 |
| `webapp/data/map-chains.json` | 26 站點網格＋各 spec | 鏈坐標（含 fit_coords 覆蓋）、錨站、色族、書籤 label_pos |
| `webapp/data/map-points.json` | book06-18 spec points | 402 點（狀態/顏色/note/label） |
| `webapp/data/basemap.json` | wuzang-overview spec | 世界海岸線/地貌塊（太平洋中心；lon_wrap_below=-25 規則內置） |
| `webapp/data/adjudications.json` | findings/ | ADJ-002…005、F-0001…0012 摘要與鏈接 |
| `webapp/images/` | draft-v2/images/ | 111 張本地實拍（複製引用） |
| `webapp/maps/` | era/adaptation/*.svg | 45 張地圖（原樣引用） |

導出器必須重跑 `kg_validate.py` 前置檢查；導出量變化（節點/邊/屬性/圖片計數）寫入 `webapp/data/manifest.json`（含 source SHA）。

## 3. 前端結構

```
webapp/
├─ index.html        # 世界地圖主視圖（SVG + pan/zoom + 圖層開關 + 詳情側欄）
├─ book.html         # 卷頁（?book=NN）
├─ entry.html        # 條目詳情（?id=SHJ-…，可被地圖/卷頁共用為側欄內容）
├─ entities.html     # 實體庫（類型樹/搜索/類名聚合）
├─ entity.html       # 實體詳情（?id=TYPE:SHJ-…）
├─ adjudications.html
├─ about.html
├─ css/app.css
├─ js/{app.js, map.js, store.js}
└─ data/ images/ maps/
```

- 座標：前端實現 `lon_wrap_below=-25` 太平洋中心投影（與渲染器同規則），equirectangular。
- 性能：點位 402＋鏈站 ~470 全部為 SVG 元素可接受；圖片 `loading="lazy"`；地圖 JSON 按需 fetch。
- 無外部字體/庫 CDN；系統字體棧。

## 4. 數據誠實性技術約束

- 導出器對每條目帶 `review_status`；前端無該字段不渲染候選（防漏標）。
- 借名/類名/神話層為數據字段（來自 mappings conflicts/unknowns/ADJ 注記），前端只讀。
- 所有頁面頁腳常駐：「全部對應為競爭假說（proposed_pending_review）；時代窗口 4000–1000 BCE」。

## 5. 測試與驗收

- 導出器：輸出 JSON schema 自檢＋計數對賬（nodes 4,334／edges 1,805／attributes 9,234／entries 869／images 111／maps 45）。
- 前端：瀏覽器目檢首頁/卷頁/實體頁；鏈接完整性腳本（所有 data/maps/images 引用存在）。
- 離線驗收：斷網打開 index.html 全功能可用。
