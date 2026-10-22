# Unit 6 — TakeMeter testing preparation (2026-10-22)

This is a preparation/audit note, **not** a completed Unit 6 submission. Do not report three-seed, baseline, agreement, or post-improvement values until they have been measured.

## Existing artifacts verified on GitHub
- `criteria.md`, `labels.csv`, `label_definitions.txt`, `results.json`, and `test_split.csv` are present.
- Existing fine-tuned result: seed 42; 30 test examples; accuracy 11/30 = **0.3667**; macro F1 **0.1341**; CPU.
- Original class distribution: analysis 43, hot_take 52, reaction 32, discussion_question 73; max share 36.5%, below precommitted 45% limit.
- Per-label F1 at seed 42: analysis 0.000; hot_take 0.000; reaction 0.000; discussion_question 0.5366.

### Original seed-42 confusion matrix — NOT the new three-seed result
Rows are true labels; columns are predictions.

| true \\ predicted | analysis | hot_take | reaction | discussion_question |
|---|---:|---:|---:|---:|
| analysis | 0 | 0 | 0 | 6 |
| hot_take | 0 | 0 | 0 | 8 |
| reaction | 0 | 0 | 0 | 5 |
| discussion_question | 0 | 0 | 0 | 11 |

**Diagnosis to investigate:** The original model assigned every example to `discussion_question`. That is consistent with class collapse and requires further tests to distinguish training/configuration problems from data/label ambiguity. It does NOT establish the cause.

## Precommitted criteria: preserve originals unchanged
1. Overall test accuracy >= 70% on **each** of three trials.
2. Every label F1 >= 0.55 on **each** trial.
3. Macro F1 >= 0.60 on **each** trial.
4. No class over 45% of the final labeled dataset.
5. Human annotation agreement >= 80% on an independently annotated shared sample.

Criterion 4 can already be checked on the original 200-label dataset (MET: 36.5% max). Criterion 5 must be checked using independently labeled posts and the specified taxonomy; the provided staff exercise uses *different* staff-defined labels, so discuss this measurement distinction explicitly rather than pretending those definitions are identical to the NBA taxonomy.

## Baseline prediction (recorded before baseline results)
The original fine-tuned model collapsed to one class. I therefore expect the label-definition-guided zero-shot baseline may outperform its 36.7% accuracy and its poor minority-class F1; this must be tested on the identical 30-post held-out set.

## Commands and execution order
On a working environment inside this **same** repository:
```powershell
.venv\Scripts\Activate.ps1
python test.py
python baseline.py
python baseline.py --trained results.json
```
- Preserve and commit `baseline_results.json`, and paste the measured baseline-vs-trained table in README.
- In `takemeter.ipynb`, run section 1 first; run section 6 with `RUN_LABEL = "before"` for seeds 42, 7, 2024, then section 7; commit `results_three_seeds_before.json` and a typed Markdown confusion matrix.
- Read `data/staff_taxonomy.md` and **personally** label all 30 original, unchanged texts in `data/staff_posts.csv` into `my_staff_labels.csv` without accessing staff answers first. Staff taxonomy is running-forum labels (`analysis`, `hot_take`, `reaction`), not the four-label r/NBATalk taxonomy.
- Request `data/staff_labels.csv` from the teaching fellow **only after** saving personal annotations; run `python agreement.py`; adjudicate every disagreement with a reason, not automatic deference.
- Compare all five targets across three seeds. Select one evidence-based improvement only. Preserve before results. Set `RUN_LABEL = "after"`; rerun exactly the same three seeds; commit `results_three_seeds_after.json`.
- Complete README sections **Baseline vs. Trained**, **Run Log — Before**, **Verdicts and Diagnoses**, **Agreement Report**, **The Improvement**, and **What's Still Broken** and explain AI assistance honestly.
- Use at least four new commits for the Unit 6 work, and submit the *same repo URL*.

## Blocking gaps as of preparation
- No Unit 6 baseline run or three-seed run has been verified.
- No personally labeled 30-row staff annotation file exists in the GitHub repository.
- No staff reference labels are present; obtain them from the TF at the instructed time.
- The inspected Windows global Python environment lacks PyTorch. Locate or recreate the project's .venv and check dependencies + available memory/disk space before training. Avoid treating this check as evidence that every local environment is missing packages.

Due: **2026-10-26 at 07:59 West Africa Time (UTC+1)**.
