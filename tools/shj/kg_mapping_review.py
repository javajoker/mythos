"""Render the LLM-authored Wuzang mapping groups into a human review report.

The report only formats the groups and coverage summary; it does not choose,
rank or alter any candidate.
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ERA = ROOT / "projects/shanhaijing/data/derived/era"
REVIEW = ROOT / "projects/shanhaijing/data/derived/review"


def read_jsonl(path):
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def main():
    groups = read_jsonl(ERA / "mapping-groups.jsonl")
    water = read_jsonl(ERA / "water-mappings.jsonl")
    mountains = read_jsonl(ERA / "mountain-mappings.jsonl")
    counts = Counter(record["mapping_group"] for record in water + mountains)
    status_counts = Counter(record["mapping_status"] for record in water + mountains)
    lines = [
        "# 五臧山經山水現實世界首輪映射審核 / Wuzang Mountain and Water Mapping Review",
        "",
        "本報告只呈現 LLM 映射判斷與覆蓋結果。所有候選仍需逐組審核；`proposed_pending_review` 不是確認，`unresolved_aggregate` 是刻意不虛構坐標。",
        "",
        f"- 水體節點：{len(water)} / 452",
        f"- 山體節點：{len(mountains)} / 488",
        f"- 狀態：{dict(sorted(status_counts.items()))}",
        "",
        "每個節點至少有三個競爭候選，並保留改道、消亡、遺址、沼澤化或未知狀態。",
        "",
        "| 組 / Group | 狀態 / Status | 覆蓋節點 / Nodes | A 候選 | B 候選 | C 候選 | LLM 理由 / Reason |",
        "|---|---|---:|---|---|---|---|",
    ]
    for group in groups:
        candidates = group["candidates"]
        names = [candidate["name"] for candidate in candidates[:3]]
        lines.append(f"| {group['id']} — {group['target']} | {group['status']} | {counts[group['id']]} | "
                     f"{names[0]} | {names[1]} | {names[2]} | {group['reason']} |")
    lines += [
        "",
        "## 審核規則",
        "",
        "1. 先審水體映射，再校準山體與其他錨點。",
        "2. 同名或共享詞根不直接合併；河段、支流、消失部分與替代名稱保持分層。",
        "3. 每個組可接受、替換、要求補證、聯合初始化、暫停或否決；否決時保留理由與反例。",
        "4. 聚合統計類（天下名山、小山、出水之山等）不虛構坐標。",
        "5. 機器只檢查覆蓋、結構與一致性；語義接受與否由 LLM 和項目發起人決定。",
    ]
    REVIEW.mkdir(parents=True, exist_ok=True)
    (REVIEW / "mapping-review.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"groups={len(groups)} water={len(water)} mountains={len(mountains)}")


if __name__ == "__main__":
    main()
