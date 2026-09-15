# Draft-checklist close-out

The 2026-09-04 dossier listed four open boxes. Status after this package:

| Item | Was | Now |
|---|---|---|
| Cross-vendor superconducting (Rigetti) | open → later marked done | **CLOSED** — structure PASS, amplitude FAIL, job id archived |
| Trapped-ion (IonQ / AQT) | open | **SPLIT** — AQT harvested FAIL; IonQ Forte still UNRUN |
| Five-target Dirac | open → later marked done | **CLOSED** — four PASS on pass 1; myosin refine required (receipted) |
| IBM maps for remaining 4 targets | open | **PROTOCOL ONLY** — `python protocol/ibm_four_maps.py fly6 TARGET` |
| Assemble narrative + figures | open | **CLOSED** — report v4 + fig1–fig4 from headlines.json |
| R1–R3 IBM job ids | stdout only | **CLOSED** — recovered 2026-09-08 by exact evs match |

## Physics-gate items added by the Mitsubishi/first-principles review

| Item | Status |
|---|---|
| Drop v4+ biology / HexaGene layers | **CLOSED** — `PHYSICS.md`, package excludes those trees |
| Lock claims to real jobs | **CLOSED** — unmarked where missing; recovered ids matched, not guessed |
| Backend correction ibm_fez vs marrakesh | **CLOSED** |
| SKEMPI +0.51 not a headline | **CLOSED** — dropped |
| Derived AUC predictor | **CLOSED** — dropped (gate FAIL) |
| Bound the 2⁹⁹ line | **CLOSED** — exhibit |

## Still required before a sendable qBraid zip

1. IonQ Forte RESULT with job id (or a written withdrawal of the card).
   One command: `python protocol/ionq_quench.py fly`
2. Four IBM K=6 RESULT files with job ids, or a written withdrawal.
   One command each: `python protocol/ibm_four_maps.py fly6 <TARGET>`

Until (1) and (2) land, sendability = **HOLD**. R1–R3 ids and the AQT
FAIL receipt are now in the zip; the package is otherwise complete enough
to send the moment those two protocol families are filled or withdrawn.
