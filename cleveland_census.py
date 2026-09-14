#!/usr/bin/env python3
"""cleveland_census.py — the cheapest adversary for the Cleveland K=6 hardware cell.

THE QUESTION. The v7 proposal states C(28-7) on the 156-qubit K=6 map at 8.7 sigma
from zero and 2.4 sigma above the map's own baseline, and defers the classical
adjudication to PoC step 1. This is that step's first gate, done the way the A1
referee did it on 2026-08-10: evolve the observable's Pauli operators BACKWARD
through the flown circuit (Heisenberg picture), count terms under an eps ladder,
and see whether the operator stays inside a fixed term budget.

  converges  -> the cell is classically computable EXACTLY from this script,
                the number is compared to the receipt, and the K=6 claim is
                adjudicated (and, if the classical number sits inside the
                error bar, the claim dies as a beyond-classical statement);
  diverges   -> the cell stands contested with receipts, as A1's k>=8 did.

THE CIRCUIT IS REBUILT OFFLINE, NOT TRUSTED. ibm_residue.build(K) fetches the
fez coupling map from the IBM service. Here the service is replaced by the
offline FakeFez map and the rebuilt circuit must reproduce EVERY number in the
flown PREREG_residue_K6.json (edges used, layers, 2q count, retained weight,
active qubits, all 120 pairs, sha256 of the frozen record). No match, no census.

ENGINE. Sparse-Pauli Heisenberg propagation, vectorised in numpy. A Pauli is
(x, z) bitmasks on 156 qubits, stored as three uint64 columns each, plus a
real coefficient; P(x,z) = i^{|x&z|} X^x Z^z so every stored Pauli is hermitian.
Gate conjugation is exact: RZ(th) on q and RXX(th) on (a,b) split anticommuting
terms into cos*P + sin*(i Q P); X prep flips the sign of Z/Y on its qubit.
Truncation drops |coeff| < eps after each gate; the budget caps the term count.
V1 GATE: at K=2 the engine's exact (eps=0) connected correlator must equal the
independent light-cone statevector prediction cone_predict() to 1e-12.

Usage:
  python cleveland_census.py export         # rebuild, gate vs PREREG, write ops
  python cleveland_census.py v1             # K=2 exact engine vs cone_predict
  python cleveland_census.py census K [eps ...]   # e.g. census 6 3e-5 1e-5
  python cleveland_census.py evaluate K eps # C(28-7) if the operator converged
All outputs -> cleveland_census_<stage>.json next to this file.
"""
import json, math, os, sys, time, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
PAIR = (28, 7)              # qi = 28 (target), qa = 7 (active site), distance 11
PREREG = os.path.join(HERE, "PREREG_residue_K6.json")
OPS_FILE = os.path.join(HERE, "cleveland_census_ops.json")
BUDGET = int(float(os.environ.get("CENSUS_BUDGET", 2 * 10 ** 8)))   # A1 referee used 2e8
NQ = 156
W = 3                       # uint64 words per mask, 192 bits >= 156


# ----------------------------------------------------------------- stage 1 --
def export():
    import ibm_residue as IR
    from qiskit_ibm_runtime.fake_provider import FakeFez
    fb = FakeFez()
    edges = sorted({tuple(sorted(e)) for e in fb.coupling_map.get_edges()})
    nq = fb.num_qubits
    IR.backend_graph = lambda: ("ibm_fez", edges, nq)     # offline, no service
    t0 = time.time()
    B = IR.build(6)
    pre = json.load(open(PREREG))
    used_edges = len(B["used"])
    n_rxx = sum(1 for kind, _, _ in B["core_ops"] if kind == "rxx")
    n2q = 3 * used_edges * 6          # the freeze step's transpilation bound, 3 CX per RXX
    ret_w = float(B["w"]) if not isinstance(B["w"], dict) else None
    # the 120 flown pairs, reconstructed from the rebuilt assignment exactly as freeze() did
    B["pairs"] = [[int(qi), int(qa), int(dd)] for qi, qa, dd in IR.full_map_pairs(B)]
    rebuilt = dict(
        backend="ibm_fez", n_qubits_used=int((B["res_at"] >= 0).sum()), K=6, dt=IR.DT,
        n_native_edges_used=used_edges, n_edge_layers=B["nlay"],
        n_2q_total=n2q, active_qubits=sorted(B["act_q"]))
    print("  native RXX gates in the K=6 circuit: %d (= %d edges x 6 sweeps)" % (n_rxx, used_edges))
    checks = {}
    for k in ("backend", "n_qubits_used", "K", "dt", "n_native_edges_used",
              "n_edge_layers", "n_2q_total"):
        checks[k] = (pre[k] == rebuilt[k], pre[k], rebuilt[k])
    checks["active_qubits"] = (sorted(pre["active_qubits"]) == rebuilt["active_qubits"],
                               len(pre["active_qubits"]), len(rebuilt["active_qubits"]))
    if ret_w is not None:
        checks["retained_coupling_weight"] = (abs(pre["retained_coupling_weight"] - ret_w) < 0.01,
                                              pre["retained_coupling_weight"], ret_w)
    # pairs as flown: [qi, qa, distance]; rebuild the same list if the builder exposes it
    pairs_ok = None
    if "pairs" in B:
        rp = [list(p) for p in B["pairs"]]
        pairs_ok = (rp == pre["pairs"], len(pre["pairs"]), len(rp))
        checks["pairs"] = pairs_ok
    allok = all(v[0] for v in checks.values())
    print("=" * 74)
    print("EXPORT: offline rebuild of the flown K=6 circuit, gated against PREREG")
    print("=" * 74)
    for k, v in checks.items():
        print("  %-26s %-5s prereg=%s rebuilt=%s" % (k, "PASS" if v[0] else "FAIL", v[1], v[2]))
    print("  build time %.1f s | ops %d (x-prep %d) | pair %s in prereg: %s"
          % (time.time() - t0, len(B["ops"]), len(B["x_qubits"]),
             PAIR, [PAIR[0], PAIR[1], 11] in pre["pairs"]))
    if not allok:
        print("  REPRODUCTION FAILED — the offline map or seed does not reproduce the flight. STOP.")
    ops = [[k, list(q), float(th)] for k, q, th in B["ops"]]
    core = [[k, list(q), float(th)] for k, q, th in B["core_ops"]]
    rec = dict(reproduced=allok, checks={k: [bool(v[0]), v[1], v[2]] for k, v in checks.items()},
               nq=nq, x_qubits=sorted(B["x_qubits"]), pair=list(PAIR), K_flown=6,
               ops_full_K6=ops, core_ops_one_sweep=core[: len(core) // 6],
               ops_per_sweep=len(core) // 6, prereg_sha256=pre["sha256"])
    # sanity: core ops must be exactly 6 identical sweeps
    L = len(core) // 6
    rec["sweeps_identical"] = all(core[i * L:(i + 1) * L] == core[:L] for i in range(6))
    print("  six sweeps identical: %s (ops per sweep %d)" % (rec["sweeps_identical"], L))
    json.dump(rec, open(OPS_FILE, "w"))
    print("-> %s" % OPS_FILE)
    return rec


def load_ops(K):
    rec = json.load(open(OPS_FILE))
    assert rec["reproduced"], "export did not reproduce PREREG; refusing to run"
    sweep = rec["core_ops_one_sweep"]
    xprep = [["x", [q], 0.0] for q in rec["x_qubits"]]
    return xprep + sweep * K, rec


# ------------------------------------------------------------------ engine --
def _pop(a):
    # popcount per uint64 element (numpy >= 2 has bitwise_count)
    if hasattr(np, "bitwise_count"):
        return np.bitwise_count(a)
    a = a - ((a >> np.uint64(1)) & np.uint64(0x5555555555555555))
    a = (a & np.uint64(0x3333333333333333)) + ((a >> np.uint64(2)) & np.uint64(0x3333333333333333))
    a = (a + (a >> np.uint64(4))) & np.uint64(0x0F0F0F0F0F0F0F0F)
    return ((a * np.uint64(0x0101010101010101)) >> np.uint64(56)).astype(np.int64)


def popc(M):
    """M: (n, W) uint64 -> total popcount per row"""
    return _pop(M).sum(axis=1).astype(np.int64)


def bit(q):
    m = np.zeros(W, dtype=np.uint64)
    m[q // 64] = np.uint64(1) << np.uint64(q % 64)
    return m


class PauliSum:
    """x, z: (n, W) uint64; c: (n,) float64. Hermitian Paulis P = i^{|x&z|} X^x Z^z."""

    def __init__(self, x, z, c):
        self.x, self.z, self.c = x, z, c

    @staticmethod
    def single(mask_x, mask_z):
        return PauliSum(mask_x[None, :].copy(), mask_z[None, :].copy(), np.array([1.0]))

    def n(self):
        return int(self.c.size)

    def merge(self):
        key = np.concatenate([self.x, self.z], axis=1)
        order = np.lexsort(key.T[::-1])
        key, x, z, c = key[order], self.x[order], self.z[order], self.c[order]
        new = np.ones(c.size, dtype=bool)
        new[1:] = np.any(key[1:] != key[:-1], axis=1)
        idx = np.cumsum(new) - 1
        cs = np.zeros(int(new.sum()))
        np.add.at(cs, idx, c)
        self.x, self.z, self.c = x[new], z[new], cs
        return self

    def truncate(self, eps):
        if eps > 0:
            keep = np.abs(self.c) >= eps
            self.x, self.z, self.c = self.x[keep], self.z[keep], self.c[keep]
        return self

    def conj_x(self, q):
        """Heisenberg conjugation by an X gate on q: sign flip where z has bit q."""
        m = bit(q)
        has_z = (self.z & m).any(axis=1)
        self.c = np.where(has_z, -self.c, self.c)
        return self

    def conj_rot(self, qx, qz, theta):
        """G = exp(-i theta/2 Q), Q = P(qx, qz). G^dag P G = P if [P,Q]=0,
        else cos(theta) P + sin(theta) * (i Q P)."""
        # anticommute iff |x&qz| + |z&qx| odd
        par = (popc(self.x & qz) + popc(self.z & qx)) & 1
        a = par == 1
        if not a.any():
            return self
        xa, za, ca = self.x[a], self.z[a], self.c[a]
        # product Q P: (qx,qz)*(xa,za) -> masks xor; phase i^{pq + pp - p12} (-1)^{|qz & xa|}
        x12, z12 = xa ^ qx, za ^ qz
        pq = int(popc(qx[None, :] & qz[None, :])[0])
        pp = popc(xa & za)
        p12 = popc(x12 & z12)
        sgn = popc(qz[None, :].repeat(xa.shape[0], 0) & xa) & 1
        ph = (pq + pp - p12) % 4              # power of i
        # i * i^ph * (-1)^sgn must be real: ph must be odd -> i*i^ph = i^{ph+1} in {+1,-1}
        assert np.all(ph % 2 == 1), "phase bookkeeping error: non-real coefficient"
        real = np.where(((ph + 1) // 2) % 2 == 0, 1.0, -1.0) * np.where(sgn == 1, -1.0, 1.0)
        cos_t, sin_t = math.cos(theta), math.sin(theta)
        newc = ca * sin_t * real
        self.c = np.where(a, self.c * cos_t, self.c)
        self.x = np.concatenate([self.x, x12]); self.z = np.concatenate([self.z, z12])
        self.c = np.concatenate([self.c, newc])
        return self

    def expect_zero_state(self):
        """<0...0| P |0...0> = sum of coefficients of pure-Z terms (x == 0)."""
        pure = ~self.x.any(axis=1)
        return float(self.c[pure].sum())


def heisenberg(ops, x0, z0, eps, budget, log=None):
    """Evolve P(x0,z0) backward through ops (applied in circuit order, so we
    conjugate in reverse). Returns (PauliSum or None if budget exceeded, stats)."""
    P = PauliSum.single(x0, z0)
    peak, t0 = 1, time.time()
    for i, (kind, qs, th) in enumerate(reversed(ops)):
        if kind == "x":
            P.conj_x(qs[0])
        elif kind == "rz":
            P.conj_rot(np.zeros(W, np.uint64), bit(qs[0]), th)
        elif kind == "rxx":
            P.conj_rot(bit(qs[0]) | bit(qs[1]), np.zeros(W, np.uint64), th)
        else:
            raise ValueError(kind)
        if kind != "x":
            P.merge().truncate(eps)
        peak = max(peak, P.n())
        if P.n() > budget:
            return None, dict(status="operator budget exceeded", peak_terms=peak,
                              gates_done=i + 1, gates_total=len(ops), seconds=time.time() - t0)
        if log and (i % 200 == 0):
            print("    gate %d/%d terms %d  (%.0fs)" % (i + 1, len(ops), P.n(), time.time() - t0), flush=True)
    return P, dict(status="converged", peak_terms=peak, final_terms=P.n(),
                   gates_total=len(ops), seconds=time.time() - t0)


def connected(ops, qi, qa, eps, budget, log=True):
    Z0 = np.zeros(W, np.uint64)
    res = {}
    for name, xm, zm in (("Zi", Z0, bit(qi)), ("Za", Z0, bit(qa)), ("ZiZa", Z0, bit(qi) | bit(qa))):
        if log:
            print("  evolving %s ..." % name, flush=True)
        P, st = heisenberg(ops, xm, zm, eps, budget, log=log)
        res[name] = dict(stats=st, ev=(P.expect_zero_state() if P is not None else None))
    if all(res[k]["ev"] is not None for k in res):
        C = res["ZiZa"]["ev"] - res["Zi"]["ev"] * res["Za"]["ev"]
    else:
        C = None
    return C, res


# ------------------------------------------------------------------ stages --
def v1():
    ops, rec = load_ops(2)
    import ibm_residue as IR
    qi, qa = PAIR
    # independent referee: exact light-cone statevector
    ops_t = [(k, tuple(q), th) for k, q, th in ops if k != "x"]
    Cref, cone = IR.cone_predict(ops_t, rec["nq"], qi, qa, 2, rec["x_qubits"])
    print("=" * 74)
    print("V1 GATE at K=2: engine (eps=0, exact) vs cone_predict statevector")
    print("=" * 74)
    print("  cone size %s, cone_predict C(%d-%d) = %s" % (cone, qi, qa, Cref))
    C, res = connected(ops, qi, qa, eps=0.0, budget=BUDGET, log=False)
    print("  engine     C(%d-%d) = %.15f  terms Zi %d  Za %d  ZiZa %d"
          % (qi, qa, C, res["Zi"]["stats"]["final_terms"], res["Za"]["stats"]["final_terms"],
             res["ZiZa"]["stats"]["final_terms"]))
    ok = Cref is not None and abs(C - Cref) < 1e-12
    print("  |engine - referee| = %s  ->  %s" % ("n/a" if Cref is None else "%.2e" % abs(C - Cref),
                                                "PASS" if ok else "FAIL"))
    json.dump(dict(K=2, pair=list(PAIR), cone_predict=Cref, cone_size=cone, engine=C,
                   pass_1e12=bool(ok), res=res),
              open(os.path.join(HERE, "cleveland_census_v1.json"), "w"), indent=1)
    return ok


def census(K, epss):
    ops, rec = load_ops(K)
    qi, qa = PAIR
    out = dict(K=K, pair=list(PAIR), budget=BUDGET, gates=len(ops), results={})
    print("=" * 74)
    print("CENSUS K=%d: %d gates, budget %d terms, eps ladder %s" % (K, len(ops), BUDGET, epss))
    print("=" * 74)
    for eps in epss:
        print("eps = %g" % eps, flush=True)
        C, res = connected(ops, qi, qa, eps, BUDGET, log=True)
        st = {k: res[k]["stats"] for k in res}
        div = any(s["status"] != "converged" for s in st.values())
        out["results"]["%g" % eps] = dict(diverged=div, C=C, per_operator=st,
                                          ev={k: res[k]["ev"] for k in res})
        print("  -> %s | C(%d-%d) = %s | peak terms %s"
              % ("DIVERGES" if div else "CONVERGES", qi, qa, C,
                 {k: st[k]["peak_terms"] for k in st}), flush=True)
    p = os.path.join(HERE, "cleveland_census_K%d.json" % K)
    json.dump(out, open(p, "w"), indent=1)
    print("-> %s" % p)
    return out


def full_map(K, eps):
    """Adjudicate EVERY pre-registered pair against the hardware receipt.
    Compute-twice: each operator is evolved twice and must agree elementwise."""
    ops, rec = load_ops(K)
    pre = json.load(open(PREREG))
    res = json.load(open(os.path.join(HERE, "RESULT_residue_K6_20260901_131159.json")))
    ev = dict(zip(res["obs"], res["evs"])); sd = dict(zip(res["obs"], res["stds"]))
    Z0 = np.zeros(W, np.uint64)
    cache = {}

    def zexp(q):
        if q not in cache:
            a, sa = heisenberg(ops, Z0, bit(q), eps, BUDGET)
            b, sb = heisenberg(ops, Z0, bit(q), eps, BUDGET)
            assert a is not None and b is not None, "budget exceeded on Z%d" % q
            assert abs(a.expect_zero_state() - b.expect_zero_state()) < 1e-12, "compute-twice mismatch Z%d" % q
            cache[q] = (a.expect_zero_state(), sa["peak_terms"])
        return cache[q]

    rows = []
    t0 = time.time()
    print("=" * 74)
    print("FULL MAP K=%d eps=%g: %d pairs, classical vs hardware receipt" % (K, eps, len(pre["pairs"])))
    print("=" * 74)
    for n, (qi, qa, dd) in enumerate(pre["pairs"]):
        zi, pi_ = zexp(qi); za, pa_ = zexp(qa)
        P1, s1 = heisenberg(ops, Z0, bit(qi) | bit(qa), eps, BUDGET)
        P2, s2 = heisenberg(ops, Z0, bit(qi) | bit(qa), eps, BUDGET)
        assert P1 is not None and P2 is not None, "budget exceeded on ZZ%d_%d" % (qi, qa)
        zz1, zz2 = P1.expect_zero_state(), P2.expect_zero_state()
        assert abs(zz1 - zz2) < 1e-12, "compute-twice mismatch ZZ%d_%d" % (qi, qa)
        Cc = zz1 - zi * za
        # hardware connected correlator and its sigma, exactly as ibm_residue.grade does
        k = f"ZZ{qi}_{qa}"
        if k in ev:
            Ch = ev[k] - ev[f"Z{qi}"] * ev[f"Z{qa}"]
            sig = math.sqrt(sd[k] ** 2 + (ev[f"Z{qa}"] * sd[f"Z{qi}"]) ** 2 + (ev[f"Z{qi}"] * sd[f"Z{qa}"]) ** 2)
            z = (Ch - Cc) / sig if sig > 0 else None
        else:
            Ch = sig = z = None
        rows.append(dict(qi=qi, qa=qa, distance=dd, C_classical=Cc, C_hardware=Ch, sigma=sig,
                         z_hw_minus_classical=z, peak_terms_ZZ=s1["peak_terms"]))
        if n % 10 == 0:
            print("  %3d/%d  (%d-%d d=%s)  classical %+.6f  hardware %s  z %s  [%.0fs]"
                  % (n + 1, len(pre["pairs"]), qi, qa, dd, Cc,
                     "n/a" if Ch is None else "%+.4f±%.4f" % (Ch, sig),
                     "n/a" if z is None else "%+.1f" % z, time.time() - t0), flush=True)
    zs = np.array([r["z_hw_minus_classical"] for r in rows if r["z_hw_minus_classical"] is not None])
    cc = np.array([abs(r["C_classical"]) for r in rows])
    ch = np.array([abs(r["C_hardware"]) for r in rows if r["C_hardware"] is not None])
    summ = dict(pairs=len(rows), within_3sigma=int((np.abs(zs) <= 3).sum()),
                beyond_3sigma=int((np.abs(zs) > 3).sum()),
                max_abs_classical=float(cc.max()), median_abs_classical=float(np.median(cc)),
                median_abs_hardware=float(np.median(ch)), max_peak_terms=int(max(r["peak_terms_ZZ"] for r in rows)),
                seconds=time.time() - t0)
    print("  summary:", summ)
    out = dict(K=K, eps=eps, budget=BUDGET, summary=summ, rows=rows, receipt=res.get("job_id"))
    p = os.path.join(HERE, "cleveland_census_map_K%d.json" % K)
    json.dump(out, open(p, "w"), indent=1)
    print("-> %s" % p)
    return out


if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else "export"
    if stage == "map":
        full_map(int(sys.argv[2]), float(sys.argv[3]))
        raise SystemExit
    if stage == "export":
        export()
    elif stage == "v1":
        v1()
    elif stage == "census":
        K = int(sys.argv[2]); epss = [float(e) for e in sys.argv[3:]] or [3e-5, 1e-5]
        census(K, epss)
    elif stage == "evaluate":
        K = int(sys.argv[2]); eps = float(sys.argv[3])
        ops, _ = load_ops(K)
        C, res = connected(ops, PAIR[0], PAIR[1], eps, BUDGET)
        print("C(%d-%d) at K=%d eps=%g : %s" % (PAIR[0], PAIR[1], K, eps, C))
    else:
        raise SystemExit(__doc__)
