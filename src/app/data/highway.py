from multiprocessing import Pool, cpu_count
import overpass

api = overpass.API(endpoint="https://overpass.kumi.systems/api/interpreter", timeout=90)


highway = [
            "[highway = primary]",
            "[highway = secondary]",
            "[highway = tertiary]",
            "[highway = unclassified]",
            "[highway = residential]", "[highway = residential][~'^parking:.*$'~'.'][!cycleway]",
            "[highway = motorway_link]",
            "[highway = primary_link]",
            "[highway = secondary_link]",
            "[highway = tertiary_link]",
            "[highway = living_street]",
            "[highway = service]",
            "[highway = pedestrian]",
            "[highway = track]",
            "[highway = busway]",
            "[highway = footway][bicycle = yes]", "[highway = footway][bicycle = no]", "[highway = footway]",
            "[highway = bridleway]",
            "[highway = steps]",
            "[highway = path]",
            "[footway = sidewalk][bicycle = yes]", "[footway = sidewalk]",
            "[footway = crossing][bicycle = yes]", "[footway = crossing]",
            ["[cycleway = lane]", "['cycleway:left' = lane]", "['cycleway:right' = lane]", "['cycleway:both' = lane]"],
            ["[cycleway = opposite]", "['cycleway:left' = opposite]", "['cycleway:right' = opposite]", "['cycleway:both' = opposite]"],
            ["[cycleway = opposite_lane]", "['cycleway:left' = opposite_lane]", "['cycleway:right' = opposite_lane]", "['cycleway:both' = opposite_lane]"],
            ["[cycleway = separate]", "['cycleway:left' = separate]", "['cycleway:right' = separate]", "['cycleway:both' = separate]", "[cycleway = track]", "['cycleway:left' = track]", "['cycleway:right' = track]", "['cycleway:both' = track]"],
            ["[cycleway = opposite_track]", "['cycleway:left' = opposite_track]", "['cycleway:right' = opposite_track]", "['cycleway:both' = opposite_track]"],
            ["[cycleway = share_busway]", "['cycleway:left' = share_busway]", "['cycleway:right' = share_busway]", "['cycleway:both' = share_busway]"],
            ["[cycleway = shared_lane]", "['cycleway:left' = shared_lane]", "['cycleway:right' = shared_lane]", "['cycleway:both' = shared_lane]"],
            "[bicycle = designated]", "[bicycle_road = yes]", "[highway = cycleway]",  # Might have to be put together if overlap is too big
            "[busway = lane]",
            "[highway = construction]"
        ]


class Highway:

    def query_area(sw = "52.51326008267224, 13.322514165234397", ne = "52.51681153023918, 13.335043884715132"):

        pool = Pool(cpu_count())
        features = pool.map(Highway.queries, [ (hw, sw, ne) for hw in highway ])
        
        pool.close()
        pool.join()

        return  { "features": features }

    def queries(args):
        infra_types = args[0]
        sw = args[1]
        ne = args[2]
        if isinstance(infra_types, list):
            query = "("
            for infra_type in infra_types:
                query += "way" + infra_type + "(" + sw + "," + ne + ");"
            query += ");"
            res = api.get(query, responseformat="json")
            return { infra_types[0]: res["elements"] }
        else:
            res = api.get("way" + infra_types + "(" + sw + "," + ne + ")", responseformat="json")
            return { infra_types: res["elements"] }


if __name__ == '__main__':
    import time

    start = time.time()
    print(len(Highway.query_area()["features"]))
    end = time.time()
    new_time = end - start
    print(new_time)

    start = time.time()
    sw = "52.51326008267224, 13.322514165234397"
    ne = "52.51681153023918, 13.335043884715132"
    elements = { "features": [ ] }
    for infra_types in highway:
        if isinstance(infra_types, list):
            query = ""
            for infra_type in infra_types:
                query += "way" + infra_type + "(" + sw + "," + ne + ");"
            res = api.get(query, responseformat="json")
            elements["features"].append({infra_types[0]: res["elements"]})
        else:
            res = api.get("way" + infra_types + "(" + sw + "," + ne + ")", responseformat="json")
            elements["features"].append( { infra_types: res["elements"] } )
    print(len(elements["features"]))
    end = time.time()
    old_time = end - start
    print(old_time)

    print( (old_time - new_time) / old_time )
