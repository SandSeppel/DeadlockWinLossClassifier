from construction_helper import fetch_dump as fd
from construction_helper import fetch_match_id as fmi
from construction_helper import fetch_obj_wins as fow
from construction_helper import sort_heroes as shs
import unit_test as ut

import pandas as pd
import http.client, json, webbrowser, tempfile
import pprint

rows = 100

dump = fd.fetch_dump(rows, 0)
data = []

def objective_team_win(match_id):
    raw = fmi.get(match_id, True)

    if not "match_info" in raw:
        print("Incomplete data in objective_team_win (no match_info in fmi.get())")
        return 

    raw = raw["match_info"]["objectives"]

    valid_ids = {1, 3, 4}
    data = [obj for obj in raw if obj["team_objective_id"] in valid_ids]
            
    return data

def fetch_training_data(match_id):
    objectives = objective_team_win(match_id)
    try:
        heroes = shs.sort(fmi.get(match_id, True)["match_info"]["players"])
    except:
        print("Error in fetch_training_data (match_info or players)")
        return None
    return [heroes, fow.get_lane_wins(objectives)]


if __name__ == "__main__":
    unit_test = False

    for match_id in dump:
        train_set = [fetch_training_data(match_id), match_id]

        if unit_test:
            for index, hero in enumerate(train_set[0][0]):
                train_set[0][0][index] = ut.hero_id_to_name(hero)

        if len(train_set[0]) == 2:  
            if train_set[0][0] != None and train_set[0][1] != None:
                if len(train_set[0][0]) == 12 and len(train_set[0][1]) == 3:
                    data.append(train_set)

    x_column = [row[0][0] for row in data]
    y_column = [row[0][1] for row in data]
    z_column = [row[1] for row in data]


    df = pd.DataFrame({
        'x': x_column,
        'y': y_column,
        'z': z_column
    
    })

    if unit_test:
        pd.set_option("display.max_colwidth", None)
        pd.set_option("display.max_rows", None)
        pd.set_option("display.max_columns", None)

    print(df)

    if not unit_test:
        df.to_hdf('training_data/data.h5', key='dataset', mode='w')
