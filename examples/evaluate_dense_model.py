"""
Code to evaluate any Sentence Transformers model on the Webis-Touche2020-v3 dataset.
Code has been taken and little modified from the BEIR repository (http://beir.io/)
Usage: CUDA_VISIBLE_DEVICES=0 python evaluate_dense_model.py
"""

from beir import util, LoggingHandler
from beir.retrieval import models
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES

import logging
import pathlib, os
import random
import json

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

dataset = "webis-touche2020-v3"
model_name = "nthakur/contriever-base-msmarco" # or "sentence-transformers/msmarco-distilbert-base-tas-b"

#### Download webis-touche-v3.zip dataset and unzip the dataset
url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{}.zip".format(dataset)
out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
data_path = util.download_and_unzip(url, out_dir)

#### Provide the data path where webis-touche2020-v3 has been downloaded and unzipped to the data loader
# data folder would contain these files: 
# (1) webis-touche2020-v3/corpus.jsonl  (format: jsonlines)
# (2) webis-touche2020-v3/queries.jsonl (format: jsonlines)
# (3) webis-touche2020-v3/qrels/test.tsv (format: tsv ("\t"))

corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")

#### Dense Retrieval using SBERT (Sentence-BERT) ####
#### Provide any pretrained sentence-transformers model
#### The model was fine-tuned using cosine-similarity.
#### Complete list - https://www.sbert.net/docs/pretrained_models.html

model = DRES(models.SentenceBERT(model_name), batch_size=128)

#### For DRAGON+ model #####
# model = DRES(models.SentenceBERT((
#     "nthakur/dragon-plus-query-encoder",
#     "nthakur/dragon-plus-context-encoder",
#     " ",
# )), batch_size=128)

retriever = EvaluateRetrieval(model, score_function="dot")

#### Retrieve dense results (format of results is identical to qrels)
results = retriever.retrieve(corpus, queries)

#### Evaluate your retrieval using NDCG@k, MAP@K ...
logging.info("Retriever evaluation for k in: {}".format(retriever.k_values))
ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)

mrr = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="mrr")
recall_cap = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="r_cap")
hole = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="hole")

#### Print top-k documents retrieved ####
top_k = 10

query_id, ranking_scores = random.choice(list(results.items()))
scores_sorted = sorted(ranking_scores.items(), key=lambda item: item[1], reverse=True)
logging.info("Query : %s\n" % queries[query_id])

#### Creating the output results directory ####
output_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "results", dataset)
os.makedirs(output_dir, exist_ok=True)

#### Save the TREC runfile ####
if "/" in model_name: model_name = model_name.split("/")[-1].strip()
runfile = os.path.join(output_dir, f'run-{model_name}.trec')
util.save_runfile(output_file=runfile, results=results, run_name=model_name)

#### Print evaluation metrics ####
metrics_filepath = os.path.join(output_dir, f'metrics-{model_name}.json')
with open(os.path.join(metrics_filepath), 'w') as f:
    metrics = {
        'nDCG': ndcg,
        'MAP': _map,
        'Recall': recall_cap,
        'Precision': precision,
        'mrr': mrr,
        'hole': hole
    }
    json.dump(metrics, f, indent=4)