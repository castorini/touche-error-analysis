from beir import util, LoggingHandler

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

def load_corpus(path):
    corpus = {}
    with open(path) as f:
        for line in f:
            data = json.loads(line)
            corpus[data["_id"]] = {"text": data["text"], "title": data["title"]}
    return corpus

def load_qrels(path):
    qrels = {}

    reader = csv.reader(open(path, encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_MINIMAL)
    next(reader)
        
    for id, data in enumerate(reader):
        if data[0] not in qrels:
            qrels[data[0]] = {}
        qrels[data[0]][data[1]] = int(data[2])
    return qrels

def load_queries(path):
    queries = {}
    with open(path) as f:
        for line in f:
            data = json.loads(line)
            queries[data["_id"]] = data["text"]
    return queries

def load_results(path):
    results = {}

    reader = csv.reader(open(path, encoding="utf-8"), delimiter=" ", quoting=csv.QUOTE_NONE)
        
    for id, data in enumerate(reader):
        if data[0] not in results:
            results[data[0]] = {}
        results[data[0]][data[2]] = float(data[4])
    return results

for words in [20]:
    #### Download nfcorpus.zip dataset and unzip the dataset
    # url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{}.zip".format(dataset)
    # out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
    # data_path = util.download_and_unzip(url, out_dir)
    data_path = f"/store2/scratch/n3thakur/beir-datasets/{dataset}"

    #### Provide the data path where nfcorpus has been downloaded and unzipped to the data loader
    # data folder would contain these files: 
    # (1) nfcorpus/corpus.jsonl  (format: jsonlines)
    # (2) nfcorpus/queries.jsonl (format: jsonlines)
    # (3) nfcorpus/qrels/test.tsv (format: tsv ("\t"))

    # _, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")

    qrels_new = {}
    count = 0
    top_k = 10
    
    qrels_judged = load_qrels("/store2/scratch/n3thakur/touche-ablations/webis-touche2020-20-words/qrels/test.tsv")
    corpus = load_corpus(f"/store2/scratch/n3thakur/touche-ablations/webis-touche2020-20-words/corpus.jsonl")
    queries = load_queries(f"/store2/scratch/n3thakur/touche-ablations/webis-touche2020-20-words/queries.jsonl")

    # Results of CITADEL+
    results_citadel = load_results("/home/n3thakur/projects/beir-analysis/webis-touche2020/runs/filtered_4_model_holes_filled/run-citadel-plus.trec")

    # Results of Dragon+
    results_dragon = load_results("/home/n3thakur/projects/beir-analysis/webis-touche2020/runs/filtered_4_model_holes_filled/run-dragon-plus-encoder.trec")

    results = [results_citadel, results_dragon]
    
    docs_visited = {query_id: set() for query_id in list(results[0].keys()) + list(results[1].keys())}
    
    for result in results:
        for query_id, ranking_scores in result.items():
            scores_sorted = sorted(ranking_scores.items(), key=lambda item: item[1], reverse=True)
            for rank in range(top_k):
                doc_id = scores_sorted[rank][0]
                if doc_id not in qrels_judged[query_id] and doc_id not in docs_visited[query_id]:
                    docs_visited[query_id].add(doc_id)

    documents_filepath = os.path.join(pathlib.Path(__file__).parent.absolute(), f"unjudged-docs-citadel-plus-dragon-plus-clean-more-than-20-words.csv")              
    with open(documents_filepath, "w") as text_file:
        writer = csv.writer(text_file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["query-id", "query", "relevant", "doc-id", "document"])

        for query_id in docs_visited:
            for doc_id in docs_visited[query_id]:
                writer.writerow([query_id, queries[query_id], "", doc_id, corpus[doc_id].get("text")])
