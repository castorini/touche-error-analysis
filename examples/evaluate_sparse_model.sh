# This script shows how to evaluate the latest SPLADEv3 model on Webis-touche-2020-v3 dataset.
# The script has been modified from the SPRINT toolkit (https://github.com/thakur-nandan/sprint)
# For more details, refer to (Thakur et al. 2023): https://dl.acm.org/doi/abs/10.1145/3539618.3591902

# The SPLADEv3 model contains one encoder for both queries and documents.
# The query and document encoder is a BERT-based model. 
# SPLADEv3: https://huggingface.co/naver/splade-v3
# For more details, refer to (Lassance et al. 2024): https://arxiv.org/abs/2403.06789

# Parameters:
# You can add multiple GPUs in the `--gpus` parameter for faster inference. 
# Add `beir_` before the dataset name in `--data_name` parameter. 
# Dataset will get downloaded in your current path (\datasets) if not present.
# Add model checkpoints (query, document) in `--ckpt_name` parameter.
# Add `--do_quantization` parameter to enable quantization.
# Add `--quantization_method` parameter to specify ndigits-round and `--ndigits` = 2 for rounding off by x100.

python -m sprint_toolkit.inference.aio \
    --encoder_name splade \
    --ckpt_name naver/splade-v3 \
    --data_name beir_webis_touche2020_v3 \
    --output_dir results/webis-touche2020-v3/splade-v3 \
    --gpus 0 \
    --do_quantization \
    --quantization_method ndigits-round \
    --ndigits 2 \
    --original_query_format beir \
    --topic_split test \
    --hits 1000

# To reproduce the numbers in the paper, we used the SPLADEv2 max model (naver/splade_v2_max) which is DistilBERT-based encoder.

# python -m sprint_toolkit.inference.aio \
#     --encoder_name splade \
#     --ckpt_name naver/splade_v2_max \
#     --data_name beir_webis_touche2020_v3 \
#     --output_dir results/webis-touche2020-v3/splade_v2_max \
#     --gpus 0 \
#     --do_quantization \
#     --quantization_method ndigits-round \
#     --ndigits 2 \
#     --original_query_format beir \
#     --topic_split test \
#     --hits 1000

# You should get the following score on the Webis-touche-2020-v3 dataset:
# {
#     "nDCG": {
#         "NDCG@1": 0.69388,
#         "NDCG@2": 0.70572,
#         "NDCG@3": 0.70773,
#         "NDCG@5": 0.68809,
#         "NDCG@10": 0.67889,
#         "NDCG@20": 0.58551,
#         "NDCG@100": 0.61202,
#         "NDCG@1000": 0.71199
#     },
#     "MAP": {
#         "MAP@1": 0.02931,
#         "MAP@2": 0.05647,
#         "MAP@3": 0.08342,
#         "MAP@5": 0.12988,
#         "MAP@10": 0.2407,
#         "MAP@20": 0.33839,
#         "MAP@100": 0.42571,
#         "MAP@1000": 0.45074
#     },
#     "Recall": {
#         "Recall@1": 0.02931,
#         "Recall@2": 0.05811,
#         "Recall@3": 0.08669,
#         "Recall@5": 0.13835,
#         "Recall@10": 0.27119,
#         "Recall@20": 0.40706,
#         "Recall@100": 0.62995,
#         "Recall@1000": 0.87859
#     },
#     "Precision": {
#         "P@1": 0.83673,
#         "P@2": 0.84694,
#         "P@3": 0.84354,
#         "P@5": 0.81633,
#         "P@10": 0.79388,
#         "P@20": 0.58776,
#         "P@100": 0.19286,
#         "P@1000": 0.02863
#     },
#     "mrr": {
#         "MRR@1": 0.83673,
#         "MRR@2": 0.89796,
#         "MRR@3": 0.89796,
#         "MRR@5": 0.90204,
#         "MRR@10": 0.90544,
#         "MRR@20": 0.90544,
#         "MRR@100": 0.90544,
#         "MRR@1000": 0.90544
#     },
#     "hole": {
#         "Hole@1": 0.0,
#         "Hole@2": 0.0,
#         "Hole@3": 0.0,
#         "Hole@5": 0.0,
#         "Hole@10": 0.0,
#         "Hole@20": 0.26735,
#         "Hole@100": 0.75245,
#         "Hole@1000": 0.95073
#     }
# }
