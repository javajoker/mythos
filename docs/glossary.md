# 詞彙表 / Glossary

| 繁中 | English | 定義 / Definition |
|---|---|---|
| 見證本 | Witness | 一部文本的某個獨立版本或轉錄 / an independent edition or transcription |
| 底本 | Base text | 編號所依據的見證本 / the witness entry IDs are keyed to |
| 工作文本 | Working text | 按最早見證本順序排列、選定讀法的文本 / the text in earliest-witness order with chosen readings |
| 異文 | Variant | 見證本之間的差異 / a difference between witnesses |
| 錯簡 | Displacement | 段落或竹簡的錯位 / a misplaced paragraph or slip |
| 條目 | Entry | 可引用的最小文本單位（段）/ the smallest citable unit (paragraph) |
| 實體 | Entity | 書中提到的一個對象（山、水、國族、生物…），名稱只是它的符號 / a thing the text mentions; its name is only a symbol |
| 符號 | Symbol | 實體在書中的寫法；不與今名比對 / an entity's spelling in the text; never matched to modern names |
| 提及 | Mention | 某實體在某段中出現一次 / one occurrence of an entity in a paragraph |
| 知識圖譜 | Knowledge graph (KG) | 實體（節點）與關係（邊）的集合，每條都附條目編號 / entities and relations, each with entry IDs |
| 關係 | Relation (edge) | 兩個實體之間的有類型連結，例如相鄰、發源、注入、位於、望見 / a typed link between entities |
| 性質 | Property | 從描述抽出的標籤，例如礦產、形態、習俗 / a tag extracted from a description |
| 真實世界庫 | World base | 全球地區、水體、動物、古文化的資料，在計分前提交 / worldwide regions, waters, animals, cultures, committed before scoring |
| 候選 | Candidate | 一個實體可能對應的真實世界實體 / a real-world entity an entity might be |
| 自身分數 | Own score | 候選與實體描述、性質的吻合度 / how well a candidate fits the entity's description |
| 關係因子 | Relation factor | 兩端候選是否在真實世界中具有書中所說的關係 / whether two candidates stand in the stated relation |
| 總分（能量）| Energy (E) | 全部自身分數與關係因子之和，減去唯一性懲罰 / the sum of own scores and factors minus uniqueness |
| 唯一性懲罰 | Uniqueness penalty | 兩個書中實體對到同一真實實體時的扣分 / the cost of two entities mapping to one real entity |
| 聯合求解 | Joint solution | 同時為所有實體選候選，使總分最高 / choosing all candidates at once to maximise E |
| 區塊調整 | Block move | 一個實體連同相鄰實體一起換候選的求解步驟 / a solver move changing an entity with its neighbours |
| 樣本 | Sample | 一次完整求解或一次丟棄部分關係的重解 / one full solve or one re-solve with relations dropped |
| 穩定度 | Stability | 樣本中選到同一候選的比例 / the share of samples agreeing |
| 邊際 | Margin | 最佳與次佳候選的局部分差 / local best minus second best |
| 可信度 | Confidence | 穩定度 × (1 − e^(−邊際)) / stability × (1 − e^(−margin)) |
| 暫定 | Tentative | 可信度 < 0.1：總分最高但樣本意見不一，不宜引用 / below 0.1: do not cite |
| 主要水體 | Major water | 單獨對應真實水體的書中之水（支流多、提及多、海湖、有完整出入）/ a water mapped individually |
| 小溪 | Minor stream | 只經由源山與去向參與驗證的書中之水 / a water acting only through its relations |
| 覆蓋檢查 | Coverage audit | 證明沒有段落、沒有名稱句式被遺漏的檢查 / the check that nothing was missed |
| 完整性檢查 | Completeness check | 交付中段落數與提及數等於原書的檢查 / deliverable rows equal the text's paragraphs and mentions |
| 紅隊 | Red team | 專門試圖推翻對應的審查 / review that tries to break the mapping |
| 里 | li | 古代長度單位，長度不預設，只作參考 / ancient length unit, a reference only |
| 出／注／潛 | rises / flows into / sinks | 山海經的水系動詞 / Shanhaijing hydrological verbs |
| 流沙 | Flowing sands | 通名，全書 21 段出現 / a generic term, 21 paragraphs |
