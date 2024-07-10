<!-- ## Code Organization

This repository has the following code organized:

- [webis-touche2020](/webis-touche2020/) contains the following folders and subfolders within the main repository.
    
    - [plots](/webis-touche2020/src/plots/) contains code for plotting boxplots for Fig. 1 in the paper.
    
    - [results](/webis-touche2020/src/results/) contains eval results for Touche 2020 experiments conducted in the paper.

    - [runs](/webis-touche2020/src/runs/) contains TREC runfiles for Touche 2020 experiments conducted in the paper.

    - [src](/webis-touche2020/src/) contains the code for experiments conducted in the paper.
        
        - [src/analysis](/webis-touche2020/src/analysis/) contains the code different analysis (document length, error, ir_axioms) done in Touche-2020.

        - [src/data](/webis-touche2020/src/data/) contains code to convert beir dataset to anserini (required for BM25) and filteration techniques.

        - [src/eval](/webis-touche2020/src/eval/) contains the code for different model evaluation in Touche-2020.

        - [src/util](/webis-touche2020/src/util/) contains simple util helper scripts. -->

# Systematic Evaluation of Neural Retrieval Models on the Touché 2020 Argument Retrieval Subset of BEIR

The zero-shot effectiveness of neural retrieval models is often evaluated on the BEIR benchmark—a combination of different IR evaluation datasets. Interestingly, previous studies found that particularly on the BEIR subset Touché 2020, an argument retrieval task, neural retrieval models are considerably less effective than BM25. Still, so far, no further investigation has been conducted on what makes argument retrieval so “special”. To more deeply analyze the respective potential limits of neural retrieval models, we run a reproducibility study on the Touché 2020 data. In our study, we focus on two experiments: 
1. A black-box evaluation (i.e., no model retraining), incorporating a theoretical exploration using retrieval axioms
2. A data denoising evaluation involving post-hoc relevance judgments.

## Getting Started

### Installation
You will need to install tookits: Anserini (BM25), Sprint-toolkit (SPLADEv2) and BEIR (Dense Models and Evaluation). To install the necessary packages, run:

```sh
conda create -n python_env python=3.10
conda activate python_env

# Install JDK 21 via conda
conda install -c conda-forge openjdk=21

# PyPI installations: BEIR, Pyserini, SPRINT
pip install -r requirements.txt
```

### Dataset

The Touche 2020 v3 dataset (denoised + post-hoc judged) can be found here: [castorini/webis-touche2020-v3](https://huggingface.co/datasets/castorini/webis-touche2020-v3).
- `corpus.jsonl` contains 303,372 arguments with argument premise as body (filtering the argument corpus).
- `queries.jsonl` contains 49 controversial queries (all test queries).
- `qrels/test.tsv` contains 2,849 relevance judgements in total (including additional post-hoc relevance judgements).

## Examples


## Citation

If you use this code or dataset in your research, please cite our SIGIR 2024 paper.

```python
@INPROCEEDINGS{Thakur_etal_SIGIR2024,
   author = "Nandan Thakur and Luiz Bonifacio and Maik {Fr\"{o}be} and Alexander Bondarenko and Ehsan Kamalloo and Martin Potthast and Matthias Hagen and Jimmy Lin",
   title = "Systematic Evaluation of Neural Retrieval Models on the {Touch\'{e}} 2020 Argument Retrieval Subset of {BEIR}",
   booktitle = "Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval",
   year = 2024,
   address_ = "Washington, D.C."
}
```

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Authors

- Nandan Thakur (University of Waterloo, Waterloo, Canada)
- Luiz Bonifacio (UNICAMP and University of Waterloo, Campinas, Brazil)
- Maik Fröbe (Friedrich-Schiller-Universität Jena, Jena, Germany)
- Alexander Bondarenko (Leipzig University and Friedrich-Schiller-Universität Jena, Leipzig, Germany)
- Ehsan Kamalloo (University of Waterloo, Waterloo, Canada)
- Martin Potthast (University of Kassel, hessian.AI, and ScaDS.AI, Kassel, Germany)
- Matthias Hagen (Friedrich-Schiller-Universität Jena, Jena, Germany)
- Jimmy Lin (University of Waterloo, Waterloo, Canada)

## Acknowledgments

We would like to thank all contributors and the institutions involved in this research. Special thanks to the BEIR benchmark and Touch-2020 authors.

```
This repository contains experimental software and is published for the sole purpose of giving additional background details on the respective publication.