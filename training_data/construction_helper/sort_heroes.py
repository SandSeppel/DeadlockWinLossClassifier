# import fetch_match_id
import pprint

def sort(players):
    #Sort by team
    teams = [[],[]]

    for player in players:
        if player["team"] == 0:
            teams[0].append(player)
        else:
            teams[1].append(player)

    sorted_teams = [[],[]]

    #Sort by lane
    for team in range(2):
        s = sorted(teams[team], key=lambda x: x["assigned_lane"])

        for player in s:
            sorted_teams[team].append(player["hero_id"])

    return sorted_teams[0] + sorted_teams[1]

# if __name__ == "__main__":
#     sorted_players = sort(fetch_match_id.get(42037161, True)["match_info"]["players"])
    
#     print(sorted_players)
