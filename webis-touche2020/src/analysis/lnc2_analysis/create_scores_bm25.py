"""
export RUN_DIR=/store2/scratch/n3thakur/touche-ablations/output
python create_scores_bm25.py \
        --sample_file /home/n3thakur/projects/beir-analysis/data/axiomatic-analysis/sample-without-title-for-lnc2.jsonl \
        --run_files /store2/scratch/n3thakur/dpr-scale/experiments/output/original_touche2020_wo_title_maik_analysis/retrieval/retrieval.trec \
        --model_names CITADEL+ \
        --output_scores_filepath sample-without-title-for-lnc2-scores.jsonl \
        --output_filepath sample-without-title-for-lnc2-citadel-scores.jsonl
"""


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import csv
import json

from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

def read_qrels(filepath: str):
    qrels = {}
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        
        for row in reader:
            query_id = row[0]
            doc_id = row[1]
            if query_id not in qrels:
                qrels[query_id] = {doc_id: int(row[2])}
            else:
                qrels[query_id][doc_id] = int(row[2])
    return qrels

def read_trec_runfile(filepath: str):
    qrels = {}
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            query_id = row[0]
            doc_id = row[2]
            if query_id not in qrels:
                qrels[query_id] = {}
            qrels[query_id][doc_id] = row[4]
    return qrels

def load_sample_file(path):
    qrels = {}
    with open(path) as f:
        for line in f:
            data = json.loads(line)
            query_id = data["qid"]
            doc_id = data["docid"]
            if query_id not in qrels:
                qrels[query_id] = {doc_id: 1}
            else:
                qrels[query_id][doc_id] = 1
    return qrels


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample_filepath", default=None)
    parser.add_argument("--run_files", nargs='+', default=[])
    parser.add_argument("--model_names", nargs='+', default=[])
    parser.add_argument("--output_filepath", default=None)
    parser.add_argument("--output_scores_filepath", default=None)
    args = parser.parse_args()

    print("Loading corpus...")
    qrels = load_sample_file(args.sample_filepath)
    
    for run_file, model_name in zip(args.run_files, args.model_names):
        average_doc_length = []
        print(f"Loading run file: {run_file}")
        trec_run_file = read_trec_runfile(run_file)

        print("length of qrels:", len(qrels))
        print(f"Computing average document length for {model_name}...")

        for query_id in qrels:
            for doc_id, _ in qrels[query_id].items():
                if doc_id in trec_run_file[query_id]:
                    qrels[query_id][doc_id] = trec_run_file[query_id][doc_id]
                else:
                    qrels[query_id][doc_id] = 0.0
        
    with open(args.output_filepath, 'w') as f:
        with open(args.output_scores_filepath, 'r') as fIn:
            for line in fIn:
                data = json.loads(line)
                query_id = data["qid"]
                doc_id = data["docid"]
                data["scores"][model_name] = float(qrels[query_id][doc_id])
                f.write(json.dumps(data) + "\n")