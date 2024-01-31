"""
export OUTPUT_DIR=/store2/scratch/n3thakur/touche-ablations/output
export RUN_DIR=/home/n3thakur/projects/beir-analysis/webis-touche2020/runs/original
python error_rate_computation.py \
        --corpus_filepath /store2/scratch/n3thakur/beir-datasets/webis-touche2020/corpus.jsonl \
        --queries_filepath /store2/scratch/n3thakur/beir-datasets/webis-touche2020/queries.jsonl \
        --qrels_filepath /store2/scratch/n3thakur/beir-datasets/webis-touche2020/qrels/test.tsv \
        --run_files ${RUN_DIR}/run-bm25-webis-touche2020-multifield.trec ${RUN_DIR}/run-citadel-plus.trec ${RUN_DIR}/run-SPLADEv2.trec ${RUN_DIR}/run-dragon-plus-encoder.trec ${RUN_DIR}/run-contriever-base-msmarco.trec ${RUN_DIR}/run-msmarco-distilbert-base-tas-b.trec \
        --model_names BM25 CITADEL+ SPLADEv2 DRAGON+ Contriever TAS-B \
        --top_k 10
"""


import matplotlib.pyplot as plt
from nltk import word_tokenize
from nltk.corpus import stopwords

stop_words = stopwords.words('english')

import csv
import json
import string

translator=str.maketrans('','',string.punctuation)

def load_queries(path):
    queries = {}
    with open(path) as f:
        for line in f:
            data = json.loads(line)
            queries[data["_id"]] = data["text"]
    return queries

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

def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus_filepath", default=None)
    parser.add_argument("--queries_filepath", default=None)
    parser.add_argument("--qrels_filepath", default=None)
    parser.add_argument("--run_files", nargs='+', default=[])
    parser.add_argument("--model_names", nargs='+', default=[])
    parser.add_argument("--output_filepath", default=None)
    parser.add_argument("--top_k", type=int, default=100)
    args = parser.parse_args()

    # print("Loading corpus...")
    corpus = load_corpus(args.corpus_filepath)
    
    # print("Loading queries...")
    queries = load_queries(args.queries_filepath)

    # print("Loading qrels...")
    qrels = read_qrels(args.qrels_filepath)

    for run_file, model_name in zip(args.run_files, args.model_names):
        errors = 0
        jaccard_similarity_score = 0
        average_doc_length = []
        # print(f"Loading run file: {run_file}")
        runs = read_trec_runfile(run_file)

        for query_id in qrels:
            query_id = str(query_id)
        
            for doc_id in list(runs[query_id].keys())[:args.top_k]:
                # relevant and good document
                if doc_id in qrels[query_id]:
                    pass
                else:
                    paragraph = corpus[doc_id]["text"]
                    title = corpus[doc_id]["title"]
                    paragraph_len = len(word_tokenize(paragraph.translate(translator)))
                    
                    title = title.translate(translator).lower()
                    title_words = [word for word in set(word_tokenize(title)) if word not in stop_words]

                    query = queries[query_id]
                    query = query.translate(translator).lower()
                    query_words = [word for word in set(word_tokenize(query)) if word not in stop_words]

                    if paragraph_len <= 20 and jaccard_similarity(query_words, title_words) > 0:
                        errors += 1
            
        final_error_rate = (errors / (args.top_k * len(qrels)))
        print(f"{model_name}:", final_error_rate)