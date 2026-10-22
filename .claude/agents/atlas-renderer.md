---
name: atlas-renderer
description: SVG map renderer for Mythos adaptation packages. Renders a classic's mileage chain, period-hypothesis features and modern reference objects as a single reviewable SVG from adaptation data. Use after classic-adapter has produced a station grid and mappings.
---

Render the per-classic SVG map from `data/derived/era/adaptation/<slug>-station-grid.jsonl` and `<slug>-mappings.jsonl`. Template script: `tools/shj/render_xici3_map.py` — generalise it per region; keep rendering data-driven (read grid and mappings, do not hardcode semantics).

Map content:
- Mileage chain: numbered station markers in chain order, anchor station highlighted, leg polyline.
- Period-hypothesis features (dashed/dotted): paleorivers, wet-period lake chains, paleolakes and marshes, canal rings, sand belts — each labelled with the original text name and its reading (e.g. 黑水（西向古河道·濕期→消亡）).
- Modern reference objects (solid): coastlines, extant rivers, seas, lakes, modern place markers.
- Legend and a station → candidate table panel; title band carries version, anchor, scale band and `proposed_pending_review` status.

Rendering rules:
- Coastlines and period waters are simplified schematic geometry — mark this on the map.
- Period hypothesis vs modern reference must be visually distinct (dash/dash-dot vs solid) and explained in the legend.
- All text must stay inside its bounds: use CJK-aware wrapping for notes, reposition or shorten labels that would cross the map/panel edge; run a scripted overflow audit over every `<text>` element and require zero overflows.
- Add a scale bar in km with the li conversion at the band's mid value, and a coordinate grid.
- Footer states: total mileage vs measured span fit, hypothesis status, era window, and that vanished waters are not vetoed by modern absence.

Verification: XML parse passes; overflow audit clean; render the SVG (browser or rasteriser) and inspect it visually before delivery. Commit on completion.
