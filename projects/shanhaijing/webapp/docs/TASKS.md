# 山海經 Web App — TASKS CHECKLIST

> 版本 0.1（2026-10-26）。對齊 PRD/UIUX/TECH 0.1。每項完成打 ✅ 並註明 commit。

## 階段 0：文檔與評審

- [x] PRD / UIUX-SPEC / TECH-SPEC / TASKS 產出（2026-10-26）
- [ ] 發起人評審四份文檔（重點：P0 範圍、誠實性約束、靜態站選型）

## 階段 1：數據導出

- [x] `tools/shj/webapp_export.py`：graph.json（KG 全量）（7a9c3ff）
- [x] entries.json（869 條目全匹配：原文＋白話＋未決＋配圖引用）（7a9c3ff）
- [x] map-chains.json（26 鏈，含 fit_coords 與色族）（7a9c3ff）
- [x] map-points.json（402 框架書點位）（7a9c3ff）
- [x] basemap.json（太平洋中心海岸線）（7a9c3ff）
- [x] adjudications.json（ADJ/F 系列）（7a9c3ff）
- [x] manifest.json 計數對賬（7a9c3ff；實際計數以 manifest 為準）
- [x] images/ 與 maps/ 複製引用到位（7a9c3ff）

## 階段 2：前端核心

- [x] index.html 世界地圖（SVG＋pan/zoom＋環繞投影）（cde02a4）
- [x] 圖層開關（cde02a4）
- [x] 點選 → 詳情卡（cde02a4）
- [x] book.html 卷頁＋hash 深鏈（cde02a4）
- [x] entities/entity（含赤水 5 實例聚合）（cde02a4）
- [x] adjudications.html、about.html（cde02a4）

## 階段 3：完善與驗收

- [x] 關係視圖、鍵盤導航、移動端抽屜（cde02a4）；置信度過濾待條目級結構化字段（後置）
- [ ] 離線驗收（file://）——回退機制已實現（data/*.js 包裝），待真實瀏覽器雙擊複核
- [x] check_refs.py 通過＋逐頁目檢（cde02a4）
- [x] 首屏約 1.3 MB（cde02a4）
- [ ] 發起人驗收覆核工作流試用

## 階段 4：交付

- [ ] 掛載入口（項目 README 鏈接）
- [ ] 紅隊/覆核工作流（P2，可後置）

## 階段 5：交互深化（2026-10-29）

- [x] timelapse.html「時光地圖」頁：三段時間軸（濕潤期／成書時代／今天）
- [x] data/timelapse.json：14 個古水體（撒哈拉濕潤期水系群、古濟水、雷澤、羅布泊等）按期變化（水體→沼澤化→消失虛線框）；6 個物種分布變遷（大象、犀牛、雙峰駝、儒艮、亞洲獅、鱷魚），當時分布 vs 現今殘存對照＋遷徙連線，區域滅絕標紅叉
- [x] js/timelapse.js：獨立 SVG 世界視圖（投影與 map.js 同源），圖層開關、pan/zoom、點選詳情卡（含時期狀態表與書中出處鏈接）、懸停提示
- [x] app.js 導航與 boot 接入；store.js 新增 timelapse 加載；check_refs.py 納入 timelapse 數據檢查
