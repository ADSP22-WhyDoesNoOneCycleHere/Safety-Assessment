import json

if __name__ == "__main__":
    with open("./src/app/areas.json") as f: # for docker: ./app/areas.json
        areas = json.load(f)
        for area in areas["areas"]:
            print(area)
    