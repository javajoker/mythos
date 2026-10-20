# Mythos — project instructions

Mythos tests ancient texts, myths and legends as possible records of real observations, using reproducible methods. The primary sub-project is the Shanhaijing 《山海經》.

## Method: era-semantic correspondence (framework v3.1, global bidirectional scope)
Settings by the initiator (2026-10-20):
- **Origin & Perspective**: Central Plains (Henan, 34.7°N, 113.6°E) as the global center ("中").
- **Global Horizon (4000–1000 BCE)**: Radiating west across Eurasia to North Africa (Egypt, Nile, Red Sea, Sahara, Sumer); east across the Pacific Rim, Beringia, and into the Americas (proto-Olmec, Caral/Norte Chico); north to the Arctic Circle (Polar Night, Aurora / Candle Dragon); south to the Indo-Pacific tropics.
- **Toponym Independence**: Ancient names never presuppose modern toponyms (e.g. ancient 華山 is not assumed to be modern Shaanxi Mount Hua; names are phonetic/descriptive symbols, not modern geographic anchors).
- **Scale Calibration**: High-confidence physical distances calibrate the ancient "里" (initial baseline: Zhou/Qin/Han li ~0.35–0.42 km/li at ~30°–35°N latitude). The Western Mountains total (18,924 里 ≈ 7,570 km) remarkably matches the geodesic distance from Henan to Cairo (7,532 km) along the 30°–35°N Golden Latitude Belt.
- **Phenomenological & Sensory Decoding**: Extreme physical and astronomical phenomena are decoded via sensory reality (e.g. Aurora/Polar Night = 燭龍; Parhelion/Atmospheric Refraction/Solar Posts = 扶桑十日; Ocean Trenches = 歸墟大壑; Stepped Pyramids/Ziggurats = 崑崙九重之臺).
- **Bidirectional Reconstruction**: Use preserved accounts of now-extinct fauna, vanished river systems (Green Sahara wadis), and altered coastlines to reverse-reconstruct the earth's environment in 4000–1000 BCE.
- **AI Reasoning over Hardcoded Scripts**: Perform semantic correlation matching, candidate generation, and cross-validation through structured LLM reasoning and attribute vectors rather than rigid local python heuristics.

## Research rules
- **Text first**: Every entity and relation carries entry IDs (e.g. `SHJ-02-3-006`) from `reference/<corpus>/data/entries.jsonl`; quotations are verbatim; commentary never enters analysis.
- **No inherited conclusions**: Prior scholarship is never evidence, input or a candidate source; evaluations are made on masked attribute input and checked for leakage.
- **The era base is committed before scoring**; later changes need a stated reason and a full re-run. Never tune a weight toward a desired answer; any rule or weight change is general and applies to the whole book and every candidate.
- Reading rules R1–R14 (framework §3.1) apply to every candidate alike; test a reading as a held configuration against rivals.
- Be direct about results, including when the evidence is insufficient or contradicts the user's own hypothesis. Never cite a tentative mapping as a finding.
- The Shanhaijing base text contains modern paragraph relocations; follow the 1470 Chenghua (`sbck`) order (`projects/shanhaijing/docs/source-assessment.md`).
- Commit each finished task.

## Layout
- `docs/`: overall docs (whitepaper and PRD as `zh-Hant`/`en` files; the other docs bilingual inline)
- `reference/<corpus>/`: sources, `data/entries.jsonl`, `text/*.md` (no interpretation)
- `projects/<corpus>/`: spec, era world, data model, tasks, checklist, red-team log, `data/era/` (era world base), `data/derived/` (text layer, `kg/`, later `era/`), `deliverables/draft-vN/`, `findings/F-*`
- `tools/<corpus>/`: standard-library Python; run from the repo root with `python3 -I`
- `.claude/agents`: textual-critic, entity-extractor, semantic-matcher, civilization-scout, palaeo-geographer, cross-validator, devils-advocate (common); shj-lead
- `.claude/skills`: source-ingest, witness-collation, entity-graph-extraction, era-world-modelling, name-semantics, observer-frame, semantic-correlation-matching, transmission-error-tolerance, graph-cross-validation (common); shj-era-mapping

## Languages
Docs are in Traditional Chinese and English. When a corpus in a new language is added, add that language per `docs/conventions.md` §1. Never convert quotations to simplified characters or normalise variant glyphs.
