import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import sklearn.metrics as skl
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio.SeqUtils import ProtParamData
from aaindex import aaindex1
from sklearn.metrics import matthews_corrcoef, accuracy_score, precision_score, recall_score, confusion_matrix, roc_curve, auc, precision_recall_curve, average_precision_score



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



def hydrophobicity(sequence, window: int, length: int):
  ''' Calculates the hydrophobicity of each residue considering the context given by sliding window of adiacent aminoacids
  '''
  sequence = sequence[:length]
  seq = ProteinAnalysis(sequence)
  kd_pos = seq.protein_scale(ProtParamData.kd,window)
  d = int(window/2)
  sequence_with_padding = "X"*d + sequence + "X"*d
  seq_padding = ProteinAnalysis(sequence_with_padding)
  kd_pos_with_padding = seq_padding.protein_scale(ProtParamData.kd, window)
  warnings.filterwarnings('ignore')
  return kd_pos_with_padding



def features(sequence, length: int, feature_code, window: int):
  ''' Creates an array of 3 values corresponding to mean, standard deviation,
      and maximum value of a given dictionary of features
  '''
  sequence = sequence[:length]
  seq = ProteinAnalysis(sequence)
  vals = aaindex1[feature_code].values
  val = seq.protein_scale(vals,window)
  mean = np.mean(val)
  std = np.std(val)
  max = np.max(val)
  return np.round([mean, std, max], 3)



def npz_to_dataframe(npz_file):
  extracted_features = np.load(npz_file)
  data = {}
  for key in extracted_features.files:
      arr = extracted_features[key]
      if arr.ndim > 1:
          # If the array is multi-dimensional, create multiple columns
          for i in range(arr.shape[1]):
              data[f'{key}_{i+1}'] = arr[:, i]
      else:
          # If the array is 1-dimensional, use it directly
          data[key] = arr
  X = pd.DataFrame(data)
  return X, data



def make_groups():
    l = [_ for _ in range(5)]
    group = {}
    for i in l:
        print(f'{(i%5)+1} {((i+1)%5)+1} {((i+2)%5)+1} {((i+3)%5)+1} {((i+4)%5)+1}')
        train = (((i%5)+1 ,((i+1)%5)+1 ,((i+2)%5)+1))
        test = ((i+3)%5)+1
        cross_val = ((i+4)%5)+1
        name_test = f'test_{i+1}'
        group[name_test] = (train, test, cross_val)
    return group



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



def metrics(obs_test, y_pred_test):
  MCC = skl.matthews_corrcoef(obs_test, y_pred_test)            # Matthews Correlation Coefficient
  ACC = skl.accuracy_score(obs_test, y_pred_test)               # Accuracy
  PPV = skl.precision_score(obs_test, y_pred_test)              # Precision
  SEN = skl.recall_score(obs_test, y_pred_test)                 # Recall
  CONF =skl.confusion_matrix(obs_test , y_pred_test)            # Confusion Matrix
  return MCC, ACC, PPV, SEN, CONF



def grid_search(C_grid, gamma_grid, X_train, Y_train, X_val, Y_val):
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
