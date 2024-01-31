
qrels = {}

with open('/home/n3thakur/projects/beir-analysis/dataset/webis-touche2020/passage_filtering_exps/datasets/webis-touche2020-20-words/anserini/qrels-new.trec') as f:
    lines = [line.rstrip() for line in f]

for line in lines:
    qid = line.split(" ")[0]
    docid = line.split(" ")[2]
    score = int(line.split(" ")[3])
    
    if qid not in qrels:
        qrels[qid] = {}
    
    if docid not in qrels[qid]:
        qrels[qid][docid] = score

with open('/home/n3thakur/projects/beir-analysis/dataset/webis-touche2020/passage_filtering_exps/datasets/webis-touche2020-20-words/anserini/qrels-new-wo-dup.trec', 'w') as fOut:
    for qid, corpus_dict in qrels.items():
        for corpus_id, score in corpus_dict.items():
            fOut.write(f"{qid} Q0 {corpus_id} {score}\n")