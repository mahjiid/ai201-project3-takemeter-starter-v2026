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
| 5. Independent annotator agreement | ≥ 80% | 56.7% staff-set proxy | N/A (one common set) | N/A | **MISSED on proxy; original taxonomy unmeasured** |

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
| 5 | Human labeling consistency | ≥ 80% agreement | **MISSED on staff proxy; original in-domain check unmeasured** | Agreement was 17/30 = 56.7% on the 3-label staff running-forum task; the original 4-label basketball taxonomy was not independently relabeled |

**Diagnoses:** The model **collapses toward `discussion_question`**, the plurality label (36.5% of training data). An imbalanced prediction pattern despite a reasonably balanced training set suggests an **under-learning, representation, or annotation quality problem**, but the current scores do **not establish** which mechanism is responsible. The baseline is even worse (13.3%), confirming that zero-shot prompting with these definitions is not an adequate substitute. The staff annotation task now demonstrates 13 concrete interpretation disagreements against a distinct three-label running-forum taxonomy. The mistakes around numerical evidence versus unsupported opinion and personal reaction justify a **label-quality risk hypothesis**; because these are not the NBA posts, they do not prove an in-domain annotation fault.

The original 30-post test set has only six `analysis` and five `reaction` examples; their F1 is inherently sensitive to small changes, though zero across all three seeds remains a serious failure.

---

## Agreement Report

**Independent annotation and reference verification.** The student's original 30 running-forum labels were saved in `my_staff_labels.csv` and committed before the official reference was received from CodePath Support on October 23, 2026. The texts and original labels remain unchanged; the official `data/staff_labels.csv` stays only on the local computer and is deliberately Git-ignored.

| Check | Verified result |
|---|---:|
| Original posts compared | 30 |
| Exact matches | 17 |
| Disagreements | 13 |
| **Raw label agreement** | **17/30 = 56.7%** |
| Reference-linked measurements | [`agreement_results.json`](agreement_results.json) |
| Full adjudication analysis | [`staff_adjudications.md`](staff_adjudications.md) |

**Verdict:** The 56.7% rate is below the 80% consistency target from Unit 5 on the *available staff exercise*, but it is **not a direct test of the original four-label basketball taxonomy**. The staff exercise uses `analysis`, `hot_take`, and `reaction` on 30 running-forum posts, rather than the basketball dataset's four-way labeling. It is a strong diagnostic of how a different written rule set was applied, not a proven 56.7% reproducibility rate for the original basketball annotations. The Unit 5 in-domain consistency criterion therefore remains *not directly measured*. The course explicitly says the staff-set agreement rate itself is not graded; the reasoned adjudication is.

### All 13 disagreement adjudications

The following is a **rule-grounded interpretation** of the 13 mismatches for student review. It preserves the original independent label selections. Unlike unconditional deference, case `sp_003` defends the initial label with a substantive explanation; the other cases explain why the reference better fits the taxonomy. Rule 1 asks whether a checkable fact *carries* an argument; Rule 2 separates a general claim from an immediate personal response; Rule 3 says recency and numbers don't replace load-bearing evidence; Rule 4 breaks defensible ties.

#### 1. sp_003 — hot_take versus analysis

> The club championship scoring changed in 2019 from top-6 to top-10. Since then our B team has finished above the A team twice. That's not depth improving, it's the scoring rewarding turnout.

**Original label:** `hot_take` · **Staff label:** `analysis` · **Preferred interpretation:** `hot_take` (defend my initial reading; staff's `analysis` also plausible)    
**Diagnosis group:** (c) defensible alternate interpretation.

The changed scoring rule (2019) and two B-team wins are checkable, so staff has a credible analysis reading. Yet the final claim attributes those wins specifically to turnout, while the post supplies no turnout counts or comparison of athlete depth. Under Rule 1, one may argue the facts establish a changed outcome but do not actually carry the asserted turnout explanation. The **hot_take** classification is defensible for this causal leap, although the staff's **analysis** classification is also reasonable under the broad 'checkable fact' wording. The original choice is retained as a documented, arguable disagreement instead of defaulting to the answer key.

#### 2. sp_004 — reaction versus analysis

> Everyone blames the hill at 18 miles. I split the field into people who ran the first half under 1:45 and over, and the slowdown after 18 was almost identical for both groups. If the hill were the problem the fast starters would fall apart harder.

**Original label:** `reaction` · **Staff label:** `analysis` · **Preferred interpretation:** `analysis` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

Dividing runners by opening-half time tests a prediction about slowdown after mile 18. The nearly identical slowdowns in both groups are the evidence used to challenge the hill explanation. This is a structured, checkable inference under Rule 1, not a recent feeling or first-person race report.

#### 3. sp_008 — reaction versus analysis

> Went back through the club results going back to 2012. Every single year the number of people who enter the spring marathon and don't start it sits between 18 and 23 percent. It's not a bad-luck year, it's the base rate.

**Original label:** `reaction` · **Staff label:** `analysis` · **Preferred interpretation:** `analysis` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

A repeated 18–23% DNS rate over results dating to 2012 directly supports the argument that the current year is not an unusual outlier. The historical range is load-bearing evidence; the post makes no immediate personal-response claim.

#### 4. sp_009 — hot_take versus analysis

> The 10K route was remeasured in 2021 and came out 60 metres long. Everyone comparing PBs from before and after that is comparing two different races, which is about 12 seconds at club pace.

**Original label:** `hot_take` · **Staff label:** `analysis` · **Preferred interpretation:** `analysis` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

The 2021 remeasurement, 60-metre distance difference, and estimated 12-second effect make a specific comparison of pre/post-2021 personal bests. These numbers carry the claim that the performances aren't directly comparable. The assertion is supported rather than a naked hot_take.

#### 5. sp_011 — reaction versus hot_take

> Anyone who races more than once a month isn't training, they're just collecting medals.

**Original label:** `reaction` · **Staff label:** `hot_take` · **Preferred interpretation:** `hot_take` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

'Anyone who races more than once a month' makes a broad judgment about other runners without support. It doesn't say what just happened to the writer or describe their present emotional response, as Rule 2 requires for reaction.

#### 6. sp_012 — analysis versus hot_take

> Heart rate zones are astrology for runners.

**Original label:** `analysis` · **Staff label:** `hot_take` · **Preferred interpretation:** `hot_take` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

Calling heart-rate zones 'astrology' is a witty analogy, but no measurement, quoted evidence, or concrete comparison carries an argument. Rule 1 does not count a metaphor as checkable support.

#### 7. sp_016 — analysis versus hot_take

> If you need a gel before 90 minutes you have a fuelling problem, not an energy problem.

**Original label:** `analysis` · **Staff label:** `hot_take` · **Preferred interpretation:** `hot_take` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

Ninety minutes is a numerical cutoff, not a measured result establishing that needing a gel proves a fuelling problem. The prescription assumes the relationship it should demonstrate. By Rule 1, a number by itself doesn't turn a claim into analysis.

#### 8. sp_018 — analysis versus hot_take

> Track sessions are wasted on anyone running slower than 8 minute miles. You'd get more out of just running more.

**Original label:** `analysis` · **Staff label:** `hot_take` · **Preferred interpretation:** `hot_take` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

Eight-minute miles sounds specific, but the author provides no test, sample, or evidence that track sessions are wasted below that pace. Both 'wasted' and 'you'd get more from mileage' are unsupported general claims.

#### 9. sp_020 — reaction versus hot_take

> Every injury thread on this forum is the same injury and the same three replies.

**Original label:** `reaction` · **Staff label:** `hot_take` · **Preferred interpretation:** `hot_take` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

'Every injury thread' makes a sweeping generalization about forum content. The author does not give thread counts or concrete checks, nor describe a just-happened personal experience. The repetitive tone may express frustration, but Rule 2 puts general unsupported claims under hot_take.

#### 10. sp_023 — hot_take versus reaction

> First run back after eight weeks out. Two miles, slower than my warm-up used to be, and I don't care even slightly.

**Original label:** `hot_take` · **Staff label:** `reaction` · **Preferred interpretation:** `reaction` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

The speaker reports their first run back after eight weeks and how they feel about its slow two-mile distance. The times and distances provide context for that personal moment; they aren't used to argue a wider claim. Rule 2 favors reaction.

#### 11. sp_025 — analysis versus reaction

> Blew up at 20 with the pace band still in my hand like it was going to help. Rough one.

**Original label:** `analysis` · **Staff label:** `reaction` · **Preferred interpretation:** `reaction` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

Blowing up at mile 20 with a pace band is an immediate lived experience followed by 'Rough one.' The numerical mile is part of the story, not a fact used to support an analysis. Rule 3 says evidence must carry an argument, which is absent.

#### 12. sp_027 — hot_take versus reaction

> Wind was so bad on the out section I was leaning at about 20 degrees. Coming back felt like cheating.

**Original label:** `hot_take` · **Staff label:** `reaction` · **Preferred interpretation:** `reaction` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

The 'about 20 degrees' detail conveys how forceful the wind felt during the writer's run. The phrase 'coming back felt like cheating' signals experience and feeling, not a generalized theory about wind. Rule 2 makes reaction the clearer choice.

#### 13. sp_028 — hot_take versus reaction

> Third DNF this year. I don't really want to talk about it, just wanted to put it somewhere.

**Original label:** `hot_take` · **Staff label:** `reaction` · **Preferred interpretation:** `reaction` (reference better supported)    
**Diagnosis group:** (a) I applied the written rule loosely.

'Third DNF this year' is countable, but the message is personal disclosure: the writer doesn't want to talk, just wants to express what happened. The count supports no argument; Rules 2 and 3 prioritize a reaction rather than hot_take or analysis.

### What the disagreements diagnose

The review exposes four recurring mistakes that can generalize to annotation work: (1) failing to recognize comparisons and historical statistics doing actual argumentative work (`sp_004`, `sp_008`, `sp_009`); (2) reading a numerical cutoff or vivid metaphor as if it were evidence (`sp_012`, `sp_016`, `sp_018`); (3) confusing unsupported general opinions with a current, personal emotional response (`sp_011`, `sp_020`); and (4) mistaking personal race experiences for analysis or general hot takes (`sp_023`, `sp_025`, `sp_027`, `sp_028`). The interesting counterexample is `sp_003`: the scoring-rule change and two finishes are checkable but do not independently show *turnout* caused the outcome, so `hot_take` has a defensible Rule 1 interpretation even though staff chose `analysis`.

These are evidence of **taxonomy-boundary application difficulty**, not proof that the separate four-label basketball model's failures are caused by those same ambiguities. The measured model experiment showed that more training recovered some `analysis` and `hot_take` ability but left `reaction` F1 at zero; label consistency would be a worthwhile *separate* follow-up study, not an established cause here.

**AI-assistance and student judgment:** The original post labels were independently selected before staff answers arrived. AI assisted with organizing, interpreting, and drafting the adjudication arguments above. The student should ensure the final positions reflect their understanding before submitting. No reference labels were substituted into the original independent file.

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
| 5. Human consistency | ≥ 80% | 56.7% staff-set proxy | N/A | N/A | **MISSED on proxy; original taxonomy unmeasured** |

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

**Human-labeling limitation:** The full 13-case rule-based adjudication now appears in the Agreement Report and in `staff_adjudications.md`. Review the reasoning and amend any judgment that does not match your interpretation of the taxonomy. The in-domain basketball labeling consistency criterion remains unmeasured; a follow-up independent re-annotation would be needed.

**The gap between my intended labels and the model's learned behavior:** I intended to distinguish four basketball discussion functions, including fast emotional reactions. After more training the model partially learned evidence-based analysis and unsupported takes, but still treated real `reaction` posts as either arguments or questions, so the intended reaction boundary remains unlearned.

**AI assistance disclosure for Unit 6:** AI helped repair testing infrastructure, run and interpret model evaluations, build the independent annotation interface and validator, calculate the reference agreement from the completed files, and draft explanations for each mismatch. My original labels were independently selected and preserved, and the complete adjudication arguments are clearly disclosed as AI-assisted rather than falsely claimed as independently authored. The baseline, before, and after runs were executed on GitHub Actions Linux CPU as an openly documented alternative to the slow local Windows dependency downloads.

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
