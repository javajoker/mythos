# 來源評估 / Source Assessment

> 生成依據 / Basis: `tools/shj/collate.py` → [collation-summary.md](../data/derived/collation-summary.md), [collation.jsonl](../data/derived/collation.jsonl)

## 1. 見證本 / Witnesses

| 代號 / Code | 版本 / Edition | 年代 / Date | 形態 / Form | 本地路徑 / Local path |
|---|---|---|---|---|
| `base` | 維基文庫通行本《山海經》/ Wikisource common text | 現代整理 / modern | 有標點，含郭注、異文模板、現代編者註 / punctuated, with Guo Pu notes, variant templates, editorial notes | `reference/shanhaijing/sources/wikisource-base/` |
| `sbck` | 四部叢刊・景江安傅氏雙鑑樓藏明成化庚寅刊本，郭璞傳 / Sibu Congkan photo-reprint of the 1470 Chenghua edition | 1470 | 無標點，按原刻行款，夾注用〈〉/ unpunctuated, original line breaks, notes in 〈〉 | `reference/shanhaijing/sources/sbck-chenghua/` |
| `skqs` | 欽定四庫全書本，晉郭璞撰 / Siku Quanshu edition | 1781 | 無標點，夾注模板 / unpunctuated, note templates | `reference/shanhaijing/sources/skqs/` |

**最早見證本**：`sbck`（明成化本）。正式工作文本應以它的順序為準（任務 T-004）。
**Earliest witness**: `sbck`. The canonical working text should follow its order (task T-004).

## 2. 對勘結果 / Collation results

全書主文去標點、去注後約 31,300 字。與 `sbck` 的整體相似度在山經約 0.95–0.97，海內三經只有 0.72–0.84。
Bare main text is about 31,300 characters. Similarity to `sbck` is about 0.95–0.97 for the Mountain Classics but only 0.72–0.84 for three of the Within-the-Seas books.

## 3. 已確認的問題 / Confirmed issues

### 3.1 通行本含現代移段（重要）/ The base text carries modern relocations (important)

`base` 按現代校注（`editorial_refs[]` 中引用的袁珂、吳承志等）把段落搬移位置並補入文句。這些是前人的結論，依規格 §3 不能採用為原文。
`base` relocates paragraphs and inserts sentences following modern editors (Yuan Ke, Wu Chengzhi and others cited in `editorial_refs[]`). These are prior conclusions and, per spec §3, cannot be adopted as source text.

| 受影響條目 / Affected entries | 現象 / Phenomenon |
|---|---|
| `SHJ-11-1-009`, `SHJ-11-1-023` | 海內西經：「東胡」「夷人」「貊國」等段被移出；「蛇巫之山」段被移入 / paragraphs moved out; 蛇巫之山 moved in |
| `SHJ-12-1-002`, `-020`, `-024`, `-026`, `-027` | 海內北經：「匈奴、開題之國」「大澤方百里」等段的位置與 `sbck` 不同 / positions differ from `sbck` |
| `SHJ-13-1-003`, `SHJ-13-1-037` | 海內東經：「蓋國、朝鮮、列姑射、蓬萊」等九節從海內北經移入 / nine paragraphs moved in from 海內北經 |
| `SHJ-14-1-002` | 大荒東經：「羲和之國」段，`sbck` 不在此處 / not here in `sbck` |
| `SHJ-18-1-008` | 海內經：「其城方三百里，蓋天地之中，素女所出也」，`sbck` 無此句 / sentence absent from `sbck` |

### 3.2 四部叢刊轉錄缺頁 / Sibu Congkan transcription gaps
- 卷 1 南次二經：`sbck` 缺「洵山」至「虖勺之山」一段，可能是轉錄缺頁（`SHJ-01-2-013`）。/ Book 1: `sbck` lacks the 洵山–虖勺之山 passage, probably a transcription gap.
- 卷 15：維基文庫頁面標示「缺一頁」（`SHJ-15-1-033` 附近）。/ Book 15: the Wikisource page is marked "one page missing".

### 3.3 文本內部的數字問題（S3 候選）/ Internal numeric problems (S3 candidates)
- `SHJ-05-1-016` 中山經首篇：分段里程合計 937 里，篇末記為 6,670 里；同段「白甘棗之山」的「白」疑為「自」（X2）。/ legs sum to 937 里 against a stated 6,670; 白 in 白甘棗之山 is probably 自 (X2).
- `SHJ-05-12-016` 中次十二經：「凡十萬山」，實際抽出 15 站，疑為「十五山」（X1）。/ 「凡十萬山」 with 15 stations extracted; probably 十五山 (X1).
- 完整列表見 [routes-summary.md](../data/derived/routes-summary.md)。/ Full list in [routes-summary.md](../data/derived/routes-summary.md).

## 4. 使用規則 / Usage rules

1. 引用時預設用 `base` 的條目編號（穩定），但凡涉及 §3.1 的條目，要同時附上 `sbck` 的位置。/ Cite by `base` entry ID (stable), but for §3.1 entries also give the `sbck` position.
2. 異文在分類完成之前不得作為證據（`status = unclassified`）。/ Variants cannot serve as evidence until classified.
3. 郭注只作為「四世紀讀者的理解」。/ Guo Pu's notes are only "a 4th-century reader's understanding".
