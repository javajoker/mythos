# -*- coding: utf-8 -*-
"""重校準應用器（adapt-recal 工具，2026-10-29）。

輸入：<slug>-recal-table.json（stations: order/name/lon/lat/region/fit）
動作：
1. <slug>-mappings.jsonl：路站 MTN 記錄的 primary_candidate(name/region/fit)、
   modern_mountain 更新；conflicts 追加校準留痕；grid 刷新自當前 station-grid。
2. <slug>-sentence-analysis.md：章節標題括注 → 新區域名；時代映射表路站行
   （含『（語義擬合站位）』或舊版坐標格）坐標格＋描述格更新；文首追加校準說明。
語義內容（region/fit）全部由 LLM 事先寫入 recal-table；本工具只做結構替換。
"""
import json
import re
import sys
from pathlib import Path

ADJ = Path(__file__).resolve().parents[2] / "projects/shanhaijing/data/derived/era/adaptation"


def main(slug, note):
    tbl = {s['order']: s for s in json.load(open(ADJ / f'{slug}-recal-table.json', encoding='utf-8'))['stations']}
    grid = {}
    for line in open(ADJ / f'{slug}-station-grid.jsonl', encoding='utf-8'):
        r = json.loads(line)
        if 'station' in r:
            grid[r['order']] = r['grid']

    # ── mappings ──
    mp = ADJ / f'{slug}-mappings.jsonl'
    out = []
    n = 0
    for line in open(mp, encoding='utf-8'):
        if not line.strip():
            continue
        r = json.loads(line)
        if 'meta' in r:
            r['meta'] = r['meta'] + f' 【{note}】'
        elif r.get('kind') == 'MTN' and r.get('order') in tbl:
            s = tbl[r['order']]
            pc = r['primary_candidate']
            pc['name'] = s['region']
            pc['fit'] = s['fit']
            r['modern_mountain'] = s['region']
            if r['order'] in grid:
                r['grid'] = grid[r['order']]
            r.setdefault('conflicts', []).append(
                f'{note}；本站落點＝{s["region"]}（{s["lat"]}°N {s["lon"]}°E）')
            n += 1
        out.append(r)
    open(mp, 'w', encoding='utf-8').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in out))

    # ── sentence-analysis ──
    sp = ADJ / f'{slug}-sentence-analysis.md'
    text = sp.read_text(encoding='utf-8')
    lines = text.split('\n')
    order = None
    nh = nr = 0
    outl = []
    for ln in lines:
        m = re.match(rf'^### 【SHJ-\d{{2}}-\d+-(\d{{3}})】', ln)
        if m:
            order = int(m.group(1))
            if order in tbl and '（' in ln and note.split('（')[0] not in ln:
                ln = re.sub(r'（[^（）]*）', f'（{tbl[order]["region"]}——{note}）', ln, count=1)
                nh += 1
            outl.append(ln)
            continue
        if order in tbl and ln.startswith('| MTN:…') and '°N' in ln:
            s = tbl[order]
            cells = ln.split('|')
            if len(cells) >= 7 and ('°N' in cells[4] or 'grid' in cells[4] or '依附' not in cells[4]):
                cells[4] = f' {s["lat"]:.2f}°N {s["lon"]:.2f}°E（{note}站位） '
                cells[5] = f' {s["region"]}；山名：{s["region"]}（{s["fit"].split("；")[0]}） '
                ln = '|'.join(cells)
                nr += 1
        outl.append(ln)
    # 文首追加說明（第二行版本行後）
    for i, ln in enumerate(outl[:8]):
        if ln.startswith('方法：') or ln.startswith('版本：'):
            outl[i] = ln + f'　**【{note}：全鏈逐腿鎖定經文走向（容差錐±22.5°）；今名不作證據；站位詳見 {slug}-adaptation.md 與 {slug}-recal-table.json】**'
            break
    sp.write_text('\n'.join(outl), encoding='utf-8')
    print(f'{slug}: mappings {n} 站更新；sentence-analysis 標題 {nh}、表行 {nr} 更新')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
