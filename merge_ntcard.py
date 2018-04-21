
# coding: utf-8

# In[19]:

import numpy as np
import pandas as pd
from glob import glob
import sys


# In[38]:

path = sys.argv[1]
out = sys.argv[2]
ntcard_files = glob(path + "/*.hist")


# In[61]:

ntcard_data = pd.DataFrame()
dataframe_list = []
for ntcard_file in ntcard_files:
    split_path = ntcard_file.split('/')
    ntcard_name = split_path[len(split_path)-2]
    k = int(split_path[len(split_path)-1].split('k')[1].split('.')[0])
    row = 'k{}_{}'.format(k, ntcard_name)
    temp_df = pd.read_csv(ntcard_file, sep='\t', index_col=0, header=None, names=['kmer count', row]).T
    temp_df['k'] = k
    dataframe_list.append(temp_df)


# In[62]:

all_data = pd.concat(dataframe_list)
all_data.to_csv(out, sep='\t')

