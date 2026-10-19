# H-0001 卷宗：崑崙在埃及（赤水＝紅海、黑水＝尼羅河、流沙＝撒哈拉、西海＝地中海）
# Dossier H-0001: Kunlun in Egypt (Red Water = Red Sea, Black Water = Nile, Flowing Sands = Sahara, West Sea = Mediterranean)

| 欄位 / Field | 值 / Value |
|---|---|
| 狀態 / Status | **adjudicated — R（否定，就目前的表述而言）/ Refuted as formulated** |
| 提出者 / Proposed by | 項目發起人（使用者範例）/ project initiator (user example), 2026-10-19 |
| 登記日期 / Registered | 2026-10-19 |
| 方法版本 / Method | [methodology-spec v0.1](../../docs/methodology-spec.md), [framework v0.1](../../../../docs/research-framework.md) |
| 校改預算 / Correction budget | log₁₀ −1.5（預設 / default）；實際使用 0 / used 0 |
| 重現 / Reproduce | `python3 -I tools/shj/chain_fit.py --section 西次三經 --anchor 昆侖之丘 --lat 29.975 --lon 31.138` |

---

## 1. 假說原文 / Hypothesis as proposed

> 西海之南，流沙之濱，赤水之後，黑水之前，有大山，名曰崑崙之丘。
> 赤水為紅海（紅藻赤潮），黑水為尼羅河，流沙為撒哈拉，西海為地中海。
> 佐證：「有神，人面虎身，有文有尾，皆白，處之」——獅身人面像。
> 佐證：泰器之山「文鰩魚……常行西海，游於東海，以夜飛」——飛魚，大西洋洄游太平洋。

**原文核對 / Text check (S0–S1)**：
- `SHJ-16-1-037`（大荒西經）與引文相符；底本作「黒水」（黑的異體）。/ matches the quotation; the base text writes 黒 (variant of 黑).
- `SHJ-02-3-006`（西次三經・泰器之山）原文是「常**從**西海**遊于**東海」，不是「常行西海，游於東海」。兩者意義相近，但引用時必須用原文。/ The source reads 「常從西海遊于東海」, not 「常行西海，游於東海」. The meaning is close, but citations must use the source wording.
- 兩條在三個見證本中都沒有影響本題的實質異文（見 `projects/shanhaijing/data/derived/collation.jsonl`）。/ Neither entry has a witness variant that matters here.

## 2. 範圍宣告 / Scope (spec §9)

假說本身引用了西次三經（泰器之山）作為佐證，所以西次三經的「昆侖之丘」屬於範圍內。依「同名同地」預設，假說要對以下全部條目負責：
The hypothesis cites 西次三經 (泰器之山) as support, so the 西次三經 昆侖之丘 is in scope. Under the same-name default it must account for:

| 名稱 / Name | 出現段數 / Paragraphs | 代表條目 / Key entries |
|---|---|---|
| 崑崙 / 昆侖 | 18 | `SHJ-02-3-008`, `SHJ-11-1-012`, `SHJ-11-1-017`, `SHJ-16-1-037`, `SHJ-17-1-017` |
| 赤水 | 20 | `SHJ-02-3-008`, `SHJ-11-1-013`, `SHJ-15-1-001` |
| 黑水 / 黒水 | 15 | `SHJ-02-3-008`, `SHJ-02-3-012`, `SHJ-11-1-015` |
| 流沙 | 21 | `SHJ-02-3-006`, `SHJ-02-3-010`, `SHJ-11-1-008`, `SHJ-04-2-004`（東山經 / Eastern Classic） |
| 西海 | 9 | `SHJ-01-1-001`（南山經首山「臨於西海之上」/ first mountain of the Southern Classic）, `SHJ-02-1-019` |

## 3. 預先登記的預測與證偽條件 / Pre-registered predictions & falsifiers

| # | 預測（若 H 為真）/ Prediction if H is true | 證偽條件 / Falsifier |
|---|---|---|
| P1 | 崑崙位於地中海之南 / Kunlun lies south of the Mediterranean | 不在其南 / it does not |
| P2 | 崑崙位於撒哈拉邊緣 / Kunlun is at the Sahara's edge | 不在 / it is not |
| P3 | 文本中的「赤水」行為與紅海相容 / the text's 赤水 behaves compatibly with the Red Sea | 赤水在文本中是發源於山、流入他處的河流 / 赤水 is a river that rises on a mountain and flows elsewhere |
| P4 | 「黑水」行為與尼羅河相容 / 黑水 behaves compatibly with the Nile | 黑水發源於崑崙，或者流向與尼羅河不符 / 黑水 rises at Kunlun, or flows contrary to the Nile |
| P5 | 文本中同發源於崑崙的「河水」在候選地有對應 / the 河水 that also rises at Kunlun has a counterpart | 候選地沒有從崑崙發源的河流 / no river rises at the candidate |
| P6 | 崑崙的神形與獅身人面像相容且有獨特性 / the Kunlun god's form fits the Sphinx distinctively | 形態不合，或者這類描述在全書很常見 / misfit, or the description is common in the corpus |
| P7 | 「炎火之山，投物輒然」在崑崙外圍可找到 / a "fire mountain" lies around Kunlun | 沒有 / none |
| P8 | 以崑崙為錨點，西次三經其餘站點都落在有對應地物的位置 / anchored at Kunlun, the rest of 西次三經 lands on matching features | 大量站點的水系或地形無法對應 / many stations' rivers or terrain have no counterpart |
| P9 | 文鰩魚為飛魚，且「從西海遊于東海」在候選框架下可行 / 文鰩魚 is a flying fish and its West→East Sea route is feasible in this frame | 路線不可行 / route infeasible |

## 4. 證據 / Evidence (S5–S7)

### 4.1 P1・西海之南 — GEO — **E1 (+0.15)**
吉薩（29.98°N, 31.14°E）位於地中海以南。但對照集很大：任何地處「某個西方海域之南」的地點都滿足。而且書中「西海」也出現在南山經首山 `SHJ-01-1-001`（「臨於西海之上」），H 對這條沒有交代。
Giza lies south of the Mediterranean. The comparison set is huge, though: any place south of some western sea satisfies this. The corpus also uses 西海 for the first Southern-Classic mountain (`SHJ-01-1-001`), which H does not address.

### 4.2 P2・流沙之濱 — TER — **E1 (+0.15)**
吉薩在西部沙漠邊緣，吻合。不過「流沙」在全書 21 段出現，包括東山經 `SHJ-04-2-004`「又南水行五百里，流沙三百里」，可見它是通名（流動的沙），不專指某個沙漠。
Giza sits on the edge of the Western Desert, a fit. But 流沙 occurs in 21 paragraphs, including the Eastern Classic, so it is a generic term ("shifting sands"), not the name of one desert.

### 4.3 P3・赤水＝紅海 — HYD（詞彙 / lexicon）— **E−2 (−1.0)**
- `SHJ-02-3-008`：「赤水出焉，而東南流注于氾天之水」。
- `SHJ-11-1-013`：「赤水出東南隅，以行其東北。西南流注南海厭火東」。

在本書詞彙中，「水」配合「出／注」指河流，而海一律稱「海」（規格 §4）。赤水從崑崙發源，最後注入南海。海洋不會從山上發源，再流入另一個海。要讓赤水指海，必須跨越詞類，相當於一次 T5 校改。這裡改以 E−2 計分，不重複扣分。紅藻赤潮可以說明「赤」名的一種可能來源，但能產生赤色水體的機制在世界各地都很常見（赤潮、紅土泥沙），所以對照集很大，不提供正向證據。

In the book's lexicon, 水 with 出/注 means a river, and seas are always 海 (spec §4). 赤水 rises at Kunlun and ends in the South Sea. A sea does not rise on a mountain and flow into another sea. Making 赤水 a sea requires crossing word categories, i.e. a T5 emendation; it is scored here as E−2 instead, without double counting. Red algal blooms are one possible origin of the name, but red water is produced worldwide (blooms, laterite sediment), so the comparison set is large and there is no positive evidence.

### 4.4 P4・黑水＝尼羅河 — HYD — **E−2 (−1.0)**
- `SHJ-02-3-008`：「黑水出焉，而西流于大杅」，即黑水**發源於崑崙**，**向西**流。/ 黑水 **rises at Kunlun** and flows **west**.
- `SHJ-11-1-015`：「洋水、黑水出西北隅，以東，東行，又東北，南入海」。
- `SHJ-02-3-012`：「軒轅之丘……洵水出焉，南流注于黑水」。軒轅之丘在崑崙以西約 1,600 里，所以黑水流經崑崙以西的地帶。/ 軒轅之丘 is about 1,600 里 west of Kunlun, so 黑水 runs through land west of Kunlun.

尼羅河發源於遙遠的南方（東非湖區和衣索比亞高原），向北流入地中海，在吉薩附近只是流經。尼羅河既不從吉薩發源，吉薩以西也沒有尼羅河。
The Nile rises far to the south (the East African lakes and the Ethiopian highlands) and flows north into the Mediterranean; at Giza it only passes by. It neither rises at Giza nor runs west of it.

### 4.5 P5・河水 — HYD — **E−2，與 P4 同根，折半計 (−0.5)** / **E−2, same root as P4, discounted 50% (−0.5)**
- `SHJ-02-3-008`：「河水出焉，而南流注于無逹」。
- `SHJ-02-3-013`（積石之山，崑崙以西約 1,580 里 / about 1,580 里 west of Kunlun）：「其下有石門，河水冒以西流」。
- `SHJ-02-3-003`（不周之山）：「東望泑澤，河水所潛也」。

文本中的「河水」發源於崑崙，先向南流，在積石穿過石門向西流，在泑澤沒入地下。吉薩一帶沒有符合這個拓撲的河流（尼羅河已經被指定為黑水）。這一條與 P4 同根（「吉薩不是河源」），按框架 §4 規則 2 折減 50%。

The text's 河水 rises at Kunlun, flows south, then flows west through a stone gate at 積石 and sinks underground at 泑澤. Nothing near Giza fits that topology (the Nile is already assigned to 黑水). This shares P4's root ("Giza is not a river source"), so it is discounted 50% under framework §4 rule 2.

### 4.6 P6・神形與獅身人面像 — ARC — **E1 (+0.3)**

| 條目 / Entry | 描述 / Description | 對獅身人面像 / vs. the Great Sphinx |
|---|---|---|
| `SHJ-16-1-037` | 人面虎身，有文有尾，皆白 | 人面 ✓；虎身 ~（獅子不是老虎）；「有文」✗（獅子沒有斑紋）；有尾 ✓；皆白 ?（石灰岩原色；原本有彩繪的痕跡）/ human face ✓; tiger body ~ (a lion is not a tiger); striped ✗ (lions have no stripes); tail ✓; all white ? (limestone; traces of original paint) |
| `SHJ-11-1-017` | 開明獸身大類虎而九首，皆人面，**東嚮立**昆侖上 | 體型巨大 ✓；人面 ✓；**東向 ✓（大獅身人面像正朝東方）**；九首 ✗；「立」~（獅身人面像是伏臥的）/ huge ✓; human face ✓; **faces east ✓ (the Great Sphinx faces due east)**; nine heads ✗; "standing" ~ (the Sphinx is couchant) |
| `SHJ-02-3-008` | 陸吾：虎身而九尾，人面而虎爪 | 九尾 ✗ / nine tails ✗ |

**基準率 / Base rate**：全書「人面＋某身」的組合至少有 22 例（鳥身 6、獸身 5、蛇身 4、虎身 2，另有馬、牛、龍、豺、魚身各 1）。「人面虎身」另見 `SHJ-05-2-009`（中次二經・蔓渠之山「馬腹」，一種吃人的獸，位於伊水入洛的水系），所以它不是崑崙獨有的特徵。最具區分力的是「東嚮」一點，但它出自另一卷，而且同段的「九首」與獅身人面像矛盾。

At least 22 human-face composites occur in the corpus (bird body 6, beast 5, snake 4, tiger 2, and one each of horse, ox, dragon, jackal, fish). 人面虎身 also describes 馬腹 at 蔓渠之山 (`SHJ-05-2-009`, a man-eating beast in the 伊水→洛 drainage), so it is not unique to Kunlun. The most discriminating detail is "faces east", but it comes from another book, and the same passage's "nine heads" contradicts the Sphinx.

### 4.7 P7・炎火之山，投物輒然 — TER — **E−1 (−0.3)**
「投物輒然」（丟進去的東西立刻燒起來）指向持續燃燒的天然氣出口，或者活火山、熔岩。吉薩一帶沒有這兩者。蘇伊士灣沿岸有油苗的記載 `needs-citation`，但油苗不等於明火，所以不計分。
"Objects thrown in catch fire at once" points to a perpetually burning gas vent, or an active volcano or lava. Giza has neither. Oil seeps are reported on the Gulf of Suez coast (`needs-citation`), but a seep is not an open flame, so it scores nothing.

### 4.8 P8・西次三經鏈條擬合 — TER/HYD — **E−2 (−1.0)**
完整表格見 [chain-fit-giza.md](chain-fit-giza.md)（里長 300–500 m，4000 次蒙地卡羅模擬，種子 1）。
Full table: [chain-fit-giza.md](chain-fit-giza.md) (里 300–500 m, 4,000 Monte Carlo runs, seed 1).

| 站 / Station | 預測位置（標稱）/ Predicted (nominal) | 文本要求 / Text requires | 判定 / Assessment |
|---|---|---|---|
| 崇吾之山 #1 | 27.2°N 38.7°E ±292 km（阿拉伯半島西北部 / NW Arabia） | 「在河之南」，四方各有望見之物 / "south of the 河", sight-lines on four sides | 附近沒有可以稱為「河」的大河 ✗ / no river that could be "the 河" ✗ |
| 峚山 #4 → 鍾山 #5 | 29.9°N 35.6°E → 31.0°N 34.4°E | 「自峚山至于鍾山，四百六十里，其閒盡澤也」/ "all marsh for 460 里 between them" | 阿拉伯谷和內蓋夫一帶是沙漠，不是沼澤 ✗ / the Arava and Negev are desert, not marsh ✗ |
| 泰器之山 #6 | 31.0°N 33.65°E ±130 km（西奈北岸 / north Sinai coast） | 「觀水出焉，西流注于流沙」/ "觀水 flows west into the shifting sands" | 北西奈確實有沙丘帶；不過當地主要的河谷向北入海 ~ / north Sinai does have dunes, but its main wadi drains north to the sea ~ |
| 槐江之山 #7 | 31.0°N 32.3°E（尼羅河三角洲東北 / NE Nile delta） | 「南望昆侖」「西望大澤」/ "looks south to Kunlun; west to a great marsh" | 西面的三角洲湖沼 ✓；但「南望」約 150 km 外的吉薩不可能看見 ~ / delta lagoons to the west ✓; but Giza is ~150 km away, too far to see ~ |
| 樂遊之山 #9 → 翼望之山 #22 | 沿 30°N 向西，從 29.6°E 到 14.4°E（利比亞沙漠）/ due west along 30°N, 29.6°E to 14.4°E (Libyan Desert) | 至少 7 條河流或水體：桃水→稷澤、洵水→黑水、積石石門的河水、濁浴之水→蕃澤（其中多文貝）、英水→湯谷…… / at least 7 rivers or water bodies | 今天是極端乾旱的沙漠，沒有常年河 ✗。綠色撒哈拉時期（約 5,500 年前以前）有河湖，但那要求文本或其來源有那麼古老，需要額外論證（規格 §7.8）/ hyperarid desert today with no perennial rivers ✗. The Green Sahara (before ~5,500 years ago) had rivers and lakes, but that would require the text or its source to be that old, which needs separate argument (spec §7.8) |

### 4.9 P9・文鰩魚 — BIO — **E−1 (−0.3)**

**分類群候選 / Candidate taxa**（規格 §5）：

| 特徵 / Feature | 飛魚科 Exocoetidae | 飛角魚科 Dactylopteridae | 胸斧魚科 Gasteropelecidae |
|---|---|---|---|
| 狀如鯉魚 | ~ | ~ | ✗ |
| 魚身而鳥翼 | ✓ | ✓（不能真正飛行 / cannot really fly） | ✓ |
| 蒼文 | ✓（背部藍色 / blue dorsum） | ✓ | ? |
| 白首、赤喙 | ✗ | ? | ✗ |
| 以夜飛 | ~（夜間也會飛 / also flies at night） | ✗ | ? |
| 其音如鸞雞 | ✗ | ~（會發聲 / produces sounds） | ✗ |
| 棲地 / Habitat | 海洋表層 / marine surface waters | 海洋底棲 / marine benthic | 淡水，僅分佈於新熱帶 / freshwater, Neotropics only |

- 飛魚科是最佳候選，但飛魚分佈於全球各溫暖海域，包括地中海、紅海、印度洋和太平洋，所以**不能區分地點**（E0）。/ Exocoetidae is the best candidate, but flying fish live in every warm sea, so this **does not discriminate location** (E0).
- **棲地矛盾**：文本說泰器之山「是多文鰩魚」，而當地的觀水是向西流入流沙的溪流。海洋魚類不可能在這裡生活。這可能是 X6 傳聞插入，對任何框架都成立，所以不計入 H。/ **Habitat conflict**: the text puts many 文鰩魚 at 泰器之山, whose stream flows into desert sand, where no marine fish could live. Possibly an X6 hearsay insertion; this holds under any frame, so it is not charged to H.
- **路線**：在 H 的框架下，西海是地中海（位於泰器之北），東海應是紅海或亞喀巴灣。兩者之間在 1869 年蘇伊士運河通航之前沒有海路，古代的尼羅河至紅海運河是淡水運河，所以這條路線不可行 → **E−1**。原始假說中的「大西洋洄游太平洋」在生物學上沒有依據：沒有任何飛魚種群在大西洋和太平洋之間洄游。而且這與 H 自己「西海＝地中海」的設定自相矛盾。/ **Route**: in H's frame the West Sea is the Mediterranean (north of 泰器) and the East Sea would be the Red Sea or Gulf of Aqaba. There was no sea route between them before the Suez Canal (1869), and the ancient Nile–Red Sea canal carried fresh water, so the route is infeasible → **E−1**. The original claim "migrates from the Atlantic to the Pacific" has no biological basis: no flying-fish population migrates between those oceans. It also contradicts H's own "West Sea = Mediterranean".

### 4.10 其他 / Other — E0
- 「赤水之後，黑水之前」：在三種前／後慣例下（規格 §4）都無法區分，而且它依賴已經被否定的 P3 和 P4。/ Non-discriminating under all three front/back conventions, and it depends on P3 and P4, which have already failed.
- 西王母「戴勝，虎齒，有豹尾，穴處」：無法區分，E0。/ Non-discriminating, E0.

## 5. 合計 / Tally (S8)

| 通道 / Channel | 項目 / Items | log₁₀ LR |
|---|---|---|
| GEO | P1 | +0.15 |
| TER | P2 +0.15, P7 −0.3, P8 −1.0 | −1.15 |
| HYD | P3 −1.0, P4 −1.0, P5 −0.5 | −2.50 |
| ARC | P6 | +0.30 |
| BIO | P9 | −0.30 |
| 校改 / Emendations | 無 / none | 0 |
| **合計 / Total** | | **−3.50** |

依框架 §6，總值 < −2 → **R（否定）**。/ Per framework §6, total < −2 → **R (Refuted)**.

## 6. 紅隊 / Red team (framework §8)

1. **反例搜尋 / Counter-examples**：§2 的同名條目已全數核對。主要反例見 P3、P4、P5，另有「西海」出現在南山經這一點，H 沒有交代。/ All same-name entries in §2 were checked; the main counter-examples are P3–P5, plus the unexplained 西海 in the Southern Classic.
2. **替身測試 / Decoy**：H 的正向證據（P1、P2、P6）是「沙漠邊緣、在西方海域之南、有人面獸身的形象」。這三點在阿拉伯半島、伊朗高原、塔里木盆地等許多地方同樣成立，所以它們不能把 H 與對立假說區分開來。/ H's positive items (desert edge, south of a western sea, a human-faced beast image) hold equally in Arabia, the Iranian plateau, the Tarim basin and elsewhere, so they do not separate H from its rivals.
3. **基準率 / Base rate**：P6 已用全書頻率校正；P2「流沙」已確認是通名。/ P6 corrected by corpus frequency; P2 流沙 confirmed as a generic term.
4. **校改 / Emendations**：未使用任何校改。如果要把赤水改讀為海，需要 T5（−1.0），結果不變。/ None used; reading 赤水 as a sea would cost T5 (−1.0) and change nothing.
5. **敏感度 / Sensitivity**：
   - 移除最強的負向證據 P3 → −2.50，仍為 R。/ Remove the strongest negative (P3) → −2.50, still R.
   - 把 HYD 三項視為完全相關、只計一次 −1.0 → −2.00，落在 R 與 L0 的邊界。/ Treat the three HYD items as fully correlated (one −1.0) → −2.00, on the R/L0 boundary.
   - 把 P8 排除（假設西次三經另有來源）→ −2.50，仍為 R。/ Exclude P8 (assume a separate source for 西次三經) → −2.50, still R.
   - 結論在合理的參數範圍內穩定，最樂觀的情況是 L0。/ The verdict is stable across reasonable parameters; the most favourable case is L0.

## 7. 裁決 / Verdict

**R — 就目前的表述而言否定。** 主要原因是**水系通道**：書中的赤水、黑水、河水都是**從崑崙發源**的河流，有明確的流向和去處。吉薩一帶不能滿足這個結構，紅海也不是河流。其次，以吉薩為錨點時，西次三經的西半段要求利比亞沙漠中存在至少 7 條河流或湖澤。正向證據（地中海之南、沙漠邊緣、人面獸身）都屬於泛化吻合，不能把 H 與其他候選區分開來。

**R: refuted as formulated.** The decisive channel is **hydrology**: the text's 赤水, 黑水 and 河水 are all rivers that **rise at Kunlun**, with stated directions and destinations. Giza cannot satisfy that structure, and the Red Sea is not a river. Secondly, anchoring at Giza makes the western half of 西次三經 require at least seven rivers or lakes in the Libyan Desert. The positive evidence (south of the Mediterranean, desert edge, human-faced beast) is all generic and does not separate H from other candidates.

## 8. 保留的觀察（任何框架都必須解釋）/ Retained observations (every frame must explain these)

| # | 觀察 / Observation | 條目 / Entry | 用途 / Use |
|---|---|---|---|
| O-1 | 巨大的人面虎形守衛「東嚮立」於崑崙上 / a huge human-faced tiger-like guardian "stands facing east" on Kunlun | `SHJ-11-1-017` | 圖本假說（X5）或紀念建築的指紋 / map-source hypothesis (X5) or monument fingerprint |
| O-2 | 似飛魚的海洋魚「從西海遊于東海」，說明敘述者知道東西兩側都有溫暖海域。**純本地框架也必須解釋這一點**，因為一個「西方的海」並不明顯存在 / a flying-fish-like marine fish "swims from the West Sea to the East Sea": the narrator knew warm seas on both sides. **A purely local frame must explain this too**, since an obvious "western sea" is not evident there | `SHJ-02-3-006` | 盲候選生成指紋：兩側都有溫暖海域、中間有可通行海路的陸塊 / blind candidate fingerprint: a landmass with warm seas on both sides and a passable sea route between them |
| O-3 | 「炎火之山，投物輒然」 | `SHJ-16-1-037` | 指紋：天然氣長明火或活火山帶 / fingerprint: perpetual gas fires or an active volcanic belt |
| O-4 | 河水：從崑崙發源，向南流 → 在積石穿石門向西流 → 在泑澤伏流 / rises at Kunlun, flows south → west through a stone gate at 積石 → sinks at 泑澤 | `SHJ-02-3-008`, `-013`, `-003` | 指紋：有峽谷段並最終注入內流盆地的河流 / fingerprint: a river with a gorge reach that ends in an endorheic basin |

## 9. 可登記的改寫 / Reformulations that may be registered

- **H-0001b**：只主張大荒西經 `SHJ-16-1-037` 一段描述東北非，並且是與山經不同的另一個崑崙傳統。依規格 §9，必須先提出語料內部的證據，證明兩個崑崙是不同地點，等級上限為 L1。下一步是用大荒西經相鄰條目的相對方位網路檢驗（任務 T-310）。/ Claims only that `SHJ-16-1-037` describes NE Africa as a Kunlun tradition separate from the Mountain Classic's. Per spec §9 it must first show internal evidence that the two are different places; capped at L1. Next test: the relative-position network of neighbouring 大荒西經 entries (task T-310).
- **對立候選必須盲生成**：依規格 §8，用 O-2、O-3、O-4 的指紋生成候選（任務 T-610），不參考任何前人比定。/ **Rivals must be generated blind** (spec §8) from fingerprints O-2–O-4 (task T-610), without consulting prior identifications.

## 10. 重測觸發條件 / Re-test triggers
- 新的見證本顯示赤水、黑水的「出焉」為後人竄入。/ A new witness shows that the 「出焉」 of 赤水 or 黑水 is an interpolation.
- 語料內部證據顯示西次三經與大荒西經的崑崙是不同地點。/ Internal evidence shows the 西次三經 and 大荒西經 Kunlun are different places.
- 獨立證據顯示西次三經的觀測年代早於撒哈拉乾旱化。/ Independent evidence dates the 西次三經 observations to before Saharan aridification.
