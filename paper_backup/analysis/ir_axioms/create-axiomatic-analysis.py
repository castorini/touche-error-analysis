
tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/bm25-webis-touche2020-multifield/original/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/bm25-webis-touche2020-multifield/original/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'

tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/bm25-webis-touche2020-multifield/filtered_4_model_holes_filled/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/bm25-webis-touche2020-multifield/filtered_4_model_holes_filled/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'



tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/dragon-plus-encoder/original/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/dragon-plus-encoder/original/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'

tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/dragon-plus-encoder/filtered_4_model_holes_filled/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/dragon-plus-encoder/filtered_4_model_holes_filled/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'


tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/contriever-base-msmarco/original/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/contriever-base-msmarco/original/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'

tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/contriever-base-msmarco/filtered_4_model_holes_filled/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/contriever-base-msmarco/filtered_4_model_holes_filled/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'


tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/msmarco-distilbert-base-tas-b/original/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/msmarco-distilbert-base-tas-b/original/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'

tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/msmarco-distilbert-base-tas-b/filtered_4_model_holes_filled/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/msmarco-distilbert-base-tas-b/filtered_4_model_holes_filled/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'


tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/SPLADEv2/original/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/SPLADEv2/original/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'

tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/SPLADEv2/filtered_4_model_holes_filled/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/SPLADEv2/filtered_4_model_holes_filled/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'


tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/RetroMAE_BEIR/original/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/RetroMAE_BEIR/original/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'

tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/RetroMAE_BEIR/filtered_4_model_holes_filled/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/data/RetroMAE_BEIR/filtered_4_model_holes_filled/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'

tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/ir-axioms-analysis/citadel-plus/filtered_4_model_holes_filled/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/ir-axioms-analysis/citadel-plus/filtered_4_model_holes_filled/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'


tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/ir-axioms-analysis/citadel-plus/original/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/ir-axioms-analysis/citadel-plus/original/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'



tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/ir-axioms-analysis/dragon-plus-encoder/filtered_4_model_holes_filled/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/ir-axioms-analysis/dragon-plus-encoder/filtered_4_model_holes_filled/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'


tira-run \
  --input-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/ir-axioms-analysis/dragon-plus-encoder/original/ \
  --input-run /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/data/axiomatic-analysis/pyterrier-index/ \
  --output-directory /mnt/ceph/storage/data-tmp/current/kibi9872/waterloo-touche-in-progress/beir-analysis/ir-axioms-analysis/dragon-plus-encoder/original/analysis \
  --image webis/ir_axioms:0.2.13 \
  --command '/venv/bin/python -m ir_axioms --offline preferences --run-file $inputDataset/run.jsonl --run-format jsonl --index-dir $inputRun/index --output-dir $outputDir AND ANTI-REG ASPECT-REG DIV LB1 LNC1 LEN-AND LEN-DIV LEN-M-AND LEN-M-TDC LNC1 M-AND M-TDC PROX1 PROX2 PROX3 PROX4 PROX5 REG STMC1 STMC2 TF-LNC TFC1 TFC3 ORIG'
