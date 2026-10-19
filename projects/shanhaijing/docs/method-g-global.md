# 方法 G：描述優先的全球比對 / Method G: Description-First Global Matching

> v0.1 ・ 2026-10-19 ・ 由項目發起人提出。與原方法（以下稱「方法 A」，[methodology-spec.md](methodology-spec.md)）並行；兩種方法的結論都保留、並列呈現。
> Proposed by the project initiator. Runs alongside the original method ("Method A", [methodology-spec.md](methodology-spec.md)); both methods' conclusions are kept and shown side by side.

---

## 1. 前提 / Premises

| # | 前提 / Premise | 說明 / Note |
|---|---|---|
| G-P1 | **全書以整個地球為範圍** / the book covers the whole Earth | 工作前提：候選地點遍及全球，不預設中國 / a working premise: candidates are global, China is not assumed |
| G-P2 | **只看描述，不看名稱** / descriptions only, never names | 古今地名、物名可能完全不同；比對時名稱一律遮蔽 / ancient and modern names may differ entirely; names are masked during matching |
| G-P3 | **距離只是參考** / distances are only a reference | 里數與方位可能不準；在方法 G 中最多只給很小的權重，不能單獨否定一個候選 / 里 and bearings may be wrong; in Method G they carry at most a small weight and cannot by themselves rule out a candidate |
| G-P4 | **允許錯誤，看累積** / errors allowed, accumulation counts | 個別條目可能錯，但吻合的描述越多、越罕見，假設越可能成立 / single entries may be wrong; the more and the rarer the matching descriptions, the stronger the assumption |

## 2. 流程 / Pipeline

```
G1 動物地圖  真實動物特徵庫 ──比對──▶ 書中每個生物描述 ──▶ 最可能的真實動物 ──▶ 其分佈區
                                                                 └─▶ 每篇的「動物分佈投票」
G2 地理假設  每篇／每個地點的動物投票 ＋ 地理性質（火山、沙漠、湖、雪山、多河之源……）
                                                                 └─▶ 候選地點清單（全球）
G3 書內證據  對每個候選地點，在書中尋找吻合與矛盾的描述，逐項加權計分
                                                                 └─▶ 候選排名；吻合越多越罕見，分數越高
```

| 階段 / Stage | 工具 / Tool | 輸入 / Input | 輸出 / Output |
|---|---|---|---|
| G1 | `tools/shj/creatures.py`, `tools/shj/animal_map.py` | `entries.jsonl`；`data/world/animals.jsonl` | `creatures.jsonl`、`animal-map.md` |
| G2 | `tools/shj/animal_map.py`（篇段投票）| 同上 | 每篇的地區分佈 / regional distribution per section |
| G3 | `tools/shj/geo_match.py` | 目標地點的條目、`data/world/loci.jsonl`、`animals.jsonl` | 候選排名與逐項證據 / candidate ranking with itemised evidence |

## 3. 特徵與計分 / Features and scoring

### 3.1 從書中抽取特徵（名稱遮蔽）/ Extracting features from the text (names masked)
- 生物：「狀如X」的體型參照、部件（翼、四角、人面、四足……）、顏色、聲音（其音如嬰兒……）、習性（夜飛、陵居、冬死夏生……）。詞彙表在 `tools/shj/cues.py`。/ Creatures: body analogy, parts, colours, sounds, behaviour; lexicon in `tools/shj/cues.py`.
- 地點：高山、多河之源與其方向、沙地、某方有海、火（投物輒然）、環繞之水、人面獸身的巨像、面向、門與井等建築、穴居、神之所居、玉石。/ Places: high peak, multi-river source and directions, sand, a sea on one side, fire, encircling water, a human-faced beast colossus and its facing, gates and wells, cave dwelling, a gods' abode, jade.

### 3.2 罕見度權重 / Rarity weight
對每個特徵 t：/ For each feature t:

  w(t) = log₁₀( N_known / N_true ) ＋ 0.05

N_known 是資料庫中對 t 有明確 T/F 值的候選數，N_true 是其中為 T 的數目。罕見的特徵權重大；幾乎處處都有的特徵接近 0。
N_known counts candidates with a definite T/F value for t, N_true those with T. Rare features weigh more; near-universal ones weigh almost nothing.

### 3.3 計分 / Score
- 候選地點具有該特徵（T）：**＋w**；明確沒有（F）：**−w**；未知（?）：0。/ T: **+w**; F: **−w**; unknown: 0.
- 生物特徵：書中生物的最佳真實動物（覆蓋率 ≥ 0.5）在該地有分佈：**＋w × 覆蓋率**；沒有分佈：**−0.5 × w × 覆蓋率**（描述可能不準，所以扣分減半）。/ Fauna: if the creature's best real match (coverage ≥ 0.5) lives there, **+w × coverage**; if not, **−0.5 × w × coverage** (halved, since descriptions may be loose).
- 距離（參考）：若有，權重固定為 0.1。/ Distance (reference only): fixed weight 0.1 when used.
- 總分 = 各項加總。總分以**排名**解讀：比較同一套規則下的所有候選。/ Total = sum; read as a **ranking** across all candidates under the same rules.

### 3.4 由排名到結論 / From ranking to conclusion
| 情況 / Situation | 結論 / Conclusion |
|---|---|
| 第一名領先第二名 ≥ 1.0，且吻合項 ≥ 5 / leader ahead by ≥ 1.0 with ≥ 5 matches | **G-強** 假設成立 / strong |
| 領先 0.3–1.0 / lead 0.3–1.0 | **G-中** 傾向成立 / moderate |
| 領先 < 0.3 / lead < 0.3 | **G-弱** 前幾名並列，需要更多描述 / weak; top candidates tied |
| 某候選總分 < 0 / a candidate scores < 0 | 該候選的矛盾多於吻合 / more contradictions than matches |

## 4. 防止「處處皆合」的規則 / Guards against "everything fits"

1. **同一規則比所有候選**：任何候選的分數都必須和其他候選一起列出，不能只報告一個地點的吻合數。/ Every candidate is scored by the same rules and reported together; never one place's match count alone.
2. **矛盾要扣分**：只數吻合、不數矛盾，任何地點都能湊出很多吻合。/ Contradictions subtract; counting matches alone lets any place collect many.
3. **罕見度加權**：「有沙漠」「有獅子」這類常見特徵，權重自動接近 0。/ Rarity weighting automatically shrinks common features toward 0.
4. **資料庫先寫、結果後看**：候選地點的特徵值（T/F/?）必須在跑分之前寫入，並附來源；跑分後若修改，要在提交訊息中說明。/ Locus values are written, with sources, before scoring; any later change is explained in the commit.
5. **名稱遮蔽**：「崑崙」「赤水」這類名字不參與計分。/ Names never score.

## 5. 資料庫 / Knowledge base

| 檔案 / File | 內容 / Content |
|---|---|
| `projects/shanhaijing/data/world/animals.jsonl` | 真實動物：特徵標籤、古代分佈區（地區代碼）、來源 / real animals: feature tags, ancient ranges (region codes), sources |
| `projects/shanhaijing/data/world/loci.jsonl` | 全球候選地點：座標、地區代碼、地理性質 T/F/?、來源 / global candidate loci: coordinates, region codes, properties T/F/?, sources |
| `projects/shanhaijing/data/world/README.md` | 標籤定義、地區代碼、距離門檻 / tag definitions, region codes, distance thresholds |

## 6. G4：全書全球對照 / G4: whole-book global mapping

| 項目 / Item | 內容 / Content |
|---|---|
| 單位 / Units | 18 卷的每一篇（山經 26 篇＋海經、大荒經、海內經 13 卷）＋具名地點（崑崙、流沙、赤水、黑水、弱水、西王母、湯谷扶桑、蓬萊、不周）/ every section plus key named places |
| 候選 / Candidates | 31 個地區，覆蓋全部有人居住的大陸（`data/world/regions.jsonl`）/ 31 regions covering every inhabited continent |
| 特徵 / Features | 礦產、植物、地形、習俗（`region-properties.jsonl`，共 36 項）＋動物地圖中被接受的比對 / minerals, plants, terrain, customs (36) plus accepted animal matches |
| 未知值 / Unknowns | 以基準率期望計分：w·(2p − 1)，p = 該性質為 T 的已知地區比例。這樣資料較詳的地區不會因此得利 / scored at base-rate expectation so better-documented regions gain nothing |
| 習俗線索 / Custom cues | 描述性族名（羽民、黑齒、毛民……）只在該族為主語時計分，作為方位參照時不計 / descriptive ethnonyms count only when that people is the subject |
| 只計出現 / Presence only | 文本沒提到不算證據 / silence is never evidence |
| 輸出 / Outputs | `global-map.md`（全部排名、每單位的假設候選與證據、jackknife、方位參考）、`global-map.svg`、`peoples-map.md` |
| 工具 / Tool | `python3 -I tools/shj/region_match.py` |

曾試過「均勻隨機特徵的虛無基準」並放棄：它會讓許多性質被標為 F 的地區（如西伯利亞），在特徵對其只是未知時反而得分。/ A uniform random-feature null baseline was tried and rejected: it rewarded regions marked absent for many properties when a section's features were merely unknown for them.

## 7. 與方法 A 的關係 / Relation to Method A

方法 A 先在書內建立結構（水系、里程），再找真實世界；方法 G 先從真實世界的動物與地理出發，再到書中找證據。兩者的結論若一致，可信度提高；若不一致，兩個結論都保留，並在報告中說明差異的原因。
Method A builds structure inside the book first (rivers, distances) and then looks to the world; Method G starts from real animals and geography and then searches the book. Agreement raises confidence; disagreement is kept and explained in the report.
