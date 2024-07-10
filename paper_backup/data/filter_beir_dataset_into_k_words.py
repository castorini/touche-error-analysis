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
output_directory = "/store2/scratch/n3thakur/touche-ablations"
threshold_words = [10, 30, 50]

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

corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")

#make translator object
translator=str.maketrans('', '', string.punctuation)


for key, value in tqdm.tqdm(corpus.items(), total=len(corpus)):
    paragraph = corpus[key]["text"]
    paragraph=paragraph.translate(translator)
    corpus[key]["words"] = len(word_tokenize(paragraph))


for word_count in threshold_words:
    print(f"processing {word_count} words....")
    
    corpus_new, qrels_new = {}, {}

    for key, value in tqdm.tqdm(corpus.items(), total=len(corpus)):
        if corpus[key]["words"] >= word_count:
            corpus_new[key] = {"title": "", "text": corpus[key]["text"]}
        
    for query_id in qrels:
        qrels_new[query_id] = {}
        for doc_id, score in qrels[query_id].items():
            if doc_id in corpus_new:
                qrels_new[query_id][doc_id] = score
    
    # Save the corpus, queries and qrels in the output directory
    words = str(word_count)
    os.makedirs(os.path.join(output_directory, f"{dataset}-{words}-words"), exist_ok=True)
    os.makedirs(os.path.join(output_directory, f"{dataset}-{words}-words", "qrels"), exist_ok=True)
    
    #saving qrels    
    with open(os.path.join(output_directory, f"{dataset}-{words}-words", "corpus.jsonl"), "w") as fOut:
        for doc_id in tqdm.tqdm(corpus_new, total=len(corpus_new)):
            document = corpus_new[doc_id].get("text", "")
            json.dump({
                "_id": doc_id, 
                "text": document,
                "title": ""
            }, fOut)
            fOut.write('\n')

    with open(os.path.join(output_directory, f"{dataset}-{words}-words", "queries.jsonl"), "w") as fOut:
        for query_id in tqdm.tqdm(queries, total=len(queries)):
            document = queries[query_id]
            json.dump({
                "_id": query_id, 
                "text": document,
            }, fOut)
            fOut.write('\n')

    with open(os.path.join(output_directory, f"{dataset}-{words}-words", "qrels", "test.tsv"), "w") as fOut:
        writer = csv.writer(fOut, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["query_id", "doc_id", "score"])
        for query_id in tqdm.tqdm(qrels_new, total=len(qrels_new)):
            for doc_id, score in qrels_new[query_id].items():
                writer.writerow([query_id, doc_id, int(score)])
