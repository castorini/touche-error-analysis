#!/usr/bin/env python3

from tqdm import tqdm
import json
import pandas as pd

docs = {}
with open('../../data/webis-touche2020/corpus.jsonl') as f:
    for l in tqdm(f):
        l = json.loads(l)
        docs[l['_id']] = {k: l[k] for k in ['text', "title"]}

queries = {}
with open('../../data/webis-touche2020/queries.jsonl') as f:
    for l in tqdm(f):
        l = json.loads(l)
        queries[l['_id']] = l['text']

run = pd.read_csv('sample-for-lnc2.trec', sep="\s+", names=["query", "Q0", "docid", "rank", "score", "system"], dtype={'query': str, 'docid': str})
ret = []
for _, i in run.iterrows():
    for k in [1, 2, 3, 4]:
        docid = i['docid'] + '_____' + str(k)
        text = docs[i['docid']]['title'] + ' ' + docs[i['docid']]['text']
        text = ' '.join([text]*k)

        ret += [{'qid': str(i['query']), 'query': queries[str(i['query'])], "docid": docid, "text": text}]

pd.DataFrame(ret).to_json('../../data/axiomatic-analysis/sample-with-title-for-lnc2.jsonl', lines=True, orient='records')

ret = []
for _, i in run.iterrows():
    for k in [1, 2, 3, 4]:
        docid = i['docid'] + '_____' + str(k)
        text = docs[i['docid']]['text']
        text = ' '.join([text]*k)

        ret += [{'qid': str(i['query']), 'query': queries[str(i['query'])], "docid": docid, "text": text}]

pd.DataFrame(ret).to_json('../../data/axiomatic-analysis/sample-without-title-for-lnc2.jsonl', lines=True, orient='records')

