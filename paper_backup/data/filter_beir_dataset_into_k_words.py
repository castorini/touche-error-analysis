"""
This script filters the Touche-2020 dataset into atleast k words.
Usage: python filter_beir_dataset_into_k_words.py
"""

from beir import util, LoggingHandler
from beir.datasets.data_loader import GenericDataLoader
from nltk import word_tokenize

import logging
import pathlib, os
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
threshold_words = [10, 30, 50]

#### Download nfcorpus.zip dataset and unzip the dataset
url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{}.zip".format(dataset)
out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
data_path = util.download_and_unzip(url, out_dir)

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


# Filter the corpus and qrels based on the word count
for word_count in threshold_words:
    print(f"processing {word_count} words....")
    
    corpus_new, qrels_new = {}, {}

    for key, value in tqdm.tqdm(corpus.items(), total=len(corpus)):
        if corpus[key]["words"] >= word_count:
            # Set title as empty string and keep the text as it is if greater than k words
            corpus_new[key] = {"title": "", "text": corpus[key]["text"]}
        
    # Update the qrels based on the new documents; only keep the documents that are in the corpus
    for query_id in qrels:
        qrels_new[query_id] = {}
        for doc_id, score in qrels[query_id].items():
            if doc_id in corpus_new:
                qrels_new[query_id][doc_id] = score
    
    # Save the corpus, queries and qrels in the output directory
    words = str(word_count)
    dataset_name = f"{dataset}-filter-{words}-words"
    os.makedirs(os.path.join(out_dir, dataset_name), exist_ok=True)
    os.makedirs(os.path.join(out_dir, dataset_name, "qrels"), exist_ok=True)
    
    # Saving filtered corpus    
    with open(os.path.join(out_dir, dataset_name, "corpus.jsonl"), "w") as fOut:
        for doc_id in tqdm.tqdm(corpus_new, total=len(corpus_new)):
            document = corpus_new[doc_id].get("text", "")
            json.dump({
                "_id": doc_id, 
                "text": document,
                "title": ""
            }, fOut)
            fOut.write('\n')

    # Saving queries
    with open(os.path.join(out_dir, dataset_name, "queries.jsonl"), "w") as fOut:
        for query_id in tqdm.tqdm(queries, total=len(queries)):
            document = queries[query_id]
            json.dump({
                "_id": query_id, 
                "text": document,
            }, fOut)
            fOut.write('\n')
    
    # Saving updated qrels
    with open(os.path.join(out_dir, dataset_name, "qrels", "test.tsv"), "w") as fOut:
        writer = csv.writer(fOut, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["query_id", "doc_id", "score"])
        for query_id in tqdm.tqdm(qrels_new, total=len(qrels_new)):
            for doc_id, score in qrels_new[query_id].items():
                writer.writerow([query_id, doc_id, int(score)])
