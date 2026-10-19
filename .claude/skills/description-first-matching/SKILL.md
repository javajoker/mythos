---
name: description-first-matching
description: Corpus-agnostic "Method G" for locating places and identifying creatures in ancient texts and myths under a global premise — build a real-world base (real animals with traits and ancient ranges, candidate loci with geographic properties) first, mask all names, match the text's descriptions to it, and rank every candidate by rarity-weighted matches minus contradictions, with a jackknife and same-river-system composites. Use when the user wants to start from real animals/geography and look for proof in the text, says the text "is about the whole Earth", says names differ from modern ones or distances are unreliable, or asks "could X be in <place>?".
---

# 描述優先的全球比對（方法 G）/ Description-first global matching (Method G)

規範 / Normative: `docs/research-framework.md` §10；山海經實作見 `projects/shanhaijing/docs/method-g-global.md`。

## 前提 / Premises (state them at the top of every result)
- 全球範圍；只看描述（名稱遮蔽）；距離與方位僅作小權重參考；允許個別錯誤，看累積。/ Global scope; descriptions only (names masked); distances and bearings a small-weight reference; single errors allowed, accumulation counts.

## 步驟 / Steps
1. **真實世界庫先行 / Real-world base first**
   - 動物：特徵標籤（體型參照、部件、顏色、聲音、習性、棲地）＋古代分佈區＋來源。/ Animals: trait tags + ancient ranges + sources.
   - 候選地點：全球、每個 river system 盡量多於一處；每個性質寫 T/F/null 並附來源。/ Candidate loci worldwide, ideally several per river system; every property T/F/null with sources.
   - **先提交庫，再寫跑分程式**，避免事後調整。/ **Commit the base before the scoring code** so values cannot be tuned afterwards.
2. **動物地圖 / Animal map**：把文本中每個生物描述轉成標籤（名稱遮蔽），按罕見度加權覆蓋率比對真實動物；覆蓋率 ≥ 0.5 且共享 ≥ 2 個標籤才採用；以其分佈區為各篇投票。/ Tag each creature description, match by rarity-weighted coverage, accept at ≥ 0.5 with ≥ 2 shared tags, vote regions per section.
3. **地理假設 / Geo assumption**：以動物投票與地點性質提出候選。/ Propose candidates from the votes and place properties.
4. **書內證據 / In-text proof**：只用「該地為主語」的段落（逐條列出）；只提到名字的段落列出但不計分。每個特徵：T +w、F −w、未知 0；生物：分佈覆蓋 +w·cov、不覆蓋 −0.5·w·cov；同一段落的兩種讀法只取較好者一次。/ Score only subject passages; mentions are listed, not scored; alternatives count once.
5. **穩健性 / Robustness**：(a) 自然／人工特徵分組；(b) 逐一移除特徵（jackknife），報告領先者出現頻率；(c) 同一水系的複合候選（標為事後分析）。/ Natural vs built groups; drop-one jackknife with leader frequency; same-river composites (post-hoc).
6. **結論 / Conclusion**：以排名與領先差距定級（G-強／中／弱），並寫出下一步要先登記的新預測。/ Grade by ranking and margin; pre-register the next predictions.

## 地區層級 / Region level
整部文本的對照用地區（覆蓋全部大陸）而不是單點；未知值以基準率期望計分（w·(2p − 1)），避免資料詳略造成的偏差；描述性族名只在作主語時計分。/ For whole-text mapping use regions covering every continent; score unknowns at base-rate expectation; count descriptive ethnonyms only as subjects.

## 必報的偏差 / Biases to report every time
- 庫的組成偏差：某水系的候選越多，複合候選的最高分越容易偏高。/ Knowledge-base composition: more loci on one river system inflate its best composite.
- 未知值在複合中會抵消矛盾。/ Unknowns cancel contradictions inside composites.
- 單一高權重特徵（例如只有一兩處為 T 的性質）可能左右排名，見 jackknife。/ A single rare, heavy feature can decide the ranking; see the jackknife.
- 資料詳略：較熟悉的地區有較少未知值。/ Documentation density: better-known regions have fewer unknowns.

## 山海經實作 / Shanhaijing implementation
`tools/shj/cues.py`、`creatures.py`、`animal_map.py`、`geo_match.py`；資料 `projects/shanhaijing/data/world/`；範例 `projects/shanhaijing/hypotheses/H-0006/`。
