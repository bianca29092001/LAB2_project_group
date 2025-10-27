# Data preparation

1. Moving the local files containing positive ([```positive.tsv```](https://github.com/Amedeoxa/LAB2_project_group_N11/blob/main/data_collection/positive.tsv), [```positive.fasta```](https://github.com/Amedeoxa/LAB2_project_group_N11/blob/main/data_collection/positive.fasta)) and negative ([```negative.tsv```](https://github.com/Amedeoxa/LAB2_project_group_N11/blob/main/data_collection/negative.tsv), [```negative.fasta```](https://github.com/Amedeoxa/LAB2_project_group_N11/blob/main/data_collection/negative.fasta)) datasets to the assigned virtual machine and viceversa with the commands:
   
   ```bash
   scp <key_config_alias> <source path> um21@m21.lsb.biocomp.unibo.it:<destination path>
   scp -i <key_config_alias> um21@m21.lsb.biocomp.unibo.it:<source path> <destination path>
   ```
3. Clustering the data with the commands:

    ```bash
   mmseqs easy-cluster positive.fasta cluster-results tmp --min-seq-id 0.3 -c 0.4 --cov-mode 0 --cluster-mode
   mmseqs easy-cluster negative.fasta cluster-results-neg tmp --min-seq-id 0.3 -c 0.4 --cov-mode 0 --cluster-mode
    ```

5. Selecting the unique ids corresponding to the representative sequences obtained through clustering with the command:

    ```bash
   cut -f 1 cluster-results-neg_cluster.tsv | uniq > uniq.neg.tsv
    ```

6. Creating the training and test set with the code in [```2_Data_preparation.ipynb```](https://github.com/Amedeoxa/LAB2_project_group_N11/blob/main/data_preparation/2_Data_preparation.ipynb)


## Results summary

|               | Training set | Test set |
|---------------|--------------|----------|
| Positive      | 874          | 219      |
| Negative      | 7147         | 1787     |
| **Total**     | 8021         | 2006     |
