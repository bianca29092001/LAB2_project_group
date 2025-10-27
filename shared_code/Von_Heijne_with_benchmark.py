import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Bio import SeqIO
from sklearn.metrics import precision_recall_curve, confusion_matrix
import sklearn.metrics as skl


swiss_freq = {
    'A': 8.25, 'Q': 3.93, 'L': 9.64, 'S': 6.65,
    'R': 5.52, 'E': 6.71, 'K': 5.79, 'T': 5.36,
    'N': 4.06, 'G': 7.07, 'M': 2.41, 'W': 1.10,
    'D': 5.46, 'H': 2.27, 'F': 3.86, 'Y': 2.92,
    'C': 1.38, 'I': 5.90, 'P': 4.74, 'V': 6.85
}

def fasta_to_dataframe(fasta_file, second_fasta):
  ''' Function that converts a fasta file into a dataframe with id and sequence'''
  records = SeqIO.parse(fasta_file, "fasta")
  records2 = SeqIO.parse(second_fasta, "fasta")
  data = {
      "id": [],
      "sequence": []
  }
  for record in records:
      data["id"].append(record.id)
      data["sequence"].append(str(record.seq))
  for record in records2:
      data["id"].append(record.id)
      data["sequence"].append(str(record.seq))
  seqs_df = pd.DataFrame(data)
  return seqs_df


def make_groups():
  ''' Function to create order the subsets for cross validation'''
  l = [_ for _ in range(5)]
  group = {}
  for i in l:
      print(f'{(i%5)+1} {((i+1)%5)+1} {((i+2)%5)+1} {((i+3)%5)+1} {((i+4)%5)+1}')
      train = (((i%5)+1 ,((i+1)%5)+1 ,((i+2)%5)+1))
      test = ((i+3)%5)+1
      cross_val = ((i+4)%5)+1
      name_run = f'Run_{i+1}'
      group[name_run] = (train, test, cross_val)
  return group

def vh_matrix_initialize(sequences_df, window:int, indexes):
  ''' Implements and initialize the von Heijne matrix'''
  PSPM = np.ones((window,20))

  for record in sequences_df['sp_cut']:
    temp_matrix = np.zeros((window,20))
    for i, aa in enumerate(record):
      if aa in indexes:
        col = indexes[aa]
        temp_matrix[i][col] += 1

    PSPM += temp_matrix
  return PSPM



def vh_matrix_calculus(PSPM, sequences_df, swiss_freq, indexes):
  x = PSPM/(len(sequences_df) +20)
  #Divide all the counts by the corresponding residue frequency in the SwissProtbackground distribution
  for key , val in indexes.items():
    x[:,val] /= swiss_freq[key]
  #log
  PSWM = np.log(x)
  return PSWM



def von_Heijne_matrix(sequences_df, window:int, swiss_freq, indexes):
  PSPM = vh_matrix_initialize(sequences_df, window, indexes)
  PSWM = vh_matrix_calculus(PSPM, sequences_df, swiss_freq, indexes)
  return PSWM
np.set_printoptions(edgeitems=10, linewidth=400)



def best_score_calculator(sequence, n_residues: int, window: int, PSWM, aa_index):
  sequence_scores = []
  for i in range(n_residues-window+1):
    window_seq = sequence[i:i+window]
    score = 0
    for j, aa in enumerate(window_seq):
      if aa in aa_index:
        score += PSWM[j, aa_index[aa]]
    sequence_scores.append(float(score))
  return max(sequence_scores)



def cut_sp_sequence(row):
    return row['sequence'][(int(row['cleavage_site'])-13):(int(row['cleavage_site'])+2)]



def training_vonHeijne(training_set, train, indexes):
  tr_set = training_set[training_set['validation_n'].isin(train)]
  tr_set = tr_set.loc[tr_set["sp_type"]==1]
  tr_set['sp_cut'] = tr_set.apply(cut_sp_sequence, axis=1)
  PSWM= von_Heijne_matrix(tr_set, 15, swiss_freq, indexes)
  return PSWM



def score_vonHeijne(dataset, pswm, aa_index):
  score = []
  for seq in dataset["sequence"]:
      seq_score = best_score_calculator(seq, 90, 15, pswm, aa_index)
      score.append(round(seq_score,3))
  return score



def validation_vonHeijne(training_set, validation, PSWM, indexes):
  validation_set = training_set[training_set['validation_n'] == validation]
  validation_scores = score_vonHeijne(validation_set, PSWM, indexes)
  y_validation = validation_set["sp_type"].to_list()
  precision, recall, thresholds = precision_recall_curve(y_validation, validation_scores)
  fscore = (2 * precision * recall) / (precision + recall)
  index = np.argmax(fscore)
  optimal_threshold = thresholds[index]
  return optimal_threshold, validation_scores, y_validation



def test_vonHeijne(training_set, test, optimal_threshold, PSWM, indexes):
  test_set = training_set[training_set['validation_n'] == test]
  test_scores = score_vonHeijne(test_set, PSWM, indexes)
  y_pred_test = [int(t_s >= optimal_threshold) for t_s in test_scores]
  obs_test = test_set["sp_type"].to_list()
  return y_pred_test, obs_test



def metrics(obs_test, y_pred_test):
  MCC = skl.matthews_corrcoef(obs_test, y_pred_test)            # Matthews Correlation Coefficient
  ACC = skl.accuracy_score(obs_test, y_pred_test)               # Accuracy
  PPV = skl.precision_score(obs_test, y_pred_test)              # Precision
  SEN = skl.recall_score(obs_test, y_pred_test)                 # Recall
  CONF =skl.confusion_matrix(obs_test , y_pred_test)            # Confusion Matrix
  return MCC, ACC, PPV, SEN, CONF



def plot_pr_and_confusion(y_true, y_scores, y_test, y_pred_test, optimal_threshold=None, labels=None, run_id = None):
    fig, axes = plt.subplots(1, 2, figsize=(12,5))
    suffix = f"{run_id}" if run_id is not None else ""
    fig.suptitle(f'{suffix}')
    

    # Precision–Recall Curve 
    precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
    axes[0].plot(recall, precision, marker=".", label="PR curve")
    if optimal_threshold is not None:
        idx = (np.abs(thresholds - optimal_threshold)).argmin()
        axes[0].scatter(recall[idx], precision[idx], color="red", s=80,
                        label=f"Threshold={optimal_threshold:.2f}")
    axes[0].set_xlabel("Recall")
    axes[0].set_ylabel("Precision")
    axes[0].set_title("Precision–Recall curve")
    axes[0].legend()
    axes[0].grid(True)

    # Confusion Matrix 
    cm = confusion_matrix(y_test, y_pred_test, labels=labels)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels, cbar=False, ax=axes[1])
    axes[1].set_xlabel("Predicted")
    axes[1].set_ylabel("True")
    axes[1].set_title("Confusion Matrix")

    plt.tight_layout()
    filename = f"pr_and_confusion{suffix}.png"
    plt.savefig(filename)
    plt.show()

