# 《山海經》參考語料 / Reference Corpus

## 來源與授權 / Provenance and licence

| 見證本 / Witness | 維基文庫頁面 / Wikisource page | 本地 / Local | 擷取日期 / Fetched |
|---|---|---|---|
| 通行本（含郭注、異文、現代編者註） | [山海經](https://zh.wikisource.org/wiki/山海經) 及子頁 | `sources/wikisource-base/*.wiki` | 2026-10-19 |
| 四部叢刊・明成化庚寅（1470）刊本 | [山海經（四部叢刊本）](https://zh.wikisource.org/wiki/山海經_(四部叢刊本)) | `sources/sbck-chenghua/*.txt` | 2026-10-19 |
| 四庫全書本（1781） | [山海經（四庫全書本）](https://zh.wikisource.org/wiki/山海經_(四庫全書本)) | `sources/skqs/*.wiki` | 2026-10-19 |

- 《山海經》原文及郭璞注屬公有領域。
- 維基文庫轉錄、標點和編排依 CC BY-SA 4.0；本目錄的衍生檔案沿用同一授權並註明出處。
- `editorial_refs[]` 中的現代校注只作為主張保存，不進入原文證據。
- `sources/manifest.json` 記錄目前 57 個快照檔案的路徑、位元組數與 SHA-256；分析只讀本地快照。

## 重新產生 / Regenerate

離線重建快照 manifest，不訪問網絡：

```bash
python3 -I tools/shj/fetch_sources.py --manifest-only
```

從現代 base 重建穩定條目與乾淨閱讀文本：

```bash
python3 -I tools/shj/ingest.py
```

只有明確需要更新上游見證本時才執行不帶 `--manifest-only` 的 `fetch_sources.py`。更新後必須重跑對勘並重新審查所有受影響產物。

## 內容 / Contents

| 路徑 / Path | 內容 / Content |
|---|---|
| `sources/manifest.json` | 原始快照的確定性雜湊清單 |
| `data/entries.jsonl` | 869 個 base 條目，含穩定 ID、主文、注疏、異文與編輯參照 |
| `text/NN-書名.md` | 18 卷乾淨閱讀文本，條目 ID 作為錨點 |

`entries.jsonl` 不是全部讀法已確認的定本；working text 的次序與讀法審核狀態見子項目的 `data/derived/working-text.jsonl`。

## 已知問題 / Known issues

1. 通行本含現代移段與補字，詳見 `projects/shanhaijing/docs/source-assessment.md` 和 F-0001。
2. 四部叢刊轉錄有缺頁：卷一洵山段、卷十五一頁，仍需掃描核實。
3. 通行本夾注以郭璞注為主，也混有後人的注；所有注疏只作轉錄。
