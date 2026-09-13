#!/usr/bin/env python3
"""
EXACT one-command protocol for the four unflown IBM residue K=6 maps.

Status: UNRUN. No RESULT_* files exist for these targets. Do not invent job ids.

This is the KRAS ibm_residue.py lane (freeze6 / fly6 / report6) with TARGET
swapped. GCK/CDK2 are registered via asd_validation. Per-target PREREG/RESULT
names so KRAS K=6 artifacts are not overwritten. fly() writes job_id.

One command per target (paid; do not run unless you intend to submit):

    python protocol/ibm_four_maps.py freeze6 BCR_ABL1
    python protocol/ibm_four_maps.py fly6 BCR_ABL1
    python protocol/ibm_four_maps.py report6 BCR_ABL1 PATH

Repeat with CARDIAC_MYOSIN / GLUCOKINASE / CDK2.

Allowed backends: ibm_fez, ibm_marrakesh, ibm_kingston.
"""
from __future__ import annotations

import json
import os
import sys
import time

TARGETS = ("BCR_ABL1", "CARDIAC_MYOSIN", "GLUCOKINASE", "CDK2")
ALLOWED_BACKENDS = ("ibm_fez", "ibm_marrakesh", "ibm_kingston")
K = 6
DT = 1.00
SHOTS = 4096
SEED = 21
RESILIENCE = 2
PER_QUBIT_2Q_MAX = 54
HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
V2 = os.path.normpath(os.path.join(PKG, "..", "cleaveland", "v2"))


def _load_residue(target):
    if target not in TARGETS:
        raise SystemExit("TARGET must be one of %s" % (TARGETS,))
    sys.path.insert(0, V2)
    import asd_validation  # noqa: F401  registers GLUCOKINASE + CDK2
    import ibm_residue as R
    R.TARGET = target
    R.DT = DT
    R.SHOTS = SHOTS
    R.SEED = SEED
    return R


def spec(target):
    return {
        "target": target or "<required>",
        "status": "UNRUN",
        "K": K,
        "dt": DT,
        "shots": SHOTS,
        "assignment_seed": SEED,
        "resilience_level": RESILIENCE,
        "per_qubit_2q_max": PER_QUBIT_2Q_MAX,
        "allowed_backends": list(ALLOWED_BACKENDS),
        "embed": "annealed residue->qubit assignment maximizing |U| on native edges; zero routing",
        "pdb": {
            "BCR_ABL1": "1OPL A 242-531",
            "CARDIAC_MYOSIN": "5TBY A",
            "GLUCOKINASE": "1V4T A",
            "CDK2": "1HCL A",
        },
        "job_id_rule": "fly6 writes job_id into RESULT_residue_K6_<TARGET>_*.json",
        "fly_command": "python protocol/ibm_four_maps.py fly6 BCR_ABL1",
    }


def freeze6(target):
    """CPU + IBM coupling-map read. Does not submit a paid Estimator job.
    Writes PREREG_residue_K6_<TARGET>.json (does not overwrite KRAS K=6)."""
    R = _load_residue(target)
    orig = os.path.join(R.HERE, "PREREG_residue_K6.json")
    dest = os.path.join(R.HERE, "PREREG_residue_K6_%s.json" % target)
    keep = None
    if os.path.exists(orig):
        keep = open(orig, "rb").read()
    try:
        R.freeze(6, "report")
        if os.path.exists(orig):
            data = json.load(open(orig, encoding="utf-8"))
            data["target"] = target
            json.dump(data, open(dest, "w"), indent=1)
            print("isolated prereg ->", dest)
    finally:
        if keep is not None:
            open(orig, "wb").write(keep)
            print("restored KRAS", orig)


def fly6(target):
    """Paid EstimatorV2 job. Writes RESULT with job_id. Do not call casually."""
    R = _load_residue(target)
    pre_src = os.path.join(R.HERE, "PREREG_residue_K6_%s.json" % target)
    if not os.path.exists(pre_src):
        raise SystemExit("freeze6 %s first -> %s" % (target, pre_src))
    orig = os.path.join(R.HERE, "PREREG_residue_K6.json")
    keep = open(orig, "rb").read() if os.path.exists(orig) else None
    try:
        open(orig, "w", encoding="utf-8").write(open(pre_src, encoding="utf-8").read())
        R.fly(6)
    finally:
        if keep is not None:
            open(orig, "wb").write(keep)
        # rename the newest RESULT_residue_K6_*.json that now has job_id
        cands = [
            os.path.join(R.HERE, n)
            for n in os.listdir(R.HERE)
            if n.startswith("RESULT_residue_K6_") and n.endswith(".json")
            and target not in n
        ]
        if cands:
            newest = max(cands, key=os.path.getmtime)
            tagged = newest.replace("RESULT_residue_K6_", "RESULT_residue_K6_%s_" % target)
            if newest != tagged:
                os.replace(newest, tagged)
                print("tagged ->", tagged)


def report6(target, path):
    R = _load_residue(target)
    orig = os.path.join(R.HERE, "PREREG_residue_K6.json")
    pre_src = os.path.join(R.HERE, "PREREG_residue_K6_%s.json" % target)
    keep = open(orig, "rb").read() if os.path.exists(orig) else None
    try:
        if os.path.exists(pre_src):
            open(orig, "w", encoding="utf-8").write(open(pre_src, encoding="utf-8").read())
        R.report(6, path)
    finally:
        if keep is not None:
            open(orig, "wb").write(keep)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "show"
    target = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("TARGET", "")
    if cmd == "freeze6":
        freeze6(target)
    elif cmd == "fly6":
        fly6(target)
    elif cmd == "report6":
        report6(target, sys.argv[3])
    else:
        s = spec(target or TARGETS[0])
        print("IBM FOUR-MAP PROTOCOL (unrun)")
        for k, v in s.items():
            print(f"  {k}: {v}")
        print("one command per target:")
        print("  python protocol/ibm_four_maps.py freeze6 BCR_ABL1")
        print("  python protocol/ibm_four_maps.py fly6 BCR_ABL1")
        print("  python protocol/ibm_four_maps.py report6 BCR_ABL1 RESULT.json")
