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

## Remaining hardware gates

IonQ Forte and four IBM residue maps remain UNRUN. AQT's harvested signal
0.077 versus 0.768 fails; an independent amplitude campaign also failed. Those
records cannot be promoted by the success of a different backend or observable.

The next campaign uses the four named residue maps, a fixed contact perturbation,
common shots and layout, null and coupling-ablation controls, and two independent
runs. Freeze the response and application ranking before submission. Acceptance
requires both the quantitative operator response and a held-out molecular mapping
test; a significant nonzero hardware correlator is only the first gate.

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
