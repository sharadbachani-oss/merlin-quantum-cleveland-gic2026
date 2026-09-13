"""
verify.py — credential-free audit of every headline number in the Cleveland
package. Reads results/headlines.json (re-derived from RESULT_*/PREREG_*).
No IBM / QCi / Braket credentials.

    python verify.py
    python contact_dynamics.py
"""
from __future__ import annotations

import json
import os
import math

import numpy as np

import contact_dynamics as FC

HERE = os.path.dirname(os.path.abspath(__file__))
H = json.load(open(os.path.join(HERE, "results", "headlines.json"), encoding="utf-8"))
n_pass = n_fail = 0


def check(name, cond, detail=""):
    global n_pass, n_fail
    ok = bool(cond)
    n_pass += int(ok)
    n_fail += int(not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}  {detail}")


print("=" * 64)
print("Cleveland package — headline audit (no credentials)")
print("=" * 64)

print("\n[1] Distilled operator H = kappa . D - A6")
w, a6, _ = FC.assemble_operator()
ev = np.linalg.eigvalsh(w)
spec = FC.exact_prep_spec()
op = H["operator"]
check("kappa", abs(spec["kappa"] - op["kappa"]) < 1e-12, f"{spec['kappa']:.6f}")
check("E0 = -3 delta", abs(ev[0] - spec["E0"]) < 1e-9, f"{ev[0]:+.6f}")
check("gap = delta", abs((ev[1] - ev[0]) - spec["gap"]) < 1e-9, f"{spec['gap']:.6f}")
check("|E(A6)| = 192", int(a6.sum() / 2) == 192)
check("exact prep 3 CNOTs", spec["cnots"] == 3)

print("\n[2] R1 11-cell estimator (ibm_marrakesh, job id recovered)")
e = H["R1_estimator"]
hl = e["headline"]
check("backend ibm_marrakesh", e["backend"] == "ibm_marrakesh")
check("C(1-0) ~ +0.6805", abs(hl["C"] - 0.680456) < 1e-5, f"{hl['C']:+.4f}+-{hl['sigma']:.4f}")
check("vs pred +0.7421 in band", hl["in_band"] is True)
check("3/3 signal in band", e["in_band"] == 3 and e["signal_pairs"] == 3)
check("U/kT ~ 106.6", abs(e["U_over_kT"] - 106.63797) < 1e-3)
check("job id archived", e.get("job_id") == "daaui7bvpcac73dd29r0")

print("\n[3] R2 156q K=2 lightcone (ibm_fez — NOT marrakesh)")
k2 = H["R2_residue_K2"]
p67 = next(p for p in k2["pairs"] if p["pair"] == "6-7")
check("backend ibm_fez", k2["backend"] == "ibm_fez")
check("C(6-7) ~ -0.4584", abs(p67["C"] + 0.45837) < 1e-4, f"{p67['C']:+.4f}+-{p67['sigma']:.4f}")
check("vs cone pred -0.4648 in band", p67["in_band"] is True)
check("job id archived", k2.get("job_id") == "dab6vi34clkc73fij1ig")

print("\n[4] R3 156q K=6 front (ibm_fez, job id recovered)")
k6 = H["R3_residue_K6"]
h6 = k6["headline"]
check("backend ibm_fez", k6["backend"] == "ibm_fez")
check("C(28-7) d=11", h6["pair"] == "28-7" and h6["d"] == 11)
check("C = -0.0757+-0.0087", abs(h6["C"] + 0.075723) < 1e-5, f"{h6['C']:+.4f}+-{h6['sigma']:.4f}")
check("8.68 sigma (report as 8.7)", abs(h6["nsigma"] - 8.68146) < 1e-3, f"{h6['nsigma']:.2f}s")
check("job id archived", k6.get("job_id") == "dab7i5mrrl7c7386gfh0")

print("\n[5] R6 Dirac-3 mediated response (real job ids)")
want = {
    "KRAS_G12C": 0.9973,
    "GLUCOKINASE": 0.9943,
    "CDK2": 0.9649,
    "BCR_ABL1": 0.9684,
}
for t in H["R6_dirac"]["targets"]:
    if t["target"] == "CARDIAC_MYOSIN":
        check("myosin pass-1 G1 FAIL (14% gap)", t["G1"] is False)
        check("myosin pass-1 cosine 0.9267", abs(t["cosine"] - 0.92671) < 1e-4)
        check("myosin pass-1 job", t["job_id"] == "6a96af7408442f441bbb6c8f")
        continue
    check(f"{t['target']} cosine", abs(t["cosine"] - want[t["target"]]) < 5e-4,
          f"{t['cosine']:.4f}  job {t['job_id']}")
    check(f"{t['target']} G1+G2", t["G1"] and t["G2"])
check("myosin refine job archived",
      H["R6_dirac"]["myosin_refine_job_id"] == "6a96c15d08442f441bbb6c91")
check("myosin refine cosine 0.9916",
      abs(H["R6_dirac"]["myosin_refine_cosine"] - 0.99162) < 1e-4)
check("myosin refine gap 1.6%",
      abs(H["R6_dirac"]["myosin_refine_obj"] + 19.6751) < 1e-3)

print("\n[6] R8 Aquila geometry-as-Hamiltonian (task ids archived)")
aq = H["R8_aquila"]
strong = next(r for r in aq["T0_rows"] if r["pair"] == "6-5")
check("T0 7/7 in band", aq["T0_in_band"] == 7 and aq["T0_signal"] == 7)
check("T0 strongest -0.1225 vs -0.1233", abs(strong["hw"] + 0.12247) < 1e-4)
check("T1 near/far ratio 1.50", abs(aq["T1_ratio"] - 1.499) < 1e-2)
check("T0 task id present", "aquila" in aq["T0_task_id"])

print("\n[7] AQT harvested (not IonQ); IonQ + 4 IBM maps stay unmarked")
p = H["pending"]
aqt = p.get("aqt_ibex") or H.get("R5_aqt")
check("AQT result archived", aqt["result_status"] == "ARCHIVED")
check("AQT job id", aqt["job_id"].endswith("6a99b67ae026787d1e5ae3d5"))
check("AQT grade FAIL (not invented PASS)", aqt["verdict"] == "FAIL")
check("IonQ Forte UNRUN", p["ionq_forte"]["status"] == "UNRUN")
check("4 IBM maps UNRUN", p["ibm_four_maps"]["status"] == "UNRUN")

print("\n[8] Honesty corrections shipped")
c = H["corrections"]
check("backend correction", "ibm_fez" in c["K2_K6_backend"])
check("R1-R3 ids recovered not invented", "RECOVERED" in c["K2_K6_job_ids"] and "daaui7b" in c["R1_job_id"])
check("SKEMPI not +0.51 full-set", "+0.342" in c["SKEMPI"])
check("derived AUC gate not claimed", "FAIL" in c["derived_AUC_gate"])

print("\n[9] Frontier leftover protocol — no invented cone death")
k6 = H["R3_residue_K6"]
check("K=6 has no registered cone prediction",
      not k6.get("cone_prediction") and not k6.get("mps_death"),
      "lightcone dimension only")
check("R1/R2 remain the checkable siblings",
      H["R1_estimator"]["headline"]["in_band"] is True
      and next(p for p in H["R2_residue_K2"]["pairs"] if p["pair"] == "6-7")["in_band"] is True)
check("IonQ still UNRUN", H["pending"]["ionq_forte"]["status"] == "UNRUN")
check("four IBM maps still UNRUN", H["pending"]["ibm_four_maps"]["status"] == "UNRUN")
check("AQT still FAIL", (H["pending"].get("aqt_ibex") or H.get("R5_aqt") or {}).get("verdict") == "FAIL")

print("\n[10] Catalytic leftover S_a(w) - local, not a recaption of R3")
lp = os.path.join(HERE, "results", "cleveland_leftover_readout.json")
if os.path.exists(lp):
    L = json.load(open(lp, encoding="utf-8"))
    check("leftover job_id is null", L.get("job_id") is None)
    check("not a hardware advantage", L.get("new_hardware_advantage_demonstrated") is False)
    check("IonQ still UNRUN", (L.get("retrieve") or {}).get("ionq", {}).get("status") == "UNRUN")
    check("AQT still FAIL on leftover card",
          (L.get("retrieve") or {}).get("aqt", {}).get("verdict") == "FAIL")
    loc = L.get("local") or {}
    leftover = loc.get("leftover_k") or []
    check("leftover series is not flat",
          leftover and max(leftover) > 1e-6)
    check("continuation misses realtime leftover",
          loc.get("continuation_misses_realtime") is True)
    check("R3 is not this leftover",
          (L.get("honesty") or {}).get("r3_is_not_leftover") is True)
else:
    check("leftover receipt present", False)

print("\n[11] Dirac geometry leftover — not a relabel of AQT FAIL")
dp = os.path.join(HERE, "results", "cleveland_dirac_leftover.json")
if os.path.exists(dp):
    D = json.load(open(dp, encoding="utf-8"))
    check("no invented Dirac job", D.get("job_id") is None)
    check("not a hardware advantage", D.get("new_hardware_advantage_demonstrated") is False)
    check("AQT not relabeled Dirac",
          (D.get("honesty") or {}).get("aqt_not_relabeled_dirac") is True)
    check("geometry leftover moves",
          (D.get("local_gates") or {}).get("cleveland_geom_moves") is True)
    check("AQT still FAIL in headlines",
          (H["pending"].get("aqt_ibex") or H.get("R5_aqt") or {}).get("verdict") == "FAIL")
else:
    check("dirac leftover receipt present", False)

print("\n[12] Full-W native card (64-cell continuous)")
fw = os.path.join(HERE, "..", "results", "dirac_full_W_flight.json")
if os.path.exists(fw):
    F = json.load(open(fw, encoding="utf-8"))
    check("64-cell sample-hamiltonian",
          F.get("n_vars") == 64 and F.get("job_type") == "sample-hamiltonian")
    check("full-W advantage not claimed",
          F.get("new_hardware_advantage_demonstrated") is False)
    check("PF vacuum not seen", F.get("pf_vacuum_seen") is False)
    leftover = json.load(open(dp, encoding="utf-8")) if os.path.exists(dp) else {}
    check("leftover job_id stays null", leftover.get("job_id") is None)
else:
    check("full-W receipt present", False)

print("\n" + "=" * 64)
print(f"{n_pass} PASS / {n_fail} FAIL")
print("=" * 64)
raise SystemExit(0 if n_fail == 0 else 1)
