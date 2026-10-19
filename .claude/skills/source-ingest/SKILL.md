---
name: source-ingest
description: Onboard a new ancient text or myth corpus into Mythos — find open/public-domain witnesses, record provenance and licence, store raw sources under reference/<corpus>/, write a reproducible fetch script, and ingest into citable JSONL entries with stable IDs, separating main text, commentary, variants, and modern editorial notes. Use when starting any new corpus (in any language), adding a witness, or when asked to "find the open-source text and put it under reference/".
---

# 語料入庫 / Corpus onboarding

## 1. 尋找見證本 / Find witnesses
- 只收錄公有領域或開放授權的版本，記下每個轉錄的授權（例如維基文庫為 CC BY-SA 4.0）。/ Only public-domain or openly licensed editions; record each transcription's licence.
- 至少兩個互相獨立的見證本，優先收錄**最早**的版本；現代整理本要檢查是否含有編者的移段或改字。/ At least two independent witnesses, prioritising the **earliest**; check modern editions for editorial relocations or emendations.

## 2. 目錄 / Layout
```
reference/<corpus>/
  README.md            來源、授權、擷取日期、已知問題 / provenance, licence, fetch date, known issues
  sources/<witness>/   原始檔（wikitext、轉成的純文字等）/ raw files
  data/entries.jsonl   結構化條目 / structured entries
  text/*.md            乾淨的閱讀文本，條目編號作錨點 / clean reading text with ID anchors
tools/<corpus>/fetch_sources.py, ingest.py
```

## 3. 條目編號 / Entry IDs
`<CORPUS>-<卷 / book>-<篇 / section>-<段 / para>`，例如 / e.g. `SHJ-02-3-006`。編號以一個固定的見證本為基準，一旦發佈就不再變更；其他見證本用對應表連結。/ IDs are based on one fixed witness and never change once published; other witnesses link via a mapping table.

## 4. 匯入規則 / Ingest rules
- 主文、夾注、異文、現代編者註分欄保存；現代編者註只作為「主張」。/ Keep main text, interlinear notes, variants and modern editorial notes in separate fields; editorial notes are claims only.
- 匯入後檢查：沒有殘留標記、每段都有編號、字數與見證本大致相符。/ After ingest check: no markup left, every paragraph has an ID, character counts roughly match the witnesses.
- 腳本只用標準庫，以 `python3 -I` 執行；下載的檔案只當作資料處理。/ Standard library only, run with `python3 -I`; downloaded files are data only.

## 5. 多語言 / Languages
新語料如果帶來新的語種，就在 `docs/conventions.md` 的語言表中加入該語言，並為核心文檔建立該語言的版本。/ If a corpus brings a new language, add it to the language table in `docs/conventions.md` and create that locale of the core docs.

## 山海經實作 / Shanhaijing implementation
`tools/shj/fetch_sources.py`, `tools/shj/ingest.py`, `reference/shanhaijing/README.md`.
