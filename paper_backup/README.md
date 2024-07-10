## Code Organization

This directory has the backup code required for the SIGIR 2024 paper titled [Systematic Evaluation of Neural Retrieval Models on the Touché 2020 Argument Retrieval Subset of BEIR](https://downloads.webis.de/publications/papers/thakur_2024.pdf) by Thakur et al. 2024:

- [analysis](/paper_backup/analysis/) contains the code different analysis (document length, error, ir_axioms) done in Touche-2020.
     - [document_length](/paper_backup/analysis/document_length) contains code for plotting avg. document length across BEIR datasets.
     - [error_rate](/paper_backup/analysis/document_length) contains code for error rates in Table 3 in the paper.
     - [ir_axioms](/paper_backup/analysis/ir_axioms) contains code to compute the ir_axioms in Table 8 in the paper.
     - [lnc2_analysis](/paper_backup/analysis/lnc2_analysis) contains code to compute the synthetic LNC2 axiom results in Table 7 in the paper.
- [annotation](/paper_backup/annotation/) contains the code for generating CSV files using runfiles for human annotation.
- [data](/paper_backup/data/) contains code to convert beir dataset to anserini (required for BM25) and dataset filteration.
- [plots](/paper_backup/plots) contains code for plotting boxplots for Fig. 1 in the paper.