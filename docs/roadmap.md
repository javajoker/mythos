# 路線圖 / Roadmap

> v2.0 ・ 2026-10-19

| 階段 / Phase | 內容 / Content | 退出條件 / Exit criteria |
|---|---|---|
| **1 山海經 / Shanhaijing** | 文本層；全書知識圖譜；全球候選；交叉驗證；逐條交付（初稿 v1 已完成）；庫的平衡、權重敏感度、紅隊審查 / text layer, whole-book KG, candidates, cross-validation, item-by-item deliverable (draft v1 done); base balance, sensitivity, red team | 交付 v2：紅隊意見已處理、敏感度已報告、中高可信度的對應在權重合理變動下不變 / draft v2 with red-team comments addressed and mid/high mappings robust to reasonable weight changes |
| **2 中文跨語料 / Chinese cross-corpus** | 接入《穆天子傳》《淮南子・地形訓》《尚書・禹貢》《水經》，以同一方法建立知識圖譜，跨書合併實體作為額外關係 / ingest these texts with the same method; cross-book entity links become extra relations | 第二部語料只靠入庫與實體句式兩個適配器即可運行 / a second corpus runs with only two adapters (ingest, entity patterns) |
| **3 多語種 / Multilingual** | 依序評估：美索不達米亞、古埃及、吠陀與往世書、希臘、瑪雅 / Mesopotamian, Egyptian, Vedic and Puranic, Greek, Maya | 每新增一個語種，同時加入該語言的文檔版本 / each language adds its doc locale |
| **4 宇宙觀 / Cosmology** | 天文與曆法實體（日月出入之山、星宿、天象）與天文回推比對 / astronomical and calendar entities vs retro-calculation | 天文類實體有中等以上可信度的對應 / astronomical entities mapped at medium confidence or better |

**挑選新語料的原則 / Corpus selection**：實體多、關係明確（方位、距離、河流去向、清單）的文本優先；有多個獨立見證本的優先。/ Texts rich in entities and explicit relations first; multiple independent witnesses preferred.
