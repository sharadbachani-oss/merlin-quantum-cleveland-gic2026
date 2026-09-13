"""Generate the four submission figures from results/headlines.json."""
from __future__ import annotations

import json
import os

import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
H = json.load(open(os.path.join(HERE, "..", "results", "headlines.json"), encoding="utf-8"))


def fig_k6_front():
    rows = H["R3_residue_K6"]["pairs"]
    by_d = {}
    for r in rows:
        by_d.setdefault(r["d"], []).append(r)
    ds = sorted(by_d)
    mag = [max(abs(x["C"]) for x in by_d[d]) for d in ds]
    sig = [max(x["nsigma"] for x in by_d[d]) for d in ds]
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(ds, mag, "o-", color="#1d4ed8", lw=1.6, ms=4, label="max |C| at distance")
    ax.axvline(11, color="#b45309", ls="--", lw=1, label="d=11  C(28-7) 8.68 sigma")
    ax.set_xlabel("lattice distance from active site")
    ax.set_ylabel("max |C(i, active)|")
    ax.set_title("ibm_fez 156q K=6 connected-correlator front (KRAS)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig1_k6_front.png"), dpi=160)
    plt.close()
    return sig


def fig_dirac():
    rows = H["R6_dirac"]["targets"]
    names = [t["target"].replace("_", " ") for t in rows]
    cos = [t["cosine"] for t in rows]
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    colors = ["#166534" if t["G1"] and t["G2"] else "#b45309" for t in rows]
    ax.barh(names, cos, color=colors)
    ax.axvline(0.90, color="#991b1b", ls="--", lw=1, label="G2 gate 0.90")
    ax.set_xlim(0.88, 1.0)
    ax.set_xlabel("cosine(x_device, x_exact)")
    ax.set_title("Dirac-3 mediated response — five targets (pass-1)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig2_dirac_cosine.png"), dpi=160)
    plt.close()


def fig_aquila():
    rows = [r for r in H["R8_aquila"]["T0_rows"] if r["signal"]]
    # unique undirected pairs
    seen = set()
    uniq = []
    for r in rows:
        a, b = sorted(map(int, r["pair"].split("-")))
        key = (a, b)
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    x = np.arange(len(uniq))
    ax.bar(x - 0.18, [r["pred"] for r in uniq], 0.36, label="pred", color="#6b7280")
    ax.bar(x + 0.18, [r["hw"] for r in uniq], 0.36, label="Aquila T0", color="#7c3aed")
    ax.set_xticks(x)
    ax.set_xticklabels([r["pair"] for r in uniq])
    ax.set_ylabel("connected correlator")
    ax.set_title("Aquila T0 — protein geometry is the Hamiltonian (7/7 in band)")
    ax.legend(fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig3_aquila_t0.png"), dpi=160)
    plt.close()


def fig_status():
    cards = [
        ("R1 11q IBM Marrakesh", "RAN", "daaui7bvpcac73dd29r0"),
        ("R2 156q K=2 ibm_fez", "RAN", "dab6vi34clkc73fij1ig"),
        ("R3 156q K=6 ibm_fez", "RAN", "dab7i5mrrl7c7386gfh0"),
        ("R6 Dirac ×5", "RAN", "job ids archived"),
        ("R7 Rigetti 107q", "RAN", "structure only"),
        ("R8 Aquila T0/T1", "RAN", "task ids archived"),
        ("IonQ Forte quench", "UNRUN", "protocol only"),
        ("AQT ibex-q1", "RAN", "FAIL — amplitude collapsed"),
        ("IBM maps ×4", "UNRUN", "protocol only"),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.axis("off")
    ax.set_title("What ran vs protocol (honest)")
    col = {"RAN": "#166534", "UNRUN": "#991b1b", "QUEUED": "#b45309", "FAIL": "#b45309"}
    for i, (name, st, note) in enumerate(cards):
        ax.text(0.02, 0.92 - i * 0.1, name, fontsize=9, va="center")
        ax.text(0.55, 0.92 - i * 0.1, st, fontsize=9, va="center", color=col[st], fontweight="bold")
        ax.text(0.70, 0.92 - i * 0.1, note, fontsize=8, va="center", color="#4b5563")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "fig4_ran_vs_protocol.png"), dpi=160)
    plt.close()


if __name__ == "__main__":
    fig_k6_front()
    fig_dirac()
    fig_aquila()
    fig_status()
    print("wrote figures/fig1-fig4")
