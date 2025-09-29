import http.client, json, webbrowser, tempfile

conn = http.client.HTTPSConnection("api.deadlock-api.com")

def get(id, all_data = False):
    conn.request(f"GET", f"/v1/matches/{id}/metadata")

    res = conn.getresponse()
    data = res.read()

    raw = data.decode("utf-8")

    parse = json.loads(raw)

    if all_data == False:
        winning_team_id = parse["match_info"]["winning_team"]
        players = parse["match_info"]["players"]

        if len(players) != 12 or type(winning_team_id) != int:
            print(f"Incomplete data found for match {id}, skipping...")
            return [[],[]]

        heroes = []

        for player in range(len(players)):
            heroes.append(player["hero_id"])

        return [heroes, [winning_team_id]]
    else:
        return parse

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        f.write("<pre>" + json.dumps(data, indent=2) + "</pre>")
        webbrowser.open("file://" + f.name)