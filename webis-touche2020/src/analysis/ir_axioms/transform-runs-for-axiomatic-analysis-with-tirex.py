#!/usr/bin/env python3

import pandas as pd

def load_queries(fileName):
    ret = pd.read_json(fileName, lines=True)
    return {str(i['_id']): str(i['text']) for _, i in ret.iterrows()}

def load_documents(fileName):
    ret = pd.read_json(fileName, lines=True)
    return {str(i["_id"]): str(i['text'] + ' ' + i['title']) for _, i in ret.iterrows()}

queries = load_queries('beir-corpus-new/queries.jsonl')
documents = load_documents('beir-corpus-new/corpus.jsonl')

print(queries['47'])
print(documents['2eb9da00-2019-04-18T12:20:27Z-00001-000'])


def process_run(run, output_file):
    run = pd.read_csv(run, sep="\s+", names=["qid", "q0", "docno", "rank", "score", "system"])
    run = run[run['docno'].isin(documents.keys())]
    run = run.copy().sort_values(["qid", "score", "docno"], ascending=[True, False, False]).reset_index()

    if 'Q0' not in run.columns:
        run['Q0'] = 0

    run = run.groupby("qid")[["qid", "Q0", "docno", "score", "system"]].head(50)

    # Make sure that rank position starts by 1
    run["rank"] = 1
    run["rank"] = run.groupby("qid")["rank"].cumsum()

    ret = []

    for _, i in run.iterrows():
        ret += [{"qid": str(i['qid']), "docno": str(i['docno']), "rank": i['rank'], "score": i['score'],"query": queries[str(i['qid'])], "text": documents[i['docno']]}]

    ret = pd.DataFrame(ret)
    ret.to_json(output_file, lines=True, orient='records')

for i in ['filtered_4_model_holes_filled', 'original']:
    for model in ['citadel-plus', 'dragon-plus-encoder']: #['RetroMAE_BEIR', 'contriever-base-msmarco', 'msmarco-distilbert-base-tas-b', 'SPLADEv2', 'dragon-plus-encoder', 'bm25-webis-touche2020-multifield']:
        process_run(f'../webis-touche2020/runs/{i}/run-{model}.trec', f'{model}/{i}/run.jsonl')

