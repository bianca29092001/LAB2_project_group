from Bio import SeqIO
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os


def fasta_to_dataframe(fasta_file):
  records = SeqIO.parse(fasta_file, "fasta")
  data = {
      "id": [],
      "sequence": []
  }
  for record in records:
      data["id"].append(record.id)
      data["sequence"].append(str(record.seq))
  pos_seqs = pd.DataFrame(data)
  return pos_seqs



def cut_sp_sequence(row):
    return str(row['sequence'])[:int(row['cleavage_site'])]



def frequences_calculator(dataset):
  dataset['sp_sequence'] = dataset.apply(cut_sp_sequence, axis=1)
  all_seq = dataset['sp_sequence'].str.cat()
  all_seq = pd.Series(list(all_seq))
  all_seq = all_seq[all_seq != 'X']
  frequences = all_seq.value_counts(normalize=True) * 100
  return frequences


def cut_sp_sequence_logo(row):
  return str(row['sequence'])[(int(row['cleavage_site'])-13):(int(row['cleavage_site'])+2)]



def to_fasta(dataset, name):
    output_file = f"Logo_sequence_{name}.fasta"
    with open(output_file, "w") as logo_seq:
        for _, row in dataset.iterrows():
            logo_seq.write(f">{row['id']}\n{row['logo_sequence']}\n")
    return logo_seq
