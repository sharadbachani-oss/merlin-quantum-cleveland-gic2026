# Distilled physics — what this package is allowed to use

first-principles (`C:\first-principles`) keeps derived-operator model **v2/v3 + chemistry** and stops before v4+
biology overlays (codon / amino / genomic / HexaGene). Cleveland's earlier
drafts used that parent stack. This package replaces it.

## Operator (one derived Hamiltonian)

```
A1. Square = {V,S,T,C}          A2. 3 space + 3 time  →  N = 6
n_cells = 64                    n_types = C(6,3) = 20
structural spectral gap = 3 − √5            κ = 3/(3−√5) ≈ 3.927
H = κ · D − A₆
```

Closed forms (recomputed in `contact_dynamics.py`, match `PHYSICS_LAYER.md`):

| Quantity | Value |
|---|---|
| E₀ | −3δ = −2.517687 |
| gap δ | 0.839229 |
| kinetic edges \|E(A₆)\| | 192 |
| exact prep | χ = atan(δ/2); θ* = π/2 − 2χ; **3 CNOTs** |

Native 6-qubit spelling:

```
H = (κ/2)(I − Z₀Z₃ + I − Z₁Z₄ + I − Z₂Z₅) − (X₀+…+X₅)
```

The three pairs commute. Ground-state prep is exact (not Trotter).

## Chemistry layer (forces, not a protein overlay)

From `CHEMISTRY_LAYER.md`, biology labels stripped:

| Rung | Energy | Role here |
|---|---|---|
| Covalent | 13.6 eV | not used (bonds held) |
| Working quantum | 0.30 eV | not used |
| H-bond / recognition | **0.21 eV** | pair term in Uᵢⱼ (CP-MP2 water dimer +0.23%) |
| Thermal floor | **0.0267 eV = kT** | site-energy scale |

Uᵢⱼ is Coulomb at derived α plus the H-bond term, evaluated on **real atomic
coordinates**. Residue names enter as molecular masses and atom lists.
That is chemistry. It is not a codon table and not HexaGene `l12()`.

Site energies sit on the derived energy ladder `M(n) = κ m_P exp(−n · Δs)` and are
rescaled to the thermal floor. The earlier phrase “regulation step” is
dropped.

## How the industrial object maps onto the operator

The Cleveland brief asks for distant control of a catalytic site. This
package does **not** answer that with a v4 protein overlay. It answers
with three hardware-native readings of the same derived force graph:

1. **Gate-model quench** — one residue / one qubit, native-edge RXX only,
   connected correlator C(i, a) = ⟨ZᵢZₐ⟩ − ⟨Zᵢ⟩⟨Zₐ⟩. Noise is the
   EstimatorV2 instrument (twirl + TREX + ZNE).
2. **Photonic quadratic** — (I − GU)x = e_act on Dirac-3, the mediated
   response of the same U.
3. **Analog geometry** — Cα coordinates become the Aquila register;
   the machine's 1/r⁶ interaction *is* the Hamiltonian.

Allostery, in this write-up, means **that correlator front** — a physical
observable of a strongly coupled molecular network (U/kT ≈ 106.6 on the
11-cell card). It does not mean a genomic or HexaGene claim.

## What was removed

| Dropped | Why |
|---|---|
| HexaGene `l12()` 20×20 amino table | v4+ overlay |
| Genome / HRS / atlas-axis campaigns | biology layers first-principles distilled out |
| Pocket-AUC “derived predictor” | `allosteric_derived_results.json` gate FAIL |
| “Protein thinks / biology regulates” framing | not L0–L2 vocabulary |
| SKEMPI ρ = +0.51 as a headline | 78-cycle subset; full 213-cycle signed ρ = +0.342 |

## What stays open in the physics

Rung-to-chain shift 0.0215 (hardware-measured, no closed form) — inherited
from first-principles, not a Cleveland-specific fit.
