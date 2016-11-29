import pandas as pd

from utils import write_xlsx, get_sleepOnset, get_sleepdurarion

raw_df = pd.read_hdf('dataset/data.h5', 'raw')

labels_df = pd.read_hdf('dataset/data.h5', 'labels')

# print(raw_df.columns)
# print(labels_df.columns)

# write_xlsx(labels_df, "labels_df.xlsx")
# get_sleepOnset(labels_df)
get_sleepdurarion(labels_df)