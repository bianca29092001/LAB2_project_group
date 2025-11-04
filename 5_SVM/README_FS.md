# Feature Extraction and Selection

## 1. Feature Extraction

This step identifies informative features to distinguish protein sequences with or without a signal peptide.  
All features are computed on the **N-terminal region** (first part of the sequence), as previous descriptive analysis shown that signal peptides are typically located there.

### Extracted Features

| Feature | Description | Computation Details |
|---------|-------------|-------------------|
| **Hydrophobicity** | Measures hydrophobic character along the sequence. | Kyte–Doolittle scale, sliding window of 5 residues over the first 40 amino acids; average value per residue. 40-dimensional numpy array|
| **Amino Acid Composition** | Frequency of each amino acid in the sequence segment. | 20-dimensional vector (numpy array) encoding the frequency of the first 22 amino acids. |
| **Net Charge** | Overall electrostatic charge; highlights positive/negative regions. | Mean, standard deviation, and maximum values per sequence; KLEP840101 scale, window 2. Tridimensional numpy array |
| **Hydrophilicity** | Indicates how exposed sequence regions are to water. | Mean, variation, and maximum values; HOPT810101 scale, sliding window 5. Tridimensional numpy array |
| **Helix Propensity** | Tendency to form α-helices; reflects secondary structure preference. | Mean, standard deviation, and maximum; CHAM830101 scale, window 7. Tridimensional numpy array|
| **Flexibility** | Local backbone flexibility; distinguishes rigid vs flexible regions. | Mean, variation, and maximum; BHAR880101 scale, window 7. Tridimensional numpy array |
| **Isoelectric Point (pI)** | Local charge balance along the sequence. | Mean, variation, and maximum; ZIMJ680104 scale, window 2. Tridimensional numpy array|
| **Bulkiness** | Steric volume of side chains; indicates packing and solvent accessibility. | Mean, variation, and maximum; ZIMJ680102 scale, window 7. Tridimensional numpy array|

## 2. Feature Selection Procedure

This part of the analysis combines **SVM classifiers** and **Random Forests** to select the most discriminative features.


### Workflow

| Step | Description |
|------|-------------|
| 1. Pipeline Definition | Create a pipeline with `StandardScaler()` for preprocessing and `SVC(kernel="rbf", C=C, gamma=gamma)` as the classifier. Ensures proper feature scaling. |
| 2. Hyperparameter Search | Perform manual grid search over `C ∈ {0.1, 1.0, 10.0, 100.0}` and `gamma ∈ {"scale", 0.01, 0.1, 1.0}`. Select the best combination based on validation accuracy. |
| 3. Cross-Validation | Divide data into 5 folds: 3 for training, 1 for validation, 1 for testing. Save each fold in `.npz` format. |
| 4. Baseline Model Evaluation | Train an SVM on all features per fold; select best hyperparameters using validation accuracy. |
| 5. Feature Importance Ranking | Train Random Forest on training data; rank features by Gini importance; select top 20 features. |
| 6. Subset Optimization | Evaluate different top-k subsets of features with the SVM to find the optimal number of features; select best hyperparameters for the chosen subset. |
| 7. Final Model Training | Train SVM with selected features and optimized parameters; evaluate on the test set. |
| 8. Performance Evaluation | Compute metrics for both selected-feature model and baseline: MCC, Accuracy, Precision (PPV), Recall (Sensitivity), and Confusion Matrix. |

### Results summary for each validation fold 

| Fold | Model | MCC   | ACC   | PPV   | SEN   |
|------|-------|-------|-------|-------|-------|
| 1    | Selected features | 0.849 | 0.970 | 0.847 | 0.886 |
|      | All features      | 0.881 | 0.976 | 0.854 | 0.937 |
| 2    | Selected features | 0.789 | 0.959 | 0.808 | 0.817 |
|      | All features      | 0.852 | 0.971 | 0.873 | 0.863 |
| 3    | Selected features | 0.829 | 0.968 | 0.903 | 0.794 |
|      | All features      | 0.825 | 0.968 | 0.913 | 0.777 |
| 4    | Selected features | 0.860 | 0.973 | 0.888 | 0.862 |
|      | All features      | 0.858 | 0.973 | 0.902 | 0.845 |
| 5    | Selected features | 0.869 | 0.974 | 0.881 | 0.886 |
|      | All features      | 0.886 | 0.978 | 0.912 | 0.886 |

### Most significant features  
Selected at least **3 times** out of **5 runs** of cross-validation:

```python
[
  "score_1",
  "hydrophilicity_1",
  "hydrophobicity_11",
  "hydrophobicity_12",
  "hydrophobicity_10",
  "hydrophobicity_13",
  "flexibility_1",
  "hydrophobicity_9",
  "hydrophobicity_14",
  "hydrophobicity_8"
]


