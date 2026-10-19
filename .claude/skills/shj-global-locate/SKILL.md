---
name: shj-global-locate
description: Locate a Shanhaijing place (崑崙, 赤水, 流沙, any 山 or 國) or identify a Shanhaijing creature under Method G — global premise, descriptions only, real animals and geography first, ranked against all candidate loci worldwide. Use when the user asks "where is X really?", "could X be in Egypt / America / …?", wants an animal map of the book, or wants proof from the book for a geographic assumption.
---

# 山海經全球定位（方法 G）/ Shanhaijing global locate (Method G)

山海經對公共 skill `description-first-matching` 的包裝。/ Shanhaijing wrapper around `description-first-matching`.

## 1. 準備 / Prepare
```bash
python3 -I tools/shj/creatures.py && python3 -I tools/shj/animal_map.py
```
讀 `projects/shanhaijing/data/derived/animal-map.md`，了解相關篇段的動物投票。/ Read the animal map for the relevant sections.

## 2. 確定主語段落 / Fix the subject passages
- 用名稱的所有寫法搜尋（例如 崑崙|昆侖|崐崘），**逐段判斷**該地是不是主語。/ Search all spellings and decide passage by passage whether the place is the subject.
- 同一描述塊中不再重複地名的相鄰段落，要明確列入（例如海內西經的四隅出水、開明諸段）。/ Add adjacent paragraphs of the same description block explicitly.
- 別處山的「望見」句只取該分句：`--clause "SHJ-02-3-007:南望昆侖，其光熊熊，其氣魂魂"`。/ From other mountains' sight-lines take only the clause.

## 3. 跑分 / Score
```bash
python3 -I tools/shj/geo_match.py --target "<名稱正則>" --entries <主語段落> [--clause "ID:原文"] --pairs --md <卷宗目錄>/geo-match.md
python3 -I tools/shj/geo_match.py ... --group natural --md <卷宗目錄>/geo-match-natural.md
python3 -I tools/shj/geo_match.py ... --group built   --md <卷宗目錄>/geo-match-built.md
```
若候選庫缺少合理的地點，先在 `data/world/loci.jsonl` 補上並**單獨提交**，再跑分。/ If a plausible locus is missing, add it and commit it separately before scoring.

## 4. 寫卷宗 / Write the dossier
依 `hypotheses/TEMPLATE.md`，另加：/ Follow the template, plus:
- 前提聲明（方法 G）；全部候選排名；自然／人工分組；jackknife 領先頻率；同水系複合（標為事後）。/ Premise statement; full ranking; groups; jackknife; composites (post-hoc).
- 與方法 A 結論並列，說明差異來源。/ Method A's conclusion side by side, with the reason for any difference.
- 先登記下一步的新預測，再停止。/ Pre-register the next predictions before stopping.

## 5. 語氣 / Tone
直接回答「可能在 X 嗎？」：給出排名、分數、決定性的特徵與段落，以及結論有多脆弱。/ Answer "could it be in X?" directly: rank, score, decisive features and passages, and how fragile the result is.
