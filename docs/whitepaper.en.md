# Mythos Whitepaper: Re-reading the World and Cosmos of Ancient Texts with Falsifiable Methods

> Version 0.1 · 2026-10-19 · [繁體中文](whitepaper.zh-Hant.md)

## Abstract

Much of humanity's earliest writing is now filed under "myth", "legend" or "the strange". Some of it is pure imagination. Some of it may be **real observation in deformed form**: records of geography, species, sky events or historical incidents that lost their original frame of reference after repeated oral retelling, redrawing, recopying and translation. Mythos builds a research method that is **text-first, multi-axis, explicit about error, and falsifiable**, together with a reproducible data pipeline and AI research agents. It puts these texts back, entry by entry, into our current picture of the world (geography, biology, climate, archaeology) and the cosmos (astronomy, calendars) and tests them there.

The first object of study is the **Shanhaijing** 《山海經》 (*Classic of Mountains and Seas*), one of the most "data-shaped" pre-Qin texts. The Five Treasuries of Mountains (五藏山經) record 400+ stations in a fixed format: bearing + distance + mountain + rivers + resources + creatures. The Classics of the Seas and of the Great Wilderness locate hundreds of peoples, gods and landforms by relative position. That structure makes the text unusually amenable to computational testing.

## 1. The problem

1. **Conclusion first.** The traditional commentaries confine the text to the Chinese heartland, and modern "Shanhaijing is world geography" theses do the opposite. Both usually start from the answer and then pick the entries that fit. The chosen entry tends to match on a single feature (say, "human face, beast body" ≈ the Sphinx), while the contradictory information along the rest of the route is ignored.
2. **Non-independent evidence.** One association, reused, gets counted as several corroborations.
3. **Free emendation.** Any distance or bearing that doesn't fit gets declared a "copying error" and changed, so every hypothesis can be made to fit.
4. **Irreproducibility.** The reasoning is scattered across books and articles and can't be re-checked step by step.

## 2. Method overview

The Mythos research framework ([research-framework.md](research-framework.md)) rests on six pillars:

| Pillar | Content |
|---|---|
| **Text & witnesses** | Collect multiple public-domain editions, give every entry a citable ID, and keep variants and commentary, treating commentary only as a *reader's claim* |
| **Structural extraction** | Turn the text into data: stations, bearings, distances, river topology, creature descriptions, minerals, peoples, sky phenomena |
| **Internal consistency** | Use the text to check itself first: leg sums vs. stated totals, river sources and confluences, bearing closure |
| **Multi-axis triangulation** | Geometry fit, hydrological topology, biogeography and migration, minerals, climate, peoples, astronomy, cross-corpus, each scored independently |
| **Error model & correction budget** | Graphic confusion, numeral corruption, displaced slips, picture-to-text, oral drift. Every emendation costs points |
| **Adjudication & publication** | Pre-registration, competing hypotheses, red team, sensitivity analysis, graded conclusions that can be retracted and re-tested |

## 3. Why now

- **The public-domain texts are digitised.** Wikisource carries the common Shanhaijing text, the Sibu Congkan (1470 Chenghua) edition and the Siku Quanshu edition.
- **Global geographic and biological data are open.** DEMs, river networks, GBIF species occurrences and palaeoclimate reconstructions make large-scale fingerprint matching possible.
- **AI agents** can do large volumes of tedious matching inside a strict protocol, leaving people free to judge and adjudicate. Mythos ships purpose-built agents and skills and writes the method as machine-executable checklists.

## 4. Lessons from the first day

The method surfaced two results while the pipeline was still being built:

1. **The common digital text is not "the original".** The Wikisource base text silently relocates many paragraphs of 海內西經, 海內北經 and 海內東經 and inserts sentences, following modern editors such as Yuan Ke. Those are modern conclusions, not source text. Collation against the 1470 Chenghua edition now flags each one ([source assessment](../projects/shanhaijing/docs/source-assessment.md)).
2. **The text can check itself.** Summing the legs of each Mountain-Classic section and comparing the result with the section's own stated total ("凡N山，N里") locates candidate corruptions objectively. For example, the first section of 中山經 has legs adding up to 937 里, while its stated total is 6,670 里.

The first hypothesis dossier, [H-0001](../projects/shanhaijing/hypotheses/H-0001/dossier.md), tests the proposal "Kunlun is in Egypt; the Red Water is the Red Sea; the Black Water is the Nile; the Flowing Sands are the Sahara". It demonstrates the full workflow: pre-registration, whole-corpus accounting, chain fitting, base-rate analysis, competing hypotheses and a graded verdict.

## 5. Scope and roadmap

- **Phase 1**: Shanhaijing. Data pipeline, methodology spec, geometric and hydrological reconstruction of every Mountain-Classic section, and the relative-position network of the Sea and Wilderness classics.
- **Phase 2**: Extract the reusable agents and skills into a common layer (already started). Ingest related Chinese texts (穆天子傳, 淮南子・地形訓, 禹貢, 水經) as cross-corpus evidence.
- **Phase 3**: Extend to texts and myths in other languages: Mesopotamian, Egyptian, Vedic, Greek, the Americas. Each new language adds a documentation locale.

## 6. Non-goals

- No predetermined answer, neither "the Shanhaijing is global geography" nor "the Shanhaijing is only about China".
- Resemblance is not evidence until it has been corrected for base rate and distinctiveness.
- No conclusion is published without a registered hypothesis and its falsifiers.

## 7. Get involved

See the [PRD](prd.en.md), the [conventions](conventions.md) and the Shanhaijing [task list](../projects/shanhaijing/docs/tasks.md).
