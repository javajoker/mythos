# 山海經 Web App — TASKS CHECKLIST

> 版本 0.1（2026-10-26）。對齊 PRD/UIUX/TECH 0.1。每項完成打 ✅ 並註明 commit。

## 階段 0：文檔與評審

- [x] PRD / UIUX-SPEC / TECH-SPEC / TASKS 產出（2026-10-26）
- [ ] 發起人評審四份文檔（重點：P0 範圍、誠實性約束、靜態站選型）

## 階段 1：數據導出

- [ ] `tools/shj/webapp_export.py`：graph.json（KG 全量）
- [ ] entries.json（869 條目：原文＋白話＋未決＋配圖引用）
- [ ] map-chains.json（26 鏈，含 fit_coords 與色族）
- [ ] map-points.json（402 框架書點位）
- [ ] basemap.json（太平洋中心海岸線）
- [ ] adjudications.json（ADJ/F 系列）
- [ ] manifest.json 計數對賬（4,334/1,805/9,234/869/111/45）
- [ ] images/ 與 maps/ 複製引用到位

## 階段 2：前端核心

- [ ] index.html 世界地圖（SVG 渲染＋pan/zoom＋經度環繞投影）
- [ ] 圖層開關（鏈/點/現代點/底圖地名）
- [ ] 點選 → 詳情卡（條目級：原文/白話/候選/配圖/置信度/未決/標記）
- [ ] book.html 卷頁（導覽＋補丁圖＋條目列表）
- [ ] entities.html + entity.html（類型樹/搜索/類名聚合頁）
- [ ] adjudications.html、about.html

## 階段 3：完善與驗收

- [ ] 置信度過濾、關係視圖、鍵盤導航、移動端抽屜
- [ ] 離線驗收（file:// 全功能）
- [ ] 鏈接完整性腳本＋瀏覽器目檢（首頁/卷頁/實體頁）
- [ ] 性能：首屏 ≤3 MB
- [ ] 發起人驗收覆核工作流試用

## 階段 4：交付

- [ ] 掛載入口（項目 README 鏈接）
- [ ] 紅隊/覆核工作流（P2，可後置）
