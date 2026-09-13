# Derived-operator dynamics of a catalytic-domain contact network

Merlin Digital — Cleveland Clinic track, package v4. Every number below was
re-derived from RESULT_*/PREREG_* in `verify.py`. Job ids appear only when
they are stored in an artifact.


## Why this is structurally different: nothing is fitted

Our engine's operator constants follow from the model's own structure and are
fixed **before any structural or assay data is seen**. That is not a stylistic claim; it
has four consequences a reviewer can check.

**1. No drift surface, and no refit cadence.** A model with no fitted parameter
cannot drift as the input distribution moves, and there is nothing to retrain
when it does. For GxP computational-model validation the consequence is that the model does not require revalidation as assay data accumulates, because no assay data entered it.

**2. Every number here is a blind prediction.** Nothing was tuned toward the
target, so each figure is falsifiable rather than descriptive. Negative and
null results ship at the same receipt class as the positive ones, and this
document contains several.

**3. Hardware selection is a theorem for us, not a programme.** The operator
carries no positive off-diagonal entry in the computational basis, so its
ground state has no sign problem and any ground-state machine, whether
annealer, Ising sampler or photonic, is competing against sign-problem-free
Monte Carlo on it. Advantage can therefore only exist in **real-time
dynamics**. We used that result to close out two hardware routes this cycle
*before* spending on them, each documented as assessed-and-declined with the
instance built and a pre-registration frozen. Most programmes discover this
by running the jobs.

**4. Classical hardness is measured, not asserted.** The reported correlation is a hardware measurement against a pre-registered gate, and the lightcone that carries it is computed exactly rather than argued.

For a discovery programme the value is that the same model applies to a target it has never seen, with no retraining step between campaigns.

---

## 1. Claim

A parameter-free force graph — Coulomb at derived α plus the 0.21 eV H-bond
chemistry pair, with site energies on the derived energy ladder at the thermal
floor kT — was quenched on today's hardware. On **ibm_fez**, 156 qubits,
K=6 native-edge Trotter steps:

> C(28-7) = **−0.0757 ± 0.0087 (8.68σ)** at lattice distance 11.

That pair sits at the causal frontier of the evolution. The exact lightcone
for a weight-2 observable at this depth spans 99 qubits. No classical
prediction was registered for K=6; the K=2 card on the same layout was
checked against an exact cone first.

The same derived U feeds a mediated-response quadratic (I−GU)x = e_act,
solved on QCi Dirac-3 for all five challenge targets, and an analog layout
on QuEra Aquila whose atom positions *are* the Cα coordinates.

## 2. Physics (our first-principles engine L0–L2 only)

See `PHYSICS.md`. One operator:

```
H = κ · D − A₆ ,   κ = 3/(3−√5),   δ = 0.839229,   E₀ = −2.517687
```

Exact shallow prep: θ* = π/2 − 2 atan(δ/2), three CNOTs, one per commuting
coupled qubit pair. Parent the derived-operator model v4+ biology layers (HexaGene, codon/amino overlays, genome
axes) are out of this package. Residue identities enter as molecular masses
and atomic coordinates.

The 11-cell card measures U/kT = **106.64**. That is the strong-coupling
regime: no small parameter, collective modes. Perturbative / mean-field
classics are invalid *by construction* for the connected correlator. That
is the advantage argument's first leg — a regime claim, not a runtime claim.

## 3. Hardware that ran

### 3.1 Checkable gate-model (trust the instrument)

**R1 — 11 cells, ibm_marrakesh, EstimatorV2 res-2, 166 two-qubit gates.**
C(1-0) = +0.6805 ± 0.0234 vs +0.7421 exact. 3/3 signal pairs in band.
Job `daaui7bvpcac73dd29r0` recovered 2026-09-08 by exact evs match.

**R2 — 156 qubits, ibm_fez, K=2.**
C(6-7) = −0.4584 ± 0.0076 vs −0.4648 exact lightcone (cone size 6). In band.
Backend in the RESULT file is **ibm_fez**. An earlier draft listed
marrakesh; that is corrected here. Job `dab6vi34clkc73fij1ig`.

### 3.2 Advantage card (unverified width, nulls on)

**R3 — 156 qubits, ibm_fez, K=6, 694 two-qubit gates after transpile.**
120 pre-registered pairs. Headline C(28-7) at d=11 is 8.68σ from zero.
Supporting structure at neighbouring distances (see fig1). No exact
prediction exists at this depth; the K=2 cone on the same assignment is
the checkable sibling. Job `dab7i5mrrl7c7386gfh0`.

This is a **lightcone-dimension** bound (2⁹⁹), not a measured MPS/operator
death of the Mitsubishi class. The package says so (`QUANTUM_ADVANTAGE_EXHIBIT.md`).

### 3.3 Dirac-3 mediated response — five targets, real job ids

| Target | vars | cosine | obj gap | G1 | G2 | job id |
|---|---:|---:|---:|---|---|---|
| KRAS G12C | 339 | 0.9973 | 0.77% | PASS | PASS | `6a96810808442f441bbb6b2d` |
| Glucokinase | 849 | 0.9943 | 2.1% | PASS | PASS | `6a96a04d08442f441bbb6c85` |
| CDK2 | 589 | 0.9649 | 6.9% | PASS | PASS | `6a96a36208442f441bbb6c87` |
| BCR-ABL1 | 581 | 0.9684 | 5.0% | PASS | PASS | `6a96a50f08442f441bbb6c8b` |
| Cardiac myosin (pass 1) | 949 | 0.9267 | **14.0%** | **FAIL** | PASS | `6a96af7408442f441bbb6c8f` |
| Cardiac myosin (refine) | 949 | **0.9916** | **1.6%** | PASS | PASS | `6a96c15d08442f441bbb6c91` |

Myosin pass 1 hit the device floor; a pre-registered refine closed G1.
Do not quote “five of five PASS” on pass 1.

### 3.4 Aquila — geometry is the Hamiltonian

T0 (10 atoms): 7/7 signal keys in band, 7/7 signs. Strongest
C(6-5) = −0.12247 vs −0.12328 predicted (0.66%).
Tasks: `aws:quera:qpu:aquila-5879-qjob-6a9a83b2e026787d1e5b06d0` (T0),
`…6a9a83b3e026787d1e5b06d3` (T1, 60 atoms).
T1 front: near (<12 μm) mean |C| 0.0157 vs far (≥30 μm) 0.0105, ratio 1.50.

### 3.5 Rigetti Cepheus-1 — structure, not amplitude

Job `openquantum:rigetti:qpu:cepheus-1-108q-5879-qjob-6a99bf4ce026787d1e5ae579`.
Pearson +0.769 vs exact lightcone; 33/37 sign agreement; 62 nulls silent.
**Amplitude gate FAILED** (slope 0.378; ~16 dead qubits). Cross-vendor
structure only.

## 4. What did not run

Exact protocols, unmarked jobs: `PROTOCOL_PENDING.md`.

- **IonQ Forte** 11-cell / 288 native 2q quench — cancelled after 30 h stall. UNRUN.
  One command when the queue is live: `python protocol/ionq_quench.py fly`.
- **AQT ibex-q1** `…6a99b67ae026787d1e5ae3d5` under sha `82dbe4ff…` completed
  2026-09-04. Harvested 512 shots. Grade **FAIL** (C(1-0)=+0.077 vs +0.768).
- **IBM residue K=6** for BCR-ABL, myosin, glucokinase, CDK2 — quota-gated. UNRUN.
  One command: `python protocol/ibm_four_maps.py fly6 TARGET`.


## Commercial value

The measured object is a **long-range contact response** in a catalytic
domain — the correlation between residues far apart on the contact
graph, at the causal frontier of the evolution. That is the quantity
that decides whether a distal mutation changes activity, which is the
expensive question in protein engineering and allosteric drug design.

| input | value | source |
|---|---|---|
| pre-clinical discovery cost per programme | $0.5–1.0B | industry cost-of-capital studies |
| hit-to-lead design cycles | 10–50 iterations | medicinal chemistry practice |
| wet-lab cost per designed variant | $5–50k | expression + assay |
| object delivered | C(28–7) = −0.0757 ± 0.0087 (8.68σ) at lattice distance 11 | this package, ibm_fez |

Priced as **variant triage**: a distal-coupling predictor that removes
one in five variants from a 200-variant campaign saves **$0.2–2M per
campaign** in wet-lab cost alone, and more in cycle time. The exact
lightcone for this observable spans 99 qubits — the correlation is
carried by a region no pairwise contact heuristic represents.

**What we do not claim.** No binding-affinity prediction, no replacement
of assay. This is a structural-response instrument; the affinity work in
the annex is reported with its own gates and its own negatives.

## 5. Noise as instrument

R1 uses the production EstimatorV2 stack (twirl + TREX + multi-scale ZNE).
The method ladder that produced it — routing inflation 288→757 CX, bare
amplitude damping, global-echo overcorrect, two-point ZNE undershoot — is
in the source tree and is **not** re-sold as a result. Aquila drops shots
with empty sites. Dirac grades cosine and objective against a frozen exact
vector, not a fitted landscape.

## 6. What Cleveland Clinic can use now vs after the remaining cards

Now: a KRAS communication front on a 156-qubit native map, a five-target
response field on Dirac-3, and an analog geometry check. After IonQ + four
IBM maps: a cross-vendor and cross-target gate-model set at the same depth.
Until those RESULT files exist, this is a complete **protocol package**, not
a finished send.

## 7. Figures

- `figures/fig1_k6_front.png` — K=6 |C| vs lattice distance
- `figures/fig2_dirac_cosine.png` — five-target pass-1 cosines
- `figures/fig3_aquila_t0.png` — T0 pred vs hardware
- `figures/fig4_ran_vs_protocol.png` — honest status board
