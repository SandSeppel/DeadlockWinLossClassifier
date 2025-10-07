import requests

url = "https://assets.deadlock-api.com/v2/heroes"

def hero_id_to_name(hero_id):
    res = requests.get(url, timeout=10)

    while res.status_code != 200:
        res = requests.get(url, timeout=10)
        print(f"Error getting Hero_id: {hero_id}, retrying...")

    data = res.json()
    for hero in data:
        if hero["id"] == hero_id:
            return hero["class_name"]


if __name__ == "__main__":
    print(hero_id_to_name(2))
