## Post-Validation Error Analysis  

This notebook performs a **post-validation error analysis** on two signal peptide (SP) prediction models:  
1. the **von Heijne model**, based on a position-specific weight matrix (PSWM), and  
2. the **Support Vector Machine (SVM)** model trained on extracted sequence features.


We investigate **False Positives (FP)** and **False Negatives (FN)** in order to understand model limitations and guide further improvements.

---

### Workflow Overview  

- **Import of validation results**  
  Loads model predictions and corresponding ground-truth labels obtained from the benchmarking phase.  

- **Identification of FP and FN**  
  Compares predicted vs. true labels to extract:  
  - **False Positives (FP):** non-SP sequences incorrectly classified as SP.  
  - **False Negatives (FN):** SP sequences missed by the model.  

- **Exploratory analysis**  
  Descriptive statistics and visualizations are used to explore FP and FN subsets for both models.  
  The analysis focuses on the physicochemical and structural features that differentiate correctly predicted signal peptides (TP) from those misclassified (FN).  

  The following aspects were investigated:
  - **Amino acid composition (AA)** among positives from the training set, true positives, and false negatives from the test set.  
  - **Von Heijne score distribution**, comparing TP and FN sequences to assess separation between canonical and borderline signal peptides.  
  - **Signal peptide sequence length**, showing how shorter or longer SPs affect model performance.  
  - **Hydrophobicity profiles** (multiple hydrophobicity feature indices), highlighting differences in the H-region between TP and FN.  
  - **Hydrophilicity distribution**, identifying polarity trends that may contribute to misclassification.  
  - **Flexibility** patterns, showing how conformational variability differs between true and false predictions.  

These plots and descriptive statistics provide a detailed view of the biochemical properties influencing model errors, supporting biological interpretation of FP/FN behavior.


---

 
The **von Heijne model** showed high precision but missed several true signal peptides, mostly short or weakly hydrophobic ones.  
The **SVM model** achieved better recall, recovering many of these cases, though at the cost of a few more false positives.  

Across all analyses — including distributions of Von Heijne scores, peptide length, hydrophobicity, hydrophilicity, and flexibility — false negatives consistently displayed lower hydrophobicity and greater variability, indicating that atypical or non-canonical sequences remain difficult to classify.  

Overall, the SVM provided a more balanced behavior, while the von Heijne approach remained more conservative but biologically interpretable.  

These observations highlight complementary strengths and suggest that future improvements could combine both strategies to achieve more robust predictions.


