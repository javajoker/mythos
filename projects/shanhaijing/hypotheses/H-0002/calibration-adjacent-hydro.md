Two-anchor calibration — anchors `anchors-yellow-yangtze.jsonl` (basis: hydrological role); 4000 Monte Carlo runs, seed 1.

| section | from → to | legs | path 里 | displacement 里 | text bearing | real km | real bearing | bearing residual | implied 里 (m) | 90% range (m) | 里 if path = distance (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 北次三經 | 謁戾之山 → 發鳩之山 | 3 | 800 | 583 | 31° | 95 | 152° | 121° | 162 | 112–232 | 118 |
| 北次三經 | 發鳩之山 → 少山 | 1 | 120 | 120 | 45° | 163 | 27° | 18° | 1360 | 826–2258 | 1360 |
| 北次三經 | 少山 → 泰戲之山 | 11 | 1990 | 1937 | 4° | 202 | 7° | 3° | 104 | 87–120 | 101 |
| 西次四經 | 白於之山 → 涇谷之山 | 2 | 355 | 341 | 308° | 238 | 218° | 90° | 699 | 445–1057 | 671 |
| 西次四經 | 涇谷之山 → 鳥鼠同穴之山 | 6 | 1450 | 1450 | 270° | 209 | 257° | 13° | 144 | 113–175 | 144 |

- pairs: 5; mean bearing residual **49°** (no-information expectation 90°); P(mean ≤ observed | no information) = **0.0396**; permutation test (shuffle which real place goes with which station) p = **0.0316**
- implied 里 length: median **162 m**, range 104–1360 m (plausible band 250–600 m)
