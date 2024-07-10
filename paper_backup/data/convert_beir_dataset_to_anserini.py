"""
This script converts the Touche-2020 dataset into Anserini format.
Usage: python convert_beir_dataset_to_anserini.py
"""

from beir import util, LoggingHandler
from beir.datasets.data_loader import GenericDataLoader

import logging
import pathlib, os
import json
import tqdm
import csv

#### Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
#### /print debug information to stdout

# Path to the BEIR dataset directory
dataset = "webis-touche2020"

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

# Make a directory to save the output
output_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets", dataset, "anserini")
os.makedirs(output_dir, exist_ok=True)

# Save the corpus, with the document text in the contents field
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

# Save the queries as a TSV file with query_id and query
with open(os.path.join(output_dir, 'queries-test.tsv'), 'w') as fOut:
    writer = csv.writer(fOut, delimiter="\t", quoting=csv.QUOTE_MINIMAL)
    for query_id in tqdm.tqdm(queries, total=len(queries)):
        query = queries[query_id]
        writer.writerow([query_id, query])

# Save the qrels as a TREC file
with open(os.path.join(output_dir, 'qrels-new.trec'), 'w') as fOut:
    for query_id in tqdm.tqdm(qrels, total=len(qrels)):
        for doc_id, score in qrels[query_id].items():
            fOut.write(" ".join([query_id, "Q0", doc_id, str(score)]))
            fOut.write('\n')

