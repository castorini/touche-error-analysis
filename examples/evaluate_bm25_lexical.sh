# This script shows how to evaluate the BM25 model on Webis-touche-2020-v3 dataset
# The script has been modified from Pyserini: https://github.com/castorini/pyserini

export DATASET="webis-touche2020-v3"
export DATA_PATH="$DATASET/corpus.jsonl"
export SPLIT="test"
export OUTPUT_RESULTS="results/$DATASET/bm25"
    
# Remember to use the title during indexing - That is important for reproducibility
python -m pyserini.index.lucene -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
    -threads 1 -input $DATA_PATH \
    -index $OUTPUT_RESULTS/indexes/lucene-index-$DATASET -storePositions -storeDocvectors -storeRaw -fields title \

# Remember to use the title during search - That is important for reproducibility
python -m pyserini.search.lucene \
        --index $OUTPUT_RESULTS/indexes/lucene-index-$DATASET \
        --topics $DATA_PATH/queries-$SPLIT.tsv \
        --output $OUTPUT_RESULTS/runs/runs.$DATASET-multifield.trec \
        --output-format trec \
        --batch 36 --threads 12 --bm25 \
        --fields contents=1.0 title=1.0 \
        --remove-query --hits 1000
    
    mkdir $OUTPUT_RESULTS/eval/
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100,1000 -m judged.10 $DATA_PATH/qrels-new.trec $OUTPUT_RESULTS/runs/runs.$DATASET-multifield.trec >> $OUTPUT_RESULTS/eval/results.txt
done

#### BM25 on webis-touche2020-v3 ####
# Results:
# recall_100            	all	0.6352
# recall_1000           	all	0.8747
# ndcg_cut_10           	all	0.7850
# judged_10             	all	0.9959