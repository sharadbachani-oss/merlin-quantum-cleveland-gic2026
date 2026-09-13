"""Swap the Cleveland observable: equal-time covariance -> retarded commutator.

WHY. Allostery is a CAUSAL statement: perturb one residue, and a distant
residue responds after a delay. The retarded response

    chi_ab(t) = i<[Z_a(t), Z_b(0)]>  =  -2 Im <Z_a(t) Z_b>

is exactly that object. The equal-time connected covariance the package
currently reports is not: it is a property of the state at one instant, and a
time series of it is not the two-time correlation that defines a response.

Two consequences are checked here, both exact, nothing fitted:
  1. chi_ab(0) = 0 identically, because Z_a and Z_b commute at equal time.
     So chi carries an ARRIVAL TIME. The covariance cannot.
  2. distance discrimination: how much each observable varies with graph
     distance on the operator's own connectivity.
"""
import collections, json, math, os
import numpy as np

K = 3.0 / (3.0 - math.sqrt(5.0))
N = 12
pairs = [(i, i + N // 2) for i in range(N // 2)]
contacts = [(i, i + 1) for i in range(N - 1)]
E = sorted({(min(a, b), max(a, b)) for a, b in pairs + contacts})
D = 1 << N
idx = np.arange(D)
zb = [(1 - 2 * ((idx >> i) & 1)).astype(np.float64) for i in range(N)]

diag = np.zeros(D)
for a, b in E:
    diag += 0.5 * (1.0 - zb[a] * zb[b])
H = np.diag(K * diag)
for i in range(N):
    H[idx ^ (1 << i), idx] -= 1.0
ev, U = np.linalg.eigh(H)
g = U[:, 0]
Ut = U.T
A0 = Ut @ g
p = g * g
times = np.linspace(0, 10, 101)
print("operator: N=%d residues, %d edges, E0=%.6f" % (N, len(E), ev[0]), flush=True)

# true graph distance: the pairing makes sequence separation the wrong metric,
# since site i is directly coupled to i + N/2
adj = collections.defaultdict(list)
for a, b in E:
    adj[a].append(b)
    adj[b].append(a)
dist = {0: 0}
q = [0]
while q:
    u = q.pop(0)
    for v in adj[u]:
        if v not in dist:
            dist[v] = dist[u] + 1
            q.append(v)
print("  graph distance from site 0:", dict(sorted((s, dist[s]) for s in range(1, N))),
      flush=True)


def equaltime(a, b):
    return float(p @ (zb[a] * zb[b]) - (p @ zb[a]) * (p @ zb[b]))


def retarded(a, b):
    B = Ut @ (zb[b] * g)
    Za = Ut @ (zb[a][:, None] * U)
    M = (A0[:, None] * Za) * B[None, :]
    dE = ev[:, None] - ev[None, :]
    return np.array([-2.0 * float((M * np.sin(dE * t)).sum()) for t in times])


targets = []
for d in sorted(set(dist[s] for s in range(1, N))):
    targets.append((d, [s for s in range(1, N) if dist[s] == d][0]))

print("\n  graph-d  site   equal-time C_ab    |chi(0)|   onset t   peak |chi|", flush=True)
rows = []
for d, site in targets:
    C = equaltime(0, site)
    chi = retarded(0, site)
    thr = max(0.02 * np.max(np.abs(chi)), 1e-5)
    on = next((times[i] for i in range(len(times)) if abs(chi[i]) > thr), None)
    rows.append(dict(graph_d=d, site=site, C_equaltime=C,
                     chi_at_0=float(abs(chi[0])),
                     onset_t=(float(on) if on is not None else None),
                     chi_peak=float(np.max(np.abs(chi)))))
    print("  %6d   %4d   %+.6f        %.1e   %-7s   %.6f"
          % (d, site, C, abs(chi[0]),
             ("%.2f" % on) if on is not None else "none", np.max(np.abs(chi))),
          flush=True)

Cs = np.array([r["C_equaltime"] for r in rows])
Ps = np.array([r["chi_peak"] for r in rows])
spread = dict(covariance_rel_spread_pct=float(100 * (Cs.max() - Cs.min()) / abs(Cs.mean())),
              commutator_dynamic_range=float(Ps.max() / Ps.min()))
print("\n  DISCRIMINATION ACROSS DISTANCE", flush=True)
print("   equal-time covariance varies by %.2f%% across all distances"
      % spread["covariance_rel_spread_pct"], flush=True)
print("   retarded commutator peak varies by %.1fx across the same distances"
      % spread["commutator_dynamic_range"], flush=True)
print("\n  chi(0) = 0 identically at every distance: Z_a and Z_b commute at", flush=True)
print("  equal time. The covariance is large and nearly flat there, so it", flush=True)
print("  carries almost no distance information and no arrival time.", flush=True)

json.dump(dict(operator=dict(N=N, edges=len(E), kappa=K, E0=float(ev[0])),
               observable="retarded chi_ab(t) = -2 Im <Z_a(t) Z_b>",
               replaces="equal-time connected covariance",
               graph_distance_used=True, rows=rows, discrimination=spread),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "results", "commutator_probe_swap.json"), "w"), indent=1)
print("wrote results/commutator_probe_swap.json", flush=True)
