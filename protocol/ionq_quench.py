#!/usr/bin/env python3
"""
EXACT one-command protocol for the IonQ Forte cross-vendor quench.

Status: UNRUN. No RESULT_ionq_*.json exists. Do not invent a result.

Cancelled Open-Quantum IonQ PENDING ids (no counts — keep UNRUN):
  openquantum:ionq:qpu:forte-1-5879-qjob-6a95dfa520aa7d3794bb67c7
  openquantum:ionq:qpu:forte-1-5879-qjob-6a95e1c720aa7d3794bb67d4
  openquantum:ionq:qpu:forte-1-5879-qjob-6a95e3e720aa7d3794bb67ef

AQT ibex-q1 under the same sha completed and was harvested separately
(RESULT_aqt_20260904_081407.json, grade FAIL). Do not treat AQT as IonQ.

One-command flight (paid; do not run unless you intend to submit):

    python protocol/ionq_quench.py fly

Forces QALLO_ROUTES=openquantum:ionq:qpu:forte-1 and QALLO_SHOTS=512,
then calls cleaveland/v2/quantum_allostery.py fly_ionq. Writes PENDING
with job_id. After completion:

    python protocol/ionq_quench.py harvest PENDING.json
    python ..\\cleaveland\\v2\\quantum_allostery.py grade RESULT_ionq_*.json
"""
from __future__ import annotations

import json
import os
import sys
import time

PREREG_SHA = "82dbe4fffcf3add24c161609af97c0e8f841d88651c2036b786b33f9990d3013"
DEVICE = "openquantum:ionq:qpu:forte-1"
N_2Q_NATIVE = 288
SHOTS = 512
CANCELLED_IONQ = (
    "openquantum:ionq:qpu:forte-1-5879-qjob-6a95dfa520aa7d3794bb67c7",
    "openquantum:ionq:qpu:forte-1-5879-qjob-6a95e1c720aa7d3794bb67d4",
    "openquantum:ionq:qpu:forte-1-5879-qjob-6a95e3e720aa7d3794bb67ef",
)
AQT_COMPLETED_FAIL = "openquantum:aqt:qpu:ibex-q1-5879-qjob-6a99b67ae026787d1e5ae3d5"
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
V2 = os.path.normpath(os.path.join(PKG, "..", "cleaveland", "v2"))


def card():
    return {
        "status": "UNRUN",
        "device": DEVICE,
        "prereg_sha": PREREG_SHA,
        "n_2q_native": N_2Q_NATIVE,
        "shots": SHOTS,
        "construction": "11-cell swap-network quench, all-to-all, zero routing",
        "grade_rule": (
            "same bands as PREREG_quantum_allostery / R1 sampler form; "
            "PASS if >=70% signal in-band and top-3 overlap >=2"
        ),
        "job_id": None,
        "cancelled_ionq_pending": list(CANCELLED_IONQ),
        "aqt_completed_fail": AQT_COMPLETED_FAIL,
        "fly_command": "python protocol/ionq_quench.py fly",
    }


def fly():
    """Submit IonQ Forte only. Paid. Writes PENDING with job_id."""
    os.environ["QALLO_ROUTES"] = DEVICE
    os.environ["QALLO_SHOTS"] = str(SHOTS)
    sys.path.insert(0, V2)
    import quantum_allostery as QA
    QA.fly_ionq()


def harvest(pending_path):
    """Pull counts for an existing PENDING job. No new submit."""
    from qbraid.runtime import QbraidProvider

    pend = json.load(open(pending_path, encoding="utf-8"))
    jid = pend["job_id"]
    p = QbraidProvider()
    r = p.client.get_job_result(jid)
    d = r.model_dump() if hasattr(r, "model_dump") else dict(r)
    counts = (d.get("resultData") or {}).get("measurementCounts")
    if not counts:
        raise SystemExit("no measurementCounts yet for " + jid)
    out = {
        "lane": "ionq" if "ionq" in str(pend.get("device", "")).lower() else "aqt",
        "device": pend.get("device"),
        "job_id": jid,
        "prereg_sha": pend.get("prereg_sha"),
        "n_2q_native": pend.get("n_2q_native", N_2Q_NATIVE),
        "shots": int(sum(int(v) for v in counts.values())),
        "counts": {str(k): int(v) for k, v in counts.items()},
        "retrieved": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    dest = os.path.join(
        V2, "RESULT_%s_%s.json" % (out["lane"], time.strftime("%Y%m%d_%H%M%S"))
    )
    json.dump(out, open(dest, "w"), indent=1)
    print("saved ->", dest, "job", jid, "shots", out["shots"])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    if cmd == "fly":
        fly()
    elif cmd == "harvest":
        harvest(sys.argv[2])
    else:
        c = card()
        print("IONQ QUENCH PROTOCOL (unrun)")
        for k, v in c.items():
            print(f"  {k}: {v}")
        print("one command: python protocol/ionq_quench.py fly")
