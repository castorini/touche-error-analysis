from beir import util, LoggingHandler
from beir.retrieval import models
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES
from nltk import word_tokenize

import logging
import pathlib, os
import random
import json
import string
import tqdm
import csv

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

DATASET_DIR = "/store2/scratch/n3thakur/beir-datasets/final/webis-touche2020-w-title"
output_dir = os.path.join(DATASET_DIR, "anserini")

def load_corpus(path):
    corpus = {}
    with open(path) as f:
        for line in f:
            data = json.loads(line)
            corpus[data["_id"]] = {"text": data["text"], "title": data["title"]}
    return corpus

def load_queries(path):
    queries = {}
    with open(path) as f:
        for line in f:
            data = json.loads(line)
            queries[data["_id"]] = data["text"]
    return queries

def load_qrels(path):
    qrels = {}

    reader = csv.reader(open(path, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_MINIMAL)
    next(reader)
        
    for id, data in enumerate(reader):
        if data[0] not in qrels:
            qrels[data[0]] = {}
        qrels[data[0]][data[1]] = int(data[2])
    return qrels


corpus = load_corpus(os.path.join(DATASET_DIR, "corpus.jsonl"))
queries = load_queries(os.path.join(DATASET_DIR, "queries.jsonl"))
qrels = load_qrels(os.path.join(DATASET_DIR, "qrels", "test.tsv"))

qrels_new = {}

for query_id in qrels:
    qrels_new[query_id] = {}
    for doc_id, score in qrels[query_id].items():
        if doc_id in corpus:
            qrels_new[query_id][doc_id] = score

queries_new = {}

for query_id in queries:
    if query_id in qrels_new:
        queries_new[query_id] = queries[query_id]

qrels = qrels_new
queries = queries_new
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, 'corpus.jsonl'), 'w') as fOut:
    for doc_id in tqdm.tqdm(corpus, total=len(corpus)):
        title = corpus[doc_id].get("title", "")
        document = corpus[doc_id].get("text", "")
        json.dump({
            "id": doc_id, 
            "contents": document,
            "title": title
        }, fOut)
        fOut.write('\n')

with open(os.path.join(output_dir, 'queries-test.tsv'), 'w') as fOut:
    writer = csv.writer(fOut, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
    for query_id in tqdm.tqdm(queries, total=len(queries)):
        query = queries[query_id]
        writer.writerow([query_id, query])

with open(os.path.join(output_dir, 'qrels-new.trec'), 'w') as fOut:
    for query_id in tqdm.tqdm(qrels, total=len(qrels)):
        for doc_id, score in qrels[query_id].items():
            fOut.write(" ".join([query_id, "Q0", doc_id, str(score)]))
            fOut.write('\n')

