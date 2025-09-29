import pandas as pd

# Read the HDF5 file
df = pd.read_hdf('training_data/data.h5', key='dataset')  # key is the same you used in to_hdf

# View the DataFrame
print(df["x"][0])