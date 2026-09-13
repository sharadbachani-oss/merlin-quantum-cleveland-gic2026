# Hardware-native maps

One derived force graph U, three encodings. Each device runs the face it
was built for. No routing on the 156q cards. No invented backends.

## Maps that ran

| Map | Device | Encoding | Native object | Depth / width | Artifact |
|---|---|---|---|---|---|
| 11-cell swap-net quench | ibm_marrakesh | all-to-all RXX via swap network | C(i,a) | 166 2q / 11q | R1 |
| Residue native-edge K=2 | **ibm_fez** | annealed residue→qubit on heavy-hex; RXX on coupling-map edges only | C(i,a) vs exact cone | 238 2q / 156q | R2 |
| Residue native-edge K=6 | **ibm_fez** | same assignment, K=6 | C(i,a) front d=1..22 | 694 2q / 156q; ≤54 2q/qubit | R3 |
| Mediated response (I−GU)x = e_act | QCi Dirac-3 | continuous polynomial / sum constraint | cosine vs exact x | 339–949 vars | R6 |
| Line-embedded chain | Rigetti Cepheus-1-108q | 107q line, 318 2q | structure vs cone | depth 6/qubit | R7 |
| Geometry-as-H | QuEra Aquila | Cα → atom xy at 5 μm blockade pitch; native 1/r⁶ | connected ⟨nᵢnₐ⟩ | 10 + 60 atoms | R8 |
| 11-cell 288-native-2q quench | AQT ibex-q1 | all-to-all RXX, zero routing | C(i,a) | 288 2q / 11q | AQT FAIL |

Open-plan spend guard for any new IBM flight: `{ibm_fez, ibm_marrakesh, ibm_kingston}` only.

## Maps written, not flown

| Map | Device | Protocol | Status |
|---|---|---|---|
| 11-cell 288-native-2q quench | IonQ Forte (all-to-all, no routing) | `python protocol/ionq_quench.py fly` | **UNRUN** |
| Residue K=6 | ibm_fez/marrakesh/kingston × {BCR_ABL1, CARDIAC_MYOSIN, GLUCOKINASE, CDK2} | `python protocol/ibm_four_maps.py fly6 TARGET` | **UNRUN** |

## Why these maps are native (first-principles doctrine)

- Heavy-hex: interactions restricted to the coupling map. The assignment
  maximises retained \|U\| on existing edges. Zero SWAP in the K=2/K=6 flights.
- Rydberg: the register *is* the molecular geometry. No gate compilation.
- Dirac: the device's native quadratic is the resolvent residual, not a
  QUBO bit-packing of a classical ML feature.
- Exact prep of the 6-qubit operator (3 CNOTs) is the L0 witness, not the
  156q flight. The 156q flight is a **derived-force** embedding of that
  same operator class onto a contact graph.
