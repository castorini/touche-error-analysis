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

dataset = "webis-touche2020"
dataset_dir = "/home/n3thakur/projects/beir-analysis/dataset/webis-touche2020/passage_filtering_exps/datasets/webis-touche2020-20-words"

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

for words in [20]:
    #### Download nfcorpus.zip dataset and unzip the dataset
    # url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{}.zip".format(dataset)
    # out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
    # data_path = util.download_and_unzip(url, out_dir)

    #### Provide the data path where nfcorpus has been downloaded and unzipped to the data loader
    # data folder would contain these files: 
    # (1) nfcorpus/corpus.jsonl  (format: jsonlines)
    # (2) nfcorpus/queries.jsonl (format: jsonlines)
    # (3) nfcorpus/qrels/test.tsv (format: tsv ("\t"))

    qrels = load_qrels(os.path.join(dataset_dir, "qrels", "test.tsv"))
    corpus = load_corpus(os.path.join(dataset_dir, "corpus.jsonl"))
    queries = load_queries(os.path.join(dataset_dir, "queries.jsonl"))

    top_k_retrieved = {}

    splade_filepath = "/home/n3thakur/projects/beir-analysis/dataset/webis-touche2020/passage_filtering_exps/output/splade/all-annotations-quantized/trec-format/run.tsv"
    reader = csv.reader(open(splade_filepath, encoding="utf-8"), delimiter=" ", quoting=csv.QUOTE_MINIMAL)
    next(reader)

    for id, data in enumerate(reader):
        query_id = str(data[0])
        if query_id not in top_k_retrieved:
            top_k_retrieved[query_id] = set()
        
        if len(top_k_retrieved[query_id]) < 10:
            top_k_retrieved[query_id].add(data[2])
    
    for query_id in top_k_retrieved.keys():
        print(query_id, len(top_k_retrieved[query_id]))

    print(queries)
    
    documents_filepath = os.path.join(pathlib.Path(__file__).parent.absolute(), "output", "all", f"unjudged-docs-splade-extra-clean-more-than-20-words.csv")
    with open(documents_filepath, "w") as text_file:
        writer = csv.writer(text_file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["query-id", "query", "relevant", "doc-id", "document"])
        for query_id in top_k_retrieved.keys():
            for doc_id in top_k_retrieved[query_id]:
                if doc_id not in qrels[query_id]:
                    writer.writerow([query_id, queries[query_id], "", doc_id, corpus[doc_id].get("text")])