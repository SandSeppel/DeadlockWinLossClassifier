import pprint

from itertools import chain

def sort(hero_ids, teams, assigned_lanes):
    def to_list_flat(x):
        if hasattr(x, "tolist"):
            x = x.tolist()
        else:
            x = list(x)
        if x and isinstance(x[0], (list, tuple)):
            x = list(chain.from_iterable(x))
        return x

    H = to_list_flat(hero_ids)
    T = to_list_flat(teams)
    L = to_list_flat(assigned_lanes)

    if not (len(H) == len(T) == len(L)):
        raise ValueError(f"Längen passen nicht: {len(H)=}, {len(T)=}, {len(L)=}")

    lane_priority = {1: 0, 4: 1, 6: 2}

    idx = sorted(range(len(H)), key=lambda i: (int(T[i]), lane_priority.get(int(L[i]), 99), i))

    return [H[i] for i in idx]


# if __name__ == "__main__":
#     sorted_players = sort(fetch_match_id.get(42037161, True)["match_info"]["players"])
    
#     print(sorted_players)
