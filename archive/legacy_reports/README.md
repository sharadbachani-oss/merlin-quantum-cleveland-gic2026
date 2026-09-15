# Merlin Digital — Cleveland Clinic contact-network dynamics

| | |
|---|---|
| **Team** | Merlin Digital |
| **Project** | Derived-operator quench of a molecular contact network on today's hardware |
| **Track** | Cleveland Clinic — KRAS / five catalytic domains |
| **Write-up** | `CLEVELAND_REPORT_v4.md` |
| **Physics** | `PHYSICS.md` — `H = κ·D − A₆` (our first-principles engine L0–L2 + chemistry only) |
| **Prior result** | GIC 2026 — dual-track finalist (Mitsubishi/AIST materials); same operator class |

## The claim in one line

A 156-qubit quench on **ibm_fez** measured a connected correlator
**C(28-7) = −0.0757 ± 0.0087 (8.68σ)** at lattice distance 11 — the causal
frontier of a K=6 native-edge evolution — from a parameter-free force graph
built on `H = κ·D − A₆`. The same derived response quadratic ran on
Dirac-3 for all five challenge targets. Aquila used the molecule's own Cα
coordinates as the atom layout.

This package is **protocol-complete and evidence-honest**. R1–R3 IBM job
ids were recovered from the IBM dashboard by exact evs match. AQT
completed and graded **FAIL**. It is **not** a sendable qBraid zip until
the unmarked IonQ card and the four remaining IBM maps have real RESULT
files (or a written withdrawal). No job id in this tree was invented.

## Verify (CPU, no credentials)

```
pip install -r requirements.txt
python contact_dynamics.py
python verify.py
python figures/generate_figures.py
```

Expected: operator closed forms PASS; R1/R2/R3/R6/R8 headlines PASS;
pending cards stay UNRUN.

## What is in this package

```
CLEVELAND_REPORT_v4.md       technical report
PHYSICS.md                   distilled our first-principles engine operator + chemistry map
RECEIPTS.md                  claim → file → job-id (or UNRUN)
CLAIM_EVIDENCE.md            claim / evidence / status table
HARDWARE_MAPS.md             native maps that ran vs protocol
PROTOCOL_PENDING.md          IonQ + 4 IBM maps — exact cards, unmarked
QUANTUM_ADVANTAGE_EXHIBIT.md advantage class and its bound
CHECKLIST.md                 draft-checklist close-out
contact_dynamics.py             operator + exact prep (numpy)
verify.py                    credential-free audit
protocol/                    unrun flight cards
results/headlines.json       every headline re-derived from RESULT_*
figures/                     fig1–fig4
```

Source artifacts live in `../cleaveland/v2/` (RESULT_*, PREREG_*, RAW_aquila_v2.json).
The package does **not** include HexaGene, genome-axis, or v4+ codon layers.

## What ran vs protocol

| Card | Status | Receipt |
|---|---|---|
| R1 11-cell estimator | RAN | ibm_marrakesh `daaui7bvpcac73dd29r0` |
| R2 156q K=2 | RAN | ibm_fez `dab6vi34clkc73fij1ig` |
| R3 156q K=6 front | RAN | ibm_fez `dab7i5mrrl7c7386gfh0` |
| R6 Dirac-3 ×5 | RAN | five job ids + myosin refine |
| R7 Rigetti 107q | RAN | structure pass; amplitude FAIL |
| R8 Aquila T0/T1 | RAN | two task ids |
| IonQ Forte quench | **UNRUN** | `python protocol/ionq_quench.py fly` |
| AQT ibex-q1 | RAN / FAIL | `…6a99b67ae026787d1e5ae3d5` |
| IBM maps ×4 | **UNRUN** | `python protocol/ibm_four_maps.py fly6 TARGET` |

## Discipline

Pre-registration hashed before flight. Nulls built into the K=6 card.
Noise treated as an instrument (EstimatorV2 res-2; analog empty-site mask).
Advantage of route is bounded: checkable lightcones first, then the
unverified front with silent nulls. Remaining hardware cards are unmarked.
