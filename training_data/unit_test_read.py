import pandas as pd
import unit_test as ut

df = pd.read_hdf("training_data/data.h5").iloc[1]
heroes = []

for i, hero in enumerate(df['x']):
    heroes.append(ut.hero_id_to_name(df['x'][i]))

print(heroes)
