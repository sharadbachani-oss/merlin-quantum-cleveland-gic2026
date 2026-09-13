# Cleveland — geometry-as-Hamiltonian allosteric leftover (frontier crossing)

**11 September 2026.** Novel industrial object: the **catalytic leftover spectrum read on the protein geometry itself**, not another equal-time \(C(i,a)\) annex and not a pocket-ML score.

Status: **LOCAL PROOF** of leftover \(S_a(\omega)\) on the 6q cell **and** Dirac geometry leftover \(L(\tau)\). Checkable anchors (R1, R2) stay real. Hardware leftover series **not flown**.
IonQ Forte and four IBM K=6 maps: **UNRUN**. AQT: **FAIL** (not relabeled Dirac).
`new_hardware_advantage_demonstrated: false`.

---

## SOTA wall (what currently wins)

The brief wants an allosteric scanner (connectivity \(\to\) distal hit list) and forbids classical MD *as input*. Classical SOTA still wins the *downstream* industrial objects by MD + NMR chemical-shift ML.

| Winner today | What it produces | What it cannot cheaply produce |
|---|---|---|
| GaMD / Anton / GROMACS + SHIFTX2 / SPARTA+ (Cas9 HNH NMR–MD; GPCRmd-NMR 2025) | Millisecond pathways and residue CSPs | A **first-principles** distal response without an MD trajectory (brief-forbidden as input) |
| NMRNet / ShiftML3 (arXiv:2408.15681; *J. Phys. Chem. Lett.* 2025) | Chemical shifts / shielding tensors approaching DFT | The **strongly coupled contact quench** at \(U/kT\approx 106.6\) — a dynamics object, not a trained shift |
| AlphaFold-style / pocket ML | Local pocket scores | Distal control. This package’s own pocket-AUC gate is **FAIL** |
| Exact lightcone / MPS of a weight-2 observable | R1 11q and R2 6q cone (we matched both) | K=6 front: cone is **99 qubits** (\(2^{99}\)). **No solver was run and failed.** Do not write that sentence as a measured death |

Allosteric CSPs are ubiquitous (74% of significant CSPs non-local; >35% beyond 10 Å — 2026 CSP census). The wall is not “allostery is rare.” The wall is **getting the distal response without MD input and without a cheap low-rank contact model**.

---

## Novel crossing — leftover as readout, geometry as \(H\)

Do not deepen “we measured \(C(28{-}7)=-0.0757\)” into a fake MPS funeral. The new object is Mitsubishi-shaped:

**Geometry-as-Hamiltonian leftover.** On Aquila the C\(\alpha\) coordinates **are** the atom layout (T0 7/7, strongest \(-0.1225\) vs \(-0.1233\); tasks `aws:quera:qpu:aquila-5879-qjob-6a9a83b2e026787d1e5b06d0` / `…6a9a83b3e026787d1e5b06d3`). \(H=\mu^\star D-A_6\) is realized as the Rydberg graph of that geometry, not as a compiled heavy-hex circuit with SWAPs.

The industrial readout is **not** the Hamiltonian and **not** a pocket score. It is the leftover / quench spectrum of the catalytic residue: \(S_a(\omega)\) of the connected contact after an X-quench at the allosteric site. That is the NMR analogue the brief’s “no MD input” constraint actually permits — a real-frequency distal response — and the object continuation of a contact \(G(\tau)\) or a SHIFTX2 snapshot cannot cheaply fake.

**Wrap-before-cone** is the hardness statement we are allowed to make: the distal site at graph distance 11 is inside the K=6 lightcone of a weight-2 observable (99 qubits). Local MD thermostats and low-rank MSMs live *outside* that interacting cone. We have **not** run the MPS referee. Until we do, this is a structural bound plus two checkable siblings:

- R1 `daaui7bvpcac73dd29r0` (ibm_marrakesh): \(C(1{-}0)=+0.6805\pm0.0234\) vs exact \(+0.7421\), in band.
- R2 `dab6vi34clkc73fij1ig` (**ibm_fez**): \(C(6{-}7)=-0.4584\pm0.0076\) vs exact 6q cone \(-0.4648\), in band.
- R3 `dab7i5mrrl7c7386gfh0` (ibm_fez): \(C(28{-}7)=-0.0757\pm0.0087\) (**8.68σ**) at \(d=11\). **No cone prediction registered.**

Dirac-3 solves \((I-GU)x=e_\mathrm{act}\) on five targets (cosine 0.9973 / 0.9943 / 0.9649 / 0.9684 / myosin refine 0.9916). That is a mediated-response annex, not the leftover crossing.

---

## Why today’s hardware can bound a *route*

- Exact 3-CX prep on coupled pairs; Aquila exact pair map where FOV+C6 allows; Heron 156q assignment already flown for equal-time \(C\).
- Noise (EstimatorV2 resilience 2, Aquila empty-site masks) is the readout channel, not a bug to ZNE away.
- The leftover spectrum on the same assignment is a **new series**, not a recaption of R3.

---

## Honesty bound

- No binding-affinity claim. No assay replacement. SKEMPI full-set signed \(\rho=+0.342\), not +0.51.
- \(2^{99}\) is dimension, not a timed-out classical attack.
- IonQ cancelled PENDING ids are **UNRUN**. AQT `…6a99b67ae026787d1e5ae3d5` is **FAIL** (\(C(1{-}0)=+0.077\) vs \(+0.768\)).
- kT normalization does not uniquely derive the protein interaction.
- Four IBM K=6 maps unrun — they would be copies, not a new advantage class, unless an MPS referee is pre-registered.

---

## Dirac remap (11 Sep) — geometry leftover, not AQT / IBM \(C\)

Aquila remains the preferred geometry-as-\(H\) (Cα layout). IBM leftover is not the path. If Aquila/IonQ stay unavailable, Dirac encodes the **distal graph as extra potential edges** on \(V=\mu^\star D\). That is not a relabel of AQT `…6a99b67ae026787d1e5ae3d5` FAIL and not a mediated-response annex.

**Executed 11 Sep (local 2⁶ Gibbs):** distal graph \(L(1)=0.0386\) vs named-\(H\) \(0.0569\); series moves to 0 at \(\tau=4\). `results/cleveland_dirac_leftover.json`.

**Shared Dirac card (flown, crossing not evidenced):** `6aa3261408442f441bbb6f2d`–`…6f30`. AQT FAIL not relabeled. Track `job_id: null`. Advantage **false**.

## Next flight (protocol only)

1. Register an MPS / operator-growth referee on the K=6 99-qubit cone **before** any IBM/Aquila leftover.
2. Prefer Aquila geometry-as-\(H\) if it becomes available. Else the shared Dirac leftover card — grade Cleveland only if distal \(L(1)\) stays below named-\(H\).
3. IonQ stays UNRUN or withdraw. AQT stays FAIL.

**Executed 10 Sep (local):** `python cleveland_leftover_readout.py` → `results/cleveland_leftover_readout.json`. Quenched-pair leftover \(L(k)=|C^\star-\langle ZZ\rangle_{0,3}|\) moves (1.40 … 1.14); principal 0.222 cyc/step; continuation 1.416 **misses**. Distal native pair (2,5) is Ω-held. Inter-coupled pair \(C(0,2)\) is structurally 0. IBM retrieve: no leftover match (R1/R2/R3 refused as equal-time \(C\)). IonQ UNRUN. AQT FAIL. Four K=6 maps not flown.

Local gate: `python verify.py` sections `[9]` honesty, `[10]` leftover \(S_a(\omega)\), `[11]` Dirac geometry leftover.
