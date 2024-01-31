"""
Script to evaluate DRAGON+ (RetroMAE as backbone) on any BEIR dataset.

Usage:
for k in 10 30 50; do
    CUDA_VISIBLE_DEVICES=4 python evaluation_sbert_dragon.py --dataset /store2/scratch/n3thakur/touche-ablations/webis-touche2020-${k}-words --output original_touche2020_${k}_words
done
"""

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
import argparse

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

parser = argparse.ArgumentParser(description='Evaluate DRAGON+ on any BEIR dataset')
parser.add_argument('--dataset', default="webis-touche2020", type=str, help='BEIR dataset name')
parser.add_argument('--output', default="", type=str, help='DRAGON+ output path')
args = parser.parse_args()


dataset = args.dataset
model_name = "nthakur/dragon-plus-encoder"

#### Download nfcorpus.zip dataset and unzip the dataset
# url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{}.zip".format(dataset)
# out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
# data_path = util.download_and_unzip(url, out_dir)
if dataset == "webis-touche2020":
    url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{}.zip".format(dataset)
    out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
    data_path = util.download_and_unzip(url, out_dir)
else:
    data_path = args.dataset

#### Provide the data path where nfcorpus has been downloaded and unzipped to the data loader
# data folder would contain these files: 
# (1) nfcorpus/corpus.jsonl  (format: jsonlines)
# (2) nfcorpus/queries.jsonl (format: jsonlines)
# (3) nfcorpus/qrels/test.tsv (format: tsv ("\t"))

corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")

#### Dense Retrieval using SBERT (Sentence-BERT) ####
#### Provide any pretrained sentence-transformers model
#### The model was fine-tuned using cosine-similarity.
#### Complete list - https://www.sbert.net/docs/pretrained_models.html

model = DRES(models.SentenceBERT((
    "nthakur/dragon-plus-query-encoder",
    "nthakur/dragon-plus-context-encoder",
    " ",
)), batch_size=128)
retriever = EvaluateRetrieval(model, score_function="dot")

#### Retrieve dense results (format of results is identical to qrels)
results = retriever.retrieve(corpus, queries)

#### Evaluate your retrieval using NDCG@k, MAP@K ...

logging.info("Retriever evaluation for k in: {}".format(retriever.k_values))
ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)

mrr = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="mrr")
recall_cap = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="r_cap")
hole = retriever.evaluate_custom(qrels, results, retriever.k_values, metric="hole")

# #### Print top-k documents retrieved ####
# top_k = 10

# query_id, ranking_scores = random.choice(list(results.items()))
# scores_sorted = sorted(ranking_scores.items(), key=lambda item: item[1], reverse=True)
# logging.info("Query : %s\n" % queries[query_id])

output_dir = os.path.join('/store2/scratch/n3thakur/touche-ablations/output', 'dragon_plus', args.output)
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
