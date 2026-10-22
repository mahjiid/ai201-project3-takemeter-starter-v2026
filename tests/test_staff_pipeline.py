"""Self-contained tests with synthetic labels; no staff answer key or student labels."""
import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent
LABELS = ["analysis", "hot_take", "reaction"]

class TestStaffAnnotationWorkflow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="unit6_mock_")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "scripts").mkdir()
        (self.root / "data").mkdir()
        shutil.copy(SOURCE / "scripts" / "validate_and_prepare_agreement.py",
                    self.root / "scripts" / "validate_and_prepare_agreement.py")
        shutil.copy(SOURCE / "data" / "staff_posts.csv", self.root / "data" / "staff_posts.csv")
        with (self.root / "data" / "staff_posts.csv").open(newline="", encoding="utf-8") as stream:
            self.posts = list(csv.DictReader(stream))
        self.assertEqual(len(self.posts), 30)

    def execute(self):
        return subprocess.run([sys.executable, "scripts/validate_and_prepare_agreement.py"],
                              cwd=self.root, capture_output=True, text=True)

    def human_file(self, mutation=None):
        path = self.root / "my_staff_labels.csv"
        with path.open("w", newline="", encoding="utf-8-sig") as stream:
            w=csv.DictWriter(stream, fieldnames=["text","label"])
            w.writeheader()
            for i, post in enumerate(self.posts):
                text = post["text"]
                label=LABELS[i % 3]
                if mutation is not None:
                    text, label = mutation(i, text, label)
                w.writerow({"text":text,"label":label})

    def staff_file(self, mutate=None):
        path = self.root / "data" / "staff_labels.csv"
        with path.open("w", newline="", encoding="utf-8") as stream:
            w=csv.DictWriter(stream, fieldnames=["id","label"])
            w.writeheader()
            for i, post in enumerate(self.posts):
                label = LABELS[i % 3]
                if mutate and i in {0, 29}: label = LABELS[(i+1) % 3]
                w.writerow({"id":post["id"],"label":label})

    def test_missing_human_is_a_blocker_not_fake_results(self):
        r=self.execute()
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertFalse((self.root/"agreement_results.json").exists())

    def test_completed_human_without_staff_is_still_blocked(self):
        self.human_file()
        r=self.execute()
        self.assertEqual(r.returncode, 3, r.stderr)
        self.assertFalse((self.root/"agreement_results.json").exists())

    def test_changed_post_rejected(self):
        self.human_file(lambda i,t,l: (t+" altered" if i==4 else t,l))
        r=self.execute()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("exact", r.stderr)
        self.assertFalse((self.root/"agreement_results.json").exists())

    def test_invalid_label_rejected(self):
        self.human_file(lambda i,t,l: (t,"unapproved" if i==4 else l))
        r=self.execute()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("invalid", r.stderr)
        self.assertFalse((self.root/"agreement_results.json").exists())

    def test_mock_reference_generates_two_disagreements_without_adjudicating(self):
        self.human_file()
        self.staff_file(mutate=True)
        r=self.execute()
        self.assertEqual(r.returncode, 0, r.stderr)
        data=json.loads((self.root/"agreement_results.json").read_text(encoding="utf-8"))
        self.assertEqual(data["compared"],30)
        self.assertEqual(data["agreed"],28)
        self.assertEqual(len(data["disagreements"]),2)
        doc=(self.root/"staff_adjudications.md").read_text(encoding="utf-8")
        self.assertEqual(doc.count("## Disagreement"),2)
        self.assertIn("[write your reasoning]",doc)

if __name__=="__main__":
    unittest.main()
