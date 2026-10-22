#!/usr/bin/env python3
"""Execute the existing TakeMeter notebook's Unit 6 three-seed cells headlessly.

This helper does not change the model, labels, splits, or metrics. It imports
function definitions from the same notebook used in class without rerunning
Unit 5's training/saving cells. Results are actual model evaluations.
"""
import argparse
import json
import os
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--run-label", choices=["before", "after"], default="before")
parser.add_argument("--epochs", type=int, default=3)
parser.add_argument("--overwrite", action="store_true")
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
os.chdir(root)
out = root / f"results_three_seeds_{args.run_label}.json"
if out.exists() and not args.overwrite:
    raise SystemExit(f"{out} already exists; refusing to overwrite previous measurements")
if args.epochs <= 0:
    raise SystemExit("Epochs must be positive")
nb = json.loads((root / "takemeter.ipynb").read_text(encoding="utf-8"))
env = {"__name__": "__main__"}

def source(i):
    return "".join(nb["cells"][i]["source"])

def run(i, text=None):
    block = source(i) if text is None else text
    print(f"[notebook] cell {i}", flush=True)
    exec(compile(block, f"takemeter.ipynb#cell{i}", "exec"), env)

for index in [2, 4, 6, 8, 10, 12]:
    run(index)
if args.epochs != 3:
    print(f"[one changed setting] EPOCHS {env['EPOCHS']} -> {args.epochs}", flush=True)
    env["EPOCHS"] = args.epochs

# Preserve Unit 5 results.json and test_split.csv: only import definitions.
training_defs = source(14).split("\n\ntrainer, tokenizer = train_model(")[0]
evaluation_defs = source(16).split("\n\nresults = evaluate(")[0]
run(14, training_defs)
run(16, evaluation_defs)
unit6 = source(19).replace('RUN_LABEL = "before"', f'RUN_LABEL = "{args.run_label}"')
if args.run_label not in unit6:
    raise SystemExit("Unit 6 notebook cell format changed")
run(19, unit6)
run(21)
run(23)
if not out.is_file():
    raise SystemExit(f"Expected result file missing: {out}")
print(f"[verified] {out} ({out.stat().st_size} bytes)", flush=True)
