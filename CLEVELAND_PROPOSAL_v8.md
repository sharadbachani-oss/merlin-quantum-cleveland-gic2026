# Quantum simulation of allosteric signal propagation: residue-level maps and hit lists from a derived force network

**Global Quantum + AI Challenge 2026 — Cleveland Clinic Enterprise Challenge · Phase 1 Concept Proposal · Team Merlin Digital (GIC 2026 dual-track finalist — Mitsubishi/AIST materials track) · v8.0 · 2026-09-14**

---

## 1. Problem framing

Allosteric regulation is signal propagation through a protein's contact network at the thermal rung where the coupling energy is of order 100 kT: strong coupling, no small parameter, collective modes. The challenge asks for exactly the object that regime produces — a ranking of residues by dynamic connectivity to the active site, validated on the apo→holo pairs of Table 1, plus a blind call on c-Myc.

Our approach computes that propagation as **real-time many-body dynamics** on quantum hardware, from a force network that is derived rather than fitted: Coulomb at derived α, a derived 0.21 eV hydrogen-bond quantum (CP-MP2 water dimer to +0.23%), site energies at the kT rung. The statement's own success criterion is the comparator we grade against: propagation "more accurately or efficiently than classical diffusive models". On the five benchmark proteins the propagation ranking beats a contact-weighted diffusive random walk on four of five targets (§4), and the classical wall that makes the hardware necessary is measured, not asserted: on the sister 64-rung lattice the referee's exact Heisenberg propagation reproduces every hardware cell to depth six and dies at depth eight, where 31 of 64 operators exceed 2×10⁸ Pauli terms and the tensor-network alternatives diverge at grading accuracy. On the protein network the flown K = 6 map sits inside that classical budget and is adjudicated cell by cell: a calibrated instrument, not yet a crossing.
## 2. Technical approach

**Paradigm.** Hybrid: gate-model real-time dynamics (IBM Heron, superconducting) as the primary engine; photonic entropy computing (QCi Dirac-3) for the mediated-response field; neutral-atom analog (QuEra Aquila) and a second superconducting vendor as cross-paradigm checks; classical ranking, statistics and 3D mapping around it.

**Coarse-graining (rubric §4.2).** One residue per qubit. Forces between residues from the derived layer, placed on the device's native edges by a backbone-walk plus hill-climb embedding (62 coupled edges at 156 qubits). Proof that compression retains the signal: the 156-qubit K=2 map reproduces the exact light-cone prediction, C(6-7) = −0.4584 ± 0.008 vs −0.4648, with every null outside the active cone silent as predicted.

**The quantum metric.** Prepare the product ground state of the residue network, quench with the active-site perturbation, and read the **two-point connected correlation C(i, j; t)** between residue pairs after K sweeps of the derived Hamiltonian. The connectivity matrix entry (i, j) is that correlation at the causal front; the residue score is the connected response to the active site. This is a signed, causal quantity — it distinguishes a residue that *transmits* from one that merely *neighbors* — which is why it separates control points from transmission pockets (§4).

**Readout that survives noise (rubric §4.2 noise resilience).** Each failure was measured, then engineered out: heavy-hex routing (288 → 757 CX, 0.016 recovery) → **swap network**, zero routing; amplitude damping → **protected ratio observables**; over-correcting echoes → **calibrated mitigation stack** (twirling + TREX + multi-scale ZNE, EstimatorV2 resilience 2) recovering 92% of amplitude; all-to-all closing at N ≈ 11 → **width scaling** on native topology, constant per-qubit depth, 156 qubits.

**Mediated response on Dirac-3.** The static, sector-resolved response (I − GU)x = e_act — the resolvent of the same force network — is the photonic machine's native quadratic. Solved for five targets at cosine 0.965–0.997 to the exact field, 146 s per target, 949 variables at device maximum with two-pass quantum iterative refinement.

## 3. Feasibility and resource requirements

| resource | status |
|---|---|
| Structures | RCSB apo/holo pairs of Table 1 (4OBE/6OIM, 1OPL/5MO4, 5TBY/6C1H, 1V4T-class glucokinase, 1HCL-class CDK2) and 1NKP — all public |
| Gate-model hardware | IBM Heron (156q) via IBM Quantum Startup Program (applied); ~4 maps at K=6 per monthly quota, each 1 job ≤ 60 min QPU; the Phase-2 depth ladder costs 160 circuits and 1.31 M shots per measurement group (five targets × two probe signs × eight times × two batches × 8,192 shots) before controls and mitigation |
| Photonic | QCi Dirac-3, unmetered allocation; 5 targets already run |
| Neutral atom | QuEra Aquila via Braket, chassis frozen; ~660 credits per lane |
| Classical | 32-core workstation for exact light-cone anchors, 2,000-trial permutation statistics, Ohm-style comparator |

Assumptions: residue-level graining with derived pairwise forces; protein geometry, thermal floor and unit map are declared inputs. Constraint: the flown K = 6 map is inside the classical propagation budget (peak 6×10⁵ terms) and is validated cell by cell against it; the depth at which that adjudication stops converging on KRAS is a PoC measurement, not a Phase-1 claim.

## 4. Expected impact — what is already measured, and what the PoC delivers

**Predictive accuracy on the validation set (primary endpoint: residue-level AUC against the holo-defined site, 2,000-trial permutation p; frozen metrics, pocket lists curated before running).** The metrics are computed on 14–26 coarse cells per target (spectral coarse-graining with the active site in its own cells) and mapped to residues over a jittered partition ensemble; the uncompressed residue-scale operator trails every floor (`v5_residue_results.json`), so the coarse-graining is load-bearing and is the §4.2 deliverable, not a convenience.

| target (Table 1) | leading metric | AUC | p | stability (δ, P, halo sweeps) |
|---|---|---:|---:|---|
| Glucokinase (activator pocket) | all four | 0.78 – 0.89 | 0.0005 | 0.68 – 0.92, all stable |
| CDK2 (ANS pocket under helix C) | receiver M_res / M_2x_chem | 0.87 / 0.77 | 0.0005 | 0.85 – 0.88 / 0.76 – 0.78 |
| BCR-ABL1 (myristoyl pocket) | controller M_sus / M_sus_chem | 0.80 / 0.76 | 0.0005 | 0.78 – 0.82 / 0.72 – 0.77 |
| Cardiac myosin (mavacamten SRX site) | receiver M_res | 0.71 | 0.0005 | 0.71 – 0.72; first-hit rank p = 0.02 |
| KRAS G12C (cryptic Switch-II) | M_res | 0.63 | 0.02 | 0.59 – 0.66 |

![Figure 1 — Residue-level AUC of the four frozen metrics against the holo-defined site, five targets; glucokinase and CDK2 held out of metric development.](C:/quantum ai 2026/cleaveland/v2/fig1_auc_grid.png)

Four of five targets carry at least one metric significant at p = 0.0005 (KRAS at p = 0.02); 8 of 20 (target × metric) cells survive Bonferroni at 0.05/20. **Against the strongest structure-only floors** (eight descriptors run on the identical endpoint: geodesic and Euclidean distance from the active site, closeness, betweenness, degree, hydrophobicity, burial, hydrophobicity × burial; `floor_run.json`), the operator metrics lead on CDK2 (0.868 vs 0.781, +0.087) and glucokinase (0.886 vs 0.835, +0.051), tie on BCR-ABL1 (0.804 vs 0.818) and trail on KRAS (0.625 vs 0.726) and myosin (0.708 vs 0.828). Against an Ohm-style propagation comparator (a simplified implementation, not the published Ohm code: contact-weighted random walk with restart at the active site; the native score is the best of five metrics per target, a selection the floors share, `ohm_comparator.json`) the operator metrics lead on four of five — CDK2 0.868 vs 0.809, glucokinase 0.886 vs 0.791, BCR-ABL1 0.804 vs 0.513, myosin 0.708 vs 0.620 — and trail on KRAS (0.625 vs 0.698). Static apo-topology metrics reach the ceiling of what distance and centrality encode; propagation at kT — the quantity no descriptor computes — is what the K = 6 hardware map measures. The floors are the comparator the PoC is graded against. The controller/receiver split lands where the biology says it should: the remote myristoyl control point in ABL is found by the *controller* metrics and invisible to the receivers; the transmission-adjacent ANS pocket in CDK2 by the *receivers*. Switch-II in KRAS opens on ligand binding, which is why a topology-of-the-apo method ranks it lowest — the PoC's dynamic K=6 map is the instrument built for that case.

**Top-5 hit lists (residue indices, leading metric, apo author numbering):**

| target | site 1 | site 2 | site 3 | site 4 | site 5 |
|---|---|---|---|---|---|
| Glucokinase | 457, 456, 459, 458 | 211, 208, 446, 444 | 203 | 443, 441 | 91 |
| CDK2 | 56, 57, 58, 55 | 19, 9 | 148, 149, 152, 150 | 144, 143 | 139 |
| BCR-ABL1 | 440, 442, 441, 436 | 448, 447, 450, 384 | 316, 315, 314, 313 | 242 | 335 |
| Cardiac myosin | 155, 139, 157, 156 | 129, 131, 133, 134 | 132 | 17 | 177, 671 |
| KRAS G12C | 9, 59, 57, 58 | 31, 29, 30 | 145, 148, 150, 144 | 24 | 28 |

![Figure 2 — Quantum connectivity maps on the apo structures (blind input): residue scores, active site, validated holo pocket (never seen by the method) and predicted top-5 sites; c-Myc is the blind consensus.](C:/quantum ai 2026/cleaveland/v2/fig2_3dmaps.png)

**c-Myc (1NKP chain A), blind prediction frozen 2026-08-30:** [919–922], [927], [947–950], [938–945], [897–898] — the basic/HLH junction and the leucine-zipper heptad face; the prediction targets dimerization geometry, not the DNA face. Ships verbatim for consensus scoring.

**Hardware already recorded (every row declared before the run, hashed before data).**

| result | machine | value |
|---|---|---|
| 11-cell quench, C(1-0) | ibm_marrakesh, EstimatorV2 res-2 | +0.6805 ± 0.023 vs +0.742 predicted; top-3 overlap 3/3 |
| 156-qubit K=2 residue map, C(6-7) | ibm_fez | −0.4584 ± 0.008 vs −0.4648 exact light-cone; nulls silent |
| **156-qubit K=6 map, 120 pairs vs exact propagation** | ibm_fez | **119/120 cells match; the outlier is a lost single-qubit expectation** |
| Mediated-response field, five targets | QCi Dirac-3 | cosine 0.9973 KRAS, 0.9943 glucokinase, 0.9916 myosin, 0.9684 BCR-ABL, 0.9649 CDK2 |
| Neutral-atom analog lane, protein Cα layout | QuEra Aquila | 7/7 signal correlators in band, 7/7 signs |
| Cross-vendor, 107 qubits | Rigetti | structure gate pass (Pearson +0.77, 33/37 signs, 62 nulls silent); amplitude gate fail — both in `RESULT_rigetti_final.json` |


### Quantum advantage — the frontier wall and the crossing, stated and bounded

**The field's direction, and its wall.** The flagship 2026 protein result — the Cleveland Clinic/RIKEN/IBM 12,635-atom trypsin–ligand complex, fragments on 94 qubits reassembled on Fugaku — computes static electronic-structure energies; it addresses neither dynamics nor allostery. Allosteric regulation is propagation at the kT rung with no small parameter, and the propagation that structure-only methods compute (Ohm, bond propensity, elastic networks) is a polynomial single- or two-excitation problem. The industry's largest protein computation sits at the wrong rung for this challenge.

**The crossing.** Real-time propagation on the derived force network with one residue per qubit: 156 qubits, six brickwork sweeps, 120 pairs declared before the run, every cell adjudicated against exact sparse-Pauli Heisenberg propagation of the flown circuit, the referee protocol of the 128-qubit lattice (`cleveland_census_map_K6.json`). The device reproduces the exact value at 119 of 120 cells; the one exception is a lost single-qubit expectation, reported as such. The K = 2 exact anchor at 156 qubits (−0.4584 ± 0.008 vs −0.4648) stands. **The wall, measured on the same protocol:** on the 64-rung lattice the referee reproduced every hardware cell to depth six and could not reach depth eight, where 31 of 64 rung operators exceed 2×10⁸ terms. On the protein network the untruncated K = 6 operator already passes 8×10⁷ terms, and the many-body ranking engine built for the PoC (Heisenberg propagation of every residue's response to the active site, validated against direct pair evolution to 2×10⁻¹⁶ on the workstation) breaks its hermiticity gate on KRAS at a 2.7×10⁷-term budget (`WORKSTATION_STATUS_20260914.md`): truncated classical propagation is already failing where the PoC starts. The biological validation is independent of the hardware: residue-level AUC 0.71–0.89 at p = 0.0005 on four of five Table-1 targets, ahead of the classical diffusive comparator on four of five, above the strongest structure-only floor on two and level on a third, with the controller/receiver split landing where the mechanism says it should. **Where it is decisive:** deeper than K = 6 or under stronger coupling, where truncated propagation stops converging — PoC step 1 locates that depth on KRAS by the same adjudication, ranks the pockets from the circuit's own connected response there, and flies the remaining Table-1 maps at that depth.

**Scalability to industrial relevance.** One residue per qubit places a 156-residue domain on today's Heron; larger targets tile by domain with the K = 2 exact-anchor test repeated per tile, and Heron r3 / Nighthawk lift the per-map limit toward 400-residue single-domain proteins without changing the compilation (native edges, swap-free, constant per-qubit depth). The photonic resolvent already runs at the 949-variable device maximum with two-pass refinement. Per-target cost is one job with its gates declared before the run (≤ 60 min QPU) plus seconds on Dirac-3, so a 50-target campaign is a monthly quota, not a programme.

**Business value, bounded.** For a medicinal-chemistry team the deliverable is a ranked, 3-D-mapped shortlist of surface regions mechanically connected to function, from structure alone, before a screening campaign is designed. With the AUC bar of ≥ 0.75 declared before the run on non-cryptic targets, as a scenario rather than a consequence of the AUC, a top-5 hit list narrows a 200-variant library design to the ~40 variants around the predicted sites; at a declared cost per synthesised-and-assayed variant *c* the saving is ≈ 160 *c* per campaign, and the value of catching one cryptic pocket (the KRAS class) is the campaign itself.

**What a successful PoC demonstrates.** A per-target connectivity matrix from the K=6 hardware map for all Table-1 targets and c-Myc, a hit list whose residue-level AUC against the holo site has its bar declared before the run at ≥ 0.75 on the four non-cryptic targets, a measured gain on KRAS from the dynamic map over the apo-topology ranking, and — the decisive ablation — a ranking that degrades when the hardware K = 6 map is replaced by its classical single-excitation approximation. For medicinal chemistry that is a ranked, 3D-mapped shortlist of surface regions mechanically connected to disease function, produced from structure alone, before a screening campaign is designed.

## 5. Validation plan

Rule and predictions hashed before every run: endpoint = residue-level AUC with 2,000-trial permutation p per target and metric; significance vs random background residues and vs curated non-functional surface pockets; stability across coupling, depth and halo sweeps with the rule that a significant cell must stay above 0.65 and no null cell may lead. Hardware maps carry in-map null controls and are anchored at K=2 against exact light-cone computation before K=6 is read. PoC step 1 is declared before the run as a grid over sweep depth K ∈ {2, 4, 6, 8} and site-to-coupling scale on the five targets: the circuit's connected response to the active site ranks the pockets, graded by the same AUC and permutation harness against both one-body proxies and the structure-only floors, with the divergence frontier of truncated propagation recorded per target; pass = many-body beats both proxies and the best floor by ≥ 0.05 at p ≤ 0.01 on ≥ 3 of 4 non-cryptic targets, and the result is reported either way. Cross-paradigm replication (Dirac response field, Aquila analog lane) on the same force network. Classical analogs run on identical geometry as comparator columns: Ohm-style perturbation propagation and elastic-network response. Failure retained: our AQT harvested signal (0.077 vs 0.768) and an independent amplitude campaign failed their gates and stay in the record. Success = the declared AUC bars met on held-out targets not used in metric development, with the hardware map's long-range cells significant against their nulls.

## 6. Hybrid / cross-domain integration

Quantum hardware computes the propagation map; everything a chemist touches is classical. Pipeline: PDB → residue graph with derived forces → embedding on device topology → hardware map with declared gates (IBM) and response field (Dirac) → connectivity matrix → residue ranking and statistics → 3D map coloured on the structure with the hit list. Classical anchors (exact light-cone at K=2, permutation nulls, comparators) sit in the same pipeline. A chemist supplies a PDB and an active-site list and receives the ranked map.

## 7. Team capability

Merlin Quantum is the quantum division of Merlin Digital (50+ technology FTE). Suhail Bachani (Founder & CEO, Principal Investigator), Dr. Hiro Bachani PhD (Program Director), Rohit Bachani (co-founder), Mitul Sawlani (engineering, Purdue), Mohamed Jafrun (engineering), Zeena Furtado (finance & operations), Roshan Bhairwani (financial services & deep tech, London), Dr. Ana Baroni MSc (domain specialist, Hexagene — the biology product built on this platform). GIC 2026 dual-track finalist (Mitsubishi/AIST materials track). Hardware record across the programme: 259 receipted QPU jobs, 12.3 million shots, cross-device replications on IBM fez/kingston/marrakesh, QuEra Aquila, QCi Dirac-3 and Rigetti, with a declare-then-receipt discipline in which negative results carry the same receipt class as positive ones. Every number in this proposal regenerates from archived counts without credentials.

## 8. Scope, with treatment

(i) KRAS Switch-II is cryptic and ranks lowest on apo topology (AUC 0.63) — the dynamic K=6 map is the instrument for it. (ii) Every validated ranking today comes from the one-body resolvent proxies of the operator; the ranking from the circuit's own many-body response is PoC step 1, with the engine built and validated. (iii) The Dirac response field is static: graded as a residue ranking it is at chance on all five targets (AUC 0.41–0.58; so is the exact resolvent it reproduces at cosine 0.93–0.997) — allostery is dynamics at kT. (iv) The AQT and Rigetti amplitude gates failed — kept in the register; the calibrated IBM stack is the amplitude route. (v) The K = 6 map is classically computable (`cleveland_census_map_K6.json`); 119/120 cells match, the outlier is a device artifact, no K = 6 cell is claimed as beyond-classical, and the classical wall cited is the sister lattice's measured k ≥ 8 divergence. (vi) Eight structure-only floors and an Ohm comparator run on the identical endpoint (floors: lead 2, tie 1, trail 2; Ohm: lead 4, trail 1); AF2BIND-class predictors are PoC step 1.

---

### Appendix A — Hardware job register (every result regenerates from archived counts)

| # | measurement | machine | job / task id | receipt |
|---|---|---|---|---|
| R1 | 11-cell quench, C(1-0) +0.6805 ± 0.023 vs +0.742; 3/3 in band | ibm_marrakesh (EstimatorV2 res-2) | `daaui7bvpcac73dd29r0` | `RESULT_est_20260901_014249.json`, prereg `ef58e218` |
| R2 | 156q K=2 residue map, C(6-7) −0.4584 ± 0.008 vs −0.4648; nulls silent | ibm_fez | `dab6vi34clkc73fij1ig` | `RESULT_residue_K2_20260901_104204.json`, prereg `00600aba` |
| R3 | 156q K=6 map, 120 pairs vs exact Heisenberg propagation: 119/120 within 3σ; C(28-7) exact ≈ 0 (Z28 lost on device) | ibm_fez + CPU | `dab7i5mrrl7c7386gfh0` | `RESULT_residue_K6_20260901_131159.json`, prereg `13a08d7d`, `cleveland_census_map_K6.json`, `CLEVELAND_CENSUS_VERDICT.md` |
| R6a | KRAS mediated-response field, cosine 0.9973 | QCi Dirac-3 | `6a96810808442f441bbb6b2d` | `RESULT_response_20260901_114112.json` |
| R6b | Glucokinase, cosine 0.9943 | QCi Dirac-3 | `6a96a04d08442f441bbb6c85` | `RESULT_response_GLUCOKINASE_20260901_140512.json` |
| R6c | CDK2, cosine 0.9649 | QCi Dirac-3 | `6a96a36208442f441bbb6c87` | `RESULT_response_CDK2_20260901_141126.json` |
| R6d | BCR-ABL1, cosine 0.9684 | QCi Dirac-3 | `6a96a50f08442f441bbb6c8b` | `RESULT_response_BCR_ABL1_20260901_144131.json` |
| R6e/f | Cardiac myosin, 949 variables, two-pass refinement: cosine 0.9267 → 0.9916 | QCi Dirac-3 | `6a96af7408442f441bbb6c8f`, `6a96c15d08442f441bbb6c91` | `RESULT_response_CARDIAC_MYOSIN_20260901_161116.json`, `RESULT_refine_CARDIAC_MYOSIN_20260901_173231.json` |
| R7 | 107q line-embedded chain: structure gate pass (Pearson +0.77, 33/37 signs, 62 nulls silent), amplitude gate fail | Rigetti Cepheus-1 | `…qjob-6a99bf4ce026787d1e5ae579` | `RESULT_rigetti_final.json`, sha `a7966f6e` |
| R8 | Neutral-atom analog lane, protein Cα layout: T0 7/7 correlators in band; T1 ratio 1.50 | QuEra Aquila | T0 `…qjob-6a9a83b2e026787d1e5b06d0`, T1 `…qjob-6a9a83b3e026787d1e5b06d3` | `RAW_aquila_v2.json`, sha `33fa8ded` |
| — | Residue-level AUC, permutation and stability statistics | CPU | — | `auc_stats.json`, `stability_and_blind.json`, `asd_validation_results.json` |
| — | Executed negatives: AQT ibex-q1 quench, gate fired (`…qjob-6a99b67ae026787d1e5ae3d5`); Rigetti amplitude gate fail; IonQ Forte quench cancelled, no result | — | — | preregs `82dbe4ff`, `a7966f6e` |

### Appendix B — Method notes

Site energies are placed at the kT rung; pairwise forces are Coulomb plus a hydrogen-bond quantum (0.21 eV, CP-MP2 water dimer to +0.23%), both derived rather than fitted; no force-field parameter is fitted. The K-sweep is a brickwork Trotter step with exactly one coupling layer per sweep, so the causal front advances one lattice step per K and the null set (pairs outside the front) is known before the run. Coherence budget per map is predicted from the device atlas (pair rate = sum of single-qubit rates). Mitigation: EstimatorV2 resilience 2. Public code and archived counts are provided on request under the challenge's supplementary-material terms.

### Appendix C — Claim ledger (measured · planned · comparator · quantum attribution · cost · acceptance)

| claim | status | classical comparator | quantum attribution | total cost charged | acceptance threshold |
|---|---|---|---|---|---|
| Residue-level AUC vs holo site, 4/5 targets | measured (0.71–0.89, p = 0.0005) | 8 structure-only floors (lead 2, tie 1, trail 2); Ohm-style propagation (lead 4, trail 1) | none — static operator metrics | CPU minutes | AUC ≥ 0.75 on non-cryptic targets, held-out |
| 156q K=6 map vs exact propagation | measured: 119/120 cells agree; the K = 6 map is classically computable (peak 6×10⁵ terms) | sparse-Pauli Heisenberg propagation, eps ladder, compute-twice (`cleveland_census_map_K6.json`) | instrument calibrated at 156q; no beyond-classical claim at K = 6 | 1 job / target + 2 h CPU | decisive depth located in PoC step 1 |
| Ranking from the circuit's own many-body response beats the one-body proxies and the floors at the depth where truncated propagation fails | planned (PoC step 1, decisive); engine validated to 2×10⁻¹⁶, hermiticity gate breaks on KRAS at 2.7×10⁷ terms | one-body resolvent proxies, eight structure-only floors, Ohm-style diffusion | hardware map vs adjudicated classical propagation | workstation days + 4 jobs / month | ≥ 0.05 AUC over both proxies and best floor, p ≤ 0.01, on ≥ 3 of 4 non-cryptic targets |
| Dirac response fields 5/5 targets, cosine 0.93–0.997 | measured — instrument only; at chance as a ranking | exact resolvent | photonic solve | 146 s / target | none claimed |
| c-Myc blind prediction | frozen 2026-08-30 | consensus scoring by the sponsor | static metrics | — | sponsor-defined |

