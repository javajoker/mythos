---
name: witness-collation
description: Collate multiple witnesses (editions/manuscripts/transcriptions) of an ancient text, attribute every difference to a citable entry, and classify variants as orthographic, scribal error, substantive, or displacement — including detecting modern editorial relocations hidden in "standard" digital texts. Use when ingesting a new corpus, before citing any passage as evidence, when two editions disagree, or when asked to "校勘", "compare editions", or "establish the working text".
---

# 見證本對勘 / Witness collation

## 原則 / Principles
- 現代數字本可能已經含有編者的結論，例如移段、補字、改字。**最早的見證本決定順序**，現代改動只登記為錯簡假說。/ Modern digital texts may already embed editorial conclusions (relocations, insertions, emendations). **The earliest witness sets the order**; modern changes are registered only as displacement hypotheses.
- 異文在分類之前不得作為證據。/ An unclassified variant is not evidence.

## 步驟 / Steps
1. **取得見證本**：至少兩個，最好三個，來源互相獨立；記錄版本、年代、轉錄者和授權。/ **Acquire witnesses**: at least two, ideally three independent ones; record edition, date, transcriber, licence.
2. **正規化**：去掉標點和注文；只摺疊純字形的異體，絕不摺疊可能改變意義的字，例如山海經的「昆／崑」「虫／蟲」都不摺疊。/ **Normalise**: drop punctuation and commentary; fold only purely graphic variants, never anything that could change meaning.
3. **對齊**：以卷為單位做序列對齊（例如 difflib，`autojunk=False`），把每一處差異歸屬到底本條目。/ **Align** book by book and attribute each difference to a base entry.
4. **偵測移段**：一卷之中如果出現長段（≥ 12 字）的對稱刪除和插入，就是段落換位的訊號；比對兩處的內容，確認是否為同一段文字。/ **Detect displacement**: long symmetric delete/insert pairs (≥ 12 characters) within a book signal moved paragraphs; check whether both sides carry the same text.
5. **分類**：每一處差異標為 `orthographic` / `scribal-error`（附錯誤類型，例如形近或數字）/ `substantive` / `displacement` / `transcription-gap`，並寫明分類者和理由。/ **Classify** each difference with classifier and reason.
6. **工作文本**：依最早見證本的順序，逐條選定讀法，並保留校勘記。/ **Working text**: follow the earliest witness's order, choose readings entry by entry, keep the apparatus.

## 山海經實作 / Shanhaijing implementation
`tools/shj/collate.py`（產出 `projects/shanhaijing/data/derived/collation.jsonl`）；發現見 `projects/shanhaijing/findings/F-0001-*`。/ findings in `F-0001-*`.
