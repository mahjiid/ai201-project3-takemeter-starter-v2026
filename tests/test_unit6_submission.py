"""Offline submission-integrity checks for CodePath AI201 Unit 6.

No access to CodePath's private reference answer key is needed or attempted.
This validates the published evidence for internal consistency, not the
student's personal acceptance of AI-assisted adjudication arguments.
"""
import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEEDS = [42, 7, 2024]
LABELS = ["analysis", "hot_take", "reaction", "discussion_question"]

def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

class Unit6SubmissionIntegrity(unittest.TestCase):
    def test_untouched_personal_annotations(self):
        with (ROOT / "data" / "staff_posts.csv").open(newline="", encoding="utf-8") as f:
            posts = list(csv.DictReader(f))
        with (ROOT / "my_staff_labels.csv").open(newline="", encoding="utf-8-sig") as f:
            mine = list(csv.DictReader(f))
        self.assertEqual(len(posts), 30)
        self.assertEqual(len(mine), 30)
        self.assertEqual([p["text"] for p in posts], [m["text"] for m in mine])
        self.assertEqual(set(m["label"] for m in mine), {"analysis", "hot_take", "reaction"})

    def test_saved_agreement_and_thirteen_disagreements(self):
        data = load("agreement_results.json")
        self.assertEqual(data["compared"], 30)
        self.assertEqual(data["agreed"], 17)
        self.assertEqual(len(data["disagreements"]), 13)
        self.assertAlmostEqual(data["agreement_rate"], 17/30)
        self.assertEqual(data["staff_posts_not_in_mine"], 0)
        ids = [d["id"] for d in data["disagreements"]]
        self.assertEqual(len(set(ids)), 13)
        with (ROOT / "data" / "staff_posts.csv").open(newline="", encoding="utf-8") as f:
            posts = {p["id"]: p["text"] for p in csv.DictReader(f)}
        with (ROOT / "my_staff_labels.csv").open(newline="", encoding="utf-8-sig") as f:
            own = {p["text"]: p["label"] for p in csv.DictReader(f)}
        for entry in data["disagreements"]:
            self.assertEqual(posts[entry["id"]], entry["text"])
            self.assertEqual(own[entry["text"]], entry["mine"])
            self.assertNotEqual(entry["staff"], entry["mine"])

    def test_full_disagreement_reasoning_in_two_artifacts(self):
        report = (ROOT / "README.md").read_text(encoding="utf-8")
        adjudications = (ROOT / "staff_adjudications.md").read_text(encoding="utf-8")
        ids = [r["id"] for r in load("agreement_results.json")["disagreements"]]
        for i, id_ in enumerate(ids, start=1):
            self.assertIn(f"#### {i}. {id_}", report)
            self.assertIn(f"### {i}. {id_}", adjudications)
        self.assertIn("AI-assisted", report)
        self.assertIn("AI assistance", adjudications + report)
        self.assertNotIn("[Approve or revise", adjudications)
        self.assertNotIn("[write your reasoning]", adjudications)

    def test_repeated_model_trials_and_single_improvement(self):
        before = load("results_three_seeds_before.json")
        after = load("results_three_seeds_after.json")
        self.assertEqual([s["seed"] for s in before], SEEDS)
        self.assertEqual([s["seed"] for s in after], SEEDS)
        self.assertTrue(all(s["n_test"] == 30 for s in before+after))
        for s in before+after:
            self.assertEqual(set(s["per_label"]), set(LABELS))
            self.assertTrue(0 <= s["accuracy"] <= 1)
            self.assertTrue(0 <= s["f1_macro"] <= 1)
        self.assertTrue(all(y["accuracy"] > x["accuracy"] for x, y in zip(before, after)))
        self.assertTrue(all(s["per_label"]["reaction"]["f1"] == 0 for s in after))

    def test_required_sections_and_private_staff_key(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        required = [
            "## Baseline vs. Trained", "## Run Log — Before",
            "## Verdicts and Diagnoses", "## Agreement Report",
            "## The Improvement", "### Run Log — After", "## What's Still Broken"
        ]
        for h in required:
            self.assertIn(h, readme)
        self.assertIn("56.7%", readme)
        self.assertIn("13 disagreement", readme)
        self.assertIn("data/staff_labels.csv", (ROOT/".gitignore").read_text())
        self.assertTrue((ROOT / "baseline_results.json").is_file())

if __name__ == "__main__":
    unittest.main()
