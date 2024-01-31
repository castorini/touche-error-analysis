tira-run \
  --input-directory /mnt/ceph/storage/data-in-progress/data-research/arguana/ecir24-touche-collab-waterloo/data/tirex-corpus \
  --output-directory /mnt/ceph/storage/data-in-progress/data-research/arguana/ecir24-touche-collab-waterloo/data/axiomatic-analysis/pyterrier-index \
  --image webis/tira-ir-starter-pyterrier:0.0.2-base \
  --command '/workspace/pyterrier_cli.py --input $inputDataset --output $outputDir --index_directory $outputDir'
