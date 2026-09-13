"""One-shot extractor: headline numbers from existing Cleveland artifacts."""
from __future__ import annotations

import json
import math
import os

import numpy as np

SRC = r"C:\quantum ai 2026\cleaveland\v2"
OUT = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(OUT, exist_ok=True)


def load(name):
    return json.load(open(os.path.join(SRC, name), encoding="utf-8"))


def connected(evd, sdd, qi, qa):
    zz = f"ZZ{qi}_{qa}"
    if zz not in evd:
        zz = f"ZZ{qa}_{qi}"
    c = evd[zz] - evd[f"Z{qi}"] * evd[f"Z{qa}"]
    sig = math.sqrt(
        sdd[zz] ** 2
        + (evd[f"Z{qa}"] * sdd[f"Z{qi}"]) ** 2
        + (evd[f"Z{qi}"] * sdd[f"Z{qa}"]) ** 2
    )
    return c, sig


def operator_block():
    n, dim = 6, 64
    a6 = np.zeros((dim, dim))
    for s in range(dim):
        for b in range(n):
            a6[s, s ^ (1 << b)] = 1.0
    d = np.diag([bin((s & 7) ^ (s >> 3)).count("1") for s in range(dim)]).astype(float)
    mu = 3.0 / (3.0 - math.sqrt(5.0))
    w = mu * d - a6
    ev = np.linalg.eigvalsh(w)
    delta = math.sqrt((mu / 2) ** 2 + 4) - mu / 2
    chi = math.atan(delta / 2)
    return {
        "kappa": mu,
        "E0": float(ev[0]),
        "gap": float(ev[1] - ev[0]),
        "delta": delta,
        "chi": chi,
        "theta_star": math.pi / 2 - 2 * chi,
        "n_kinetic_edges": int(a6.sum() / 2),
        "prep": "exact RY(theta*)-CNOT-H⊗H per pair; 3 CNOTs total",
    }


def k2_block():
    pre = load("PREREG_residue_K2.json")
    res = load("RESULT_residue_K2_20260901_104204.json")
    evd = dict(zip(res["obs"], res["evs"]))
    sdd = dict(zip(res["obs"], res["stds"]))
    rows = []
    inband = nsig = 0
    for qi, qa, dd in pre["pairs"]:
        key = f"{qi}-{qa}"
        if f"ZZ{qi}_{qa}" not in evd and f"ZZ{qa}_{qi}" not in evd:
            continue
        c, sig = connected(evd, sdd, qi, qa)
        pred = pre["pred_connected"].get(key)
        band = 3.0 * sig + 0.03
        row = {
            "pair": key,
            "d": dd,
            "C": c,
            "sigma": sig,
            "pred": pred,
            "cone": pre["cone_sizes"].get(key),
        }
        if pred is not None and abs(pred) > 0.077:
            nsig += 1
            ok = abs(c - pred) <= band
            inband += int(ok)
            row["in_band"] = ok
        rows.append(row)
    return {
        "backend": res["backend"],
        "prereg_sha": res["prereg_sha"],
        "job_id": res.get("job_id"),
        "job_id_in_artifact": "job_id" in res,
        "n_2q": res["n_2q"],
        "shots": res["shots"],
        "n_qubits": pre["n_qubits_used"],
        "signal_pairs": nsig,
        "in_band": inband,
        "pairs": rows,
    }


def k6_block():
    pre = load("PREREG_residue_K6.json")
    res = load("RESULT_residue_K6_20260901_131159.json")
    evd = dict(zip(res["obs"], res["evs"]))
    sdd = dict(zip(res["obs"], res["stds"]))
    rows = []
    for qi, qa, dd in pre["pairs"]:
        if f"ZZ{qi}_{qa}" not in evd and f"ZZ{qa}_{qi}" not in evd:
            continue
        c, sig = connected(evd, sdd, qi, qa)
        rows.append(
            {
                "pair": f"{qi}-{qa}",
                "d": dd,
                "C": c,
                "sigma": sig,
                "nsigma": abs(c) / sig if sig else 0.0,
            }
        )
    front = [r for r in rows if r["pair"] == "28-7" or r["pair"] == "7-28"]
    by_d = {}
    for r in rows:
        by_d.setdefault(r["d"], []).append(r)
    best_by_d = {
        str(d): max(v, key=lambda z: z["nsigma"]) for d, v in sorted(by_d.items())
    }
    return {
        "backend": res["backend"],
        "prereg_sha": res["prereg_sha"],
        "job_id": res.get("job_id"),
        "job_id_in_artifact": "job_id" in res,
        "n_2q": res["n_2q"],
        "shots": res["shots"],
        "n_qubits": pre["n_qubits_used"],
        "n_pairs_graded": len(rows),
        "n_pairs_prereg": len(pre["pairs"]),
        "headline": front[0] if front else None,
        "best_by_distance": best_by_d,
        "pairs": rows,
    }


def est_block():
    pre = load("PREREG_ibm_estimator.json")
    res = load("RESULT_est_20260901_014249.json")
    order = pre["final_order"]
    pos_of = {order[p]: p for p in range(pre["N_cells"])}
    evd = dict(zip(res["obs"], res["evs"]))
    sdd = dict(zip(res["obs"], res["stds"]))
    rows = []
    inband = nsig = 0
    for k, pv in pre["pred_connected"].items():
        i, a = map(int, k.split("-"))
        pi, pa = pos_of[i], pos_of[a]
        zz = "ZZ%d_%d" % tuple(sorted((pi, pa)))
        if zz not in evd:
            zz = "ZZ%d_%d" % tuple(sorted((pi, pa), reverse=True))
        if zz not in evd:
            continue
        c = evd[zz] - evd["Z%d" % pi] * evd["Z%d" % pa]
        sig = math.sqrt(
            sdd[zz] ** 2
            + (evd["Z%d" % pa] * sdd["Z%d" % pi]) ** 2
            + (evd["Z%d" % pi] * sdd["Z%d" % pa]) ** 2
        )
        band = 3.0 * sig + 0.03
        signal = abs(pv) > 0.077
        ok = abs(c - pv) <= band if signal else None
        if signal:
            nsig += 1
            inband += int(ok)
        rows.append({"pair": k, "pred": pv, "C": c, "sigma": sig, "signal": signal, "in_band": ok})
    headline = next((r for r in rows if r["pair"] in ("1-0", "0-1")), rows[0] if rows else None)
    return {
        "backend": res["backend"],
        "prereg_sha": res["prereg_sha"],
        "job_id": res.get("job_id"),
        "job_id_in_artifact": "job_id" in res,
        "n_2q": res["n_2q"],
        "shots": res["shots"],
        "U_over_kT": pre["regime"]["U_over_kT"],
        "signal_pairs": nsig,
        "in_band": inband,
        "headline": headline,
        "pairs": rows,
    }


def dirac_one(inst_name, res_name):
    inst = load(inst_name)
    res = load(res_name)
    n = inst["n_res"]
    k = int(np.argmin(res["energies"]))
    v = np.array(res["solutions"][k], float)
    x = v[:n] - v[n : 2 * n]
    xe = np.array(inst["x_exact"])
    e = float(res["energies"][k])
    cos = float(x @ xe / (np.linalg.norm(x) * np.linalg.norm(xe) + 1e-12))
    gap = (e - inst["exact_obj"]) / abs(inst["exact_obj"])
    return {
        "target": inst["target"],
        "n_vars": inst["n_vars"],
        "n_res": n,
        "job_id": res["job_id"],
        "prereg_sha": res["prereg_sha"],
        "E_best": e,
        "exact_obj": inst["exact_obj"],
        "obj_gap_frac": gap,
        "cosine": cos,
        "G1": e <= inst["exact_obj"] + 0.1 * abs(inst["exact_obj"]),
        "G2": cos >= 0.90,
    }


def dirac_block():
    rows = [
        dirac_one("dirac_response_instance.json", "RESULT_response_20260901_114112.json"),
        dirac_one(
            "dirac_response_instance_GLUCOKINASE.json",
            "RESULT_response_GLUCOKINASE_20260901_140512.json",
        ),
        dirac_one(
            "dirac_response_instance_CDK2.json",
            "RESULT_response_CDK2_20260901_141126.json",
        ),
        dirac_one(
            "dirac_response_instance_BCR_ABL1.json",
            "RESULT_response_BCR_ABL1_20260901_144131.json",
        ),
        dirac_one(
            "dirac_response_instance_CARDIAC_MYOSIN.json",
            "RESULT_response_CARDIAC_MYOSIN_20260901_161116.json",
        ),
    ]
    refine = load("RESULT_refine_CARDIAC_MYOSIN_20260901_173231.json")
    inst_m = load("dirac_response_instance_CARDIAC_MYOSIN.json")
    pre_r = load("PREREG_dirac_refine_CARDIAC_MYOSIN.json")
    n = inst_m["n_res"]
    x0 = np.array(pre_r["x0"], float)
    Q = np.array(inst_m["Q"])
    c = np.array(inst_m["c"])
    xe = np.array(inst_m["x_exact"])
    best, bobj = None, None
    for sol in refine["solutions"]:
        v = np.array(sol, float)
        d = v[:n] - v[n : 2 * n]
        x = x0 + d
        obj = float(x @ Q @ x - 2 * c @ x)
        if bobj is None or obj < bobj:
            best, bobj = x, obj
    return {
        "targets": rows,
        "myosin_refine_job_id": refine["job_id"],
        "myosin_refine_prereg_sha": refine["prereg_sha"],
        "myosin_refine_cosine": float(
            best @ xe / (np.linalg.norm(best) * np.linalg.norm(xe) + 1e-12)
        ),
        "myosin_refine_obj": bobj,
        "myosin_refine_exact_obj": inst_m["exact_obj"],
    }


def aquila_block():
    pre = load("PREREG_aquila_v2.json")
    raw = load("RAW_aquila_v2.json")
    pending = load("PENDING_aquilav2_20260904_123916.json")

    def occ_matrix(counts):
        rows = []
        for s, c in counts.items():
            v = np.array(
                [1.0 if ch == "r" else (0.0 if ch == "g" else np.nan) for ch in s]
            )
            rows.extend([v] * int(c))
        return np.array(rows)

    def conn(R, i, a):
        m = ~np.isnan(R[:, i]) & ~np.isnan(R[:, a])
        if m.sum() < 20:
            return float("nan"), 0
        x, y = R[m, i], R[m, a]
        return float((x * y).mean() - x.mean() * y.mean()), int(m.sum())

    R0 = occ_matrix(raw["results"]["T0"]["measurementCounts"])
    preds = pre["pred_cluster_connected"]
    strong = sorted(preds.items(), key=lambda z: -abs(z[1]))[:8]
    rho = float(np.nanmean(R0))
    inb = nsig = nsign = 0
    t0_rows = []
    for k, pv in strong:
        i, a = map(int, k.split("-"))
        hv, n = conn(R0, i, a)
        if np.isnan(hv):
            continue
        sig = math.sqrt(max(rho * rho * (1 - rho * rho), 0.01)) / math.sqrt(n)
        band = 3.0 * sig + 0.02
        signal = abs(pv) > band
        ok = abs(hv - pv) <= band if signal else None
        if signal:
            nsig += 1
            inb += int(ok)
            nsign += int(np.sign(pv) == np.sign(hv))
        t0_rows.append(
            {"pair": k, "pred": pv, "hw": hv, "band": band, "signal": signal, "in_band": ok}
        )
    geo = load("aquila_v2_geometry.json")
    R1 = occ_matrix(raw["results"]["T1"]["measurementCounts"])
    pos = np.array(geo["positions_um"])
    act = set(geo["active_idx"])
    n_at = R1.shape[1]
    anchors = [a for a in geo["active_idx"] if a < n_at][:3]
    near, far = [], []
    for a in anchors:
        for i in range(n_at):
            if i == a or i in act:
                continue
            d = float(np.linalg.norm(pos[i] - pos[a]))
            hv, n = conn(R1, i, a)
            if np.isnan(hv):
                continue
            if d < 12:
                near.append(abs(hv))
            elif d >= 30:
                far.append(abs(hv))
    return {
        "prereg_sha": raw["prereg_sha"],
        "T0_task_id": pending["tasks"]["T0"]["task_id"],
        "T1_task_id": pending["tasks"]["T1"]["task_id"],
        "T0_shots": int(R0.shape[0]),
        "T0_signal": nsig,
        "T0_in_band": inb,
        "T0_signs": nsign,
        "T0_rows": t0_rows,
        "T1_near_mean_absC": float(np.mean(near)) if near else None,
        "T1_far_mean_absC": float(np.mean(far)) if far else None,
        "T1_ratio": float(np.mean(near) / np.mean(far)) if near and far else None,
        "T1_n_atoms": int(R1.shape[1]),
    }


def rigetti_block():
    res = load("RESULT_rigetti_final.json")
    return {
        "device": res["device"],
        "job_id": res["job_id"],
        "prereg_sha": res["prereg_sha"],
        "note": "structure pass documented in RESULTS_DOSSIER; amplitude gate FAILED",
    }


def aqt_block():
    res = load("RESULT_aqt_20260904_081407.json")
    return {
        "device": res["device"],
        "job_id": res["job_id"],
        "prereg_sha": res["prereg_sha"],
        "shots": res["shots"],
        "result_status": "ARCHIVED",
        "verdict": res["grade"]["verdict"],
        "C_1_0": res["grade"]["endian_native"]["C_1_0"],
        "signal_in_band": res["grade"]["endian_native"]["signal_in_band"],
        "top3_overlap": res["grade"]["endian_native"]["top3_overlap"],
        "note": res["grade"]["note"],
    }


def pending_block():
    return {
        "aqt_ibex": aqt_block(),
        "ionq_forte": {
            "status": "UNRUN",
            "cancelled_pending_ids": [
                "openquantum:ionq:qpu:forte-1-5879-qjob-6a95dfa520aa7d3794bb67c7",
                "openquantum:ionq:qpu:forte-1-5879-qjob-6a95e1c720aa7d3794bb67d4",
                "openquantum:ionq:qpu:forte-1-5879-qjob-6a95e3e720aa7d3794bb67ef",
            ],
            "note": "Open-Quantum IonQ jobs cancelled after 30h stall; no RESULT_ionq_*. Do not invent a result. Cancelled ids are PENDING only.",
        },
        "ibm_four_maps": {
            "status": "UNRUN",
            "targets": ["BCR_ABL1", "CARDIAC_MYOSIN", "GLUCOKINASE", "CDK2"],
            "note": "quota-gated; protocol shipped; no RESULT_* files exist",
        },
    }


def main():
    out = {
        "operator": operator_block(),
        "R1_estimator": est_block(),
        "R2_residue_K2": k2_block(),
        "R3_residue_K6": k6_block(),
        "R6_dirac": dirac_block(),
        "R7_rigetti": rigetti_block(),
        "R8_aquila": aquila_block(),
        "R5_aqt": aqt_block(),
        "pending": pending_block(),
        "corrections": {
            "K2_K6_backend": "ibm_fez (RESULT JSON). Draft dossier incorrectly listed ibm_marrakesh.",
            "K2_K6_job_ids": "RECOVERED 2026-09-08 from IBM Runtime by exact evs match: R2 dab6vi34clkc73fij1ig, R3 dab7i5mrrl7c7386gfh0.",
            "R1_job_id": "RECOVERED 2026-09-08 from IBM Runtime by exact evs match: daaui7bvpcac73dd29r0.",
            "SKEMPI": "Do not quote +0.51 as the full-set figure. Referee note: +0.51 was 78-cycle nonzero subset; 213-cycle pooled signed rho is +0.342 (pure_interactions / ATLAS_REFEREE_REPLY).",
            "derived_AUC_gate": "allosteric_derived_results.json: pocket-AUC gate FAIL on all five targets. Not a sendable claim.",
            "biology_layers_dropped": "hexagene l12, genome axes, HRS onset, HexaGene cardiac product, codon/v4+ overlays excluded from this package.",
        },
    }
    path = os.path.join(OUT, "headlines.json")
    json.dump(out, open(path, "w"), indent=2)
    k6 = out["R3_residue_K6"]["headline"]
    print("wrote", path)
    print("K2 C(6-7)", [p for p in out["R2_residue_K2"]["pairs"] if p["pair"] == "6-7"])
    print("K6 headline", k6)
    print("EST", out["R1_estimator"]["headline"])
    for t in out["R6_dirac"]["targets"]:
        print("DIRAC", t["target"], "cos", round(t["cosine"], 4), "job", t["job_id"])
    print("AQUILA T0", out["R8_aquila"]["T0_in_band"], "/", out["R8_aquila"]["T0_signal"])
    print("AQUILA T1 ratio", out["R8_aquila"]["T1_ratio"])


if __name__ == "__main__":
    main()
