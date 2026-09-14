# Workstation status — cleveland_manybody (2026-09-14, interim)

- `validate`: **PASS** on this box — worst |join − direct| 2.2e-16, **4 pairs with non-zero C** (the
  zero-pairs gap flagged in the START doc is covered). `manybody_validate.json` returned.
- First sweep attempt (MB_WORKERS=30, MB_BUDGET=2.7e7 per the free-RAM formula on this 64 GB box, 46 GB free):
  - **KRAS_G12C failed the hermiticity gate at its first grid point** — `join imaginary part 8.31e-04`
    vs the 1e-8 assert. Reading: at budget 2.7e7 the operator truncation is aggressive enough to break
    hermiticity outright rather than just moving the divergence frontier. You may want the script to
    catch this as "diverged at this budget" rather than a crash.
  - **C_MYC cannot run from this bundle**: `spec["valid"]` is `None` → TypeError in
    `auc_stats.pocket_mask` line 24. Needs the valid-residue spec shipped for C_MYC; skipped.
- Second attempt now running: **MB_WORKERS=6, MB_BUDGET=8e7** (~27 GB worst case), C_MYC skipped,
  other five targets in the prescribed order. Outputs will be returned here as they land, with the
  Verdict section appended at the end.
- Box context: eon57_qaoa_mps (queue job 5) running concurrently; its p=1 result is already POOR at
  every chi — contention slows wall-clocks only.
