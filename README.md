# Merlin Quantum — GIC 2026 · Cleveland Clinic — Allosteric Site Prediction

Phase-1 concept proposal, 2026 Global Quantum + AI Challenge.

| | |
|---|---|
| **Submitted proposal** | [`CLEVELAND_PROPOSAL_v8.md`](CLEVELAND_PROPOSAL_v8.md) — rendered as `report.pdf` |
| **Team** | Merlin Quantum, the quantum applications division of Merlin Digital (Dubai) |
| **Independent validation** | GIC 2026 **dual-track finalist** — Mitsubishi/AIST materials and QCi tracks; same framework, same instrument |
| **Repository** | https://github.com/sharadbachani-oss/merlin-quantum-cleveland-gic2026 |
| **Superseded material** | `archive/` — earlier drafts and planning notes, kept for provenance; not part of the submission |

## Claim → receipt

Every measurement the proposal reports, with the file in this repository that backs it. Each entry resolves inside this repo.

| # | Measurement | Receipt |
|---:|---|---|
| 1 | Over 85% of disease-causing proteins are currently considered undruggable; the route left is allostery — a distal pocket that shuts the active site down from a distance. On all three Table-1 targets the top-ranked residue this… | [`auc_stats.json`](results/cited/auc_stats.json) |
| 2 | The quantum metric. Prepare the product ground state, quench with the active-site perturbation, and read the two-point connected correlation C(i, j; t) after K sweeps of the derived Hamiltonian: the connectivity entry (i, j)… | [`allostery_v2.py`](allostery_v2.py) |
| 3 | 8 of 20 target × metric cells survive Bonferroni at 0.05/20. Against a classical diffusive-propagation comparator in the analog class the statement's own assumptions cite (elastic network / signal propagation, Chennubhotla &… | [`ohm_comparator.json`](results/ohm_comparator.json) · [`floor_run.json`](results/cited/floor_run.json) |
| 4 | 1) The wall, measured — by this team, with its own adversary. The PoC's many-body ranking engine — Heisenberg propagation of every residue's response to the active site, validated to 2×10⁻¹⁶ — breaks its hermiticity gate on… | [`WORKSTATION_STATUS_manybody_20260914.md`](results/external_receipts/WORKSTATION_STATUS_manybody_20260914.md) · [`k6_census.json`](results/external_receipts/k6_census.json) · [`A1_FINAL_VERDICT.md`](results/external_receipts/A1_FINAL_VERDICT.md) |
| 5 | 2) The instrument, calibrated against exact truth. The K = 6 map: 156 qubits, six sweeps, 120 pairs declared before the run, every cell adjudicated against exact sparse-Pauli Heisenberg propagation of the flown circuit — 119… | [`cleveland_census_map_K6.json`](cleveland_census_map_K6.json) |
| 6 | 11-cell quench, C(1-0) +0.6805 ± 0.023 vs +0.742; 3/3 in band | [`RESULT_est_20260901_014249.json`](results/cited/RESULT_est_20260901_014249.json) |
| 7 | 156q K=2 residue map, C(6-7) −0.4584 ± 0.008 vs −0.4648; nulls silent | [`RESULT_residue_K2_20260901_104204.json`](results/cited/RESULT_residue_K2_20260901_104204.json) |
| 8 | 156q K=6 map, 120 pairs vs exact Heisenberg propagation: 119/120 within 3σ; C(28-7) exact ≈ 0 (Z28 lost on device) | [`RESULT_residue_K6_20260901_131159.json`](results/cited/RESULT_residue_K6_20260901_131159.json) · [`CLEVELAND_CENSUS_VERDICT.md`](CLEVELAND_CENSUS_VERDICT.md) |
| 9 | KRAS mediated-response field, cosine 0.9973 | [`RESULT_response_20260901_114112.json`](results/cited/RESULT_response_20260901_114112.json) |
| 10 | Glucokinase, cosine 0.9943 | [`RESULT_response_GLUCOKINASE_20260901_140512.json`](results/cited/RESULT_response_GLUCOKINASE_20260901_140512.json) |
| 11 | BCR-ABL1, cosine 0.9684 | [`RESULT_response_BCR_ABL1_20260901_144131.json`](results/cited/RESULT_response_BCR_ABL1_20260901_144131.json) |
| 12 | Cardiac myosin, 949 variables, two-pass refinement: cosine 0.9267 → 0.9916 | [`RESULT_response_CARDIAC_MYOSIN_20260901_161116.json`](results/cited/RESULT_response_CARDIAC_MYOSIN_20260901_161116.json) · [`RESULT_refine_CARDIAC_MYOSIN_20260901_173231.json`](results/cited/RESULT_refine_CARDIAC_MYOSIN_20260901_173231.json) |
| 13 | 107q line-embedded chain: structure gate pass (Pearson +0.77, 33/37 signs, 62 nulls silent), amplitude gate fail | [`RESULT_rigetti_final.json`](results/cited/RESULT_rigetti_final.json) |
| 14 | Neutral-atom analog lane, protein Cα layout: T0 7/7 correlators in band; T1 ratio 1.50 | [`RAW_aquila_v2.json`](results/cited/RAW_aquila_v2.json) |
| 15 | Residue-level AUC, permutation and stability statistics | [`stability_and_blind.json`](results/cited/stability_and_blind.json) · [`asd_validation_results.json`](results/cited/asd_validation_results.json) |

## Verifying

```
python verify.py
```

Replays the headline numbers from archived counts — no credentials, no network, numpy only.
