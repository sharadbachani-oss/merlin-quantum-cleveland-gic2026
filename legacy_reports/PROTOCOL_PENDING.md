# Pending hardware cards — exact protocol, unmarked jobs

Do not fill a job id, a significance, or a PASS/FAIL on any *unrun* card
until a RESULT JSON exists. Recovered IBM ids below were matched to
existing RESULT evs. AQT now has a RESULT (grade FAIL). IonQ and the
four IBM maps stay UNRUN.

## 1. IonQ Forte quench — still UNRUN

File: `protocol/ionq_quench.py`

| Field | Frozen value |
|---|---|
| Status | **UNRUN** |
| Device | `openquantum:ionq:qpu:forte-1` |
| Prereg sha | `82dbe4fffcf3add24c161609af97c0e8f841d88651c2036b786b33f9990d3013` |
| Circuit | 11-cell swap-network quench, **288 native 2q**, all-to-all, zero routing |
| Shots | 512 |
| Observable | C(i,a) from counts, same pairs as R1 / PREREG_quantum_allostery |
| Grade | \|C − pred\| ≤ 3/√S + 0.03; PASS if ≥70% signal in band **and** top-3 overlap ≥ 2 |
| Job id | *none* (cancelled PENDING ids are not results) |

**One command** (paid; do not run unless you intend to submit):

```
python protocol/ionq_quench.py fly
```

That forces `QALLO_ROUTES=openquantum:ionq:qpu:forte-1` and `QALLO_SHOTS=512`.
After the device returns counts:

```
python protocol/ionq_quench.py harvest PENDING_ionq_<UTC>.json
python ..\cleaveland\v2\quantum_allostery.py grade RESULT_ionq_*.json
```

Cancelled IonQ PENDING ids (no counts; keep UNRUN):
`…6a95dfa5…67c7`, `…6a95e1c7…67d4`, `…6a95e3e7…67ef`.

Do **not** treat the AQT result as IonQ data.

## 2. AQT ibex-q1 — harvested, FAIL

Not a pending card anymore. Artifact:
`results/RESULT_aqt_20260904_081407.json` (copy also in `../cleaveland/v2/`).

| Field | Value |
|---|---|
| Status | **RAN / FAIL** |
| Job id | `openquantum:aqt:qpu:ibex-q1-5879-qjob-6a99b67ae026787d1e5ae3d5` |
| Shots | 512 (449 bitstrings) |
| C(1-0) | +0.077 vs pred +0.768 (either endian) |
| Signal in band | 1/3 |
| Top-3 overlap | 0 |
| Verdict | **FAIL** — amplitude collapsed; structure not recovered |

## 3. Four IBM residue K=6 maps — still UNRUN

File: `protocol/ibm_four_maps.py`

| Field | Frozen value |
|---|---|
| Status | **UNRUN** |
| Targets | BCR_ABL1 (1OPL A 242–531), CARDIAC_MYOSIN (5TBY A), GLUCOKINASE (1V4T A), CDK2 (1HCL A) |
| K, dt, shots | 6, 1.00, 4096 |
| Assignment seed | 21 |
| Embed | anneal residue→qubit maximizing \|U\| on native edges; **zero routing** |
| Ops | RZ(2 dᵢ dt) per used qubit; RXX(2 Uᵢⱼ dt) on used native edges only |
| Resilience | EstimatorV2 level 2 |
| Allowed backends | ibm_fez, ibm_marrakesh, ibm_kingston |
| Per-qubit 2q cap | 54 |
| Observable | C(i, active) vs lattice distance; report-mode (no cone prediction) |
| Job id | *none per target* |

**One command per target** (paid; do not run unless you intend to submit):

```
python protocol/ibm_four_maps.py freeze6 BCR_ABL1
python protocol/ibm_four_maps.py fly6 BCR_ABL1
python protocol/ibm_four_maps.py report6 BCR_ABL1 PATH
```

Repeat with `CARDIAC_MYOSIN`, `GLUCOKINASE`, `CDK2`.
`freeze6` writes `PREREG_residue_K6_<TARGET>.json` and restores the KRAS
K=6 prereg. `fly6` writes `job_id` into `RESULT_residue_K6_<TARGET>_*.json`.
GCK/CDK2 are registered via `asd_validation`. PDBs live in `../cleaveland/v2/pdb/`.

## 4. How a card moves from UNRUN to CLOSED

1. Freeze (hash circuit + grade rule + backend name).
2. Fly. Save job id.
3. Grade against the frozen file only.
4. Append a row to `RECEIPTS.md` and flip the status in `CHECKLIST.md`.
5. Re-run `python verify.py`. If a number appeared without a RESULT file,
   the audit must fail.
