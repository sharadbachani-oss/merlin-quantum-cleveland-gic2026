# Cleveland K=6 cell C(28-7) — classical census verdict (laptop, 2026-09-14)

Engine and receipts: `cleveland_census.py`, `cleveland_census_ops.json`, `cleveland_census_v1.json`,
`cleveland_census_K2.json`, `cleveland_census_K4.json`, `cleveland_census_K6.json` (eps ladder),
`cleveland_census_K6_probe_budget2e7.json`, logs alongside. Method is the A1 referee's of
2026-08-10: Heisenberg propagation of the observable backward through the flown circuit under an
eps ladder and a term budget.

## Gates passed before any number was read

| gate | result |
|---|---|
| offline rebuild of the flown circuit vs frozen `PREREG_residue_K6.json` | every field reproduced: backend, 156 qubits, K, dt, 62 edges, 3 layers, 2q bound 1116, all 24 active qubits, retained weight 688.6718 vs 688.67, **all 120 pairs identical**, six sweeps bit-identical |
| V1: engine (eps = 0) vs independent light-cone statevector at K = 2 | C = 0 vs −2.2e-16, agreement 2.2e-16 |

## The census

| K | eps | C(28-7) classical | peak terms (Zi / Za / ZiZa) | time |
|---:|---:|---:|---|---:|
| 2 | 0 | 0 exactly | 279 / 14 / 3,906 | s |
| 4 | 3e-5 | +1.74e-5 | 2,032 / 36 / 12,813 | s |
| 4 | 1e-5 | +1.86e-5 | 3,278 / 39 / 21,503 | s |
| 6 | 3e-5 | **+1.28e-4** | 11,917 / 93 / 71,633 | 36 s |
| 6 | 1e-5 | **−3.01e-5** | 22,886 / 136 / 143,687 | 73 s |
| 6 | 0 | not reached here: Zi passed 8.0e7 terms and the laptop could not allocate the next 1.8 GB | — | GPU box job |

**CONVERGES.** At K = 6 the eps ladder brackets C(28-7) = 0 ± 2e-4, with the three underlying
expectations stable to four digits between rungs (⟨Z28⟩ 0.26575 / 0.26571, ⟨Z7⟩ −0.40970 / −0.40969,
⟨Z28 Z7⟩ −0.10875 / −0.10889). The budget was 2e7 on the laptop; the A1 standard 2e8 was never approached
at either truncation. The cell is classically computable in about a minute.

## Against the hardware receipt (ibm_fez `dab7i5mrrl7c7386gfh0`)

| observable | hardware | classical | hw / classical |
|---|---:|---:|---:|
| Z28 | −0.027 ± 0.015 | +0.266 | −0.10 |
| Z7 | −0.369 ± 0.119 | −0.410 | 0.90 |
| Z28 Z7 | −0.066 ± 0.006 | −0.109 | 0.61 |
| **C(28-7)** | **−0.0757 ± 0.0087** | **−0.00003** | (hw − cl)/σ = **−8.7** |

The device tracks Z7 at 0.90 and the pair at 0.61, and has lost Z28 entirely (wrong sign, 20σ). No single
damping factor maps classical to hardware, so the A1 "shape × envelope" reading is unavailable. The
hardware connected value is a noisy pair expectation minus a product that has collapsed to zero on the
device: it is the flat baseline |C| ≈ 0.055 that `floor_cleveland_K6.json` found at every distance
including unreachable pairs. **The 8.7σ the proposal quotes against zero is 8.7σ against the exact answer,
because the exact answer is zero.**

## Verdict

- The K = 6 cell C(28-7) at distance 11 is **not a beyond-classical object**. It is 1.4e5 terms and 73 s.
- The hardware value at that cell is **a device artifact**, not propagation, and the floor already said so.
- The K = 2 anchor (−0.4584 ± 0.008 vs −0.4648) stands; it is the cell the device got right.
- What the proposal must change: the "where it is decisive: past the ~40-qubit exact wall, on the K = 6
  front" sentence. This front is not past a wall. The wall for this circuit family, if any, is deeper
  than K = 6 or needs a different observable; the eps = 0 growth (8e7+ terms at K = 6) says the untruncated
  operator is large, but the truncated one that carries the physics is small, which is what "classically
  easy" means in the A1 protocol.
- What the proposal keeps: the biological validation, which the text already made independent of the
  hardware claim; and the honest structure, which is why this finding costs a sentence and not a track.

## In flight

- `cleveland_census.py map 6 1e-5`: all 120 pre-registered pairs, compute-twice, ~3.5 min/pair on this
  laptop, ~7 h; first 11 pairs: classical |C| ≤ 5e-5, hardware within 0.2σ of classical.
- K = 4, eps = 0 exact leg.
- GPU box: the eps = 0 exact K = 6 run and the full map at box speed (`START_CLEVELAND_CENSUS.md` on G:).

Rule honoured: the cheapest adversary ran first, on the laptop, before any box time. It settled the cell.

## Full map, 120 pairs at K = 6, eps = 1e-5 (laptop, 2 h 5 min, compute-twice throughout)

Receipt `cleveland_census_map_K6.json`, log alongside. Max peak terms over the whole map 611,228, far
under the 2e8 budget. Every pair converged.

| quantity | value |
|---|---:|
| hardware cells within 3σ of their classical value | **119 of 120** |
| the one cell beyond 3σ | **(28-7), d = 11, the proposal's headline cell, z = −8.7** |
| next largest |z| | 2.4 |
| median |z| over the map | 0.34 |
| median classical |C| | 2.1e-5 |
| median hardware |C| | 0.032 |

Hardware |C| by lattice distance: median 0.021 (d 1–5), 0.033 (d 6–10), 0.028 (d 11–15), **0.078 (d 16–25)**,
against classical medians of 1.9e-4, 2.3e-5, 2.7e-5, 1.0e-5. The hardware "front to distance 22" is the
device baseline growing with distance and depth. The 21 pre-registered null pairs are in the map and behave
like every other cell.

**So the whole K = 6 map is classically zero at every distance beyond the short-range cells, the device
reproduces that zero at 119 cells, and the single cell the proposal headlined is the single cell where the
device disagrees with the exact answer, in the direction of device error (Z28 lost).** The map measured the
device baseline, adjudicated pair by pair, and the K = 6 hardware line cannot be stated as decisive anywhere
on this map.
