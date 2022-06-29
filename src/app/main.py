import json

if __name__ == "__main__":
    with open("areas.json") as f:
        areas = json.loads(f)
        for area in areas["areas"]:
            print("sw", area[0])
            print("ne", area[1])
    