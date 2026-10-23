#!/usr/bin/env python3
"""Validate independent staff annotations and produce Unit 6 disagreement template.

Python standard library only. NEVER obtains or generates staff answers.
The human must label all posts BEFORE reading the TF's reference file.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAFF_POSTS = ROOT / "data" / "staff_posts.csv"
PERSONAL = ROOT / "my_staff_labels.csv"
REFERENCE = ROOT / "data" / "staff_labels.csv"
ALLOWED = {"analysis", "hot_take", "reaction"}

def rows(path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

def check_mine():
    posts = rows(STAFF_POSTS)
    assert len(posts) == 30, f"Expected 30 staff posts, found {len(posts)}"
    assert len(set(p["text"] for p in posts)) == 30, "Duplicate source posts"
    if not PERSONAL.exists():
        print("Human annotations are missing. Open staff_annotation_helper.html, label all 30 yourself and export my_staff_labels.csv.")
        return None
    mine = rows(PERSONAL)
    if len(mine) != 30:
        raise ValueError(f"Expected 30 human-labeled rows; got {len(mine)}")
    if not all({"text", "label"}.issubset(item) for item in mine):
        raise ValueError("my_staff_labels.csv needs columns text,label")
    if [p["text"] for p in posts] != [p["text"] for p in mine]:
        raise ValueError("Human file must contain the original exact 30 texts, in order. Do not trim or retype.")
    problems = [(i + 1, entry["label"]) for i, entry in enumerate(mine) if entry["label"] not in ALLOWED]
    if problems:
        raise ValueError(f"Missing/invalid human labels: {problems}")
    print("PASS: 30 genuine selections, all valid labels, exact original texts.")
    return posts, mine

def main():
    checked = check_mine()
    if checked is None:
        return 2
    posts, mine = checked
    if not REFERENCE.exists():
        print("Awaiting TF reference file data/staff_labels.csv. Do NOT substitute generated or guessed labels.")
        print("Your personal labels are validated and safe to commit, but agreement cannot be computed yet.")
        return 3
    staff = rows(REFERENCE)
    if not all("id" in row for row in staff):
        raise ValueError("Staff label file must have id column")
    col = next((k for k in ("label", "staff_label", "my_label", "your_label") if all(k in x for x in staff)), None)
    if col is None:
        raise ValueError("Staff file missing a recognized label column")
    answer = {r["id"]: r[col] for r in staff}
    expected_ids = [p["id"] for p in posts]
    if len(staff) != 30 or len(answer) != 30 or set(answer) != set(expected_ids):
        raise ValueError("Reference must contain exactly the same 30 post IDs")
    if any(label not in ALLOWED for label in answer.values()):
        raise ValueError("Reference contains invalid labels")
    disagreements = []
    for p, m in zip(posts, mine):
        ref = answer[p["id"]]
        if ref != m["label"]:
            disagreements.append({"id": p["id"], "text": p["text"], "staff": ref, "mine": m["label"]})
    agreement_rate = (30 - len(disagreements)) / 30
    payload = {
        "compared": 30,
        "agreed": 30-len(disagreements),
        "agreement_rate": agreement_rate,
        "disagreements": disagreements,
        "staff_posts_not_in_mine": 0
    }
    (ROOT / "agreement_results.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    out = [
        "# Unit 6 — Agreement adjudications",
        "",
        f"Compared: 30; agreed: {30-len(disagreements)}; disagreements: {len(disagreements)}; agreement: {agreement_rate:.1%}.",
        "",
        "For **every** disagreement, make your own decision using data/staff_taxonomy.md.",
        "Choose (a) rule applies but I used it loosely; (b) genuine rule gap;",
        "or (c) both interpretations defensible. Never defer automatically.",
        ""
    ]
    for i, row in enumerate(disagreements, 1):
        quoted_text = row["text"].replace("\n", " ").replace("|", "\\|")
        out.extend([
            f"## Disagreement {i}: {row['id']}",
            "",
            f"> {quoted_text}",
            "",
            f"- **My independent label:** `{row['mine']}`",
            f"- **Staff reference label:** `{row['staff']}`",
            "- **My decision (mine/staff/either):** [write your decision]",
            "- **My evidence-based reason (cite taxonomy decision rule):** [write your reasoning]",
            "- **Category (a/b/c):** [choose]",
            ""
        ])
    if not disagreements:
        out.append("No disagreements. Explain briefly whether rules were unusually clear or whether the examples were easy.")
    adjudication_path = ROOT / "staff_adjudications.md"
    if adjudication_path.exists():
        print("Preserved existing staff_adjudications.md to avoid overwriting student-reviewed decisions.")
    else:
        adjudication_path.write_text("\n".join(out)+"\n",encoding="utf-8")
        print("Created staff_adjudications.md template for independent review.")
    print(f"PASS: agreement {agreement_rate:.1%}; {len(disagreements)} disagreements.")
    print("Wrote agreement_results.json. Adjudication text is preserved if already present.")
    print("Fill in ALL adjudication decisions and reasons yourself; then copy the report to README.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
