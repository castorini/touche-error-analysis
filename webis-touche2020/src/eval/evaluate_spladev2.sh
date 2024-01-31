python -m sprint_toolkit.inference.aio \
    --encoder_name splade \
    --ckpt_name /home/n3thakur/projects/splade/weights/distilsplade_max \
    --data_name beir_webis_touche2020 \
    --data_dir /store2/scratch/n3thakur/beir-datasets/final/webis-touche2020 \
    --output_dir /store2/scratch/n3thakur/touche-ablations/output/splade/original_touche2020 \
    --gpus 0 \
    --do_quantization \
    --quantization_method ndigits-round \
    --ndigits 2 \
    --original_query_format beir \
    --topic_split test \
    --hits 1000