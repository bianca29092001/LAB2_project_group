# LAB2_project_group_N11

Machine Learning project aimed at predicting **signal peptides** (SPs) in protein sequences using two complementary approaches: **Von Heijne’s statistical model** and **Support Vector Machine (SVM)**. 

##  [Data Collection](1_data_collection/README_DC.md)
-  Download positive (with SP) and negative (without SP) protein sets from UniProt in JSON format using specific selection criteria.
The corresponding queries are available in [`query_pos.txt`](query_pos.txt) and [`query_neg.txt`](query_neg.txt).
- After applying additional filtering steps, results are converted into TSV and FASTA files. 
---
## [Data Preparation](2_data_preparation/README_DP.md) 
- Remove redundancy: Positive and negative sequences are clustered separately using MMseqs, producing:
[`non_redundant_pos.tsv`](non_redundant_pos.tsv)
[`non_redundant_neg.tsv`](non_redundant_neg.tsv)
- Dataset split: 80% of each class is used for training and 20% for testing.
- Cross-validation: The training set is further divided into 5 folds for model evaluation.
---
## [Data Analysis](3_data_analysis/README_DA.md)
- **Sequence length distribution**: comparison of positive and negative sequences in the training and test sets, visualized with histograms.  
- **Signal peptide length distribution**: analysis of SP length in positive sequences from training and test sets, visualized with density plots.  
- **Amino acid composition**: comparison of SP amino acid frequencies between our dataset (training/test) and SwissProt reference data using barplots.  
- **Taxonomic classification**: comparison of the taxonomic composition (kingdom and species levels) between training and test sets using pie charts.
---
## [Von Heijne Model](4_von_Heijne/README_vh.md)
- Implementation of a **cross-validation pipeline** based on the von Heijne algorithm for SP identification.
- Construction of a Position-Specific Weight Matrix (PSWM) from positive SP sequences. 
- Application of the model to the **training set** to detect SPs and compute relevant performance metrics.
- Final evaluation on an **independent benchmarking set**, achieving an average MCC of 0.65 and ACC of 0.93.
- Analysis of **Precision–Recall** and **Confusion Matrix** confirming strong generalization on unseen sequences.

---
## [Support Vector Machine Model](5_SVM/README_FS.md)
- **Feature extraction**: identify the features that can possibly be informative for the identification of the presence of the signal peptide. (extracted features: Hydrophobicity, Amino Acid Composition, Net Charge, Hydrophilicity, Helix Propensity, Flexibility, Isoelectric Point (pI), Bulkiness).
- An **SVM model** is trained, and feature selection using **RFE (Recursive Feature Elimination)** is applied for each of the five validation folds (3 training sets, 1 validation set, and 1 test set).
- Final **benchmarking comparison** between SVM models trained *with* and *without* feature selection.  
- Evaluation based on **MCC, ACC, PPV, SEN, F1-score**, along with **ROC** and **Precision–Recall curves**.  
- Both models show **high accuracy (≈0.97–0.98)** and robust performance, with the non-FS model achieving slightly higher precision.
---

## [Error Analysis](6_FP_FN_evaluation/README_fp_fn.md)
Post-validation analysis of both models focused on False Positives (FP) and False Negatives (FN) to identify the main sources of misclassification.    
By comparing feature distributions (Von Heijne scores, peptide length, hydrophobicity, hydrophilicity, and flexibility), the analysis revealed that short or weakly hydrophobic sequences are more frequently misclassified.  
The SVM model recovered several of these cases, showing better recall, while the von Heijne model remained more conservative but highly precise.

---
## Requirements 
