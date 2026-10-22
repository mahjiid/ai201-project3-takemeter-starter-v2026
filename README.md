# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter classifies public discussion posts from **r/NBATalk**, a large public NBA discussion community. I chose it because the feed contains a real mix of evidence-backed basketball arguments, unsupported opinion posts, immediate reactions to news or events, and open-ended discussion prompts. The classifier will learn to separate those writing patterns rather than judge whether an opinion is correct.

**Milestone 1 observations from reading the community**

- Some posts support a claim with checkable evidence such as statistics, awards, dates, records, or explicit historical comparisons; others make equally strong claims without showing evidence.
- Some posts are mainly immediate reactions to recent news, a quote, a result, or an image, while others are intended as broader arguments that should still make sense after the event passes.
- A large share of posts are neutral questions asking readers to compare, rank, predict, or choose, which is different from the author making their own evaluative claim.

---

## Label Taxonomy

### `analysis`

**Definition:** Advances a basketball claim and supports it with at least one specific, checkable fact, statistic, record, date, quote, or piece of basketball evidence that is used to justify the claim.

**Example 1:**
> “Who’s ranked higher all-time: Carmelo or PG13?” — the post compares All-Star selections, All-NBA teams, and MVP finishes before asking for the ranking.

**Example 2:**
> “The 5 greatest playoffs performances of all time in my opinion.” — the post lists specific point, rebound, assist, and block totals for each selected performance.

### `hot_take`

**Definition:** Advances a confident evaluative basketball claim or ranking without giving specific, checkable support for the central claim.

**Example 1:**
> “MIKE BROWN is not getting enough credit as Reason Knicks won the chip… this dude was ZEN MASTER 2.0.”

**Example 2:**
> “If you don’t have MJ, Lebron, Russell, Wilt, Shaq, Kobe, Duncan, Kareem, Hakeem, Bird, Magic all in your top five you don’t know ball.”

### `reaction`

**Definition:** Primarily reports or responds to a recent NBA event, quote, result, image, or news item with short commentary or emotion instead of building a sustained argument.

**Example 1:**
> “This is hilarious, Ben Simmons ain't win MVP ever.”

**Example 2:**
> “Did not expect that ending lmao.”

### `discussion_question`

**Definition:** Primarily invites readers to compare, rank, predict, choose, or explain something without the author committing to a substantive answer of their own.

**Example 1:**
> “Is Blake Griffin a Hall of Famer?”

**Example 2:**
> “Which big 3 would you build around?”

### The hardest boundary

**Which two labels:** `analysis` and `hot_take`

**The decision rule I used every time:** If the post makes a central evaluative claim and uses at least one specific, checkable fact, statistic, record, date, quote, or observable basketball detail **as evidence for that claim**, label it `analysis`. If it makes the claim confidently but provides no such support, label it `hot_take`. Merely mentioning a player, score, event, or number is not enough; the evidence has to do argumentative work.

**Secondary boundary rule:** If a post is phrased as a question but the author clearly gives their own verdict and argues for it, classify it as `analysis` or `hot_take` according to the evidence rule above. Use `discussion_question` only when the post's main purpose is genuinely to solicit other people's answers.

---

## The Dataset

**Where the posts came from:** Public posts from **r/NBATalk** on Reddit. I collected whole visible post text and excluded comments and advertisements.

**How I labelled them:** I labelled the first 20 posts cold without AI assistance. AI then pre-labelled 180 additional posts using my taxonomy, and I reviewed and approved that batch before training. The final file stays as one unsplit `labels.csv` with `text`, `label`, and `note` columns.

**Counts per label:**

| Label | Count | Share |
|---|---:|---:|
| `analysis` | 43 | 21.5% |
| `hot_take` | 52 | 26.0% |
| `reaction` | 32 | 16.0% |
| `discussion_question` | 73 | 36.5% |
| **Total** | **200** | **100%** |

No label exceeds 45% of the dataset, so the dataset also meets my own balance criterion.

**Three hard cases**

**1.**
> *The post:* “What’s a controversial NBA take that you would stand on no matter how many people disagree? Mine is that fan obsession with ring culture has completely ruined how we evaluate individual greatness...”
>
> *Could have been:* `hot_take` or `discussion_question`
>
> *I chose, because:* `hot_take`. Although the title asks a question, the author gives a clear unsupported position of their own.

**2.**
> *The post:* “Is it fair to still call Jokic the best in the world? ... 3 straight seasons of no deep playoff runs with extremely disastrous endings?”
>
> *Could have been:* `hot_take`, `analysis`, or `discussion_question`
>
> *I chose, because:* `hot_take`. The author is pushing a position rather than only inviting answers, but the support is too thin to count as a developed evidence-backed analysis.

**3.**
> *The post:* “What if hand checking came back ... I kinda feel like it may bring a little balance back ... So your thoughts ... Yeah or nay?”
>
> *Could have been:* `discussion_question` or `hot_take`
>
> *I chose, because:* `discussion_question`. The author gives a tentative view, but the main purpose of the post is still to solicit other people’s answers.

---

## The Training Run

**Base model:** `distilbert-base-uncased` (DistilBERT)

**Settings:** 3 epochs, learning rate `2e-5`, batch size 16, maximum length 128 tokens, seed 42.

**Anything I changed from the defaults, and why:** I kept the starter training hyperparameters unchanged so the first run is directly comparable to the course defaults.

**Training device:** CPU (`torch 2.14.1+cpu`).

**Split sizes:** 139 train / 31 validation / 30 test.

| Label | Train | Validation | Test |
|---|---:|---:|---:|
| `analysis` | 30 | 7 | 6 |
| `hot_take` | 36 | 8 | 8 |
| `reaction` | 22 | 5 | 5 |
| `discussion_question` | 51 | 11 | 11 |

The held-out test split has only 6 `analysis` examples and 5 `reaction` examples. I recorded that now because per-label metrics for those classes may move substantially between seeds in Unit 6.

---

## How I Used AI

**Moment 1**

- *What I asked for:* Help stress-test the distinctions I observed in r/NBATalk and check whether the proposed labels had clear boundaries.
- *What came back:* Boundary questions around evidence-backed claims, unsupported takes, reactions, and neutral discussion prompts.
- *What I changed:* I kept four labels and wrote explicit rules for the hardest `analysis` vs `hot_take` boundary and for question-shaped posts that contain an author opinion.

**Moment 2**

- *What I asked for:* Pre-label the non-cold portion of the collected dataset using my taxonomy and flag class-balance problems.
- *What came back:* An initial pre-label draft where `reaction` was too thin, followed by a corrected draft with better coverage of clear news/highlight/reaction posts.
- *What I changed:* I reviewed and approved the AI-assisted labels before training, while keeping the first 20 rows as my unaided `cold` labels.

**Pre-labelling disclosure:** AI pre-labelled 180 of the 200 posts. I reviewed and approved that batch before training. The first 20 posts were labelled cold without AI assistance.


<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

The first zero-shot run (`facebook/bart-large-mnli`) and the original trained model both used the **same 30 held-out posts** from `test_split.csv`. The results below are real measurements from GitHub Actions on Linux CPU; the original Unit 5 run was on Windows CPU.

| Measure | Baseline | Trained (seed 42) | Trained − baseline |
|---|---:|---:|---:|
| Overall accuracy | 0.1333 | 0.3667 | +0.2334 |
| Macro F1 | 0.0588 | 0.1341 | +0.0753 |
| F1 — `analysis` | 0.2353 | 0.0000 | −0.2353 |
| F1 — `hot_take` | 0.0000 | 0.0000 | 0.0000 |
| F1 — `reaction` | 0.0000 | 0.0000 | 0.0000 |
| F1 — `discussion_question` | 0.0000 | 0.5366 | +0.5366 |

**What I predicted before I looked (committed before the baseline ran):** Given the original fine-tuned model assigned all 30 held-out posts to `discussion_question`, I predicted that the definition-guided zero-shot baseline might exceed its 36.7% accuracy and improve F1 on the other labels.

**What the gap actually means:** My prediction was **wrong**: baseline accuracy was 13.3%, not above 36.7%. Fine-tuning improved overall accuracy, but largely by favoring the most frequent test label: it recognized none of the `analysis` or `reaction` examples. Conversely, the baseline recognized some `analysis` posts but failed the other labels. **Neither result supports a reliable four-label classifier.**

Data: `baseline_results.json` (measured), `results.json` (original trained model), `test_split.csv` (shared held-out set).

---

## Run Log — Before

Measured by running the original notebook's training functions at seeds **42, 7, 2024**, without changing the original data, taxonomy, or training settings (3 epochs, learning rate 2e-5, batch 16). Each seed retrains and evaluates on its own stratified split. Execution: GitHub-hosted Linux CPU, torch 2.14.1+cu130.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---:|---:|---:|---|
| 1. Overall accuracy | ≥ 0.70 | 0.367 | 0.433 | 0.367 | **MISSED** |
| 2. Minimum per-label F1 | ≥ 0.55 | 0.000 | 0.000 | 0.000 | **MISSED** |
| 3. Macro F1 | ≥ 0.60 | 0.134 | 0.236 | 0.134 | **MISSED** |
| 4. Largest class share | ≤ 45% | 36.5% | 36.5% | 36.5% | **MET** |
| 5. Independent annotator agreement | ≥ 80% | Not measured | Not measured | Not measured | **PENDING** |

The accuracy spread is 0.067 (6.7 percentage points); **consistently poor performance** is not a sign the classifier is good. Mean accuracy is 0.389; mean macro F1 is 0.168. See `results_three_seeds_before.json` for measured details.

### Confusion matrix — seed 42, before improvement

Rows are true labels and columns predicted labels.

| true \\ predicted | analysis | hot_take | reaction | discussion_question |
|---|---:|---:|---:|---:|
| **analysis** | 0 | 0 | 0 | 6 |
| **hot_take** | 0 | 0 | 0 | 8 |
| **reaction** | 0 | 0 | 0 | 5 |
| **discussion_question** | 0 | 0 | 0 | 11 |

**Biggest off-diagonal cell:** Eight genuine `hot_take` posts were classified as `discussion_question`; zero true `discussion_question` posts were called `hot_take`. This is **one-way class collapse**, not just a symmetric borderline confusion. Seeds 42 and 2024 predict `discussion_question` for every post; seed 7 recognizes two `hot_take` posts.

---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | Evidence / interpretation |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 70% in all three | **MISSED** | 36.7%, 43.3%, 36.7%; none reaches target |
| 2 | Every label F1 | ≥ 0.55 in all three | **MISSED** | Minimum F1 is zero on every split; `analysis` and `reaction` never recognized |
| 3 | Macro F1 | ≥ 0.60 in all three | **MISSED** | 0.134, 0.236, 0.134 |
| 4 | Dataset balance | Largest label ≤ 45% | **MET** | `discussion_question` is 73/200 = 36.5% |
| 5 | Human labeling consistency | ≥ 80% agreement | **PENDING** | Requires genuinely independent annotations and staff reference answers; not guessed |

**Diagnoses:** The model **collapses toward `discussion_question`**, the plurality label (36.5% of training data). An imbalanced prediction pattern despite a reasonably balanced training set suggests an **under-learning, representation, or annotation quality problem**, but the current scores do **not establish** which mechanism is responsible. The baseline is even worse (13.3%), confirming that zero-shot prompting with these definitions is not an adequate substitute. The separate staff annotation task may expose inconsistency in how written definitions were applied, but **its reference answers have not been obtained**, so do not claim to have verified a labeling cause yet.

The original 30-post test set has only six `analysis` and five `reaction` examples; their F1 is inherently sensitive to small changes, though zero across all three seeds remains a serious failure.

---

## Agreement Report

**Status: awaiting independent human annotations and teaching-fellow reference labels.**

I have prepared `staff_annotation_worksheet.csv` with the exact 30 texts and empty labels. This is **not yet** `my_staff_labels.csv` and does **not** represent independent human labeling. Apply the three labels in `data/staff_taxonomy.md` yourself, save the finished `my_staff_labels.csv`, and only then request `data/staff_labels.csv` from the teaching fellow. Run `python agreement.py` and document **every** disagreement with both labels, a written conclusion and reasoning. Nothing here has been fabricated.

**Measurement caveat:** The staff exercise uses three labels from a fictional running forum, while the user's Unit 5 classifier uses four labels from NBA posts. Therefore staff agreement directly measures how reliably an external written taxonomy is interpreted; it is **not identical** to independently relabeling the original NBA four-label corpus. The precommitted ≥80% NBA consistency criterion is not established by this staff set alone.

---

## The Improvement

**Single change selected from the before-run diagnosis:** Increase `EPOCHS` from **3 to 6** for the *same* DistilBERT fine-tuning setup. Keep training examples, labels, token length (128), learning rate (2e-5), batch size (16), and seeds (42, 7, 2024) fixed. The before-run collapse suggests the classifier may not have learned decision boundaries sufficiently from the short fine-tune, making epochs a plausible, testable **single-variable hypothesis**, not a proven solution.

**Why this is an experiment:** If more epochs still produce class collapse, the results weaken the under-training explanation and shift attention toward data ambiguity or insufficient examples; worse results are also valid evidence.

### Run Log — After

**Actual measured experiment:** `EPOCHS: 3 → 6` and **no other changes** (same dataset, taxonomy, learning rate, batch size, and seeds). Run in GitHub Actions Linux CPU. The authentic values below are from `results_three_seeds_after.json`.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---:|---:|---:|---|
| 1. Accuracy | ≥ 0.70 | 0.533 | 0.500 | 0.500 | **MISSED** |
| 2. Minimum label F1 | ≥ 0.55 | 0.000 | 0.000 | 0.000 | **MISSED** |
| 3. Macro F1 | ≥ 0.60 | 0.416 | 0.349 | 0.375 | **MISSED** |
| 4. Class share | ≤ 45% | 36.5% | 36.5% | 36.5% | **MET** |
| 5. Human consistency | ≥ 80% | not measured | not measured | not measured | **PENDING** |

#### Before versus after (three-seed results)

| Measure | Before (3 epochs), seeds 42/7/2024 | After (6 epochs), seeds 42/7/2024 |
|---|---|---|
| Accuracy | 0.367 / 0.433 / 0.367 | **0.533 / 0.500 / 0.500** |
| Macro F1 | 0.134 / 0.236 / 0.134 | **0.416 / 0.349 / 0.375** |
| F1 — `analysis` | 0 / 0 / 0 | 0.429 / 0.400 / 0.500 |
| F1 — `hot_take` | 0 / 0.333 / 0 | 0.545 / 0.308 / 0.308 |
| F1 — `reaction` | 0 / 0 / 0 | **0 / 0 / 0** |
| F1 — `discussion_question` | 0.537 / 0.611 / 0.537 | 0.690 / 0.688 / 0.692 |

**Did it help? Yes, but not enough.** Mean accuracy increased from **38.9% to 51.1%** (+12.2 percentage points), and mean macro F1 rose from **0.168 to 0.380** (+0.212). The model began recognizing `analysis` and `hot_take`, but **never correctly recognized `reaction`** across any seed, and none of the original performance criteria became met. Increased training exposure was helpful but cannot by itself make this a reliable classifier.

#### After-run confusion matrix — seed 42

| true \\ predicted | analysis | hot_take | reaction | discussion_question |
|---|---:|---:|---:|---:|
| **analysis** | 3 | 0 | 0 | 3 |
| **hot_take** | 2 | 3 | 1 | 2 |
| **reaction** | 2 | 0 | 0 | 3 |
| **discussion_question** | 1 | 0 | 0 | 10 |

All five actual `reaction` posts in this seed were misclassified: two as `analysis` and three as `discussion_question`. That is now the highest-priority unresolved error.
---

## What's Still Broken

The measured six-epoch change improved average accuracy and macro F1 but **failed** the 70% accuracy, 0.55 worst-class F1, and 0.60 macro-F1 criteria across all three seeds. Most importantly, `reaction` F1 remained **zero** on all three runs. For this class there are only 32 labeled examples in the original 200-post dataset (16%), of which 22 were in the original training split, and its boundary with short `hot_take` or event-driven `discussion_question` content may require checking more examples and annotation consistency. These are hypotheses, not established causes.

**Further work if allowed in a later experiment:** Independently review `reaction` examples and edge cases against the original taxonomy, increase clearly labeled examples after a quality audit, or test a separate training hyperparameter in isolation. I have **not** made those extra changes in this unit because the assignment calls for one measured improvement.

**Still required from a human and the TF:** Label the 30 running-forum posts independently using `data/staff_taxonomy.md`, then obtain `data/staff_labels.csv`, run `agreement.py`, and adjudicate every disagreement with a defensible reason. Until then, human agreement is **not measured** and no grading claim about it is warranted.

**The gap between my intended labels and the model's learned behavior:** I intended to distinguish four basketball discussion functions, including fast emotional reactions. After more training the model partially learned evidence-based analysis and unsupported takes, but still treated real `reaction` posts as either arguments or questions, so the intended reaction boundary remains unlearned.

**AI assistance disclosure for Unit 6:** AI helped repair testing infrastructure, run and interpret model evaluations, and write up the measured tables. It did **not** create an independent human annotation or claim to have adjudicated staff disagreements. The baseline, before, and after runs were executed on GitHub Actions Linux CPU as an openly documented alternative to the slow local Windows dependency downloads.

---

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
