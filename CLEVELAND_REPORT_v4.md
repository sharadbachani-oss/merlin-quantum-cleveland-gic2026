# Sector-resolved contact-network response with an explicit molecular bridge

Team Merlin Digital | Cleveland | Native physics revision 6 | 10 September 2026

## Delivered evidence

The archived 11-cell experiment reports C(1)-C(0)=0.6805 +/- 0.0234 against
0.7421 predicted, with three signal checks in band. The 156-qubit K=2 result
on ibm_fez reports -0.4584 +/- 0.0076 versus -0.4648. The K=6 front at distance
11 is -0.0757 +/- 0.0087, about 8.7 standard errors from zero. These are measured
operator responses with a declared model, not established clinical predictions.

The mediated-response Dirac results give cosine agreement 0.9973 for KRAS,
0.9943 for glucokinase, 0.9649 for CDK2 and 0.9684 for BCR-ABL1. Myosin's first
pass failed the objective gate at 14%; the refinement reached 1.6%. Both records
remain in the package. The new offline ledger verifier passes 47 checks, which
confirms stored values and attribution rather than independently reproducing jobs.

## Native interpretation

The exact coupled pair supplies a prepared reference, structural kappa and analytically
known nulls. A contact-network perturbation specifies the interacting target.
Sector-resolved response retains exterior influence through the Feshbach term
Sigma(z)=H_PQ(z-H_QQ)^-1 H_QP. Dropping exterior states without that term is a
different approximation. The shared projected_response.py implements the exact
reference identity and has been validated on the framework's actual Omega sector.
Its later application to a molecule requires that molecule's Hamiltonian and a
declared probe; this validation is not a protein calculation.

The existing residue mass table, molecular coordinates, thermal floor and
normalization of site energies are model inputs. The normalization to kT does
not establish a uniquely derived protein interaction. Relative molecular response
must be checked against an independently defined molecular observable before
being described as binding affinity or mutation effect.

## Observable correction: retarded commutator replaces equal-time covariance

Allostery is a causal statement: perturb one residue and a distant one responds
after a delay. The object that says this is the retarded response

    chi_ab(t) = i<[Z_a(t), Z_b(0)]> = -2 Im <Z_a(t) Z_b>

An equal-time connected covariance is a property of the state at one instant,
and a time series of it is not the two-time correlation that defines a response,
so it cannot express a delay. The archived covariance receipts are unchanged and
stand; what changes is which observable the allosteric claim rests on.

Measured exactly on the derived contact operator, 12 residues, 17 edges,
E0=-1.107333, using graph distance on the operator's own connectivity because
the pairing makes sequence separation the wrong metric:

| graph distance | equal-time C_ab | chi(0) | onset time | peak abs chi |
|---:|---:|---:|---:|---:|
| 1 | +0.953498 | 0 | 0.20 | 0.015251 |
| 2 | +0.953055 | 0 | 0.30 | 0.002306 |
| 3 | +0.953049 | 0 | 1.20 | 0.001540 |
| 4 | +0.953041 | 0 | 1.50 | 0.001914 |

The equal-time covariance varies by 0.05% across every distance in the network.
It is large, nearly flat and therefore carries almost no distance information.
The retarded commutator peak varies by 9.9x over the same distances.

chi(0)=0 identically at every distance, because Z_a and Z_b commute at equal
time. That zero is what makes the observable causal: the response grows from
nothing and so has an arrival time, which rises monotonically with graph
distance at 0.20, 0.30, 1.20, 1.50. The covariance has no such structure since
at t=0 it already sits at essentially its full value. An allosteric
communication delay is therefore measurable with this observable and is not
defined with the previous one.

The instrument is realisable as specified: two opposite RZ(pi/2) probes with
local Z readout give exactly i<[Z,Z(t)]>/2 for this Pauli probe, with no
ancilla, no inverse ground-state preparation and no weak-probe extrapolation.
Uncoupled calibration is reproduced by independent matrix evolution to 1.2e-15.

This is exact diagonalisation on a 12-residue operator. It establishes that the
observable is the right one and that it discriminates distance where the
previous one does not. It is not a hardware result, not a validated molecular
interpretation and not an advantage claim. The device version of this probe on
the 156-qubit map is the next artifact.

Receipt: results/commutator_probe_swap.json. Reproduce with
python commutator_probe_swap.py.

## The advantage to establish

The strongest target is a selected, boundary-sensitive response that changes a
ranking between molecular candidates, with the same geometry and target operator
used by the classical and quantum arms. Compare the full response, bare sector,
dressed sector, low-rank approximation and geometry-matched null. This directly
tests the information lost through truncation instead of equating large qubit
count or a lightcone size with a proof of classical intractability.

If a photonic solver returns a simplex-normalized vector, grade the exact
device objective and separately justify the conversion to an L2-normalized
wavefunction or Born probabilities. Similar-looking amplitudes do not make
those constraints equivalent. Ground-state stoquasticity alone neither proves
classical ease nor establishes a quantum advantage.

## Classical comparator arm, measured

The advantage gate needs the other side of the comparison on the same operator,
the same observable and a matched accuracy target. This is it. The classical
method is the matrix-product route, which is the strongest available for a
real-time response, and the accuracy target is 99.9% state fidelity with the
bond dimension taken as the maximum over all cuts.

Two orderings were searched, sequence order and an ordering that keeps each
derived pair adjacent, and the better of the two is reported so the comparison
is the classical method's best case rather than ours.

| residues | edges | chi, sequence | chi, pair-adjacent | best | cap | classical chi^2 N | quantum logical CX |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 8 | 11 | 16 | 14 | 14 | 16 | 1.57e3 | 88 |
| 10 | 14 | 30 | 25 | 25 | 32 | 6.25e3 | 112 |
| 12 | 17 | 57 | 46 | 46 | 64 | 2.54e4 | 136 |

**The two costs scale differently.** Bond dimension grows **1.79x then 1.84x**
per two added residues, against a theoretical cap growth of 2x, so it tracks
the maximum exponential rate at roughly 90%. Reordering to keep pairs adjacent
saves 19% at twelve residues and does not change that rate. The device cost is
8 logical CX per evolved pair, constant in evolution time, growing **1.27x then
1.21x** over the same steps because it is linear in the edge count.

**Why this operator is hard for the classical route, structurally.** Its ground
state is stoquastic, so imaginary-time sampling of the ground state carries no
sign problem and is easy. The retarded response is real-time, where the
cancellation returns. Independently, the derived pairing couples residue i
directly to i + N/2, which is exactly the long-range structure that makes
matrix-product orderings poor. Those are two separate reasons, and rather than
argue from either we measured the cost.

**Scope, stated precisely.** This is a measured cost for this instance family,
this observable, this accuracy target and the orderings searched. It is a
credible classical baseline and a censored benchmark observation. It is not a
complexity proof, and a truncation test is specific to its state, ordering and
tolerance. Physical routing on the device remains a separate cost that is not
included in the CX column.

Receipt: `results/classical_comparator.json`. Reproduce with
`python classical_comparator.py`.

## Remaining hardware gates

IonQ Forte and four IBM residue maps remain UNRUN. AQT's harvested signal
0.077 versus 0.768 fails; an independent amplitude campaign also failed. Those
records cannot be promoted by the success of a different backend or observable.

The next campaign uses the four named residue maps, a fixed contact perturbation,
common shots and layout, null and coupling-ablation controls, and two independent
runs. Freeze the response and application ranking before submission. Acceptance
requires both the quantitative operator response and a held-out molecular mapping
test; a significant nonzero hardware correlator is only the first gate.

## Commercial value

Priced as variant triage on a discovery programme, not as a replacement for
assay.

| input | value | basis |
|---|---|---|
| pre-clinical programme cost | $0.5B - $1.0B | industry range |
| variants screened per campaign | ~200 | programme scale |
| deflection assumed | one in five | conservative |
| wet-lab cost avoided | **$0.2M - $2M per campaign** | deflected variants only |

The saving is wet-lab cost on variants that never enter assay. It is deliberately
narrow, and the reason it is worth having is the second line rather than the
first: a model whose operator constants are derived carries no training
population to re-baseline, so it does not require revalidation as assay data
accumulates. On a GxP computational-model file that is the recurring cost, not
the initial one.

**What we do not claim.** No affinity prediction. No replacement of assay or of
irradiation-style empirical validation. No share of programme value beyond
deflected wet-lab cost. No clinical endpoint.

## Acceptance standard

The physics program fixes the sector, boundary treatment, initial state, operator,
probe, observable and unit map before compilation. Structural kappa is fixed by the
framework; application geometry and scientific interpretation are explicit inputs.
Fixed constants remove refitting of those constants, not the need to validate a
new application or operating condition.

The primary comparison uses the same instance and observable, the same accuracy
target, and total preparation, compilation, execution, readout and post-processing
cost. Exact small-instance calculations anchor the implementation. Direct classical
real-time methods, converged tensor networks and application-specific algorithms
remain eligible comparators. Analytic-continuation failure alone does not exclude
them. Hardware superiority is reported only after its confidence bounds separate
from those of the best matched comparator, with controls and independent replication.

## Reproducibility

This report supersedes earlier narrative claims; original reports are retained in
legacy_reports/. Existing experimental receipts keep their original identity. New
classical model checks are labelled as such and never become cloud results. The
package includes NATIVE_EXPERIMENT.json, EVIDENCE_STATUS.json and the shared
FRAMEWORK_AND_ADVANTAGE.md. Run the shared validate_upgrades.py from the parent
directory to verify integrity and the new mathematical checks. No new hardware
measurement is claimed by this revision.
