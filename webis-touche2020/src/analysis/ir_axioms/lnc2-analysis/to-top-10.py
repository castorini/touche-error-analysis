#!/usr/bin/env python3

from glob import glob
import pandas as pd

runs = []

for f in glob('../../webis-touche2020/runs/original/*'):
    run = pd.read_csv(f, sep="\s+", names=["query", "Q0", "docid", "rank", "score", "system"])
    # normalize runs (some had initially negative ranks). Code from trectools
    run = run.copy().sort_values(["query", "score", "docid"], ascending=[True, False, False]).reset_index()
    run = run.groupby("query")[["query", "Q0", "docid", "score", "system"]].head(10)

    # Make sure that rank position starts by 1
    run["rank"] = 1
    run["rank"] = run.groupby("query")["rank"].cumsum()
    runs += [run]

runs = pd.concat(runs)
runs.to_csv('potential-input-runs.trec', sep=' ', index=False, header=False)

