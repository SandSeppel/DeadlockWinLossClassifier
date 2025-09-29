import pandas as pd

df = pd.read_hdf('training_data/data.h5', key='dataset')
print(len(df["x"]))