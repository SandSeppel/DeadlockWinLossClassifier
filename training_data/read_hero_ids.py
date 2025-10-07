import pyarrow.parquet as pq
import numpy as np

from construction_helper import sort_heroes

table = pq.read_table("training_data/raw/match_player_35.parquet")


df = table.select(["match_id", "hero_id", "team", "assigned_lane"]).to_pandas()

out = (
    df.sort_values(['match_id'])
      .groupby('match_id', sort=False)  
      .agg(list)             
      .reset_index()
)

out_12 = out[out['hero_id'].str.len() == 12]

def get_hero_ids(match_id):
    row = out_12.loc[out_12['match_id'] == match_id]
    unsorted = row.iloc[0] if not row.empty else None

    if unsorted is not None:
        sorted = sort_heroes.sort(
            unsorted["hero_id"],
            unsorted["team"],
            unsorted["assigned_lane"]
        )
        return sorted

    return None