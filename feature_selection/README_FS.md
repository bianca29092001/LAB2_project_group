# Features extraction and selection

## Extraction 
This step involves finding features that can better help the model to distinguish protein sequences on the base of presence or not of the signal peptide. 
In particular the festures chosen are calculated on the first part of the sequence since we know from previous explorative analysis that the signal peptide is in the first positions of the sequence:  
*  **Hydrophobicity:** calculated through an hydrophobicity profile of each sequence applying the Kyte–Doolittle scale over a sliding window (5 residues) in the first 40 aa, and recording the average hydrophobicity value at each residue position.
*  **Aminoacid Composition:** vector of 20 position indicating the frequences of the first 22 aa of each sequence.
*  **Net Charge:** Measures the overall electrical charge of amino acids, indicating regions that are positively or negatively charged. For each sequence is indicated the mean, standard deviation and maximum value for each sequence.
*  **hydrophilicity:** Mean, variation, and peak hydrophilicity of the sequences calculated in a sliding window of 5 residues — indicating how exposed different regions are to water.
*  **Helix Propensity:** Statistical tendency (mean, std, and maximum) of residues to form alpha-helices calculated on a sliding window of 7 residues, reflecting local structural preferences.
*  **Flexibility:** Average, variation, and maximum flexibility scores, describing how flexible or rigid different parts of the protein are. Calculated on sliding window of 7 residues.
*  **Isoelectric Point:** Captures the average, variation, and peak local isoelectric point (pI) values along the sequence, reflecting how the balance between positive and negative charges changes across different regions of the protein.
*  **Bulkiness:** average, variation, and maximum local side-chain volume along the sequence. It describes how large or crowded the amino acid residues are in a region, how tightly it packs, and how accessible certain regions are to solvent or other molecules. Calculated on sliding window of 7 residues.


## Selection procedure

1. Create a **pipeline** with `StandardScaler()` for preprocessing and `SVC(kernel="rbf", C=C, gamma=gamma, random_state=42)` as model.
2. Define search grids for SVM hyperparameters C and gamma.
3. Perform a cross-validation fold for each combination of the 5 validation sets (at each fold of validation 3 sets are train, 1 validation and 1 test set).
4. Each cross-validation fold involves:
   * store the sets of each fold in a `.npz` format file.
   * perform a manual grid search over C and gamma values.
   * train a Random Forest classifier on the training data using the Gini importance to rank features by their predictive power and select the 20 most important features.
   * try different combinations of the selected features to choose the better one and the optimal number of features for the SVM model.
   * select the best parameters for these features
   * train a final SVM on the selected features using the best parameters.
   * evaluate the performances on the test set comparing it with the baseline model (implemented inside the pipeline) through the metrics `MCC (Matthews Correlation Coefficient), Accuracy, Precision, Recall, Confusion Matrix`. 
