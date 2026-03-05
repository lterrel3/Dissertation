import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt 
import csv

#Load csv with audio feature data
PL_1 = pd.read_csv('Location/FileName.csv')

#input data frame
#calculate p values of correlations
#return p values
def calculate_pvalues(df):
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            tmp = df[df[r].notnull() & df[c].notnull()]
            pvalues[r][c] = round(pearsonr(tmp[r], tmp[c])[1], 8)
    return pvalues

#assign labels for figure
labels = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 
          'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']

#calculate Pearson correlation coefficients, return correlation matrix
matrix = PL_1.corr(method='pearson')

#calculate and print p values for matrix
print(calculate_pvalues(matrix))

#create figure
fig, ax = plt.subplots(figsize=(8,8))
#create matrix in figure with heatmap
ax.matshow(matrix, cmap='RdBu')
#formatting
ax.set_xticks(range(12), labels=labels, rotation=45, ha='left')
ax.set_yticks(range(12), labels=labels, rotation=45)
for (i, j), z in np.ndenumerate(matrix):
    ax.text(j, i, '{:0.2f}'.format(z), ha='center', va='center', fontsize='xx-small')

#show figure
plt.show()