# Error Analysis for Argument Retrieval on Touche 2020
This code repository contains data, code and results for our work in an undergoing submission at ECIR 2024.

The paper title is "Old is Gold? Systematic Error Analysis of Neural Retrieval Models against BM25 for Argument Retrieval"

## DATA: webis-touche2020-v3 (Contains Denoised and Human-judged annotations)

The Touche 2020 dataset (denoised + post-hoc judged) can be downloaded from here: [https://huggingface.co/datasets/OldisGold/webis-touche2020-v3](https://huggingface.co/datasets/OldisGold/webis-touche2020-v3).
- `corpus.jsonl` contains 303,372 arguments with empty title and argument premise as body.
- `queries.jsonl` contains 49 controversial queries (all test).
- `qrels/test.tsv` contains 2,849 relevance judgements in total.

## Installation

You will need to install tookits: Anserini (BM25), Sprint-toolkit (SPLADEv2) and BEIR (Dense Models and Evaluation).

## Code Organization

This repository has the following code organized:

- [webis-touche2020](/webis-touche2020/) contains the following folders and subfolders within the main repository.
    
    - [plots](/webis-touche2020/src/plots/) contains code for plotting boxplots for Fig. 1 in the paper.
    
    - [results](/webis-touche2020/src/results/) contains eval results for Touche 2020 experiments conducted in the paper.

    - [runs](/webis-touche2020/src/runs/) contains TREC runfiles for Touche 2020 experiments conducted in the paper.

    - [src](/webis-touche2020/src/) contains the code for experiments conducted in the paper.
        
        - [src/analysis](/webis-touche2020/src/analysis/) contains the code different analysis (document length, error, ir_axioms) done in Touche-2020.

        - [src/data](/webis-touche2020/src/data/) contains code to convert beir dataset to anserini (required for BM25) and filteration techniques.

        - [src/eval](/webis-touche2020/src/eval/) contains the code for different model evaluation in Touche-2020.

        - [src/util](/webis-touche2020/src/util/) contains simple util helper scripts.

