import pandas as pd
import pickle

from construction_helper import fetch_obj_wins

import read_hero_ids

df = pd.read_parquet("training_data/raw/match_info_35.parquet")

rank_col = "average_badge_team0"
duration_col = "duration_s"
game_mode_col = "game_mode"
time_cutoff_col = "start_time"

rank_mask = df[rank_col].between(83, 116, inclusive="both")
duration_mask = df[duration_col] >= 1080
game_mode_mask = df[game_mode_col].isin([1, 2])

ts = pd.Timestamp("2024-02-26 00:00:00+00:00", tz="UTC")
time_mask = pd.to_datetime(df[time_cutoff_col], utc=True) >= ts

all_mask = rank_mask & duration_mask & game_mode_mask & time_mask
df_filtered = df.loc[all_mask].reset_index(drop=True)

arr_df = []

for index in range(df_filtered.shape[0]):
    if index % 10000 == 0:
        print(f"Index {index}/{df_filtered.shape[0]}")

    team_obj_id = df_filtered["objectives.team_objective"][index].tolist()
    team_id = df_filtered["objectives.team"][index].tolist()
    time_destroyed = df_filtered["objectives.destroyed_time_s"][index].tolist()

    match_id = df_filtered["match_id"][index]
    heroes = read_hero_ids.get_hero_ids(df_filtered["match_id"][index])
    wins = fetch_obj_wins.get_lane_wins(team_obj_id, team_id, time_destroyed)

    if heroes is not None:
        arr = [[heroes, wins], match_id.item()]
        arr_df.append(arr)

with open("data.pkl", "wb") as f:
    pickle.dump(arr_df, f)