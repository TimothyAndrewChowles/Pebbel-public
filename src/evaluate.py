"""Minimal evaluation scaffold for IT 344.

Expected CSV columns:
- gold_label
- predicted_label

Optional:
- latency_ms
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def evaluate(rows: list[dict[str, str]]) -> dict[str, object]:
    if not rows:
        raise ValueError("No rows found")

    correct = 0
    invalid = 0
    labels = set()
    tp = Counter()
    fp = Counter()
    fn = Counter()
    latencies: list[float] = []

    for row in rows:
        gold = row["gold_label"].strip()
        pred = row["predicted_label"].strip()
        labels.add(gold)

        if not pred:
            invalid += 1

        if gold == pred:
            correct += 1
            tp[gold] += 1
        else:
            fn[gold] += 1
            if pred:
                fp[pred] += 1

        raw_latency = row.get("latency_ms", "").strip()
        if raw_latency:
            latencies.append(float(raw_latency))

    per_label_f1 = {}
    for label in sorted(labels):
        precision_denom = tp[label] + fp[label]
        recall_denom = tp[label] + fn[label]
        precision = tp[label] / precision_denom if precision_denom else 0.0
        recall = tp[label] / recall_denom if recall_denom else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall
            else 0.0
        )
        per_label_f1[label] = f1

    result = {
        "n": len(rows),
        "exact_accuracy": correct / len(rows),
        "macro_f1": sum(per_label_f1.values()) / len(per_label_f1),
        "invalid_or_unmapped_rate": invalid / len(rows),
        "per_label_f1": per_label_f1,
    }

    if latencies:
        latencies.sort()
        result["mean_latency_ms"] = sum(latencies) / len(latencies)

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions_csv", type=Path)
    args = parser.parse_args()

    result = evaluate(load_rows(args.predictions_csv))
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
