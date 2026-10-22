# CodePath AI201 — TakeMeter Unit 6 current handoff (updated October 22, 2026)

**This replaces the initial pre-testing checklist.** The authoritative detailed report is in `README.md`; this file is the operational handoff for another agent or the project owner.

## Current progress — verified

| Required artifact | State |
|---|---|
| Original Unit 5 criteria and labels | Preserved in `criteria.md`, `labels.csv`, `label_definitions.txt` |
| Baseline on the original 30 held-out posts | **Measured**, `baseline_results.json`: accuracy 0.1333 |
| 3-seed run with 3 epochs | **Measured**, `results_three_seeds_before.json`: accuracy 0.3667 / 0.4333 / 0.3667 |
| 3-seed single-change improvement with 6 epochs | **Measured**, `results_three_seeds_after.json`: accuracy 0.5333 / 0.5000 / 0.5000 |
| Baseline comparison, confusion matrices, diagnoses, before-vs-after | **Documented** in `README.md` |
| Staff-independent 30-row labels | **Pending human decisions**; `staff_annotation_helper.html` is ready |
| TF reference answers | **Not received**; no `data/staff_labels.csv` |
| Agreement rate and adjudications | **Not performed** until both sets exist |
| Final submission | **Not yet complete** |

Three-epoch to six-epoch training improved mean accuracy from **38.9% to 51.1%**, but `reaction` F1 remains **0** across all three improved seeds. Meeting the originally declared thresholds is *not* required for credit; diagnose misses honestly. Do not invent improved accuracy, staff agreement, or decisions.

## The one essential human step: 30 independent labels

On ZairPlanet, the repository lives at:

`C:\Users\mahjiid\Documents\Projects\CodePath\ai201-project3-takemeter-starter-v2026`

1. Open `staff_annotation_helper.html` in a browser (this was already opened automatically). Read `data/staff_taxonomy.md` to follow staff decision rules rather than the four-label NBA taxonomy. The helper displays those rules for convenience.
2. Choose **analysis**, **hot_take**, or **reaction** on all **30** original running-forum posts. Labels are deliberately *not* prefilled by AI. Download `my_staff_labels.csv` when the helper displays 30/30.
3. Move the exported file from Downloads into the repository root as `my_staff_labels.csv`, without changing texts.
4. Run `python scripts/validate_and_prepare_agreement.py`. Python standard library suffices; it checks 30 exact original texts and permitted label values. At this stage it should say staff labels are missing.
5. **Only after recording your own labels**, ask your CodePath teaching fellow for `data/staff_labels.csv`. Put that file in `data/` locally. It is ignored in Git to avoid distributing the answer key publicly.
6. Run `python scripts/validate_and_prepare_agreement.py` again. It writes the actual `agreement_results.json` and `staff_adjudications.md` templates, listing each disagreement.
7. For **every** disagreement, personally decide which label better follows the staff definition and explain why, categorizing as (a) applied existing rule loosely, (b) rule genuinely missing, or (c) reasonable ambiguity. Keep the adjudication in your own words.
8. Copy the full agreement report into the `README.md` Agreement section, with a candid diagnosis. Commit and push `my_staff_labels.csv`, `agreement_results.json`, `staff_adjudications.md`, and the updated README. Do not commit `data/staff_labels.csv`.
9. Submit the **same GitHub repository URL** used for Unit 5: https://github.com/mahjiid/ai201-project3-takemeter-starter-v2026.

**Due: Monday October 26, 2026 at 07:59 WAT (UTC+1).** The separate CodePath attendance appeal remains a program-enrollment matter and is not resolved by publishing coursework.

## Technical state

- GitHub-hosted Linux Python evaluation succeeded for both the baseline and three-seed before/after model runs. JSON measurement files are committed, not estimates.
- The lightweight verification workflow passed on GitHub Actions: https://github.com/mahjiid/ai201-project3-takemeter-starter-v2026/actions/runs/39792506506
- The original evaluation workflow showed a red badge because of a Git push race. The recovery workflow committed all three output files successfully, but itself reported a non-critical post-job pip-cache cleanup error. The later lightweight verification passed.
- The local Windows repository is synchronized; a virtual environment exists, but heavy PyTorch/model dependencies were **not successfully installed** locally because downloads were slow. Do not claim the local model stack is operational. Staff-annotation validator works using only standard-library Python.
- The `scripts/run_unit6.py` runner is available for repeatable future evaluation. Avoid re-running the single improvement unless needed for evidence; the assignment calls for exactly one measured change.
- Five synthetic-only tests in `tests/test_staff_pipeline.py` passed locally; they check that the pipeline refuses missing/invalid annotations and does not fabricate agreement.
- No secrets, actual student records, or staff reference answers should be committed. Staff-provided labels are ignored by `.gitignore`.

## Completion gate

**Do not report the Unit 6 submission as complete** until the independently labeled personal CSV, actual TF reference set, agreement output, every adjudication, and final updated README are present and reviewed.
