for dataset in webis-touche2020;
do
    export data_path="/store2/scratch/n3thakur/touche-ablations/${dataset}/anserini"
    export output_results_path="/store2/scratch/n3thakur/touche-ablations/output/bm25/${dataset}"
    export split="test"
    
    # Remember to use the title during indexing - That is important for reproducibility
    python -m pyserini.index.lucene -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
        -threads 1 -input ${data_path} \
        -index ${output_results_path}/indexes/lucene-index-${dataset} -storePositions -storeDocvectors -storeRaw -fields title \

    # Remember to use the title during search - That is important for reproducibility
    python -m pyserini.search.lucene \
            --index ${output_results_path}/indexes/lucene-index-${dataset} \
            --topics ${data_path}/queries-${split}.tsv \
            --output ${output_results_path}/runs/runs.${dataset}-multifield.trec \
            --output-format trec \
            --batch 36 --threads 12 --bm25 \
            --fields contents=1.0 title=1.0 \
            --remove-query --hits 1000
    
    mkdir ${output_results_path}/eval/
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100,1000 -m judged.10 ${data_path}/qrels-new.trec ${output_results_path}/runs/runs.${dataset}-multifield.trec >> ${output_results_path}/eval/results.txt
done