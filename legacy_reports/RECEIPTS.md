# RECEIPTS — claim → file → job-id

Hardware claims require a job id **stored in an artifact**. R1–R3 ids were
recovered 2026-09-08 from IBM Runtime by exact `evs` match (see
`results/ibm_r1_r3_jobs.json`). Unrun cards say **UNRUN**. Failed harvested
cards say **FAIL**. Nothing in this table was invented.

Source tree: `../cleaveland/v2/`. Compact re-derivation: `results/headlines.json`.

## Operator

| Claim | Artifact | Receipt |
|---|---|---|
| H = κ·D − A₆; E₀ = −2.517687; δ = 0.839229; 3-CNOT prep | `contact_dynamics.py` | CPU closed form |

## Ran

| # | Claim | Artifact | Machine | Job / task id |
|---|---|---|---|---|
| R1 | C(1-0) = +0.6805±0.0234 vs +0.7421; 3/3 in band | `RESULT_est_20260901_014249.json` sha `ef58e218…` | ibm_marrakesh | `daaui7bvpcac73dd29r0` |
| R2 | C(6-7) = −0.4584±0.0076 vs −0.4648 cone | `RESULT_residue_K2_20260901_104204.json` sha `00600aba…` | **ibm_fez** | `dab6vi34clkc73fij1ig` |
| R3 | C(28-7) = −0.0757±0.0087 (8.68σ) at d=11 | `RESULT_residue_K6_20260901_131159.json` sha `13a08d7d…` | **ibm_fez** | `dab7i5mrrl7c7386gfh0` |
| R6a | KRAS cosine 0.9973 | `RESULT_response_20260901_114112.json` | Dirac-3 | `6a96810808442f441bbb6b2d` |
| R6b | Glucokinase 0.9943 | `RESULT_response_GLUCOKINASE_20260901_140512.json` | Dirac-3 | `6a96a04d08442f441bbb6c85` |
| R6c | CDK2 0.9649 | `RESULT_response_CDK2_20260901_141126.json` | Dirac-3 | `6a96a36208442f441bbb6c87` |
| R6d | BCR-ABL 0.9684 | `RESULT_response_BCR_ABL1_20260901_144131.json` | Dirac-3 | `6a96a50f08442f441bbb6c8b` |
| R6e | Myosin pass-1 0.9267, G1 FAIL | `RESULT_response_CARDIAC_MYOSIN_20260901_161116.json` | Dirac-3 | `6a96af7408442f441bbb6c8f` |
| R6f | Myosin refine 0.9916, gap 1.6% | `RESULT_refine_CARDIAC_MYOSIN_20260901_173231.json` | Dirac-3 | `6a96c15d08442f441bbb6c91` |
| R7 | Rigetti structure +0.769; amplitude FAIL | `RESULT_rigetti_final.json` sha `a7966f6e…` | Cepheus-1-108q | `openquantum:rigetti:qpu:cepheus-1-108q-5879-qjob-6a99bf4ce026787d1e5ae579` |
| R8 | Aquila T0 7/7; T1 ratio 1.50 | `RAW_aquila_v2.json` / `PENDING_aquilav2_20260904_123916.json` sha `33fa8ded…` | Aquila | T0 `aws:quera:qpu:aquila-5879-qjob-6a9a83b2e026787d1e5b06d0` · T1 `…6a9a83b3e026787d1e5b06d3` |

## Unrun / harvested-fail

| Card | Protocol | Status | Id |
|---|---|---|---|
| IonQ Forte 288-2q quench | `protocol/ionq_quench.py fly` | **UNRUN** | cancelled PENDING only; no RESULT |
| AQT ibex-q1 | same prereg sha `82dbe4ff…` | **RAN / FAIL** | `openquantum:aqt:qpu:ibex-q1-5879-qjob-6a99b67ae026787d1e5ae3d5` |
| IBM K=6 × BCR-ABL, myosin, GCK, CDK2 | `protocol/ibm_four_maps.py fly6 TARGET` | **UNRUN** | none |

## Corrections vs the 2026-09-04 draft dossier

| Draft said | Artifact says |
|---|---|
| R2/R3 on ibm_marrakesh | RESULT JSON `backend: ibm_fez` |
| IonQ Forte queued as R5 | PENDING file is **AQT ibex-q1**; IonQ cancelled. AQT later COMPLETED and graded **FAIL** |
| SKEMPI ρ = +0.51 | 78-cycle subset; 213-cycle signed ρ = +0.342 |
| Five Dirac targets PASS | myosin pass-1 **G1 FAIL**; refine closed it |
| Derived pocket AUC as a claim | `allosteric_derived_results.json` **FAIL** — not claimed |
