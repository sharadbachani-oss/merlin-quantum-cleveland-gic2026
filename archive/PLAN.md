# Internal plan — Cleveland → Mitsubishi v4 bar

Written before the package was assembled. Closed items are marked.

## Physics cleanup
- [x] Drop parent derived-operator model v4+ biology (HexaGene l12, genome axes, HRS, codon overlays).
- [x] Re-state the industrial object as a **molecular contact-network quench** of `H = κ·D − A₆` plus the chemistry force layer (Coulomb + 0.21 eV H-bond). kT is the thermal floor, not a “regulation step.”
- [x] Keep residue Cα geometry as analog Hamiltonian (chemistry / molecular layout, not a protein overlay).
- [x] Do not ship pocket-AUC / derived-site-predictor claims (`allosteric_derived_results.json` gate FAIL).

## Checklist close-out
- [x] R1–R3, R6–R8 closed from existing artifacts; numbers re-derived.
- [x] Backend correction: K2/K6 ran on **ibm_fez**, not marrakesh.
- [x] IBM job ids for R1–R3: recovered 2026-09-08 by exact evs match; patched into RESULT JSON.
- [x] IonQ Forte: protocol only, UNRUN; one-command `python protocol/ionq_quench.py fly`.
- [x] Four IBM maps: protocol only, UNRUN; one-command `python protocol/ibm_four_maps.py fly6 TARGET`.
- [x] AQT ibex-q1: harvested COMPLETED, graded **FAIL**.
- [x] Figures generated from headlines.json.

## Packaging
- [x] README, report, receipts, claim/evidence table, hardware map, pending protocols, verify.py.
- [x] Honesty table: SKEMPI +0.51 was a 78-cycle subset; myosin pass-1 G1 failed; Rigetti amplitude failed.

## Not done (requires hardware)
- [ ] IonQ Forte quench RESULT
- [ ] IBM residue K=6 maps for BCR-ABL, myosin, glucokinase, CDK2
- [x] Archive IBM job ids for R1–R3 (stdout-only at flight time → dashboard evs match)
