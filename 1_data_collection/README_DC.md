## Data Collection

Filter protein sequences from **UniProt** to distinguish:
- **Positive** proteins (with signal peptides)  
- **Negative** proteins (without signal peptides)

The queries used for these searches are stored in the files [`query_neg.txt`](query_neg.txt) and [`query_pos.txt`](query_pos.txt).

### Positive subset
Proteins **with experimentally verified signal peptides** are retrieved using the following filters:
- Non-fragmented entries 
- Taxonomy ID = Eukaryota
- Sequence length ≥ 40
- Reviewed entries (SwissProt)
- Evidence at protein level
- Presence of a signal peptide feature 
- Additional filtering: SP length > 13 and cleavage site not null 

**Output files:**
[`positive.tsv`](positive.tsv)
[`positive.fasta`](positive.fasta)


### Negative subset
Proteins **without signal peptides** are retrieved using complementary filtering:
- Same base criteria as the positive query
- **No signal peptide annotation**
- Inclusion of proteins experimentally localized to compartments incompatible with signal peptides 
  (e.g., **cytoplasm**, **nucleus**, **mitochondria**, etc.)
- Detection of **transmembrane (TM) helices** in the first 90 residues
  
**Output files:**
[`negative.tsv`](negative.tsv)
[`negative.fasta`](negative.fasta)








### Results summary
| Set            | Total entry | Filtered | Transmembrane       |
|----------------|-------------|----------|---------------------|
|**Positive set**| 2949        | 2932     | –                   |
|**Negative set**| 20615       | –        | 1384                |
