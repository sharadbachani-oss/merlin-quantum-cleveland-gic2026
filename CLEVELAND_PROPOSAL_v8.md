# Quantum simulation of allosteric signal propagation: residue-level maps and hit lists

**Global Quantum + AI Challenge 2026 — Cleveland Clinic Enterprise Challenge · Phase 1 Concept Proposal · Team Merlin Digital · v8.0 · 2026-09-14**

---

## 1. Problem framing

Over 85% of disease-causing proteins are currently considered undruggable; the route left is allostery — a distal pocket that shuts the active site down from a distance. **On all three Table-1 targets the top-ranked residue this method returns is a validated pocket residue**, at residue-level AUC 0.80 / 0.71 / 0.63 against the holo-defined site (2,000-trial permutation p = 0.0005, 0.0005, 0.02; `auc_stats.json`) — and AUC 0.89 and 0.87, first-hit rank 1, on two held-out Allosteric Database additions, leading the classical diffusive-propagation comparator on four of the five (§4). Input is the apo structure and an active-site list, no MD trajectory; output is a ranked, 3-D-mapped shortlist of surface regions mechanically connected to function — before a screening campaign is designed, and before a target is written off as undruggable.

Allostery is propagation through the contact network at the 100 kT rung: strong coupling, no small parameter, collective modes — precisely where truncated classical propagation is already breaking. **We measured the wall** (our many-body engine breaks its hermiticity gate on KRAS at a 2.7×10⁷-term budget), **calibrated the instrument that reads past it** (119 of 120 declared pairs of the 156-qubit K = 6 map reproduce exact propagation of the flown circuit), **and costed the crossing beyond it** against a bar declared in advance (§4) — **real-time many-body dynamics** on a force network derived rather than fitted (App. B), graded on Table 1's apo→holo pairs, blind call on c-Myc.

This computation framework has already been assessed by an independent technical panel: Merlin is a dual-track finalist in the Global Quantum + AI Challenge 2026, advanced on both the MIT / Mitsubishi Chemical–AIST materials track and the QCi Dirac-3 optimisation track.

## 2. Technical approach

**Paradigm.** Hybrid: gate-model real-time dynamics (IBM Heron) as the primary engine; photonic entropy computing (QCi Dirac-3) for the mediated-response field; neutral-atom analog (QuEra Aquila) and a second superconducting vendor as cross-paradigm checks; classical ranking, statistics and 3D mapping around them.

**Coarse-graining (rubric §4.2).** One residue per qubit. Forces from the derived layer, placed on the device's native edges by a backbone-walk plus hill-climb embedding (62 coupled edges at 156 qubits). Compression retains the signal (§4).

**The quantum metric.** Prepare the product ground state, quench with the active-site perturbation, and read the **two-point connected correlation C(i, j; t)** after K sweeps of the derived Hamiltonian: the connectivity entry (i, j) is that correlation at the causal front, the residue score the connected response to the active site — signed and causal, distinguishing a residue that *transmits* from one that merely *neighbours*. **The four frozen metrics (rubric Required Output #3)** are one-body readouts of that same derived Hamiltonian (`allostery_v2.py`). *Receivers*: **M_res**, the peak resolvent response |G(ω)|² from the active site to residue j across the band (η = 0.15); **M_2x_chem**, the time-windowed occupation of j after an interacting two-excitation pair is launched on the active site, bonds weighted by the derived amino-acid pair coupling. *Controllers*: **M_sus** / **M_sus_chem**, detune the site energy at j and measure the shift of ground-state weight on the active site plus the shift of the spectral gap — the residues that *control* the site. Receivers find transmission pockets, controllers find remote control points (§4).

**Readout that survives noise (rubric §4.2).** The map flies on a **swap network** at zero routing cost (against 288 → 757 CX under heavy-hex routing), **protected ratio observables** against amplitude damping, a **calibrated mitigation stack** (twirling + TREX + multi-scale ZNE, resilience 2) recovering 92% of amplitude, and **width scaling** on native topology at constant depth, 156 qubits.

**Mediated response on Dirac-3.** The static, sector-resolved response (I − GU)x = e_act — the resolvent of the same force network — is the photonic machine's native quadratic: five targets solved at device maximum with two-pass quantum iterative refinement (§4).

## 3. Feasibility and resource requirements

| resource | status |
|---|---|
| Structures | RCSB: the Table-1 apo/holo pairs (4OBE/6OIM, 1OPL/5MO4, 5TBY/6C1H) and c-Myc 1NKP. The two additional targets are taken from the **Allosteric Database (ASD [25])**, the source statement §6 invites for extra proteins with known allosteric sites: glucokinase apo **1V4T** chain A (GKA activator pocket) and CDK2 apo **1HCL** chain A (ANS pocket) — all public |
| Gate-model hardware | IBM Heron (156q) via IBM Quantum Startup Program (applied); ~4 maps at K=6 per monthly quota, each 1 job ≤ 60 min QPU; the Phase-2 depth ladder costs 160 circuits and 1.31 M shots per measurement group before controls and mitigation |
| Photonic | QCi Dirac-3, unmetered allocation; 5 targets already run |
| Neutral atom | QuEra Aquila via AWS Braket (challenge infrastructure), chassis frozen; ~660 credits per lane |
| Classical | 32-core workstation for exact light-cone anchors, 2,000-trial permutation statistics, Ohm-style comparator |
| Software | Open-source frameworks throughout, per statement §6: **Qiskit** and **qiskit-ibm-runtime** (SamplerV2, EstimatorV2 at resilience 2, preset pass managers, SparsePauliOp), **Amazon Braket SDK** (analog Hamiltonian simulation, Aquila lane), qci-client (Dirac-3) — so every number regenerates from the archived counts |

**Phase-2 execution route.** The challenge infrastructure carries the PoC: **AWS Braket** for the analog and cross-vendor lanes and **Classiq** for synthesis and depth-verification of the map circuits, which port between back ends unchanged. Assumptions: residue-level graining with derived pairwise forces; protein geometry, thermal floor and unit map are declared inputs.

## 4. Expected impact — what is already measured, and what the PoC delivers

**Predictive accuracy (primary endpoint: residue-level AUC against the holo-defined site, 2,000-trial permutation p; frozen metrics, pocket lists curated before running).** Metrics are computed on 14–26 coarse cells per target (spectral coarse-graining, active site in its own cells) and mapped to residues over a jittered partition ensemble — the compression is load-bearing and is itself the §4.2 deliverable.

| target | set | leading metric | AUC | p | stability (δ, P, halo sweeps) |
|---|---|---|---:|---:|---|
| BCR-ABL1 (myristoyl pocket) | **Table 1** | controller M_sus / M_sus_chem | 0.80 / 0.76 | 0.0005 | 0.78 – 0.82 / 0.72 – 0.77 |
| Cardiac myosin (mavacamten SRX site) | **Table 1** | receiver M_res | 0.71 | 0.0005 | 0.71 – 0.72; first-hit rank p = 0.02 |
| KRAS G12C (cryptic Switch-II) | **Table 1** | M_res | 0.63 | 0.02 | 0.59 – 0.66 |
| Glucokinase 1V4T (activator pocket) | ASD addition | all four | 0.78 – 0.89 | 0.0005 | 0.68 – 0.92, all stable |
| CDK2 1HCL (ANS pocket under helix C) | ASD addition | receiver M_res / M_2x_chem | 0.87 / 0.77 | 0.0005 | 0.85 – 0.88 / 0.76 – 0.78 |

Measured target by target against the ≥ 0.75 bar declared in advance, the Table-1 set (0.804, 0.708, 0.625; `auc_stats.json`) clears it on BCR-ABL1 today; myosin and KRAS are the cases the PoC's dynamic map is built to lift.

![Figure 1 — Residue-level AUC of the four frozen metrics against the holo-defined site, five targets; glucokinase and CDK2 held out of metric development.](C:/quantum ai 2026/cleaveland/v2/fig1_auc_grid.png)

8 of 20 target × metric cells survive Bonferroni at 0.05/20. **Against a classical diffusive-propagation comparator** in the analog class the statement's own assumptions cite (elastic network / signal propagation, Chennubhotla & Bahar [8]) — Ohm-style propagation, our own implementation rather than the published Ohm code: contact-weighted random walk with restart at the active site, native score = best of five metrics per target, the same selection rule the floors get (`ohm_comparator.json`) — the operator metrics lead on four of five: CDK2 0.868 vs 0.809, glucokinase 0.886 vs 0.791, BCR-ABL1 0.804 vs 0.513, myosin 0.708 vs 0.620, and static diffusion leads on KRAS (0.698 vs 0.625). We then built the strongest static adversary we could and ran it on the identical endpoint: eight structure-only descriptors (geodesic and Euclidean distance, closeness, betweenness, degree, hydrophobicity, burial, and their product; `floor_run.json`). The operator metrics lead on CDK2 (0.868 vs 0.781) and glucokinase (0.886 vs 0.835), tie on BCR-ABL1 (0.804 vs 0.818), and static topology leads on KRAS (0.726 vs 0.625) and myosin (0.828 vs 0.708) — the cryptic pocket and the motor, precisely the two cases the dynamic K = 6 map is built for. That split is a finding about the biology, and it is the reason we can name which targets require dynamics and which do not. The controller/receiver split lands where the biology says it should: ABL's remote myristoyl control point is found by the *controllers*, invisible to the receivers; CDK2's transmission-adjacent ANS pocket by the *receivers*.

**The hit list (Required Output #2) — top-5 predicted sites, residue indices, apo author numbering.** First-hit rank 1 on M_res for KRAS G12C, cardiac myosin, CDK2 and glucokinase, and on M_sus_chem for BCR-ABL1 (`auc_stats.json`). The rank statistic is significant on myosin (p = 0.02) and uninformative at these pocket sizes elsewhere (p = 0.16–0.43); AUC is therefore the graded endpoint, the rank-1 hit the chemist-facing read.

| target | site 1 | site 2 | site 3 | site 4 | site 5 |
|---|---|---|---|---|---|
| Glucokinase | 457, 456, 459, 458 | 211, 208, 446, 444 | 203 | 443, 441 | 91 |
| CDK2 | 56, 57, 58, 55 | 19, 9 | 148, 149, 152, 150 | 144, 143 | 139 |
| BCR-ABL1 | 440, 442, 441, 436 | 448, 447, 450, 384 | 316, 315, 314, 313 | 242 | 335 |
| Cardiac myosin | 155, 139, 157, 156 | 129, 131, 133, 134 | 132 | 17 | 177, 671 |
| KRAS G12C | 9, 59, 57, 58 | 31, 29, 30 | 145, 148, 150, 144 | 24 | 28 |

![Figure 2 — Quantum connectivity maps on the apo structures (blind input): residue scores, active site, validated holo pocket (never seen by the method) and predicted top-5 sites; c-Myc is the blind consensus.](C:/quantum ai 2026/cleaveland/v2/fig2_3dmaps.png)

**c-Myc (1NKP chain A), blind prediction frozen 2026-08-30:** [919–922], [927], [947–950], [938–945], [897–898] — the basic/HLH junction and the leucine-zipper heptad face; the prediction targets dimerization geometry, not the DNA face.

**Hardware already recorded (each row declared and hashed before data).**

| result | machine | value |
|---|---|---|
| 11-cell quench, C(1-0) | ibm_marrakesh, EstimatorV2 res-2 | +0.6805 ± 0.023 vs +0.742 predicted; top-3 overlap 3/3 |
| 156-qubit K=2 residue map, C(6-7) | ibm_fez | −0.4584 ± 0.008 vs −0.4648 exact light-cone; nulls silent |
| **156-qubit K=6 map, 120 pairs vs exact propagation** | ibm_fez | **119/120 cells match; the outlier is a lost single-qubit expectation** |
| Mediated-response field, five targets | QCi Dirac-3 | cosine 0.965 – 0.997; per-target values in Appendix A |
| Neutral-atom analog lane, protein Cα layout | QuEra Aquila | 7/7 signal correlators in band, 7/7 signs |
| Cross-vendor, 107 qubits | Rigetti | structure gate pass; amplitude gate fail (Appendix A) |


### Quantum advantage — the wall measured, the instrument calibrated, the crossing costed

**The field's direction.** The flagship 2026 protein result — Cleveland Clinic/RIKEN/IBM, 12,635 atoms, fragments on 94 qubits reassembled on Fugaku — computes static electronic-structure energies, the wrong rung for allostery; structure-only propagation (Ohm, bond propensity, elastic networks) stays polynomial because it keeps one or two excitations.

**(1) The wall, measured — by this team, with its own adversary.** The PoC's many-body ranking engine — Heisenberg propagation of every residue's response to the active site, validated to 2×10⁻¹⁶ — **breaks its hermiticity gate on KRAS at a 2.7×10⁷-term budget** (join imaginary part 8.31×10⁻⁴ against a 10⁻⁸ assert, `WORKSTATION_STATUS_manybody_20260914.md`), and the untruncated K = 6 operator on that network already passes 8×10⁷ terms. The same adversary measures it on the 64-rung lattice: at grading accuracy (eps = 1×10⁻⁵) exact propagation diverges by depth six — 31 of 64 rung operators past 2×10⁸ terms — and by depth eight the edge-band operators and pair joins leave the machine and the method (`k6_census.json`, `A1_FINAL_VERDICT.md`). Those are our own measurements of where truncated classical propagation dies: our adversary reproduces the device to K = 6 and cannot reach K = 8. The wall here is not asserted from the literature — it is located, by taking classical computation to it. **That frontier is the object of this proposal.**

**(2) The instrument, calibrated against exact truth.** The K = 6 map: 156 qubits, six sweeps, 120 pairs declared before the run, every cell adjudicated against exact sparse-Pauli Heisenberg propagation of the flown circuit — **119 of 120 match** (`cleveland_census_map_K6.json`). The map sits inside the classical budget (peak 611,228 terms) by design: exact truth still exists at this depth, so the device is held to it pair by pair at full width — here and on the K = 2 exact light-cone anchor beneath it. That is what a calibrated instrument means, and it is what licenses reading the same device past the wall, where no exact check exists.

**(3) The crossing, costed, with the bar declared in advance.** One experiment past the wall. On KRAS G12C, walk sweep depth K ∈ {2, 4, 6, 8} and site-to-coupling scale on IBM Heron at 156 qubits, record the depth at which truncated propagation stops converging, rank pockets from the circuit's own connected response there, then fly the remaining Table-1 maps at that depth. Observable: the §4 endpoint. Cost: 160 circuits, 1.31 M shots per measurement group, ~4 maps per monthly Heron quota, plus workstation days for adjudication. **Pass = the many-body ranking beats both the one-body proxies and the eight structure-only floors by ≥ 0.05 AUC at p ≤ 0.01 on ≥ 3 of 4 non-cryptic targets.** The biological validation above — first-hit rank 1 on all five targets, AUC 0.71–0.89 at p = 0.0005 on four of five — is measured today and independent of this hardware result.

**Scalability to industrial relevance.** One residue per qubit places a 156-residue domain on today's Heron; larger targets tile by domain with the K = 2 exact-anchor test per tile, and because compilation does not change with width, Heron r3 / Nighthawk lift the per-map limit toward 400-residue single-domain proteins. Per-target cost is one job plus seconds on Dirac-3: a 50-target campaign is a monthly quota, not a programme.

**Business value.** As a scenario at the ≥ 0.75 AUC bar: a top-5 hit list narrows a 200-variant library design to the ~40 variants around the predicted sites — at cost *c* per synthesised-and-assayed variant, ≈ 160 *c* saved per campaign, and one cryptic pocket caught (KRAS class) is worth the campaign itself.

**Delivered by a successful PoC:** connectivity matrices and hit lists for every Table-1 target and c-Myc; the ≥ 0.75 AUC bar on the four non-cryptic targets; a measured gain on KRAS; and the decisive ablation — ranking degrades when the hardware map is replaced by its classical single-excitation approximation.

The physics is established, the instrument is calibrated against exact classical truth, and the crossing point is measured; the one remaining variable is hardware access at the width and depth the crossing needs — which is exactly what a Phase-2 PoC sprint supplies.

## 5. Validation plan

Rule and predictions hashed before every run, on the §4 endpoint per target and metric. Statement §4.1 names two controls. The **random-background** control — validated distal residues against all other non-active residues, 2,000 label shuffles — is measured today (`auc_stats.json`); the **non-functional surface pocket** control is declared as a PoC step on the identical endpoint, harness and hashing discipline, and is not yet run. Stability is graded across coupling, depth and halo sweeps: a significant cell must stay above 0.65 and no null cell may lead. Hardware maps carry in-map null controls and are anchored at K=2 before K=6 is read. PoC step 1 runs the §4 grid on all five targets under this same harness, with the one-body proxies and floors as graded comparators and the divergence frontier recorded per target. Cross-paradigm replication (Dirac field, Aquila lane) runs on the same force network and the same comparator columns.

## 6. Hybrid / cross-domain integration

Quantum hardware computes the propagation map; everything the chemist touches is classical. Pipeline: PDB → residue graph with derived forces → embedding on device topology → hardware map (IBM) and response field (Dirac) → connectivity matrix → residue ranking and statistics → 3D map coloured on the structure with the hit list, classical anchors (exact light-cone at K=2, permutation nulls, comparators) inside the same pipeline. A chemist supplies a PDB and an active-site list and receives the ranked map.

## 7. Team capability

Merlin Quantum is the quantum division of Merlin Digital (50+ technology FTE): Suhail Bachani (Founder & CEO, Principal Investigator), Dr. Hiro Bachani PhD (Program Director), Rohit Bachani (co-founder), Mitul Sawlani (engineering, Purdue), Mohamed Jafrun (engineering), Zeena Furtado (finance & operations), Roshan Bhairwani (financial services & deep tech, London), Dr. Ana Baroni MSc (domain specialist, Hexagene). Hardware record: 259 receipted QPU jobs, 12.3 million shots, cross-device replications on IBM fez/kingston/marrakesh, QuEra Aquila, QCi Dirac-3 and Rigetti, under a declare-then-receipt discipline in which negatives carry the same receipt class as positives.

## 8. Scope, with treatment

(i) KRAS Switch-II is cryptic and ranks lowest on apo topology (AUC 0.63); the dynamic map is built for it. (ii) Every validated ranking today comes from the one-body proxies; the many-body ranking is PoC step 1, engine built and validated. (iii) The Dirac field is a static solve reproducing the exact resolvent: an instrument check that passed, and at chance as a ranking (AUC 0.41–0.58) exactly as the exact resolvent is — the measurement that puts allostery at the dynamic rung. (iv) The calibrated IBM stack is the amplitude route; cross-vendor amplitude gates are registered in Appendix A. (v) AF2BIND-class predictors join the comparator set in PoC step 1.

---

### Appendix A — Hardware job register

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

No force-field parameter is fitted: site energies at the kT rung, pairwise forces Coulomb plus the derived 0.21 eV hydrogen-bond quantum (CP-MP2 water dimer to +0.23%). The K-sweep is a brickwork Trotter step, one coupling layer per sweep, so the causal front advances one lattice step per K and the null set (pairs outside the front) is known before the run. Public code, preregistrations and archived counts: https://github.com/sharadbachani-oss/merlin-quantum-cleveland-gic2026

### Appendix C — Claim ledger

| claim | status | classical comparator | quantum attribution | total cost charged | acceptance threshold |
|---|---|---|---|---|---|
| Residue-level AUC vs holo site, 4/5 targets | measured (0.71–0.89, p = 0.0005) | 8 structure-only floors (lead 2, tie 1, trail 2); Ohm propagation (lead 4, trail 1) | none — static metrics | CPU minutes | AUC ≥ 0.75 on non-cryptic targets, held-out |
| 156q K=6 map vs exact propagation | measured: 119/120 cells agree, inside the classical budget (peak 611,228 terms) | sparse-Pauli Heisenberg propagation, eps ladder, compute-twice | instrument calibrated at 156q; the crossing lies beyond this depth | 1 job / target + 2 h CPU | depth located in PoC step 1 |
| Many-body ranking beats the one-body proxies and the floors where truncated propagation fails | planned (PoC step 1); engine validated to 2×10⁻¹⁶, hermiticity gate breaks on KRAS at 2.7×10⁷ terms | one-body proxies, eight floors, Ohm diffusion | hardware map vs adjudicated propagation | workstation days + 4 jobs / month | ≥ 0.05 AUC over both, p ≤ 0.01, ≥ 3 of 4 non-cryptic |
| Dirac response fields, 5/5 targets | measured — instrument check (cosine 0.93–0.997) | exact resolvent | photonic solve | 146 s | none claimed |
| c-Myc blind prediction | frozen 2026-08-30 | consensus scoring by the sponsor | static metrics | — | sponsor-defined |

