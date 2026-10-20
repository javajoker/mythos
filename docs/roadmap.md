# 路線圖 / Roadmap

> v2.0 ・ 2026-10-19

| 階段 / Phase | 內容 / Content | 退出條件 / Exit criteria |
|---|---|---|
| **1 山海經 / Shanhaijing** | 文本層；全書知識圖譜；全球候選；交叉驗證；逐條交付；庫的平衡、權重敏感度、紅隊審查；空間關係與解讀規則（初稿 v3 已完成） / text layer, whole-book KG, candidates, cross-validation, item-by-item deliverable; base balance, sensitivity, red team; spatial relations and reading rules (draft v3 done) | 交付 v4：同名誤併修正、更細的地點（T-C10）、求解器收斂（T-X03）、R1 的約束（T-X09）/ draft v4 with homonyms fixed, finer places, convergence and an R1 constraint |
| **1b 時代語義版 / Era-semantic version** | 框架 v3：前 4000–前 2000 年的時代世界、中原原點、遮蔽的大模型語義判斷、當時地圖；西山經與大荒西經試點 / framework v3, era world, masked LLM judgments, era map; West-books pilot | 交付 v4 並通過紅隊審查 / draft v4 passes review |
| **2 中文跨語料 / Chinese cross-corpus** | 接入《穆天子傳》《淮南子・地形訓》《尚書・禹貢》《水經》，以同一方法建立知識圖譜，跨書合併實體作為額外關係 / ingest these texts with the same method; cross-book entity links become extra relations | 第二部語料只靠入庫與實體句式兩個適配器即可運行 / a second corpus runs with only two adapters (ingest, entity patterns) |
| **3 多語種 / Multilingual** | 依序評估：美索不達米亞、古埃及、吠陀與往世書、希臘、瑪雅 / Mesopotamian, Egyptian, Vedic and Puranic, Greek, Maya | 每新增一個語種，同時加入該語言的文檔版本 / each language adds its doc locale |
| **4 宇宙觀 / Cosmology** | 天文與曆法實體（日月出入之山、星宿、天象）與天文回推比對 / astronomical and calendar entities vs retro-calculation | 天文類實體有中等以上可信度的對應 / astronomical entities mapped at medium confidence or better |

**挑選新語料的原則 / Corpus selection**：實體多、關係明確（方位、距離、河流去向、清單）的文本優先；有多個獨立見證本的優先。/ Texts rich in entities and explicit relations first; multiple independent witnesses preferred.
