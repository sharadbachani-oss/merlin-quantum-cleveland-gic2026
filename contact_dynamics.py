"""
contact_dynamics.py — distilled L0–L2 physics for the Cleveland contact-network
lane. No derived-operator model v4+ overlays (no codon/amino tables, no HexaGene, no genomic axes).

Operator (PHYSICS_LAYER.md):
    N = 6  →  κ = 3/(3−√5)  →  H = κ·D − A₆
Exact shallow prep (QUANTUM_LAYER_RESOLUTION.md):
    χ = atan(δ/2),  θ* = π/2 − 2χ,  3 CNOTs (one per pair).
Chemistry (CHEMISTRY_LAYER.md):
    Coulomb at derived α; H-bond band 0.21 eV (CP-MP2 water-dimer +0.23%);
    kT = 0.0267 eV is the thermal floor, not a regulatory claim.
Site energies: mass-ladder depth M(n) = κ m_P exp(−n·Δs) evaluated at that
thermal floor. Residue identities enter only as molecular masses / atomic
coordinates (chemistry), never as a codon overlay.

    python contact_dynamics.py
"""
from __future__ import annotations

import math

import numpy as np

KAPPA = 3.0 / (3.0 - math.sqrt(5.0))
DELTA = math.sqrt((KAPPA / 2.0) ** 2 + 4.0) - KAPPA / 2.0
CHI = math.atan(DELTA / 2.0)
THETA_STAR = math.pi / 2.0 - 2.0 * CHI
DELTA_S = 0.4862544
M_PLANCK_KG = 2.176434e-8
U_AMU = 1.66053906660e-27
KT_EV = 0.0267
KCAL_PER_EV = 23.0609
KT_KCAL = KT_EV * KCAL_PER_EV
E_HB_EV = 0.21
E_HB_KCAL = E_HB_EV * KCAL_PER_EV
KC = 332.0637

RES_MASS = {
    "GLY": 57.05, "ALA": 71.08, "SER": 87.08, "PRO": 97.12, "VAL": 99.13,
    "THR": 101.10, "CYS": 103.14, "LEU": 113.16, "ILE": 113.16, "ASN": 114.10,
    "ASP": 115.09, "GLN": 128.13, "LYS": 128.17, "GLU": 129.12, "MET": 131.19,
    "HIS": 137.14, "PHE": 147.18, "ARG": 156.19, "TYR": 163.18, "TRP": 186.21,
}
_MEANM = float(np.mean(list(RES_MASS.values())))


def assemble_operator():
    """64×64 H = κ·D − A₆. A₆ = Σ Xᵢ; D = Σ ½(I − Zᵢ Zᵢ₊₃) in the cell basis."""
    dim = 64
    a6 = np.zeros((dim, dim))
    for s in range(dim):
        for b in range(6):
            a6[s, s ^ (1 << b)] = 1.0
    d = np.diag([bin((s & 7) ^ (s >> 3)).count("1") for s in range(dim)]).astype(float)
    return KAPPA * d - a6, a6, d


def exact_prep_spec():
    return {
        "kappa": KAPPA,
        "delta": DELTA,
        "chi": CHI,
        "theta_star": THETA_STAR,
        "cnots": 3,
        "circuit": "per pair: RY(θ*)–CNOT–H⊗H on (r, r+3)",
        "E0": -3.0 * DELTA,
        "gap": DELTA,
    }


def mass_ladder_depth(name3):
    m = RES_MASS.get(name3, _MEANM) * U_AMU
    return float(np.log(KAPPA * M_PLANCK_KG / m) / DELTA_S)


def site_energies_thermal(names):
    """Site energies at the chemistry thermal floor (kT). No biology label."""
    dep = np.array([mass_ladder_depth(n) for n in names])
    dep = dep - dep.min()
    if np.ptp(dep) > 0:
        dep = dep / np.ptp(dep) * KT_KCAL
    return dep


def main():
    w, a6, _ = assemble_operator()
    ev = np.linalg.eigvalsh(w)
    spec = exact_prep_spec()
    print("H = mu* . D - A6")
    print(f"  mu*         {spec['kappa']:.12f}")
    print(f"  |E(A6)|     {int(a6.sum()/2)}")
    print(f"  E0          {ev[0]:+.9f}   closed form {spec['E0']:+.9f}")
    print(f"  gap delta   {ev[1]-ev[0]:.9f}   closed form {spec['gap']:.9f}")
    print(f"  theta*      {spec['theta_star']:.9f}   chi = atan(delta/2)")
    print(f"  prep        per-pair RY(theta*)-CNOT-H x H  ({spec['cnots']} CNOTs)")
    print(f"  kT floor    {KT_EV} eV = {KT_KCAL:.4f} kcal/mol  (thermal, not regulatory)")
    print(f"  H-bond      {E_HB_EV} eV = {E_HB_KCAL:.2f} kcal/mol  (chemistry pair)")
    assert abs(ev[0] - spec["E0"]) < 1e-9
    assert abs((ev[1] - ev[0]) - spec["gap"]) < 1e-9
    print("PASS  operator + exact-prep closed forms")


if __name__ == "__main__":
    main()
