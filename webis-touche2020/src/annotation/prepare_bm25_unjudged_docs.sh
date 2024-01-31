for dataset in webis-touche2020
do
    export output_path=/home/n3thakur/projects/beir-analysis/dataset/${dataset}/passage_filtering_exps/datasets/${dataset}-20-words/anserini
    export output_results_path=/home/n3thakur/projects/beir-analysis/dataset/${dataset}/passage_filtering_exps/output/bm25

    python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
        -threads 1 -input ${output_path} \
        -index ${output_results_path}/indexes/lucene-index-d2q-${dataset} -storePositions -storeDocvectors -storeRaw -fields title

    python -m pyserini.search.lucene \
              --index ${output_results_path}/indexes/lucene-index-d2q-${dataset} \
              --topics ${output_path}/queries-test.tsv \
              --output ${output_results_path}/runs/run.beir-v1.0.0-${dataset}-multifield-top10.trec \
              --output-format trec \
              --batch 36 --threads 12 \
              --fields contents=1.0 title=1.0 \
              --remove-query --hits 10
    
    python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100,1000 /home/n3thakur/projects/beir-analysis/dataset/webis-touche2020/passage_filtering_exps/datasets/webis-touche2020-20-words/anserini/qrels-new-wo-dup.trec ${output_results_path}/runs/run.beir-v1.0.0-${dataset}-multifield.trec >> ${output_results_path}/eval/results_with_tasb_4_annotators.txt
done