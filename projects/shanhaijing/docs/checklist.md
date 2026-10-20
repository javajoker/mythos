# 山海經交付檢查清單 / Shanhaijing Deliverable Checklist

> v3.0 ・ 每次產生或更新交付版本（`deliverables/draft-vN/`）之前逐項勾選。`shj-lead` 負責，`devils-advocate` 複核。
> Tick every item before producing or updating a deliverable. Owned by `shj-lead`, reviewed by `devils-advocate`.

## 1. 文本 / Text
- [ ] 段落次序依工作文本（明成化本），讀法依草稿讀法政策（[source-assessment](source-assessment.md) §4）/ working-text order, draft-reading policy
- [ ] 若某條異文會改變抽出的實體或關係，已列出三個見證本的讀法並說明採用哪一個 / variants that change an entity or relation are listed with the choice made

## 2. 實體與關係 / Entities and relations（步驟 1–2）
- [ ] `kg_extract.py` 覆蓋檢查：沒有實體的段落 = 0，未解釋的名稱句式 = 0 / coverage audit at 0 and 0
- [ ] 新增的「已解釋」類別附有原文例句 / every new explained category has an example
- [ ] 名稱沒有被改成今名，也沒有因同名而合併不同篇的山 / no modern renaming; no merge by name alone across sections

## 3. 候選 / Candidates（步驟 3）
- [ ] 真實世界庫的修改在看結果之前提交，提交訊息說明理由 / base changes committed, with reasons, before looking at results
- [ ] 名稱不計分 / names never score
- [ ] 檢查庫的平衡（各大河的支流數、各地區的性質數）/ base balance checked

## 4. 交叉驗證 / Cross-validation（步驟 4）
- [ ] 兩次執行輸出逐位元組相同 / two runs, identical bytes
- [ ] 各鏈總分與最佳總分已記錄於 `crossval-log.json` / chain energies logged
- [ ] 抽查原文自己的陳述（「A 注于 B」）：A、B 的對應屬於同一水系，或已說明為何不是 / spot-check the text's own statements
- [ ] 權重或求解器的修改有一般性的理由，並套用到全書 / weight or solver changes have a general reason and apply to the whole book

## 5. 交付 / Deliverable（步驟 5）
- [ ] `coverage.md` 為 PASS：段落數、提及數與寫入的列數相等 / completeness PASS
- [ ] 每個未對應的實體都寫明原因 / every unmapped entity states its reason
- [ ] README 的措辭符合可信度級別：「暫定」不當作結論引用 / README wording matches the tiers; tentative items are not cited as findings
- [ ] README 寫明限制與主要的其他候選 / limits and main alternatives stated
- [ ] `devils-advocate` 的審查意見已處理或記錄 / red-team comments addressed or recorded
- [ ] 已提交 / committed

## 6. 時代語義版 / Era-semantic version（規格 v3）
- [ ] 輸入只有原文（明成化本次序與讀法），沒有注疏 / original text only, no commentary
- [ ] 每個候選在前 4000–前 2000 年內存在或可見，並標明年代與當時樣貌 / every candidate dated within the window
- [ ] 判斷時名稱已遮蔽；名稱特徵單獨計分並標明；理由中沒有今名比對 / names masked; name features flagged; no modern-name matching in reasons
- [ ] 每個判斷至少 3 個樣本，紀錄完整（證據、理由、模型、提示詞版本）/ three samples, complete records
- [ ] 洩漏抽樣與誘餌已執行，結果寫入紅隊紀錄 / leakage probes and decoys run
- [ ] 重點文明（兩河、哈拉帕、埃及）的每一個比較都包含其他同時期文明作為對立候選 / rivals present in every comparison
- [ ] 新增的候選類別在全世界同類中一起加入 / new kinds added worldwide
- [ ] 當時地圖的海岸線、河道與界線注明為簡化示意 / era map marked as schematic
