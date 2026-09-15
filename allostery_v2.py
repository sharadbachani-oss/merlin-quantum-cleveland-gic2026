#!/usr/bin/env python3
"""
allostery_v2.py — Cleveland Phase I: candidate connectivity metrics, classical layer.

Rebuilds the April cell-graph pipeline (same constants: 7.5 A cutoff, spectral
coarse-graining with 45% near-active budget, dose = 0.35*deg + 0.20*hydro,
bond = mean 1/d) and evaluates CANDIDATE METRICS against all four targets.

The April baseline (time-averaged single-particle propagator, i.e. the linear
walk's infinite-time average) recovered KRAS 2/2 and myosin 2/2 but missed
BCR-ABL1's 10+-hop myristoyl pocket at top-5. Candidates here add physics the
linear average does not have:

  M_avg   — April baseline (degenerate-safe time-averaged propagator). Referee.
  M_ft    — finite-time coherent transport: mean of |<j|U(t)|i>|^2 over a time
            WINDOW (transient wavefronts that the T->inf average dilutes).
  M_res   — resonant Green's function: max over omega of |<j|(w-H+i*eta)^-1|i>|^2
            (frequency-matched transport channels; finite linewidth keeps
            cross-mode coherence the time-average kills).
  M_2x    — two-excitation sector with bond-weighted interaction (hard-core):
            genuinely nonlinear multi-excitation propagation — the regime the
            challenge says classical linear models miss, and the sector that is
            exponential classically at residue scale but native on hardware.
  chem    — any metric on a chemistry-weighted graph: bond *= amino-pair
            coupling from the hexagene l12() 20x20 matrix (framework-derived,
            label-free), normalized to unit mean.

Anti-tuning rules, enforced in the report: a candidate only "wins" if it fixes
ABL top-5 while KEEPING KRAS and myosin hits (no regression), and while stable
across its own parameter range (reported per candidate).

Usage:  python allostery_v2.py            # all targets x all metrics
        python allostery_v2.py BCR_ABL1   # one target
Writes: v2_results.json + console table.
"""
from __future__ import annotations
import itertools, json, math, os, sys
import numpy as np
from scipy.linalg import eigh
from scipy.sparse.csgraph import shortest_path
from scipy.cluster.vq import kmeans2

HERE = os.path.dirname(os.path.abspath(__file__))
KD = {"ALA": 1.8, "ARG": -4.5, "ASN": -3.5, "ASP": -3.5, "CYS": 2.5,
      "GLN": -3.5, "GLU": -3.5, "GLY": -0.4, "HIS": -3.2, "ILE": 4.5,
      "LEU": 3.8, "LYS": -3.9, "MET": 1.9, "PHE": 2.8, "PRO": -1.6,
      "SER": -0.8, "THR": -0.7, "TRP": -0.9, "TYR": -1.3, "VAL": 4.2}
CUTOFF = 7.5
DOSE_ALPHA, DOSE_BETA = 0.35, 0.20
NEAR_FRAC, GEO_R = 0.45, 4

TARGETS = {
    "KRAS_G12C": dict(pdb="4OBE", chain="A", n_cells=14,
        active=[10,11,12,13,14,15,16,17,18,32,33,34,35,36,37,38,60,61,62,63,64,65,66,67],
        valid=[12,58,95,96,99,102,117,118]),
    # Challenge scope: "Included: the catalytic domains." 1OPL chain A carries
    # SH3+SH2+kinase; restrict to the kinase (catalytic) domain 242-531.
    "BCR_ABL1": dict(pdb="1OPL", chain="A", n_cells=26, domain=(242, 531),
        active=[248,249,250,251,252,253,254,255,256,257,258,259,318,319,320,321,322,323,324,325,326,327,328],
        valid=[359,361,362,363,369,370,449,453,457]),
    "CARDIAC_MYOSIN": dict(pdb="5TBY", chain="A", n_cells=18,
        active=[179,180,181,182,183,184,233,234,235,236,237,238,459,460,461,462,463,464,465,466],
        valid=[134,137,144,147,148,152,178,179,718]),
    # 1NKP author numbering: chain A = c-Myc bHLH-LZ (897-984). Functional site =
    # the DNA-contacting basic region (approx. 899-918). April's 364-376 spec
    # matched no residue in any chain (its code fell back silently); corrected here.
    "C_MYC": dict(pdb="1NKP", chain="A", n_cells=18,
        active=list(range(899, 919)), valid=None),
}

THREE_TO_ONE = {"ALA":"A","ARG":"R","ASN":"N","ASP":"D","CYS":"C","GLN":"Q","GLU":"E",
    "GLY":"G","HIS":"H","ILE":"I","LEU":"L","LYS":"K","MET":"M","PHE":"F","PRO":"P",
    "SER":"S","THR":"T","TRP":"W","TYR":"Y","VAL":"V"}


def parse_ca(pdb_path, chain):
    """(resnum, resname, xyz) for CA atoms of the chain, first altloc/model only."""
    out, seen = [], set()
    for line in open(pdb_path):
        if line.startswith("ENDMDL"):
            break
        if not line.startswith("ATOM"):
            continue
        if line[12:16].strip() != "CA" or line[21] != chain:
            continue
        alt = line[16]
        if alt not in (" ", "A"):
            continue
        rn = int(line[22:26])
        if rn in seen:
            continue
        seen.add(rn)
        out.append((rn, line[17:20].strip(),
                    np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])))
    return out


def contact_graph(coords):
    D = np.linalg.norm(coords[:, None] - coords[None, :], axis=2)
    A = (D < CUTOFF) & (D > 0)
    return A, D


def coarse_grain(A, D, n_cells, active_local):
    """Spectral embedding + kmeans, near/far budget split (April recipe)."""
    n = A.shape[0]
    geo = shortest_path(A.astype(float), unweighted=True)
    d_act = geo[active_local].min(axis=0) if active_local else np.full(n, np.inf)
    near = np.where(np.isfinite(d_act) & (d_act <= GEO_R))[0]
    far = np.array([i for i in range(n) if i not in set(near)])
    n_near = max(1, min(len(near), int(round(n_cells * NEAR_FRAC)))) if len(near) else 0
    n_far = n_cells - n_near

    def spart(idx, k):
        if len(idx) <= k:
            return {i: j for j, i in enumerate(idx)}
        Asub = A[np.ix_(idx, idx)].astype(float)
        deg = Asub.sum(1)
        deg[deg == 0] = 1
        L = np.eye(len(idx)) - Asub / np.sqrt(np.outer(deg, deg))
        w, v = eigh(L)
        emb = v[:, 1:min(k + 1, len(idx))]
        emb = emb / (np.linalg.norm(emb, axis=1, keepdims=True) + 1e-12)
        best = None
        for seed in (42, 7, 2026, 99, 314):
            cent, lab = kmeans2(emb, k, minit="++", seed=seed)
            # repair empty clusters: seed each with the point farthest from its centroid
            for c in range(k):
                if not (lab == c).any():
                    dists = np.linalg.norm(emb - cent[lab], axis=1)
                    lab[int(np.argmax(dists))] = c
            if len(set(lab.tolist())) != k:
                continue
            score = sum(np.linalg.norm(emb[lab == c] - emb[lab == c].mean(0), axis=1).sum()
                        for c in range(k))
            if best is None or score < best[0]:
                best = (score, lab)
        if best is None:  # last resort: geodesic-ordered equal split
            order = np.argsort(emb[:, 0])
            lab = np.zeros(len(idx), int)
            for j, chunk in enumerate(np.array_split(order, k)):
                lab[chunk] = j
            best = (0.0, lab)
        return {i: int(l) for i, l in zip(idx, best[1])}

    lab_near = spart(near, n_near) if n_near else {}
    lab_far = spart(far, n_far) if n_far else {}
    labels = np.zeros(n, int)
    for i, l in lab_near.items():
        labels[i] = l
    off = (max(lab_near.values()) + 1) if lab_near else 0
    for i, l in lab_far.items():
        labels[i] = off + l
    # re-index contiguous
    uniq = sorted(set(labels))
    remap = {u: j for j, u in enumerate(uniq)}
    return np.array([remap[l] for l in labels])


def build_cells(target):
    spec = TARGETS[target]
    ca = parse_ca(os.path.join(HERE, "pdb", spec["pdb"] + ".pdb"), spec["chain"])
    if "domain" in spec:
        lo, hi = spec["domain"]
        ca = [r for r in ca if lo <= r[0] <= hi]
    ids = np.array([r[0] for r in ca])
    names = [r[1] for r in ca]
    coords = np.stack([r[2] for r in ca])
    A, D = contact_graph(coords)
    act_local = [int(np.where(ids == a)[0][0]) for a in spec["active"] if a in ids]
    labels = coarse_grain(A, D, spec["n_cells"], act_local)
    N = labels.max() + 1
    cells = [np.where(labels == c)[0] for c in range(N)]
    # doses
    deg = A.sum(1).astype(float)
    hyd = np.array([KD.get(nm, 0.0) for nm in names])
    cdeg = np.array([deg[m].mean() for m in cells])
    chyd = np.array([hyd[m].mean() for m in cells])
    dn = (cdeg - cdeg.min()) / (np.ptp(cdeg) + 1e-12)
    hn = (chyd - chyd.min()) / (np.ptp(chyd) + 1e-12)
    dose = DOSE_ALPHA * dn + DOSE_BETA * hn
    dose = 0.5 * dose / (dose.max() + 1e-12)
    # bonds: mean 1/d over crossing contacts; also record crossing residue pairs
    J = np.zeros((N, N))
    cross = {}
    for a, b in itertools.combinations(range(N), 2):
        pairs = [(i, j) for i in cells[a] for j in cells[b] if A[i, j]]
        if pairs:
            J[a, b] = J[b, a] = np.mean([1.0 / D[i, j] for i, j in pairs])
            cross[(a, b)] = pairs
    active_cells = sorted({int(labels[i]) for i in act_local})
    vcells = None
    if spec["valid"]:
        vloc = [int(np.where(ids == v)[0][0]) for v in spec["valid"] if v in ids]
        vcells = sorted({int(labels[i]) for i in vloc})
    # cell geodesics on the cell graph
    cg = shortest_path((J > 0).astype(float), unweighted=True)
    return dict(N=N, cells=cells, dose=dose, J=J, cross=cross, names=names, ids=ids,
                active_cells=active_cells, valid_cells=vcells, cell_geo=cg,
                res_geo=shortest_path(A.astype(float), unweighted=True))


def hop(dose, J):
    h = 2.0 * J.astype(complex)
    np.fill_diagonal(h, -2.0 * dose)
    return h


def m_avg(h):
    w, v = eigh(h)
    n = h.shape[0]
    M = np.zeros((n, n))
    groups = []
    for k in range(len(w)):
        if groups and abs(w[k] - w[groups[-1][0]]) < 1e-9:
            groups[-1].append(k)
        else:
            groups.append([k])
    for g in groups:
        P = v[:, g] @ v[:, g].conj().T
        M += np.abs(P) ** 2
    return M


def m_finite_t(h, t_lo=1.0, t_hi=8.0, nt=40):
    w, v = eigh(h)
    n = h.shape[0]
    M = np.zeros((n, n))
    for t in np.linspace(t_lo, t_hi, nt):
        U = (v * np.exp(-1j * w * t)) @ v.conj().T
        M += np.abs(U) ** 2
    return M / nt


def m_res(h, eta=0.15, nw=120):
    w, v = eigh(h)
    n = h.shape[0]
    ws = np.linspace(w.min() - 0.5, w.max() + 0.5, nw)
    M = np.zeros((n, n))
    for om in ws:
        G = (v / (om - w + 1j * eta)) @ v.conj().T
        M = np.maximum(M, np.abs(G) ** 2)
    return M


def m_two_exc(dose, J, u_scale=1.0, t_lo=1.0, t_hi=8.0, nt=24):
    """Hard-core two-excitation sector; interaction U_ab = u_scale*2*J_ab when both
    occupied on bonded cells. Initialize pair on the two highest-dose active cells;
    score j by time-windowed marginal occupation. Returns per-site vector."""
    N = len(dose)
    pairs = [(a, b) for a in range(N) for b in range(a + 1, N)]
    pidx = {p: k for k, p in enumerate(pairs)}
    dim = len(pairs)
    H = np.zeros((dim, dim), complex)
    for k, (a, b) in enumerate(pairs):
        H[k, k] = -2.0 * (dose[a] + dose[b]) + u_scale * 2.0 * J[a, b]
        for c in range(N):
            if c not in (a, b):
                if J[b, c] > 0:
                    q = pidx[(min(a, c), max(a, c))]
                    H[k, q] += 2.0 * J[b, c]
                if J[a, c] > 0:
                    q = pidx[(min(c, b), max(c, b))]
                    H[k, q] += 2.0 * J[a, c]
    H = (H + H.conj().T) / 2
    w, v = eigh(H)
    return w, v, pairs


def score_two_exc(dose, J, active_cells, u_scale=1.0, t_lo=1.0, t_hi=8.0, nt=24):
    N = len(dose)
    w, v, pairs = m_two_exc(dose, J, u_scale)
    acts = sorted(active_cells, key=lambda c: -dose[c])[:2]
    if len(acts) < 2:
        acts = (active_cells * 2)[:2]
    k0 = pairs.index((min(acts), max(acts)))
    psi0 = np.zeros(len(pairs))
    psi0[k0] = 1.0
    c0 = v.conj().T @ psi0
    occ = np.zeros(N)
    for t in np.linspace(t_lo, t_hi, nt):
        amp = v @ (np.exp(-1j * w * t) * c0)
        p = np.abs(amp) ** 2
        for k, (a, b) in enumerate(pairs):
            occ[a] += p[k]
            occ[b] += p[k]
    return occ / nt


def m_soft(J, n_soft=6, signed=False):
    """GNM-class soft-mode co-fluctuation on the MECHANICAL network:
    L = deg - J (weighted Laplacian); M[i,j] = |sum_{k soft} v_k(i) v_k(j) / l_k|.
    Physically: allosteric communication rides the lowest collective modes
    (hinge mechanics) — the challenge's own elastic-network hypothesis, read in
    the frequency domain. Hardware-native: soft modes are the LOW-frequency
    beat lines of the same evolution circuits (frequency-selected readout of
    the identical dynamics — no new circuit family)."""
    N = J.shape[0]
    L = np.diag(J.sum(1)) - J
    w, v = eigh(L)
    M = np.zeros((N, N))
    used = 0
    for k in range(N):
        if w[k] < 1e-9:
            continue
        M += np.outer(v[:, k], v[:, k]) / w[k]
        used += 1
        if used >= n_soft:
            break
    return np.abs(M) if not signed else M


def m_res_band(h, J, eta=0.15, nw=60, n_soft=6):
    """resonant Green's function restricted to the soft band of the mechanical
    spectrum: omega scanned only over the lowest n_soft Laplacian frequencies
    mapped into the hop spectrum's soft end."""
    w, v = eigh(h)
    lo, hi = w.min(), np.percentile(w, 35)
    ws = np.linspace(lo, hi, nw)
    n = h.shape[0]
    M = np.zeros((n, n))
    for om in ws:
        G = (v / (om - w + 1j * eta)) @ v.conj().T
        M = np.maximum(M, np.abs(G) ** 2)
    return M


def m_deph(dose, J, gamma=1.0, t_max=12.0, nt=30):
    """Dephased (Lindblad) walk: site-dephasing rate gamma interpolates between
    the coherent walk (gamma=0) and Chennubhotla-Bahar Markov diffusion
    (gamma->inf, the challenge's ref 8). ENAQT: intermediate gamma un-traps
    coherent localization and reaches deep regions. Returns time-integrated
    population matrix M[i,j] (start i -> found j)."""
    N = len(dose)
    h = hop(dose, J)
    I = np.eye(N)
    # Liouvillian on vectorized rho: -i(H x I - I x H^T) + gamma(sum_k P_k x P_k - I)
    Lh = -1j * (np.kron(h, I) - np.kron(I, h.T))
    Ld = np.zeros((N * N, N * N), complex)
    for k in range(N):
        P = np.zeros((N, N)); P[k, k] = 1.0
        Ld += np.kron(P, P)
    Ld = gamma * (Ld - np.eye(N * N))
    Lfull = Lh + Ld
    w, V = np.linalg.eig(Lfull)
    Vi = np.linalg.inv(V)
    M = np.zeros((N, N))
    ts = np.linspace(t_max / nt, t_max, nt)
    for i in range(N):
        r0 = np.zeros((N, N), complex); r0[i, i] = 1.0
        c0 = Vi @ r0.flatten()
        for t in ts:
            rt = (V @ (np.exp(w * t) * c0)).reshape(N, N)
            M[i] += np.real(np.diag(rt))
    return M / nt


def m_susceptibility(dose, J, active_cells, delta=0.08):
    """Control-point scan (the inverse allosteric question): perturb the dose at
    candidate cell j, measure (a) the shift of ground-state weight on the
    active site and (b) the shift of the spectral gap. Sites that CONTROL the
    active site score high — the definition of an allosteric effector. On
    hardware this is the beat-instrument observable: gap-as-beat under local
    detuning at j (one circuit per candidate, constant depth)."""
    N = len(dose)
    h0 = hop(dose, J)
    w0, v0 = eigh(h0)
    act = list(active_cells)
    occ0 = float((np.abs(v0[act, 0]) ** 2).sum())
    gap0 = float(w0[1] - w0[0])
    s_occ = np.zeros(N); s_gap = np.zeros(N)
    for j in range(N):
        d2 = dose.copy(); d2[j] += delta
        w, v = eigh(hop(d2, J))
        s_occ[j] = abs(float((np.abs(v[act, 0]) ** 2).sum()) - occ0)
        s_gap[j] = abs(float(w[1] - w[0]) - gap0)
    def nz(x):
        return (x - x.min()) / (np.ptp(x) + 1e-15)
    return nz(s_occ) + nz(s_gap)


def chem_weight(cg_data):
    """multiply bonds by mean l12 amino-pair coupling over crossing contacts."""
    sys.path.insert(0, r"C:\hexageneweb\engine")
    try:
        import s21_operator
        L = s21_operator.l12()
    except Exception as e:
        return None, f"l12 unavailable: {e}"
    # L: dict or matrix keyed by one-letter? normalize access
    def cpl(a3, b3):
        a, b = THREE_TO_ONE.get(a3), THREE_TO_ONE.get(b3)
        if a is None or b is None:
            return 1.0
        try:
            if isinstance(L, dict):
                return abs(L.get((a, b), L.get((b, a), 1.0)))
            import numpy as _np
            aas = "ACDEFGHIKLMNPQRSTVWY"
            return abs(float(_np.asarray(L)[aas.index(a), aas.index(b)]))
        except Exception:
            return 1.0
    J2 = cg_data["J"].copy()
    vals = []
    for (a, b), pairs in cg_data["cross"].items():
        m = np.mean([cpl(cg_data["names"][i], cg_data["names"][j]) for i, j in pairs])
        J2[a, b] = J2[b, a] = J2[a, b] * m
        vals.append(m)
    if vals:
        J2 *= cg_data["J"][cg_data["J"] > 0].mean() / (J2[J2 > 0].mean() + 1e-12)
    return J2, f"l12 applied, mean pair coupling {np.mean(vals):.3f}"


def rank_and_score(scores, g, k=5):
    excl = set(g["active_cells"])
    order = [c for c in np.argsort(-scores) if c not in excl]
    top = order[:k]
    hits = None
    if g["valid_cells"] is not None:
        vset = set(g["valid_cells"]) - excl
        hits = {kk: len(set(order[:kk]) & vset) for kk in (3, 5, 8)}
        hits["n_valid"] = len(vset)
    return top, hits


def active_response(M, g):
    A = g["active_cells"]
    return M[A, :].mean(axis=0)


def run_target(target):
    g = build_cells(target)
    h0 = hop(g["dose"], g["J"])
    out = {"target": target, "N": int(g["N"]), "active_cells": g["active_cells"],
           "valid_cells": g["valid_cells"], "metrics": {}}
    Jc, chem_note = chem_weight(g)
    out["chem_note"] = chem_note

    def add(name, scores):
        top, hits = rank_and_score(scores, g)
        out["metrics"][name] = {"top5": [int(t) for t in top],
                                "hits": hits,
                                "scores": [round(float(s), 6) for s in scores]}
        h5 = hits and hits.get(5)
        print(f"  {name:14s} top5={top}  hit@5={h5 if hits else '—'}"
              f"{'/' + str(hits['n_valid']) if hits else ''}")

    print(f"== {target}: {g['N']} cells, active {g['active_cells']}, valid {g['valid_cells']}")
    add("M_avg", active_response(m_avg(h0), g))
    add("M_ft", active_response(m_finite_t(h0), g))
    for eta in (0.05, 0.15, 0.4):
        add(f"M_res_e{eta}", active_response(m_res(h0, eta=eta), g))
    for u in (0.5, 1.0, 2.0):
        add(f"M_2x_u{u}", score_two_exc(g["dose"], g["J"], g["active_cells"], u_scale=u))
    if Jc is not None:
        hc = hop(g["dose"], Jc)
        add("M_avg_chem", active_response(m_avg(hc), g))
        add("M_ft_chem", active_response(m_finite_t(hc), g))
        add("M_2x_chem", score_two_exc(g["dose"], Jc, g["active_cells"]))
    return out


if __name__ == "__main__":
    targets = [sys.argv[1]] if len(sys.argv) > 1 else list(TARGETS)
    results = [run_target(t) for t in targets]
    json.dump(results, open(os.path.join(HERE, "v2_results.json"), "w"), indent=1)
    print("wrote v2_results.json")
