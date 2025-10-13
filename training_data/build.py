import duckdb
import pickle
import numpy as np
from construction_helper import fetch_obj_wins
from construction_helper import sort_heroes

#Testing
import pprint
import unit_test

with duckdb.connect() as con:
    con.execute(
        """CREATE VIEW match_info AS FROM 
        read_parquet('https://s3-cache.deadlock-api.com/db-snapshot/public/match_metadata/match_info_44.parquet')
    """)
    con.execute(
        """CREATE VIEW match_player AS FROM
        read_parquet('https://s3-cache.deadlock-api.com/db-snapshot/public/match_metadata/match_player_44.parquet')
    """)

    df_info = con.execute(
        """SELECT match_id, "objectives.team_objective", "objectives.team", "objectives.destroyed_time_s"
        FROM match_info
        WHERE start_time > TIMESTAMP '2024-02-27 00:00:00' 
        AND duration_s > 1080
        AND game_mode = 'Normal'
        AND average_badge_team0 > 100
        AND (match_mode = 'Unranked' OR match_mode = 'Ranked')
        ORDER BY match_id
    """).fetchdf()

    df_player = con.execute(
        """SELECT match_id, hero_id, team, assigned_lane, player_slot FROM match_player
        ORDER BY match_id
    """).fetchdf()

df_player = (
    df_player.sort_values(['match_id'])
      .groupby('match_id', sort=False)  
      .agg(list)             
      .reset_index()
)

df_player = df_player[df_player['match_id'].isin(df_info['match_id'])].reset_index()
del df_player["index"]

def sort_list_by_primary(primary_list, list2):
    list1 = primary_list
    list1, list2 = zip(*sorted(zip(list1, list2)))

    return list1, list2

def get_hero_team(df, row):
    row = df.iloc[row]["team"]
    return np.array([int(s[-1]) for s in row])

def get_wins(df, row):
    keep_obj_set = {
        'Tier1Lane1',
        'Tier1Lane3',
        'Tier1Lane4'
    }

    mask_obj_list = df.iloc[row]["objectives.team_objective"]

    mask = np.isin(mask_obj_list, list(keep_obj_set))

    masked_team = df.iloc[row]["objectives.team"][mask]
    masked_team = np.array([int(s[-1]) for s in masked_team])

    masked_team_objective = df.iloc[row]["objectives.team_objective"][mask]
    masked_team_objective = np.array([int(s[-1]) for s in masked_team_objective])

    masked_destroyed_time = df.iloc[row]["objectives.destroyed_time_s"][mask]

    wins = fetch_obj_wins.get_lane_wins(masked_team_objective, masked_team, masked_destroyed_time)

    return wins

print("---------- UNIT TEST, CHECK IF YOU WANT ----------")
for row in range(5):
    keep_obj_set = {
        'Tier1Lane1',
        'Tier1Lane3',
        'Tier1Lane4'
    }

    match_id = df_info.iloc[row]["match_id"]
    wins = get_wins(df_info, row)

    team = get_hero_team(df_player, row)
    hero_id = df_player.iloc[row]["hero_id"]
    assigned_lane = df_player.iloc[row]["assigned_lane"]

    sorted = sort_heroes.sort(hero_id, team, assigned_lane)

    print(f"Match_id: {match_id}, Wins: {wins}, Heroes: {sorted}")

print("---------- -------------------------- ------------")

training_data = []

for row in range(len(df_info.index)):
    keep_obj_set = {
        'Tier1Lane1',
        'Tier1Lane3',
        'Tier1Lane4'
    }

    match_id = df_info.iloc[row]["match_id"]
    wins = get_wins(df_info, row)

    team = get_hero_team(df_player, row)
    hero_id = df_player.iloc[row]["hero_id"]
    assigned_lane = df_player.iloc[row]["assigned_lane"]

    heroes = sort_heroes.sort(hero_id, team, assigned_lane)

    training_set = [[heroes, wins], match_id.item()]
    training_data.append(training_set)

print(f"Matches: {len(training_data)}")

with open("data.pkl", "wb") as f:
    pickle.dump(training_data, f)
