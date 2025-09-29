from functools import lru_cache

import requests

@lru_cache(maxsize=1000)
def get_heroes():
    return requests.get("https://assets.deadlock-api.com/v2/heroes").json()

def hero_id_to_name(hero_id: int) -> str:
    result = next((hero for hero in get_heroes() if hero["id"] == hero_id), None)
    if result:
        return result["name"]
    return "Hero not found"

data = requests.get("https://api.deadlock-api.com/v1/matches/42160545/metadata").json()["match_info"]["players"]
player_data = []
for player in data:
    player_data.append(
        {
            "hero_id": player["hero_id"],
            "team": player["team"],
            "player_slot": player["player_slot"],
            "assigned_lane": player["assigned_lane"],
        }
    )

# sort by team, assigned_lane, player_slot
player_data.sort(key=lambda x: (-x["team"], x["assigned_lane"], x["player_slot"]))
print([hero_id_to_name(player["hero_id"]) for player in player_data])