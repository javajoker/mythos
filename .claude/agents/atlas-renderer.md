---
name: atlas-renderer
description: SVG map renderer for Mythos adaptation packages. Renders per-scroll chain maps and multi-chain overview maps as reviewable SVGs from spec JSON configs. Use after classic-adapter has produced a station grid and mappings, or when producing classic-level / global overview maps.
---

Render SVG maps under `projects/shanhaijing/data/derived/era/adaptation/` from spec JSON files in `specs/`. The spec is the single source of truth — basemap geometry, period-hypothesis features, annotations, modern reference points, legend, panel notes and footers all live in the spec, never only in the SVG.

## Renderers

- Per-scroll chain map: `tools/shj/render_nanci_map.py specs/<slug>-map.json` → `<slug>-map.svg`. Reads `<slug>-station-grid.jsonl`; spec keys: `window`, `anchor_index`, `basemap` (line/blob), `ranges`, `features_extra` (dashed period-hypothesis geometry), `stations_short` (`name` or `name#order` keys for duplicate station names), `legend`, `annotations`, `modern`, `panel_notes`, `footer1/2`, `scale_bar_frac`.
- Overview map (one per classic + one global): `tools/shj/render_overview_map.py specs/<name>-overview.json` → `<name>-overview.svg`. Multi-chain spec: `chains[{grid,label,short,color,anchor_index?,label_pos?,fit?}]`; `fit: true` auto-applies the scroll spec's `fit_coords`. Existing set: `xishan/zhongshan/beishan/dongshan/nanshan-overview` + `wuzang-overview` (26 chains).

## Spec features for divergent arithmetic grids

- `fit_coords` (per-scroll spec): plotting-only coordinate overrides by station order for scrolls whose raw arithmetic grid diverges grossly from the fitted corridor (e.g. beici3 eastward leg layering). The grid file stays arithmetic-only; the divergence must be recorded as a variant in the report and annotated on the map.
- `key_labels` + compact markers: dense station clusters draw r=3 unlabelled dots; only listed orders get name labels.
- Station list panel switches to two columns automatically when the estimated list bottom would exceed the panel.

## Rendering rules

- Coastlines and period waters are simplified schematic geometry — mark this on the map.
- Period hypothesis vs modern reference must be visually distinct (dashed vs solid) and explained in the legend.
- Mountain entries in `stations_short` carry the real modern mountain name (`⛰…` suffix) per the initiator's 2026-10-23 ruling.
- All text must stay inside its bounds: CJK-aware width estimation, wrap or reposition; the built-in overflow audit covers plain-text rows AND `<tspan>` rows (position and width) plus station circles — require zero overflows.
- Scale bar in km with the li conversion at the band's mid value, and a coordinate grid.
- Footer states: total mileage vs measured span fit, hypothesis status, era window, and that vanished waters are not vetoed by modern absence.

## Verification

Re-render from spec, require `overflow: none`, then inspect the SVG visually in the browser (including the right panel bottom edge) before delivery. Commit on completion.
