# H-0006 卷宗（方法 G）：崑崙在哪裡？——全球、描述優先的比對
# Dossier H-0006 (Method G): Where is Kunlun? A global, description-first match

| 欄位 / Field | 值 / Value |
|---|---|
| 方法 / Method | **方法 G**（[method-g-global.md](../../docs/method-g-global.md)）：全書以整個地球為範圍；只看描述、名稱遮蔽；距離不用 / **Method G**: whole-Earth premise; descriptions only, names masked; distances not used |
| 狀態 / Status | adjudicated (draft v0.2) |
| 結論 / Verdict | **單一地點：G-弱至中**（安那托利亞中部、吉薩、墨西哥中部並列前三，領先不穩）。**同一水系複合：尼羅河（吉薩 ＋ 月亮山／魯文佐里）6.51，為庫中最高，但屬事後分析**。/ **Single place: G-weak to moderate** (Central Anatolia, Giza, Central Mexico in the top three, leader unstable). **Same-river composite: the Nile (Giza + Rwenzori "Mountains of the Moon") 6.51, highest in the base, but post-hoc.** |
| 重現 / Reproduce | 見 §8 / see §8 |
| 資料 / Data | `data/world/loci.jsonl`（27 處候選，跑分前提交）、`data/world/animals.jsonl`（94 種動物）/ 27 loci committed before scoring; 94 animals |

---

## 1. 問題 / Question

項目發起人：「崑崙在哪裡？可能在埃及。」本卷宗不預設答案，把全球 27 處候選用同一套規則排名，埃及只是其中之一。
The initiator: "Where is Kunlun? It could be in Egypt." No answer is assumed; 27 candidates worldwide are ranked under one rule set, Egypt among them.

## 2. 書中對崑崙的描述（名稱遮蔽後）/ What the book says about Kunlun (names masked)

**計分段落（崑崙為主語）/ Scored passages**：`SHJ-02-3-008`、`SHJ-06-1-017`、`SHJ-11-1-012`–`022`、`SHJ-16-1-037`，以及 `SHJ-02-3-007` 的分句「南望昆侖，其光熊熊，其氣魂魂」。只提到名稱的其他 13 段列出但不計分（見 [geo-match.md](geo-match.md)）。/ Other mentions are listed but not scored.

| 特徵 / Feature | 書中依據 / Text | 罕見度權重 / Weight |
|---|---|---|
| 人面獸身的巨型守衛 / human-faced feline guardian | `SHJ-11-1-017`「開明獸身大類虎而九首，皆人面」；`SHJ-16-1-037`「有神，人面虎身，有文有尾，皆白」；`SHJ-02-3-008`「虎身而九尾，人面而虎爪」 | 0.85（或讀為真實動物：雪豹 0.53×0.74）/ or animal reading: snow leopard |
| **面向東方** / **faces east** | `SHJ-11-1-017`「東嚮立昆侖上」 | **1.41**（只有 1 處候選為 T）/ only one locus is T |
| 門與井的建築 / gates and wells | `SHJ-11-1-012`「面有九井，以玉為檻。面有九門，門有開明獸守之」 | 0.55 |
| 北面有海 / a sea to the north | `SHJ-16-1-037`「西海之南」 | 0.60 |
| 沙地邊緣 / edge of sands | `SHJ-16-1-037`「流沙之濱」 | 0.43 |
| 環繞之水 / encircling water | `SHJ-16-1-037`「其下有弱水之淵環之」 | 0.65 |
| 火 / fire | `SHJ-16-1-037`「其外有炎火之山，投物輒然」 | 0.37 |
| 光 / glow（雪或火）| `SHJ-02-3-007`「其光熊熊，其氣魂魂」 | 0.23 / 0.37 |
| 大河之源、四方出水 / great river source, rivers in all directions | `SHJ-02-3-008`（河、赤、洋、黑四水）；`SHJ-11-1-013`–`016`（四隅出八水）| 0.33 + 0.41 |
| 高大 / great height | `SHJ-11-1-012`「方八百里，高萬仞」 | 0.18 |
| 穴居 / cave dwelling | `SHJ-16-1-037` 西王母「穴處」 | 1.20 |
| 神之所居 / gods' abode | `SHJ-02-3-008`「帝之下都」 | 0.17 |
| 玉 / jade | `SHJ-11-1-012`「以玉為檻」 | 0.69 |
| 動物：四角似羊 / four-horned sheep-like beast | `SHJ-02-3-008` 土螻 →（最佳）四角羚 0.80 | 1.00 |
| 動物：五采如雞之鳥 / five-coloured fowl | `SHJ-11-1-018` 鳳皇、鸞鳥；描述取自 `SHJ-01-3-003`「其狀如雞，五采而文」→ 孔雀類 | 1.18 |

## 3. 單一地點排名 / Ranking as a single place

| 名次 | 候選 / Locus | 分數 | 吻合 | 矛盾 |
|---|---|---|---|---|
| 1 | 安那托利亞中部（赫梯哈圖沙、卡帕多細亞）/ Central Anatolia | **0.59** | 6 | 7 |
| 2 | **吉薩高原，下埃及 / Giza** | **0.13** | 5 | 8 |
| 3 | 墨西哥中部 / Central Mexico | 0.10 | 5 | 4 |
| 4 | 興都庫什 / Hindu Kush | −0.58 | 7 | 5 |
| 5 | 魯文佐里與尼羅河湖區 / Rwenzori and the Nile lakes | −0.86 | 7 | 6 |
| … | 岡仁波齊 −1.64、亞拉拉特 −1.82、衣索比亞高原 −1.94、青海湖 −2.88、西崑崙（和田）−3.05、西奈 −3.09 … | | | |

**留一檢驗 / Jackknife**：16 次中領先者為安那托利亞 10 次、吉薩 3 次、墨西哥 2 次、興都庫什 1 次。只要移除「穴居」一項，吉薩就領先 1.23；移除「火」或「光」，吉薩也領先。**單一地點的結論不穩**：沒有任何一處能同時滿足大部分描述，每個候選的矛盾都和吻合差不多多。
Anatolia leads 10 of 16 times, Giza 3, Mexico 2, Hindu Kush 1. Removing "cave dwelling" alone puts Giza ahead by 1.23; removing "fire" or "glow" also does. **The single-place result is unstable**: no locus satisfies most of the description, and every candidate has about as many contradictions as matches.

## 4. 兩種描述 / Two descriptions in one name

逐項明細顯示，書中的崑崙同時有兩套互不相容的描述。/ The itemised scores show two mutually incompatible descriptions.

| 描述 / Description | 第一 / 1st | 第二 / 2nd | 第三 / 3rd |
|---|---|---|---|
| **自然**：高山、雪或火光、四方出水、環繞之水、火山、動物 / **natural** | 魯文佐里（月亮山）0.96 | 興都庫什 0.44 | 岡仁波齊 −0.07 |
| **人工**：人面獸身巨像、東向、門與井、穴居、神居 / **built** | 安那托利亞中部 2.60 | **吉薩 1.61** | 墨西哥中部 0.55 |

- 「人工」描述中，**吉薩是唯一滿足「東向」的候選**（大獅身人面像正朝東，+1.41）。安那托利亞之所以領先，只因「穴居」一項（+1.20 對吉薩 −1.20）；而「穴處」原文說的是西王母這個人，不一定指一種地方傳統。/ In the built description **Giza is the only locus that satisfies "faces east"**. Anatolia leads only through "cave dwelling", and 「穴處」 describes the person 西王母, not necessarily a local tradition.
- 「自然」描述中，魯文佐里的領先主要來自鳳皇→孔雀（剛果孔雀分佈於該區，+1.18）；移除這一項後領先消失。/ In the natural description Rwenzori's lead comes mainly from 鳳皇 → peafowl (the Congo peafowl lives there); without it the lead disappears.

## 5. 同一水系的複合讀法（事後分析）/ Same-river composite reading (post-hoc)

書中說河水「出」崑崙（`SHJ-02-3-008`、`SHJ-11-1-014`）。若崑崙是**同一條河上的兩處**，例如下游的聖所與上游的源頭雪山，每個特徵可取兩處中較好者：
The book says the 河 issues from Kunlun. If Kunlun is **two places on one river**, a sanctuary downstream and a snow-capped source upstream, each feature takes the better of the two:

| 複合 / Composite | 水系 / River | 分數 / Score |
|---|---|---|
| **吉薩 ＋ 魯文佐里（月亮山）/ Giza + Rwenzori** | **尼羅河 / Nile** | **6.51** |
| 吉薩 ＋ 衣索比亞高原 / Giza + Ethiopian Highlands | 尼羅河 | 4.50 |
| 魯文佐里 ＋ 傑貝爾巴卡爾 / Rwenzori + Jebel Barkal | 尼羅河 | 3.37 |
| 岡仁波齊 ＋ 興都庫什 / Kailash + Hindu Kush | 印度河 / Indus | 0.73 |
| 岡仁波齊 ＋ 珠峰區 / Kailash + Everest | 恆河 / Ganges | 0.14 |
| 基爾庫克 ＋ 亞拉拉特 / Kirkuk + Ararat | 底格里斯河 / Tigris | −1.12 |

吉薩＋月亮山這一組的組成：吉薩提供人面獸身守衛、東向、門井建築、北面有海、沙漠邊緣（＋3.84）；月亮山提供高山、火山熔岩湖（尼拉貢戈，「投物輒然」）、環繞的湖泊、光、河源、孔雀（＋3.08）。
Giza supplies the guardian, east-facing pose, gates and wells, sea to the north and desert edge (+3.84); the Mountains of the Moon supply the high peak, the lava lake of Nyiragongo (「投物輒然」), the ringing lakes, the glow, the river source and the peafowl (+3.08).

**這一結果的弱點 / Weaknesses**（紅隊 / red team）：
1. **事後分析**：複合讀法是看到單一地點結果之後才提出的。/ **Post-hoc**: proposed after seeing the single-place results.
2. **庫的組成偏差**：尼羅河水系在庫中有 4 處候選，其他水系最多 3 處，多數只有 1 處。可組合的配對越多，最高分越容易偏高。這是因為建庫時特意加入了與埃及假說相關的候選。/ **Base composition**: the Nile has 4 loci, others at most 3, most only 1; more pairs inflate the best composite. This happened because Egypt-related candidates were deliberately included.
3. **未知值抵消矛盾**：在複合中，一處的「未知」會抵消另一處的「否」。/ **Unknowns cancel contradictions** inside composites.
4. 土螻（四角羚，印度）在所有尼羅河組合中仍是矛盾（−0.40）。/ 土螻 (four-horned antelope, India) remains a contradiction in every Nile composite.

## 6. 預先登記的檢驗 / Pre-registered test

**N4（先登記、後執行）**：若崑崙在尼羅河，那麼崑崙所在路線（西次三經）的動物描述投票，應有北非、東非或中非進入前三。/ **N4 (registered before running)**: if Kunlun is on the Nile, the creature vote of its route section (西次三經) should put NAF, EAF or CAF in its top three.

**結果：弱通過**。西次三經投票為 印度 0.50、喜馬拉雅 0.40、**東非 0.20**。東非進入前三，但印度、喜馬拉雅領先，主要因為土螻（四角羚）一項。五個被接受的比對中，三個的分佈含非洲：舉父「如禺而文臂……善投」→ 狒狒，狡「如犬而豹文」→ 鬣狗，䱻魚「如蛇而四足」→ 巨蜥。
**Result: weak pass.** 西次三經 votes India 0.50, Himalaya 0.40, **East Africa 0.20**: Africa makes the top three, but India/Himalaya lead, mainly through 土螻. Three of five accepted matches range into Africa: 舉父 → baboon, 狡 → hyena, 䱻魚 → monitor lizard.

**下一步要先登記的檢驗 / Next pre-registered tests**（任務 / tasks T-660–T-662）：
- **N5 庫的平衡**：把幼發拉底–底格里斯、印度河、恆河、黃河、長江、亞馬遜、密西西比等水系各補到 ≥ 4 處候選（含當地的古代紀念建築）之後，尼羅河複合仍須排第一。/ **Balanced base**: after bringing each major river system to ≥ 4 loci, the Nile composite must still rank first.
- **N6 相鄰地名**：書中「流沙」「赤水」「黑水」「弱水」「西王母之山」作為獨立地點分別比對時，前幾名應落在尼羅河軸線上。/ **Neighbouring names**: matched as separate places, these should rank Nile-axis loci near the top.
- **N7 動物**：西王母「虎齒、豹尾、穴處、善嘯」等描述，以及海內西經開明諸段的動物，在動物地圖中應投向非洲。/ **Animals**: the creatures around 開明 and 西王母's description should vote for Africa.

## 7. 結論與兩種方法的比較 / Conclusion and the two methods compared

**繁中**：
- **「崑崙可能在埃及嗎？」——在方法 G 之下，可能，但尚未證實。** 埃及是全球 27 處中，**唯一**符合「巨大的人面獸身守衛、面向東方」的地點，在單一地點排名中位居第二。若把崑崙讀成「同一條大河上的聖所加源頭雪山」，尼羅河（吉薩＋月亮山）是目前庫中得分最高的組合，而且領先很多（6.51 對下一個非尼羅河組合 0.73）。
- **但結果脆弱**：單一地點的領先者會隨一個特徵改變；複合讀法是事後提出的，且受到庫的組成偏差影響。在 N5 庫平衡檢驗通過之前，只能定為**候選**。
- **與方法 A 的差異**：方法 A（H-0001：R；H-0003：青海湖 L1）把書中「河」與其他山經河流（渭、汾、洛……）的關係、以及里程方位當成主要證據，因此把「河」定為黃河，崑崙在其上游。方法 G 遮蔽名稱、不用距離，所以「河」這個名字與其他篇的連結不參與計分；決定性的反而是「東向的人面獸身守衛」這類只有吉薩具備的描述。兩種結論都保留：**它們回答的是不同的問題**。方法 A 問的是「以書的內部結構為準，崑崙在哪」；方法 G 問的是「以描述本身為準，地球上哪裡最像」。

**EN**:
- **"Could Kunlun be in Egypt?" Under Method G: possibly, not yet proven.** Egypt is the **only** one of 27 loci that satisfies "a huge human-faced feline guardian facing east", and ranks second as a single place. Read as "a sanctuary plus a snow-capped source on one great river", the Nile (Giza + Mountains of the Moon) is the best composite in the base by a wide margin (6.51 against 0.73 for the best non-Nile composite).
- **But it is fragile**: the single-place leader changes with one feature, and the composite reading is post-hoc and affected by base composition. Until the balanced-base test N5 passes, it is only a **candidate**.
- **Versus Method A**: Method A (H-0001: R; H-0003: Qinghai Lake L1) treats the 河's links to the other Mountain-Classic rivers, and the distances and bearings, as primary evidence, so it reads the 河 as the Yellow River with Kunlun upstream. Method G masks names and drops distances, so those links do not score; what decides instead is a description only Giza has. Both conclusions are kept: **they answer different questions**. Method A asks where Kunlun is given the book's internal structure; Method G asks which place on Earth best matches the description itself.

## 8. 重現 / Reproduce

```bash
python3 -I tools/shj/creatures.py && python3 -I tools/shj/animal_map.py
E=SHJ-02-3-008,SHJ-06-1-017,SHJ-11-1-012,SHJ-11-1-013,SHJ-11-1-014,SHJ-11-1-015,SHJ-11-1-016,SHJ-11-1-017,SHJ-11-1-018,SHJ-11-1-019,SHJ-11-1-020,SHJ-11-1-021,SHJ-11-1-022,SHJ-16-1-037
python3 -I tools/shj/geo_match.py --target "崑崙|昆侖|崐崘" --entries $E --clause "SHJ-02-3-007:南望昆侖，其光熊熊，其氣魂魂" --pairs --md projects/shanhaijing/hypotheses/H-0006/geo-match.md
python3 -I tools/shj/geo_match.py --target "崑崙|昆侖|崐崘" --entries $E --clause "SHJ-02-3-007:南望昆侖，其光熊熊，其氣魂魂" --group natural --md projects/shanhaijing/hypotheses/H-0006/geo-match-natural.md
python3 -I tools/shj/geo_match.py --target "崑崙|昆侖|崐崘" --entries $E --clause "SHJ-02-3-007:南望昆侖，其光熊熊，其氣魂魂" --group built --md projects/shanhaijing/hypotheses/H-0006/geo-match-built.md
```
