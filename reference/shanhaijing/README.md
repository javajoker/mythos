# 《山海經》參考語料 / Shanhaijing Reference Corpus

## 來源與授權 / Provenance & licence

| 見證本 / Witness | 維基文庫頁面 / Wikisource page | 本地 / Local | 擷取日期 / Fetched |
|---|---|---|---|
| 通行本（含郭注、異文、現代編者註）/ common text | [山海經](https://zh.wikisource.org/wiki/山海經) 及子頁 / and subpages | `sources/wikisource-base/*.wiki` | 2026-10-19 |
| 四部叢刊・明成化庚寅（1470）刊本 / Sibu Congkan, 1470 Chenghua | [山海經 (四部叢刊本)](https://zh.wikisource.org/wiki/山海經_(四部叢刊本)) | `sources/sbck-chenghua/*.txt`（由渲染頁轉成的純文字 / plain text from the rendered page） | 2026-10-19 |
| 四庫全書本（1781）/ Siku Quanshu | [山海經 (四庫全書本)](https://zh.wikisource.org/wiki/山海經_(四庫全書本)) | `sources/skqs/*.wiki` | 2026-10-19 |

- 《山海經》原文及郭璞注屬公有領域（PD-old）。/ The text and Guo Pu's commentary are public domain.
- 維基文庫的轉錄、標點和編排依 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 授權；本目錄的衍生檔案（`data/`、`text/`）沿用同一授權並註明出處。/ Wikisource transcription, punctuation and layout are CC BY-SA 4.0; the derived files here (`data/`, `text/`) carry the same licence with attribution.
- `editorial_refs[]` 中引用的現代校注（如袁珂）屬短篇引用，僅作為「主張」保存。/ Modern editorial notes quoted in `editorial_refs[]` (e.g. Yuan Ke) are short quotations, kept only as claims.

## 重新產生 / Regenerate

```bash
python3 -I tools/shj/fetch_sources.py
```

```bash
python3 -I tools/shj/ingest.py
```

## 內容 / Contents

| 路徑 / Path | 說明 / Description |
|---|---|
| `data/entries.jsonl` | 869 段，每段一筆，編號 `SHJ-BB-S-EEE`；結構見 [data-model](../../projects/shanhaijing/docs/data-model.md) / 869 paragraphs |
| `text/NN-書名.md` | 18 卷乾淨的閱讀文本，條目編號作為錨點 / clean reading text for all 18 books |

## 已知問題 / Known issues

1. **通行本含現代移段**：海內西、北、東經，大荒東經和海內經有段落被移位或補字。詳見 [source-assessment](../../projects/shanhaijing/docs/source-assessment.md) 和 [F-0001](../../projects/shanhaijing/findings/F-0001-base-text-modern-relocations.md)。/ **The base text contains modern relocations.**
2. 四部叢刊本轉錄有缺頁：卷 1 洵山段、卷 15 一頁。/ Sibu Congkan transcription gaps (book 1 洵山 passage; one page of book 15).
3. 通行本的夾注以郭璞注為主，也混有後人的注（例如「璨曰」）。/ The base text's notes are mostly Guo Pu's but include later ones (e.g. 「璨曰」).
