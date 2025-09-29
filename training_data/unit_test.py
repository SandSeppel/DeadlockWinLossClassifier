import requests

url = "https://assets.deadlock-api.com/v2/heroes"

def hero_id_to_name(hero_id):
    res = requests.get(url)
    data = res.json()
    for hero in data:
        if hero["id"] == hero_id:
            return hero["class_name"]


if __name__ == "__main__":
    print(hero_id_to_name(2))
