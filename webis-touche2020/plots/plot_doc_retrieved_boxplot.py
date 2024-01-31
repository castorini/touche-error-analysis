"""
export OUTPUT_DIR=/store2/scratch/n3thakur/touche-ablations/output
export RUN_DIR=/home/n3thakur/projects/beir-analysis/webis-touche2020/runs/original
python plot_doc_retrieved_boxplot.py \
        --corpus_filepath /store2/scratch/n3thakur/beir-datasets/webis-touche2020/corpus.jsonl \
        --qrels_filepath /store2/scratch/n3thakur/beir-datasets/webis-touche2020/qrels/test.tsv \
        --run_files ${RUN_DIR}/run-bm25-webis-touche2020-multifield.trec ${RUN_DIR}/run-citadel-plus.trec ${RUN_DIR}/run-SPLADEv2.trec ${RUN_DIR}/run-dragon-plus-encoder.trec ${RUN_DIR}/run-contriever-base-msmarco.trec ${RUN_DIR}/run-msmarco-distilbert-base-tas-b.trec \
        --model_names BM25 CITADEL+ SPLADEv2 DRAGON+ Contriever TAS-B \
        --top_k 10 \
        --output_filepath doc_length_boxplot_top_10_final.pdf


export OUTPUT_DIR=/store2/scratch/n3thakur/touche-ablations/output
python plot_doc_retrieved_violin_plots.py \
        --corpus_filepath /store2/scratch/n3thakur/beir-datasets/final/webis-touche2020/corpus.jsonl \
        --run_files ${OUTPUT_DIR}/msmarco-distilbert-cos-v5/original_touche2020/run-msmarco-distilbert-cos-v5.trec ${OUTPUT_DIR}/msmarco-distilbert-dot-v5/original_touche2020/run-msmarco-distilbert-dot-v5.trec \
        --model_names sbert_cos_v5 sbert_dot_v5 \
        --output_filepath plots/violin_plot_cos_dot_v5.png
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
            qrels[query_id][doc_id] = int(row[3])
    return qrels

def load_corpus(path):
    corpus = {}
    with open(path) as f:
        for line in f:
            data = json.loads(line)
            corpus[data["_id"]] = {"text": data["text"], "title": data["title"]}
    return corpus

def plot_box_plot(df, x_label, y_label, save_path):
    plt.figure(figsize=(8, 3.5))
    custom_params = {"axes.spines.right": False, "axes.spines.top": False}
    sns.set_theme(style="ticks", rc=custom_params)
    ax = sns.boxplot(x=x_label, y=y_label, data=df, width=0.5, whis=[5, 95], flierprops=dict(markerfacecolor='0.9', markersize=3.5, marker="o", linestyle='none'))
    for i,box in enumerate(ax.artists):
        box.set_edgecolor('black')
        box.set_facecolor('white')
    plt.xlabel("Touché 2020 Document Length (in words)")
    plt.ylabel("")
    plt.tight_layout()

    plt.savefig(save_path, format='pdf')
    plt.close()

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus_filepath", default=None)
    parser.add_argument("--qrels_filepath", default=None)
    parser.add_argument("--run_files", nargs='+', default=[])
    parser.add_argument("--model_names", nargs='+', default=[])
    parser.add_argument("--output_filepath", default=None)
    parser.add_argument("--top_k", type=int, default=100)
    args = parser.parse_args()

    print("Loading corpus...")
    corpus = load_corpus(args.corpus_filepath)
    qrels = read_qrels(args.qrels_filepath)

    df = pd.DataFrame({
        'model_name': pd.Series(dtype='str'), 
        'avg_doc_length': pd.Series(dtype='int')})
    
    average_doc_length = []

    for query_id in qrels:
        doc_length_retrieved, count = 0, 0
        for doc_id, score in qrels[query_id].items():
            if doc_id in corpus and score > 0:
                doc_text = corpus[doc_id]["title"] + " " + corpus[doc_id]["text"]
                doc_length_retrieved += len(tokenizer.tokenize(doc_text))
                count += 1
        doc_length_retrieved /= count
        average_doc_length.append(doc_length_retrieved)
        df = df.append({'model_name': "Oracle", 'avg_doc_length': doc_length_retrieved}, ignore_index=True)

    print("Oracle average doc length:", sum(average_doc_length)/len(average_doc_length))
    
    for run_file, model_name in zip(args.run_files, args.model_names):
        average_doc_length = []
        print(f"Loading run file: {run_file}")
        qrels = read_trec_runfile(run_file)

        print("length of qrels:", len(qrels))
        print(f"Computing average document length for {model_name}...")

        for query_id in qrels:
            doc_length_retrieved, count = 0, 0
            for doc_id, score in qrels[query_id].items():
                if doc_id in corpus and count < args.top_k:
                    doc_text = corpus[doc_id]["title"] + " " + corpus[doc_id]["text"]
                    doc_length_retrieved += len(tokenizer.tokenize(doc_text))
                    count += 1
            doc_length_retrieved /= count
            average_doc_length.append(doc_length_retrieved)
            df = df.append({'model_name': model_name, 'avg_doc_length': doc_length_retrieved}, ignore_index=True)
        
        print(f"{model_name} average doc length:", sum(average_doc_length)/len(average_doc_length))
    
    plot_box_plot(df, x_label='avg_doc_length', y_label='model_name', save_path=args.output_filepath)