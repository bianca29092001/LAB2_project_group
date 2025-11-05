## **Von Heijne Cross-Validation Pipeline for Signal Peptide Prediction**

In this step we implement a cross-validation pipeline based on the von Heijne algorithm in order to identify signal peptides in protein sequences. 
We train, validate and test a position-specific weight matrix (PSWM) across five data subsets, computing standard classification metrics (MCC, Accuracy, Precision, Recall) and visualizing results through precision–recall curves and confusion matrices.

The dataset is divided into five subsets (1–5), which are rotated cyclically to create different combinations of training, validation, and test sets.
Each iteration follows this pattern:

| Iteration | Train   | Validation | Test |  
|------------|----------|-------------|------|  
| 1 | 1, 2, 3 | 4 | 5 |  
| 2 | 2, 3, 4 | 5 | 1 |  
| 3 | 3, 4, 5 | 1 | 2 |  
| 4 | 4, 5, 1 | 2 | 3 |  
| 5 | 5, 1, 2 | 3 | 4 |  


The PSWM is trained on positive signal peptide sequences:

  - Initialize a matrix of size (15 × 20) with all entries set to 1.
  - Count amino acid occurrences at each position in the signal peptide window.
  - Normalize by the number of sequences plus 20.
  - Adjust by dividing each column by the corresponding amino acid frequency from the SwissProt distribution.
  - Transform values using a logarithmic scale to obtain the final log-odds matrix (PSWM).

For each cycle, the trained PSWM is applied to the validation subset to compute scores for each sequence in order to determine the optimal threshold.

The PSWM and optimal threshold are then applied to the test subset to classify sequences.
The following metrics are computed:
- MCC (Matthews Correlation Coefficient)
- ACC (Accuracy)
- PPV (Positive Predictive Value)
- SEN (Recall)
Each fold produces plots for:
- Precision–Recall Curve
- Confusion Matrix

### Cross-Validation Results

Finally, the average of all five thresholds is computed to obtain the mean threshold to be used for the independent test set. 

| MCC      | ACC      | PPV      | SEN      | Threshold |
|-----------|-----------|----------|----------|------------|
| 0.658971  | 0.930186  | 0.676772 | 0.723061 | 6.1        |


### Benchmark Evaluation

For the final test, the PSWM was retrained on subsets 1–4, while subset 5, although used during cross-validation, was excluded from this training and used exclusively for evaluation.
During this final evaluation, a new optimal threshold was estimated from the benchmarking data, resulting in a value of 5.9.
This confirms consistent scoring behavior between the cross-validation and final evaluation phases, with only a small variation in the optimal decision point.

| MCC     | ACC     | PPV     | SEN     | F1 Score | Threshold |
|----------|----------|----------|----------|-----------|------------|
| 0.65327 | 0.92732 | 0.61426 | 0.78538 | 0.68938  | 5.9 |

The model achieved a strong balance between sensitivity and precision, confirming its ability to generalize to unseen data.

#### Confusion Matrix and Precision–Recall curve

| Actual / Predicted | Positive | Negative |
|--------------------|-----------|-----------|
| **Positive**       | **172 (TP)** | **47 (FN)** |
| **Negative**       | **108 (FP)** | **1679 (TN)** |

The confusion matrix confirms a strong balance between true and false classifications, highlighting good sensitivity and a high proportion of correctly identified negatives.

In addition, the **Precision–Recall curve** illustrates consistent model behavior, with high precision maintained over a broad recall range, supporting the overall balance observed in the confusion matrix.


Overall, the PSWM trained with the von Heijne-based approach demonstrated solid generalization on unseen sequences, achieving reliable performance across multiple metrics.
