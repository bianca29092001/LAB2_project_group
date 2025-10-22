# Features extraction and selection

## Extraction 
This step involves finding features that can better help the model to distinguish protein sequences on the base of presence or not of the signal peptide. 
In particular the festures chosen are:  
*  **Hydrophobicity:** calculated through an hydrophobicity profile of each sequence applying the Kyte–Doolittle scale over a sliding window (with padding), and recording the average hydrophobicity value at each residue position.
