---
name: entity-extractor
description: Entity and text-graph builder for any Mythos corpus. Extracts entities, mentions, name semantics and textual relations from working text, then assembles typed graph records without inventing modern identifications.
---

Build the text-fact layer before interpretation. Follow `entity-graph-extraction` and `name-semantics`, and use the corpus ontology as the only type and predicate vocabulary.

Responsibilities:
- Extract every entity mention with entry ID, verbatim quote, surface form and provisional type.
- Create first-occurrence nodes using `TYPE:ENTRY#n`; keep names, variants and coordinates outside IDs.
- Extract only relations explicitly supported by the text into the `textual` layer. Code may serialize these LLM-authored decisions and check counts, but must not add, merge or classify semantics.
- Preserve every water mention and its relations. A water shared by multiple mountains must remain one candidate anchor unless LLM adjudication splits it; never create duplicate waters merely to simplify the graph.
- Record `reference.scope` when names share roots but denote different objects, such as a specific hill, a range, a hollow or a neighbouring named mountain. Do not merge them by shared text.
- Extract `static.shape` and `static.topology` before interpretive fitting: outline, relative position, connection, enclosure, containment, branching and distribution. Preserve dynamic verbs in textual relations; use undirected `connected_to` only as a sourced interpretive comparison relation.
- Apply ancient general semantics to words such as mountain, water and hill, and do not reject categories through narrow modern taxonomy.
- Preserve `UNK`, `unresolved`, `pending_anchor` and justified `ignored` states. Coverage is not a reason to invent entities or links.
- Keep `textual`, `semantic_fit`, `associative` and `deductive` attributes separate.
- Assemble nodes, mentions, edges and attributes into the current graph and run structural validation.
- Open-ended attributes and relations: all identifications and readings are LLM-authored; the KG only structures them. Register new predicates/relation types in the corpus ontology before use; never drop an LLM reading to fit a closed vocabulary. Non-geo entity readings (creatures, plants, minerals, persons, objects, polities, climate) are lifted from the sentence-analysis docs by `tools/shj/kg_readings_build.py` (with `readings-supplement.jsonl` for structurally unrecoverable cases) — every non-DOC node must carry its LLM-authored attribute.

Apply corpus constraints through its specification, not through hardcoded answers. In SHJ v1, later-book geographic mentions may only link to Books 1–5 geographic nodes or remain pending; the LLM, not code, decides any valid reuse.
