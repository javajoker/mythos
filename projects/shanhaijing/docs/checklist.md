# 山海經交付檢查清單 / Shanhaijing Deliverable Checklist

> v3.0 ・ 2026-10-20 ・ 每次產生或更新交付版本之前逐項勾選；`shj-lead` 負責，`devils-advocate` 複核。
> Tick every item before producing or updating a deliverable; owned by `shj-lead`, reviewed by `devils-advocate`.

## 1. 文本 / Text
- [ ] 只用原文：明成化本的次序與讀法；注疏沒有進入任何步驟 / original text only; no commentary
- [ ] 每個替代讀法（形近字、數字、錯簡）都有見證本或明列的錯誤類型，並記錄在判斷紀錄中 / every variant reading sourced and recorded

## 2. 知識圖譜 / Knowledge graph
- [ ] 覆蓋檢查：沒有實體的段落 = 0、未解釋的名稱句式 = 0 / coverage 0 and 0
- [ ] 名稱特徵已抽出，且沒有被當作辨識依據 / name features extracted, never identifiers

## 3. 時代世界 / Era world
- [ ] 世界庫的修改在計分之前提交，提交訊息說明原因 / base committed before scoring
- [ ] 每個候選在前 4000–前 2000 年內存在或可見，標明年代與當時樣貌 / every candidate dated within the window
- [ ] 新增的候選類別在全世界同類中一起加入；重點文明之外有同時期的對立文明 / symmetry and rivals
- [ ] 來源是一般性的考古、古地理、動物學資料，沒有對山海經的既有詮釋 / general sources only

## 4. 語義判斷 / Semantic judgments
- [ ] 判斷時名稱已遮蔽；名稱特徵單獨計分並標明 / names masked; name features flagged
- [ ] 理由中沒有今名比對，也沒有「有名」之類的理由 / no modern-name or fame reasons
- [ ] 每個判斷至少 3 個樣本，紀錄完整（證據、理由、模型、提示詞版本、雜湊）/ three samples, complete records
- [ ] 洩漏抽樣（10%）與誘餌（5%）已執行，結果寫入紅隊紀錄 / leakage probes and decoys run

## 5. 求解與可信度 / Solving and confidence
- [ ] 兩次執行輸出逐位元組相同 / two runs, identical bytes
- [ ] 抽查原文自己的陳述（「A 注于 B」「X 在 Y 西」）在對應中是否成立，或說明為何不成立 / spot-check the text's own statements
- [ ] 權重的修改有一般性的理由，並套用到全書 / weight changes general and book-wide

## 6. 交付 / Deliverable
- [ ] 完整性檢查 PASS：段落數、提及數與寫入的列數相等 / completeness PASS
- [ ] 每個未對應的實體寫明原因 / every unmapped entity has a reason
- [ ] README 的措辭符合可信度級別；暫定不當作結論 / wording matches tiers
- [ ] 當時地圖的輪廓注明為簡化示意 / era map marked schematic
- [ ] 紅隊意見已處理或記錄；已提交 / review addressed; committed
