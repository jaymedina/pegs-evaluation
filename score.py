#!/usr/bin/env python3
"""Score prediction file for Task 1.

Metrics to return:
    - ROC curve
    - PR curve
"""

import argparse
import json

import pandas as pd
from sklearn.metrics import (roc_auc_score,
                             average_precision_score)


def get_args():
    """Set up command-line interface and get arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--predictions_file",
                        type=str, required=True)
    parser.add_argument("-g", "--goldstandard_file",
                        type=str, required=True)
    parser.add_argument("-o", "--output",
                        type=str, default="results.json")
    return parser.parse_args()


def score(gold, gold_col, pred, pred_col):
    """
    Calculate metrics for: AUC-ROC, AUCPR
    """
    roc = roc_auc_score(gold[gold_col], pred[pred_col])
    pr = average_precision_score(gold[gold_col], pred[pred_col])

    return {'auc_roc': roc, 'auprc': pr}


def main():
    """Main function."""
    args = get_args()

    pred = pd.read_csv(args.predictions_file)
    gold = pd.read_csv(args.goldstandard_file)
    scores = score(gold, "disease", pred, "disease_probability")

    with open(args.output) as out:
        res = json.load(out)

    res |= {
        "validation_status": "SCORED",
        **scores
    }
    with open(args.output, "w") as out:
        out.write(json.dumps(res))


if __name__ == "__main__":
    main()
