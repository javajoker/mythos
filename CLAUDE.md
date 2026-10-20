# Mythos — project instructions

Mythos tests ancient texts, myths and legends as possible records of real observations, using reproducible methods. The primary sub-project is the Shanhaijing 《山海經》.

## Method: era-semantic correspondence (framework v3.1, global bidirectional scope)
Settings by the initiator (2026-10-20):
- **Origin & Perspective**: Central Plains (Henan, 34.7°N, 113.6°E) as the global center ("中").
- **Global Horizon (4000–1000 BCE)**: Radiating west across Eurasia to North Africa (Egypt, Nile, Red Sea, Sahara, Sumer); east across the Pacific Rim, Beringia, and into the Americas (proto-Olmec, Caral/Norte Chico); north to the Arctic Circle (Polar Night, Aurora / Candle Dragon); south to the Indo-Pacific tropics.
- **Toponym Independence**: Ancient names never presuppose modern toponyms (e.g. ancient 華山 is not assumed to be modern Shaanxi Mount Hua; names are phonetic/descriptive symbols, not modern geographic anchors).
- **Distance-Based Disambiguation (R15)**: Distance is the primary arbiter of homonyms:
  1. **Far-Distance Homonym Split**: Same-name entities located in geographically distant macro-regions are treated as distinct physical entities (e.g., Nile Black Water vs Siberian Black Water vs Sichuan Black Water; Cairo Kunlun vs Silk Road Inland Kunlun).
  2. **Proximate Trans-Book Merge**: Same-name entities in proximate geographic regions across different books are treated as the same entity (e.g., West Mountain Kunlun and Great Wilderness West Kunlun = Cairo Giza; Jianmu in Sea South and Inland = Sanxingdui).
  3. **Dispute Flagging & Forward Pipeline**: Unresolved disputes are documented with explicit notes and logical reasoning hypotheses, allowing the full-book draft to proceed without stalling, to be revisited and audited upon draft completion.
- **Scale Calibration**: High-confidence physical distances calibrate the ancient "里" (initial baseline: Zhou/Qin/Han li ~0.35–0.42 km/li at ~30°–35°N latitude). The Western Mountains total (18,924 里 ≈ 7,570 km) remarkably matches Henan to Cairo (7,534 km), and Eastern Mountains (18,869 里 ≈ 7,547 km) matches the North American longitudinal cordillera (~7,500 km).
- **Phenomenological & Sensory Decoding**: Extreme physical and astronomical phenomena are decoded via sensory reality (e.g. Aurora/Polar Night = 燭龍; Parhelion/Atmospheric Refraction/Solar Posts = 扶桑十日 / Maya E-Groups; Ocean Trenches = 歸墟大壑; Stepped Pyramids/Ziggurats = 崑崙九重之臺).
- **Bidirectional Reconstruction**: Use preserved accounts of now-extinct fauna, vanished river systems (Green Sahara wadis), and altered coastlines to reverse-reconstruct the earth's environment in 4000–1000 BCE.

## Research rules
- **Text first**: Every entity and relation carries entry IDs (e.g. `SHJ-02-3-006`) from `reference/<corpus>/data/entries.jsonl`; quotations are verbatim; commentary never enters analysis.
- **No inherited conclusions**: Prior scholarship is never evidence, input or a candidate source; evaluations are made on masked attribute input and checked for leakage.
- Reading rules R1–R15 (framework §3.1) apply to every candidate alike.
- Commit each finished task.

## Layout
- `docs/`: overall docs (whitepaper and PRD as `zh-Hant`/`en` files; the other docs bilingual inline)
- `reference/<corpus>/`: sources, `data/entries.jsonl`, `text/*.md` (no interpretation)
- `projects/<corpus>/`: spec, era world, data model, tasks, checklist, red-team log, `data/era/` (era world base), `data/derived/` (text layer, `kg/`, later `era/`), `deliverables/draft-vN/`, `findings/F-*`
- `tools/<corpus>/`: standard-library Python; run from the repo root with `python3 -I`
