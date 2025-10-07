import http.client
import json

conn = http.client.HTTPSConnection("assets.deadlock-api.com")
conn.request("GET", "/v2/heroes")

res = conn.getresponse()
data = res.read()

# Parse JSON
heroes = json.loads(data.decode("utf-8"))

hero_list = []

for hero in heroes:
    hero_list.append(hero["id"])  # Access 'id' of each hero

print(hero_list)
