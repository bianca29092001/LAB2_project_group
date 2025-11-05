import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import sklearn.metrics as skl
import seaborn as sns
import math
import io
import warnings
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from Bio.SeqUtils.ProtParam import ProteinAnalysis, ProtParamData
from aaindex import aaindex1
from sklearn.metrics import matthews_corrcoef, accuracy_score, precision_score, recall_score, confusion_matrix, roc_curve, auc, precision_recall_curve, average_precision_score
sys.path.append('../shared_code')
import Data_analysis as da
import Von_Heijne_model as vh

def aa_composition(sequence, length: int, aa_index):
  ''' Calculate the aminoacid frequency of a sequence of a given length
  '''
  sequence = sequence[:length]
  freq = np.zeros((1, 20))
  for aa in sequence:
    if aa in aa_index.keys():
      freq[0, aa_index[aa]] += 1
  freq = np.round(freq/len(sequence), 3)
  return freq

def shannon_entropy(seq, window: int):
    """Calculates the Shannon entropy on a given window of residues"""
    seq = seq[:window]
    L = len(seq)
    if L == 0:
        return 0
    freqs = {aa: seq.count(aa) / L for aa in set(seq)}
    H = -sum(p * math.log2(p) for p in freqs.values())
    return H

def hydrophobicity(sequence, window: int, length: int):
    """Calculates hydrophobicity ignoring Biopython warnings about non-standard amino acids."""
    sequence = sequence[:length]
    d = int(window / 2)
    sequence_with_padding = "X" * d + sequence + "X" * d
    # hyde warning messages
    stderr_backup = sys.stderr
    sys.stderr = io.StringIO()
    try:
        seq_padding = ProteinAnalysis(sequence_with_padding)
        kd_pos_with_padding = seq_padding.protein_scale(ProtParamData.kd, window)
    finally:
        sys.stderr = stderr_backup  
    return kd_pos_with_padding


def feature_to_array(sequence, length: int, feature_code, window: int):
    """Creates an array [mean, std, max] for a given AAindex feature,
    suppressing Biopython's non-standard amino acid warnings without altering the sequence."""
    
    sequence = sequence[:length]
    vals = aaindex1[feature_code].values

    # Hides temporarily the warnong messages 
    stderr_backup = sys.stderr
    sys.stderr = io.StringIO()
    try:
        seq = ProteinAnalysis(sequence)
        val = seq.protein_scale(vals, window)
    finally:
        sys.stderr = stderr_backup  # Restore the original stderr 

    mean = np.mean(val)
    std = np.std(val)
    max_val = np.max(val)

    return np.round([mean, std, max_val], 3)

def npz_to_dataframe(npz_file):
    '''
        Creates a dataframe from a .npz format file handling also multidimensional arrays
    '''
    matrices = np.load(npz_file)
    data = {}
    for key in matrices.files: 
        arr = matrices[key]
        if arr.ndim > 1:
          # If the array is multi-dimensional, create multiple columns
            for i in range(arr.shape[1]):
                data[f'{key}_{i+1}'] = arr[:, i]
        else:
          # If the array is 1-dimensional, use it directly
            data[key] = arr
    X = pd.DataFrame(data)
    return X, data
    
def svm_pipeline(C, gamma):
    return Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(kernel="rbf", C=C, gamma=gamma, random_state=42))
    ])

def accuracy_on_subset(C, gamma, subset_features):
    # subset by feature names
    # Convert data keys to a NumPy array for use with np.where
    data_keys_np = np.array(list(data.keys()))
    idx = [np.where(data_keys_np == f)[0][0] for f in subset_features]
    Xtr = X_train.iloc[:, idx]
    Xva = X_val.iloc[:, idx]
    pipe = svm_pipeline(C, gamma)
    pipe.fit(Xtr, y_train)     # train on TRAIN only
    return pipe.score(Xva, y_val)  # accuracy on VALIDATION

def grid_search(C_grid, gamma_grid, X_train, Y_train, X_val, Y_val):
    '''
        Selects the best scores and the best params by training a SVM model on given train and validation sets
    '''
    best_score = -np.inf
    best_params = None
    for C in C_grid:
        for gamma in gamma_grid:
            pipe = svm_pipeline(C, gamma)
            pipe.fit(X_train, Y_train)
            val_acc = pipe.score(X_val, Y_val)
            if val_acc > best_score:
                best_score = val_acc
                best_params = {"C": C, "gamma": gamma}

    return best_score, best_params
