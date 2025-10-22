# LAB2_project_group_N11

Machine Learning project aimed at predicting **signal peptides** (SPs) in protein sequences using two complementary approaches: **Von Heijne’s statistical model** and **Support Vector Machine (SVM)**. 

## Data Collection
-  Download positive (with SP) and negative (without SP) protein sets from UniProt in JSON format using specific selection criteria.
The corresponding queries are available in [`query_pos.txt`](query_pos.txt) and [`query_neg.txt`](query_neg.txt).
- After applying additional filtering steps, results are converted into TSV and FASTA files. 
---
## Data Preparation 
- Remove redundancy: Positive and negative sequences are clustered separately using MMseqs, producing:
[`non_redundant_pos.tsv`](non_redundant_pos.tsv)
[`non_redundant_neg.tsv`](non_redundant_neg.tsv)
- Dataset split: 80% of each class is used for training and 20% for testing.
- Cross-validation: The training set is further divided into 5 folds for model evaluation.
---
## Data Analysis
- **Sequence length distribution**: comparison of positive and negative sequences in the training and test sets, visualized with histograms.  
- **Signal peptide length distribution**: analysis of SP length in positive sequences from training and test sets, visualized with density plots.  
- **Amino acid composition**: comparison of SP amino acid frequencies between our dataset (training/test) and SwissProt reference data using barplots.  
- **Taxonomic classification**: comparison of the taxonomic composition (kingdom and species levels) between training and test sets using pie charts.
---
## Von Heijne Model
- Implementation of a **cross-validation pipeline** based on the von Heijne algorithm for SP identification.
- Construction of a Position-Specific Weight Matrix (PSWM) from positive SP sequences. 
- Application of the model to the **training set** to detect SPs and compute relevant performance metrics.

---
## Support Vector Machine Model
- **Feature extraction**: identify the features that can possibly be informative for the identification of the presence of the signal peptide. (extracted features: Hydrophobicity, Amino Acid Composition, Net Charge, Hydrophilicity, Helix Propensity, Flexibility, Isoelectric Point (pI), Bulkiness).
- An **SVM model** is trained, and feature selection using **RFE (Recursive Feature Elimination)** is applied for each of the five validation folds (3 training sets, 1 validation set, and 1 test set).
More details in 

---
## Requirements 
