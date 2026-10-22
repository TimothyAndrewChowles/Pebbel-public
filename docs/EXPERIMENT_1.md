# Experiment 1: Untuned compact model baseline

## Objective
Establish the first **actual model inference** baseline for mapping an account
description to one of six simplified standardized categories. This educational
public demo is a small illustrative subset of the wider IT 344 project.

## Input and data safety
`data/synthetic_accounts.csv` contains 18 wholly invented labels, three per
category. It contains no customer workbooks, financial values, property names,
proprietary prompts, production weights, or access tokens.

## Run
Requires Python 3.10+ and internet access once to download the public model.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-demo.txt
python src/run_compact_baseline.py
```

Windows activation: `.venv\\Scripts\\activate`.

A prediction CSV is written to `results/compact_baseline.csv`, and JSON
metrics print to the terminal. To rescore without invoking the model:

```bash
python src/evaluate.py results/compact_baseline.csv
```

The scripts use a public, untuned `google/flan-t5-small` instruction model,
greedy decoding, a fixed public example prompt, and a strict six-label parser.
Unknown labels are recorded as invalid instead of silently remapped.

## Evaluation
Primary: exact mapping accuracy. Secondary: macro F1, per-class F1,
invalid/unmapped output rate, and observed inference latency. Predictions and
metric values must come from an actual run. This repository intentionally
does **not** publish invented scores for the compact model.

## Limitations and next steps
- Small synthetic samples are a smoke test, not evidence of real-world accuracy.
- The public six-label taxonomy is intentionally simplified.
- The script is a model inference demo, **not** QLoRA fine-tuning.
- For the course experiment, freeze labeled and de-duplicated private splits,
  collect compact base predictions, adapt only on training data, then compare
  the adapted checkpoint and the frontier baseline on the same held-out data.
- Record model revision, hardware, seed, throughput, and per-class error analysis
  before making performance claims.
- Never commit real customer records, proprietary charts of accounts, weights,
  prompts, or private experimental results.
