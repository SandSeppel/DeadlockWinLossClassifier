import pprint, pickle
from unit_test import hero_id_to_name

with open("data.pkl", "rb") as f:
    df = pickle.load(f)

for index, match in enumerate(df):
    heroes = match[0][0]
    named_heroes = []

    for index, hero in enumerate(heroes):
        named_heroes.append(hero_id_to_name(hero))

    print([[named_heroes], match[0][1]], match[1])