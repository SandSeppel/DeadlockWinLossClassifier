import json
import pprint

def get_lane_wins(obj_ids, team_ids, time_destroyed):
    allowed = {1, 3, 4}
    per_lane = {}  # lane_id -> {team_id: time}

    # Sammeln
    for lane, team, t in zip(obj_ids, team_ids, time_destroyed):
        if lane in allowed:
            per_lane.setdefault(lane, {})[team] = t

    def eff(x):
        # 0 oder None behandeln wir als "nie zerstört" = sehr schlecht
        return float("inf") if (x is None or x == 0) else x

    winners = []
    for lane in sorted(allowed):  # feste Reihenfolge (1,3,4)
        tmap = per_lane.get(lane, {})
        t0, t1 = tmap.get(0), tmap.get(1)
        e0, e1 = eff(t0), eff(t1)

        if e0 < e1:
            winners.append(0)
        elif e1 < e0:
            winners.append(1)
        else:
            winners.append(-1)  # Gleichstand/keine Daten

    return winners
