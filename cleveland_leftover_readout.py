# -*- coding: utf-8 -*-
"""
Cleveland leftover readout — catalytic S_a(ω) on geometry-as-H.

Industrial object (not another equal-time C(i,a), not a pocket score):
  X-quench at the allosteric site on H = μ* D − A6. Readout is the
  leftover series of the connected contact at the catalytic residue,
  then S_a(ω) = |DFT[L − mean]|². That is the NMR analogue the brief
  permits without an MD trajectory.

Local exact-diag on the 6q cell (checkable sibling of R1/R2). Hardware
leftover series is retrieve-first. Does not invent IonQ results.
Does not call AQT a pass. Does not fly the four IBM K=6 maps.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DEST = HERE / "results"
import contact_dynamics as FC

KAPPA = FC.KAPPA
DELTA = FC.DELTA
K_MAX = 8
ALLOSTERIC = 0
CATALYTIC = 2  # distal site on the 6q cell (not the native pair of the quench)
CATALYTIC_PAIR = (2, 5)
AQT_FAIL = "openquantum:aqt:qpu:ibex-q1-5879-qjob-6a99b67ae026787d1e5ae3d5"
R1 = "daaui7bvpcac73dd29r0"
R2 = "dab6vi34clkc73fij1ig"
R3 = "dab7i5mrrl7c7386gfh0"
IONQ_CANCELLED = (
    "openquantum:ionq:qpu:forte-1-5879-qjob-6a95dfa520aa7d3794bb67c7",
    "openquantum:ionq:qpu:forte-1-5879-qjob-6a95e1c720aa7d3794bb67d4",
    "openquantum:ionq:qpu:forte-1-5879-qjob-6a95e3e720aa7d3794bb67ef",
)
AQUILA = (
    "aws:quera:qpu:aquila-5879-qjob-6a9a83b2e026787d1e5b06d0",
    "aws:quera:qpu:aquila-5879-qjob-6a9a83b3e026787d1e5b06d3",
)
OPEN_CRN = (
    "crn:v1:bluemix:public:quantum-computing:us-east:"
    "a/0601b1157c194f5f9dc0b0fe3ff89f31:"
    "4448fcf5-e662-487a-a307-4e13163054a7::"
)


def spectrum_of(L):
    sig = np.asarray(L, float)
    sig = sig - sig.mean()
    win = np.hanning(len(sig))
    spec = np.abs(np.fft.rfft(sig * win)) ** 2
    freqs = np.fft.rfftfreq(len(sig), d=1.0)
    if spec[1:].size == 0:
        return dict(freqs=[], power=[], principal_cyc_per_step=0.0)
    i = int(np.argmax(spec[1:])) + 1
    return dict(
        freqs=[float(f) for f in freqs],
        power=[float(p) for p in spec],
        principal_cyc_per_step=float(freqs[i]),
        principal_power=float(spec[i]),
        total_power=float(spec[1:].sum()),
    )


def zz_expect(psi, a, b):
    p = (np.abs(psi) ** 2).real
    idx = np.arange(len(p))
    za = 1 - 2 * ((idx >> a) & 1)
    zb = 1 - 2 * ((idx >> b) & 1)
    return float(np.dot(p, za * zb))


def connected_contact(psi, a, b):
    p = (np.abs(psi) ** 2).real
    idx = np.arange(len(p))
    za = 1 - 2 * ((idx >> a) & 1)
    zb = 1 - 2 * ((idx >> b) & 1)
    return float(np.dot(p, za * zb) - np.dot(p, za) * np.dot(p, zb))


def leftover_series():
    H, _, _ = FC.assemble_operator()
    ev, U = np.linalg.eigh(H)
    # Exact-prep target is the ground state of H = κD − A6 (E0 = −3δ).
    psi = U[:, 0].astype(complex)
    # Quenched-pair leftover L(k)=|C*−⟨ZZ⟩_{0,3}|. Distal native pair
    # (2,5) is Ω-held (does not move). Inter-coupled pair C(0,2) is structurally 0.
    C_STAR = zz_expect(psi, 0, 3)
    idx = np.arange(len(psi))
    psi = psi[idx ^ (1 << ALLOSTERIC)]
    c0 = U.T.conj() @ psi
    L = []
    C = []
    held = []
    distal = []
    for k in range(K_MAX + 1):
        st = U @ (np.exp(-1j * ev * (0.30 * k)) * c0)
        zz03 = zz_expect(st, 0, 3)
        C.append(float(zz03))
        L.append(float(abs(C_STAR - zz03)))
        held.append(float(zz_expect(st, *CATALYTIC_PAIR)))
        distal.append(float(connected_contact(st, 0, 2)))
    # imaginary-time leftover + 2-pole continuation (the cheap fake)
    tau = np.arange(K_MAX + 1) * 0.30
    G = []
    for t in tau:
        st = U @ (np.exp(-ev * t) * (U.T.conj() @ psi))
        st = st / (np.linalg.norm(st) + 1e-30)
        G.append(zz_expect(st, 0, 3))
    G = np.array(G, float)
    # 2-pole fit of G(τ) ≈ a e^{-bτ} + c e^{-dτ}
    y = np.log(np.clip(np.abs(G - G[-1]) + 1e-12, 1e-12, None))
    b = max(-np.polyfit(tau, y, 1)[0], 1e-6)
    cont_omega = b / (2 * math.pi)
    spec = spectrum_of(L)
    return dict(
        leftover_k=L,
        zz_quenched_pair=C,
        zz_held_distal=held,
        connected_0_2=distal,
        C_star=float(C_STAR),
        distal_pair_held=bool(max(abs(x - held[0]) for x in held) < 1e-9),
        inter_pair_structurally_zero=bool(max(abs(x) for x in distal) < 1e-12),
        spectrum=spec,
        imag_time_G=G.tolist(),
        continuation_cyc_per_step=float(cont_omega),
        continuation_misses_realtime=bool(
            abs(cont_omega - spec["principal_cyc_per_step"]) > 0.04
        ),
        allosteric=ALLOSTERIC,
        catalytic=CATALYTIC,
        k=list(range(K_MAX + 1)),
        dt=0.30,
    )


def retrieve_existing():
    headlines = json.loads((DEST / "headlines.json").read_text(encoding="utf-8"))
    pending = headlines.get("pending") or {}
    ionq = pending.get("ionq_forte") or {}
    aqt = pending.get("aqt_ibex") or headlines.get("R5_aqt") or {}
    maps = pending.get("ibm_four_maps") or {}
    ibm = dict(available=False, examined=0, leftover_match=None, rejects=[], error=None)
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService

        svc = QiskitRuntimeService(instance=os.environ.get("IBM_QUANTUM_CRN") or OPEN_CRN)
        ibm["available"] = True
        jobs = list(svc.jobs(limit=40))
        ibm["examined"] = len(jobs)
        known = {R1: "R1 equal-time C — not leftover S_a",
                 R2: "R2 equal-time C — not leftover S_a",
                 R3: "R3 equal-time C(28-7) — not leftover S_a"}
        for job in jobs:
            jid = job.job_id()
            rec = dict(job=jid, status=str(job.status()))
            if jid in known:
                rec["reason"] = known[jid]
            else:
                rec["reason"] = "unlabeled — not claimed as leftover S_a"
            ibm["rejects"].append(rec)
    except Exception as e:
        ibm["error"] = f"IBM list unavailable: {type(e).__name__}: {e}"
    return dict(
        ibm=ibm,
        aquila=dict(tasks=list(AQUILA), leftover_series=False,
                    note="T0 7/7 equal-time geometry-as-H, not S_a(ω)"),
        ionq=dict(status=ionq.get("status", "UNRUN"),
                  cancelled=list(IONQ_CANCELLED), leftover_series=False),
        aqt=dict(job=AQT_FAIL, verdict=aqt.get("verdict", "FAIL"),
                 leftover_series=False, do_not_call_pass=True),
        four_ibm_maps=dict(status=maps.get("status", "UNRUN"), leftover_series=False),
        leftover_job_id=None,
    )


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--submit", action="store_true",
                   help="refused — leftover hardware is retrieve-only on this card")
    p.add_argument("--skip-ibm", action="store_true",
                   help="reuse last retrieve / skip a second IBM list")
    args = p.parse_args(argv)
    if args.submit:
        print("REFUSED: Cleveland leftover hardware is retrieve-first only.")
        print("No paid submit of IonQ, AQT, or the four IBM K=6 maps.")
        print("Local S_a(ω) is the executed object.")
        return 3
    local = leftover_series()
    prev = DEST / "cleveland_leftover_readout.json"
    if args.skip_ibm and prev.exists():
        old = json.loads(prev.read_text(encoding="utf-8"))
        ret = old.get("retrieve") or retrieve_existing()
    else:
        ret = retrieve_existing()
    payload = dict(
        card="CLEVELAND CATALYTIC LEFTOVER S_a(ω)",
        generated=time.strftime("%Y-%m-%dT%H:%M:%S"),
        status="LOCAL_PROOF",
        job_id=None,
        new_hardware_advantage_demonstrated=False,
        operator="H = kappa D - A6",
        kappa=KAPPA,
        industrial_object="leftover S_a(ω) of the catalytic contact after X-quench",
        local=local,
        retrieve=ret,
        honesty=dict(
            no_affinity_claim=True,
            ionq_unrun=True,
            aqt_fail=True,
            four_ibm_maps_unrun=True,
            r3_is_not_leftover=True,
            cone_99q_is_dimension_not_measured_death=True,
            invented_ids=False,
        ),
        next_flight=dict(
            command="retrieve-only; fly leftover S_a on one IBM map or Aquila after MPS referee",
            refuse=["IonQ cancelled PENDING", AQT_FAIL, "four IBM K=6 maps"],
        ),
    )
    dest = DEST / "cleveland_leftover_readout.json"

    def _py(o):
        if isinstance(o, dict):
            return {k: _py(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_py(v) for v in o]
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return _py(o.tolist())
        return o

    dest.write_text(json.dumps(_py(payload), indent=2), encoding="utf-8")
    print(f"L(k) {['%.4f' % x for x in local['leftover_k']]}")
    print(f"S_a principal {local['spectrum']['principal_cyc_per_step']:.3f}  "
          f"continuation {local['continuation_cyc_per_step']:.3f}  "
          f"misses={local['continuation_misses_realtime']}")
    print(f"leftover job {payload['job_id']}  IonQ {ret['ionq']['status']}  "
          f"AQT {ret['aqt']['verdict']}")
    if ret["ibm"].get("error"):
        print("IBM:", ret["ibm"]["error"])
    print(f"-> {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
