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

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



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
