import json
import pprint

def get_lane_wins(objectives):
    obj_ids = []
    team_ids = []
    time_destroyed = []

    if objectives == None:
        print("Incomplete data in get_lane_wins (no objectives)")
        return

    for obj in range(len(objectives)):
        obj_ids.append(objectives[obj]["team_objective_id"])
        team_ids.append(objectives[obj]["team"])
        time_destroyed.append(objectives[obj]["destroyed_time_s"])

    obj_ids_set = list(set(obj_ids))
    win_team = []

    for id in range(len(obj_ids_set)):
        current_id = obj_ids_set[id]
        current_objects = ([i for i, n in enumerate(obj_ids) if n == current_id])

        if len(current_objects) < 2:
            print("Incomplete data in fetch_obj_wins")
            return

        td1 = time_destroyed[current_objects[0]]
        td2 = time_destroyed[current_objects[1]]

        if time_destroyed[current_objects[0]] <= time_destroyed[current_objects[1]]:
            win_team.append(team_ids[current_objects[1]])
        else:
            win_team.append(team_ids[current_objects[0]])

    return win_team