import pandas as pd
import numpy as np
import os
from Bio import SeqIO


def filter_redundancy(unique_ids, total_dataset, cols):
    unique_ids = pd.read_csv(unique_ids, header=None, sep='\t', names=cols)
    total_df = pd.read_csv(total_dataset, header=None, sep='\t', names=cols)
    filtered = total_df[total_df.iloc[:,0].isin(unique_ids.iloc[:,0])]
    return filtered



def split_train_test(df: pd.DataFrame, split: int):
    random_seed = 42
    shuffle_df = df.sample(frac=1, random_state=random_seed)
    split_idx = split*len(df.index)//100
    training_set = shuffle_df.iloc[:split_idx,:].copy()
    test_set = shuffle_df.iloc[split_idx:,:].copy()
    return training_set, test_set
