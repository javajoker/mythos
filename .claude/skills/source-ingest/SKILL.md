---
name: source-ingest
description: Onboard an ancient-text corpus with open witnesses, provenance, deterministic source manifests, stable entry IDs and separated main text, commentary, variants and editorial claims.
---

# 語料入庫 / Corpus onboarding

1. **取得見證本**：使用公有領域或開放授權版本，至少兩個獨立見證本，優先最早版本；記錄版本、年代、轉錄者、來源與授權。
2. **保存快照**：原始檔放 `reference/<corpus>/sources/<witness>/`，生成 `manifest.json`，記錄每個檔案的路徑、位元組數與 SHA-256。
3. **下載與分析分離**：分析只讀本地快照。更新上游後，必須產生新 manifest 並重審所有受影響產物。
4. **建立穩定 ID**：`<CORPUS>-BB-S-EEE` 以固定 base 為基準，一經發布不改變；其他見證本用定位表連接。
5. **分離內容**：主文、夾注、異文與現代編者註分欄保存。注疏只作轉錄，現代編者內容只作主張。
6. **區別 base 與 working text**：base ingest 只建立穩定條目，不代表最早見證本的次序和讀法已確認。
7. **檢查**：沒有殘留標記，每段有 ID，字數與見證本大致相符，輸出可重跑且排序穩定。
8. **保留時間因果**：後世名稱、注釋與地理歸類只作後來資料，不得反向解釋早期文本的形成原因。

目錄：

```text
reference/<corpus>/
  README.md
  sources/<witness>/
  sources/manifest.json
  data/entries.jsonl
  text/*.md
tools/<corpus>/fetch_sources.py, ingest.py
```

山海經實作：`tools/shj/fetch_sources.py`、`tools/shj/ingest.py`、`reference/shanhaijing/README.md`。
