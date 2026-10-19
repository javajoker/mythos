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

#### 3.1.1 錯簡假說登記 / Registered displacement hypotheses (X3, task T-104)

`tools/shj/align_witness.py` 以與順序無關的 n-gram 投票，在兩個見證本中定位每一條底本條目（[alignment-summary.md](../data/derived/alignment-summary.md)）。下列 8 個段落塊的位置，**明成化本和四庫本一致**，而與底本不同。工作文本（[working-text.jsonl](../data/derived/working-text.jsonl)）依兩個見證本排序；底本的排法只作為錯簡假說登記（[displacements.jsonl](../data/derived/displacements.jsonl)），要採用它，必須在卷宗中以 T3 成本論證。
`tools/shj/align_witness.py` locates every base entry in both witnesses by order-independent n-gram voting. For the 8 blocks below, **the 1470 Chenghua and the Siku editions agree with each other** and disagree with the base text. The working text follows the two witnesses; the base arrangement is registered only as a displacement hypothesis, which a dossier may adopt only by arguing it at T3 cost.

| X3 | 條目 / Entries | 底本所在 / In base | 兩見證本所在 / In both witnesses | 底本引現代編者 / Base cites modern editor | 首句 / Opening |
|---|---|---|---|---|---|
| X3-001 | `SHJ-11-1-009`–`011` | 海內西經 | 海內東經 | ✓ | 國在流沙中者埻端、璽蓉… |
| X3-002 | `SHJ-11-1-023`–`024` | 海內西經 | 海內北經 | ✓ | 蛇巫之山…西王母梯几而戴勝… |
| X3-003 | `SHJ-12-1-002` | 海內北經 | 海內西經 | | 匈奴、開題之國、列人之國… |
| X3-004 | `SHJ-12-1-020`–`021` | 海內北經 | 海內西經 | | 大澤方百里…鴈門山… |
| X3-005 | `SHJ-12-1-024`–`027` | 海內北經 | 海內西經 | ✓ | 東胡、夷人、貊國、孟鳥 |
| X3-006 | `SHJ-13-1-003`–`004` | 海內東經 | 海內北經 | ✓ | 蓋國…朝鮮…列姑射 |
| X3-007 | `SHJ-13-1-037`–`043` | 海內東經 | 海內北經 | ✓ | 姑射國…大蟹…陵魚…蓬萊山…大人之市 |
| X3-008 | `SHJ-14-1-002` | 大荒東經 | 大荒南經 | ✓ | 羲和之國…方浴日于甘淵 |

**影響 / Impact**：海內西、北、東三經之間的相對方位推理（規格 §7.6）必須用工作文本的次序。H-0001 引用的 `SHJ-11-1-017`（開明獸「東嚮立」）不在任何移段塊中，且兩個見證本都有此段，只有「昆侖／崑崙」等字形差異。/ Relative-position reasoning across these three books must use working-text order. `SHJ-11-1-017`, cited by H-0001, is in no relocated block and is present in both witnesses, with only glyph differences such as 昆侖/崑崙.

#### 3.1.2 底本補入的文字 / Text the base inserted

| 編號 / ID | 條目 / Entry | 內容 / Content | 證據 / Evidence |
|---|---|---|---|
| I-001 | `SHJ-18-1-008` | 「其城方三百里，蓋天地之中，素女所出也」 | 兩個見證本都沒有（底本以 `{{另2}}` 標「或無此句」）/ absent from both witnesses (the base itself marks it 「或無此句」) |
| I-002 | `SHJ-12-1-022` | 「高柳在代北」 | 與 `SHJ-11-1-005` 重複；兩個見證本都只在海內西經出現一次 / duplicates `SHJ-11-1-005`; both witnesses have it once, in 海內西經 |

### 3.2 四部叢刊轉錄缺頁 / Sibu Congkan transcription gaps
- 卷 1 南次二經：`sbck` 在「咸陰之山」與「鹿吳之山」之間缺**三座山**：洵山、虖勺之山、區吳之山（`SHJ-01-2-013`–`015`），四庫本則三者俱全。由於 `sbck` 本篇的篇末仍作「凡十七山，七千二百里」，而實存只有 14 山，這是轉錄缺頁或刻本漏刻，不是版本異文。須對照掃描頁核實（T-005）。/ Book 1: `sbck` lacks **three mountains** between 咸陰之山 and 鹿吳之山 (洵山, 虖勺之山, 區吳之山); the Siku has all three. Since `sbck`'s own total still reads 「凡十七山」 with only 14 present, this is a transcription or carving gap, not an edition variant. Verify against the scan (T-005).
- 卷 15：維基文庫頁面標示「缺一頁」（`SHJ-15-1-033` 附近）。/ Book 15: the Wikisource page is marked "one page missing".
- 卷 9 末的劉秀校上題記（「建平元年四月丙戌…」，`SHJ-09-1-017`）：四庫本缺。/ The Liu Xiu colophon at the end of book 9 is absent from the Siku.

### 3.3 重大實質異文（T-102 優先處理）/ Heavy substantive variants (T-102 priority)

對齊時相似度低於 0.8 的條目。下列是去除純字形差異（如昆侖／崑崙）後，**可能影響詮釋**的例子。/ Entries aligning below 0.8 similarity; those below **may affect interpretation** once pure glyph differences (e.g. 昆侖/崑崙) are set aside.

| 條目 / Entry | 底本 / Base | 明成化本 / Chenghua |
|---|---|---|
| `SHJ-06-1-016` | 反舌國……其為人反舌。一日支舌國 | 岐舌國（無「其為人反舌」/ lacks 其為人反舌） |
| `SHJ-07-1-021` | 有樹名曰雒棠，聖人代立，于此取衣 | 有樹名曰雄常，先入代帝，於此取 |
| `SHJ-08-1-015` | 跂踵國在拘癭**南**，其為人兩足皆支。一曰反踵 | 跂踵國在拘纓**東**，其為人大，兩足亦大。一曰大踵 |
| `SHJ-14-1-007` | 有神，人面獸身 | 靖人神，人面獸身（句讀不同 / different division） |
| `SHJ-18-1-017` | 贑巨人，人面長**脣** | 贑巨人，人靣長**臂** |

### 3.4 文本內部的數字問題（S3 候選）/ Internal numeric problems (S3 candidates)
- `SHJ-05-1-016` 中山經首篇：分段里程合計 937 里，篇末記為 6,670 里；同段「白甘棗之山」的「白」疑為「自」（X2）。/ legs sum to 937 里 against a stated 6,670; 白 in 白甘棗之山 is probably 自 (X2).
- `SHJ-05-12-016` 中次十二經：「凡十萬山」，實際抽出 15 站，疑為「十五山」（X1）。/ 「凡十萬山」 with 15 stations extracted; probably 十五山 (X1).
- 完整列表見 [routes-summary.md](../data/derived/routes-summary.md)。/ Full list in [routes-summary.md](../data/derived/routes-summary.md).

## 4. 使用規則 / Usage rules

1. 引用時預設用 `base` 的條目編號（穩定），但凡涉及 §3.1 的條目，要同時附上 `sbck` 的位置。/ Cite by `base` entry ID (stable), but for §3.1 entries also give the `sbck` position.
2. 異文在分類完成之前不得作為證據（`status = unclassified`）。/ Variants cannot serve as evidence until classified.
3. 郭注只作為「四世紀讀者的理解」。/ Guo Pu's notes are only "a 4th-century reader's understanding".
