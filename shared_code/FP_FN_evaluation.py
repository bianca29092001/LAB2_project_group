sys.path.append('../shared_code')
import os
import SVM_model as svm
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import Data_analysis as da
import matplotlib.ticker as ticker
import Von_Heijne_model as vh

def pie_chart_plot (name, dataset_p, dataset_n, dataset_t):
    kingdom_count_fp = dataset_p['kingdom'].value_counts()
    kingdom_count_fn = dataset_n['kingdom'].value_counts()
    kingdoms = sorted(dataset_t['kingdom'].unique())
    palette = sns.color_palette("tab10", n_colors=len(kingdoms))
    color_map = dict(zip(kingdoms, palette))
    colors_fp = [color_map[k] for k in kingdom_count_fp.index]
    colors_fn = [color_map[k] for k in kingdom_count_fn.index]
    
    fig, axes = plt.subplots(1, 2, figsize=(12,6))
    
    axes[0].pie(
        kingdom_count_fp,
        labels=kingdom_count_fp.index,
        colors=colors_fp,
        autopct='%1.1f%%',
        startangle=90
    )
    axes[0].set_title("False Positives")
    
    axes[1].pie(
        kingdom_count_fn,
        labels=kingdom_count_fn.index,
        colors=colors_fn,
        autopct='%1.1f%%',
        startangle=90
    )
    axes[1].set_title("False Negatives")
    
    plt.tight_layout()
    plt.savefig(name, dpi=500, format='png')
    plt.show()