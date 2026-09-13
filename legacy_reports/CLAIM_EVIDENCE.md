# Claim / evidence table

| Claim | Evidence | Status |
|---|---|---|
| One derived operator H = κ·D − A₆; exact 3-CNOT prep | `contact_dynamics.py` matches our first-principles engine closed forms | **CLOSED** |
| Forces = Coulomb + 0.21 eV H-bond; kT thermal floor | `PHYSICS.md`; chemistry layer, no v4+ overlay | **CLOSED** |
| U/kT ≈ 106.6 on the 11-cell KRAS card | `PREREG_ibm_estimator.json` regime block | **CLOSED** |
| R1 C(1-0) = +0.6805±0.023 vs +0.7421; 3/3 in band | `RESULT_est_20260901_014249.json` job `daaui7bvpcac73dd29r0` | **CLOSED** |
| R2 C(6-7) = −0.4584±0.0076 vs −0.4648; ibm_fez | `RESULT_residue_K2_20260901_104204.json` job `dab6vi34clkc73fij1ig` | **CLOSED** |
| R3 C(28-7) = −0.0757±0.0087 (8.68σ) at d=11; ibm_fez | `RESULT_residue_K6_20260901_131159.json` job `dab7i5mrrl7c7386gfh0` | **CLOSED** |
| K=6 exact classical counterpart is 2⁹⁹ | lightcone size on heavy-hex at depth 6; not an MPS death | **BOUNDED** |
| Dirac KRAS / GCK / CDK2 / ABL PASS G1+G2 | RESULT_response_* job ids in RECEIPTS | **CLOSED** |
| Dirac myosin needs refine (pass-1 G1 FAIL) | pass-1 gap 14%; refine cosine 0.9916 job `6a96c15d…` | **CLOSED** |
| Aquila T0 7/7; strongest 0.66% | RAW + PENDING task ids | **CLOSED** |
| Aquila T1 near/far ratio 1.50 | same RAW, 60 atoms | **CLOSED** |
| Rigetti structure vendor-independent; amplitude not | RESULT_rigetti_final; amplitude gate FAIL | **CLOSED** (negative kept) |
| IonQ Forte cross-vendor quench | `protocol/ionq_quench.py` | **UNRUN** |
| AQT ibex-q1 | `RESULT_aqt_20260904_081407.json` | **RAN / FAIL** |
| IBM K=6 maps for four other targets | `protocol/ibm_four_maps.py` | **UNRUN** |
| SKEMPI +0.51 as a headline | 78-cycle subset only | **DROPPED** |
| Derived pocket-AUC predictor | allosteric_derived_results.json FAIL | **DROPPED** |
| HexaGene / genome-axis / v4+ biology | our first-principles engine distilled these out | **DROPPED** |
