"""Public IT 344 experimental arm: untuned compact language-model baseline.

All examples are invented. This is not the production Pebbel parser or a trained
Pebbel model. The first run downloads a public model. No credentials are required.
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

from evaluate import evaluate

LABELS = (
    "RENTAL_INCOME",
    "UTILITIES",
    "REPAIRS_MAINTENANCE",
    "PAYROLL",
    "PROPERTY_TAX",
    "INSURANCE",
)
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "synthetic_accounts.csv"


def run(input_csv: Path, output_csv: Path, model_id: str) -> dict:
    from transformers import pipeline

    with input_csv.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    if not rows or not {"account_label", "gold_label"}.issubset(rows[0]):
        raise ValueError("Input must contain account_label and gold_label columns")
    for row in rows:
        if row["gold_label"] not in LABELS:
            raise ValueError("Unrecognized gold label in input")

    generator = pipeline("text2text-generation", model=model_id, device=-1)
    predictions = []
    for row in rows:
        prompt = (
            "Classify this property operating statement account. "
            "Reply with exactly one label from: " + ", ".join(LABELS) + ". "
            "Account: " + row["account_label"] + "\nLabel:"
        )
        start = time.perf_counter()
        raw = generator(prompt, max_new_tokens=24, do_sample=False)[0]["generated_text"]
        elapsed = (time.perf_counter() - start) * 1000
        label = raw.strip().upper().replace(" ", "_")
        if label not in LABELS:
            label = ""  # Treat out-of-vocabulary output as invalid, never silently guess.
        predictions.append({
            "account_label": row["account_label"],
            "gold_label": row["gold_label"],
            "predicted_label": label,
            "latency_ms": f"{elapsed:.3f}",
        })

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(predictions[0]))
        writer.writeheader()
        writer.writerows(predictions)
    metrics = evaluate(predictions)
    return {"model": model_id, "dataset": str(input_csv), "output": str(output_csv), "synthetic_only": True, **metrics}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DATA)
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "compact_baseline.csv")
    parser.add_argument("--model", default="google/flan-t5-small")
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output, args.model), indent=2))


if __name__ == "__main__":
    main()
