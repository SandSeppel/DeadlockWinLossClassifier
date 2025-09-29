import http.client
import json

conn = http.client.HTTPSConnection("assets.deadlock-api.com")
conn.request("GET", "/v2/heroes")

res = conn.getresponse()
data = res.read()

# Parse JSON
heroes = json.loads(data.decode("utf-8"))

for hero in heroes:
    print(hero["id"])  # Access 'id' of each hero
