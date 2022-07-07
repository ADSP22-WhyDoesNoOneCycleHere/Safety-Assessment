import json

from data.get_data import main

if __name__ == "__main__":
    main()
    with open("./src/app/areas.json") as f: # for docker: ./app/areas.json
        areas = json.load(f)
        for area in areas["areas"]:
            print(area)
    