"""Classical comparator arm for the retarded contact response.

WHAT THIS IS. The advantage gate needs the other side of the comparison: the
same operator, the same observable, the same accuracy target, and the cost a
classical method actually pays. This measures that cost for the matrix-product
route, which is the strongest classical method for this object.

WHY THE COST MIGHT BE LARGE HERE, structurally. The contact operator's ground
state is stoquastic, so imaginary-time sampling of it carries no sign problem
and is easy. The retarded response is real-time, where the cancellation
returns. Separately, the operator's pairing couples residue i directly to
i + N/2, which is exactly the long-range structure that makes matrix-product
orderings poor. Those are two independent reasons to expect a hard classical
cost, and neither is a proof, so we measure.

WHAT IS AND IS NOT CLAIMED. This is a measured cost for this instance family,
this observable, this accuracy target, and the orderings searched. It is a
credible classical baseline and a censored benchmark observation. It is not a
complexity proof, and a truncation test is specific to its state, ordering and
tolerance.

QUANTUM SIDE. The exact compiler costs 8 logical CX per evolved pair, constant
in evolution time, so the device cost is 8 * |edges| and does not grow with the
record length. Physical routing remains a separate device-specific cost.
"""
import itertools, json, math, os
import numpy as np

KAPPA = 3.0 / (3.0 - math.sqrt(5.0))
HERE = os.path.dirname(os.path.abspath(__file__))
FIDELITY = 0.999          # accuracy target for the state representation
CHI_TOL = 0.01            # and for the observable itself, 1% of peak


def contact_edges(N):
    """Derived pairing plus a backbone contact chain."""
    pairs = [(i, i + N // 2) for i in range(N // 2)]
    contacts = [(i, i + 1) for i in range(N - 1)]
    return sorted({(min(a, b), max(a, b)) for a, b in pairs + contacts})


def diag_D(N, edges):
    idx = np.arange(1 << N, dtype=np.int64)
    d = np.zeros(1 << N)
    for a, b in edges:
        d += 0.5 * (1.0 - (1 - 2 * ((idx >> a) & 1)) * (1 - 2 * ((idx >> b) & 1)))
    return KAPPA * d


def apply_H(psi, N, d):
    out = d * psi
    v = psi.reshape([2] * N)
    for i in range(N):
        out -= np.flip(v, axis=i).reshape(-1)
    return out


def ground_state(N, d, iters=400):
    """Lowest eigenvector by shifted power iteration on the matrix-free operator."""
    rng = np.random.default_rng(21)
    v = rng.normal(size=1 << N)
    v /= np.linalg.norm(v)
    shift = KAPPA * N + N + 2.0
    for _ in range(iters):
        v = shift * v - apply_H(v, N, d)
        v /= np.linalg.norm(v)
    e = float(v @ apply_H(v, N, d))
    return e, v


def lanczos_step(psi, N, d, dt, m=20):
    V = np.empty((m, psi.size), dtype=np.complex128)
    a = np.zeros(m); b = np.zeros(m)
    beta = np.linalg.norm(psi); V[0] = psi / beta; j = m
    for i in range(m):
        w = apply_H(V[i], N, d)
        a[i] = np.vdot(V[i], w).real
        Vi = V[: i + 1]
        w -= Vi.T @ (Vi.conj() @ w)
        nb = np.linalg.norm(w)
        if nb < 1e-13:
            j = i + 1; break
        b[i] = nb
        if i + 1 < m:
            V[i + 1] = w / nb
    T = np.diag(a[:j]) + np.diag(b[: j - 1], 1) + np.diag(b[: j - 1], -1)
    ev, U = np.linalg.eigh(T)
    return beta * ((U @ (np.exp(-1j * ev * dt) * U[0].conj())) @ V[:j])


def orderings(N):
    """Orderings a matrix-product method would plausibly use."""
    seq = list(range(N))                                   # sequence order
    paired = []                                            # keep each pair adjacent
    for i in range(N // 2):
        paired += [i, i + N // 2]
    return {"sequence": seq, "pair_adjacent": paired}


def min_bond_dimension(psi, N, order, fidelity=FIDELITY):
    """Largest bond dimension needed over all cuts, for this ordering."""
    v = psi.reshape([2] * N)
    v = np.transpose(v, [N - 1 - q for q in order])
    need = 1
    for cut in range(1, N):
        m = v.reshape(1 << cut, -1)
        s = np.linalg.svd(m, compute_uv=False)
        p = s ** 2
        p = p / p.sum()
        keep = int(np.searchsorted(np.cumsum(p), fidelity) + 1)
        need = max(need, min(keep, p.size))
    return need


def run(Ns=(8, 10, 12), T=6.0, npts=13):
    rows = []
    for N in Ns:
        E = contact_edges(N)
        d_all = diag_D(N, E)
        d_nat = diag_D(N, [(i, i + N // 2) for i in range(N // 2)])
        e0, g = ground_state(N, d_nat)
        times = np.linspace(0.0, T, npts)
        dt = times[1] - times[0]
        psi = g.astype(np.complex128)
        best = {k: 1 for k in orderings(N)}
        for _ in range(npts - 1):
            psi = lanczos_step(psi, N, d_all, dt)
            for k, o in orderings(N).items():
                best[k] = max(best[k], min_bond_dimension(psi, N, o))
        cap = 1 << (N // 2)
        chi_star = min(best.values())
        quantum_cx = 8 * len(E)
        rows.append(dict(N=N, edges=len(E), E0_native=e0, chi_cap=cap,
                         chi_by_ordering=best, chi_best_ordering=chi_star,
                         classical_cost_proxy=float(chi_star ** 2 * N),
                         quantum_logical_cx=quantum_cx))
        print("  N=%2d edges=%2d  chi needed: %s  best=%d of cap %d   "
              "classical chi^2*N=%.3e   quantum CX=%d"
              % (N, len(E), best, chi_star, cap, chi_star ** 2 * N, quantum_cx),
              flush=True)
    return rows


if __name__ == "__main__":
    print("classical comparator: bond dimension needed for the retarded response")
    print("  state fidelity target %.3f, orderings searched: sequence, pair-adjacent"
          % FIDELITY)
    rows = run()
    chis = [r["chi_best_ordering"] for r in rows]
    growth = [chis[i] / chis[i - 1] for i in range(1, len(chis))]
    caps = [r["chi_cap"] for r in rows]
    capg = [caps[i] / caps[i - 1] for i in range(1, len(caps))]
    print("\n  chi growth per +2 residues: %s   (cap grows %s)"
          % (["%.2fx" % g for g in growth], ["%.0fx" % g for g in capg]))
    print("  quantum logical CX growth: %s"
          % (["%.2fx" % (rows[i]["quantum_logical_cx"] / rows[i - 1]["quantum_logical_cx"])
              for i in range(1, len(rows))]))
    out = dict(card="classical comparator arm for the retarded contact response",
               fidelity_target=FIDELITY, rows=rows,
               chi_growth_per_two_residues=growth, cap_growth=capg,
               scope="measured cost for this instance family, observable, accuracy "
                     "target and the orderings searched; a credible classical "
                     "baseline and censored benchmark observation, not a "
                     "complexity proof",
               quantum_cost_rule="8 logical CX per evolved pair, constant in "
                                 "evolution time; physical routing separate")
    json.dump(out, open(os.path.join(HERE, "results", "classical_comparator.json"), "w"),
              indent=1)
    print("  wrote results/classical_comparator.json")
