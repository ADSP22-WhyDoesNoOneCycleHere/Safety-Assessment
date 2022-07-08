from multiprocessing import Pool, cpu_count

import overpass

api = overpass.API(endpoint="https://overpass.kumi.systems/api/interpreter", timeout=90)

highway = [
            "[highway = primary]",
            "[highway = secondary]",
            "[highway = tertiary]",
            "[highway = unclassified]",
            "[highway = residential]",
            "[highway = residential][~'^parking:.*$'~'.']",
            "[highway = primary_link]",
            "[highway = secondary_link]",
            "[highway = tertiary_link]",
            "[highway = living_street]",
            "[highway = living_street][~'^parking:.*$'~'.']",
            "[highway = service]",
            "[highway = pedestrian]",
            "[highway = track]",
            "[highway = road]",
            "[highway = busway]",
            "[highway = footway][bicycle = yes]", "[highway = footway][bicycle = no]", "[highway = footway]",
            "[highway = bridleway]",
            "[highway = path]",
            "[footway = sidewalk][bicycle = yes]", "[footway = sidewalk][bicycle = yes][segregated=yes]", "[footway = sidewalk]",
            "[footway = crossing][bicycle = yes]", "[footway = crossing]",
            ["[cycleway = lane]", "['cycleway:left' = lane]", "['cycleway:right' = lane]", "['cycleway:both' = lane]"],
            ["[cycleway = lane]", "['cycleway:left' = lane]", "['cycleway:right' = lane]", "['cycleway:both' = lane]"],
            ["[cycleway = lane][~'^parking:.*$'~'.']", "['cycleway:left' = lane][~'^parking:.*$'~'.']", "['cycleway:right' = lane][~'^parking:.*$'~'.']", "['cycleway:both' = lane][~'^parking:.*$'~'.']"],
            ["[cycleway = opposite]", "['cycleway:left' = opposite]", "['cycleway:right' = opposite]", "['cycleway:both' = oppposite]"],
            ["[cycleway = opposite][~'^parking:.*$'~'.']", "['cycleway:left' = opposite][~'^parking:.*$'~'.']", "['cycleway:right' = opposite][~'^parking:.*$'~'.']", "['cycleway:both' = oppposite][~'^parking:.*$'~'.']"],
            ["[cycleway = opposite_lane]", "['cycleway:left' = opposite_lane]", "['cycleway:right' = opposite_lane]", "['cycleway:both' = opposite_lane]"],
            ["[cycleway = track]", "['cycleway:left' = track]", "['cycleway:right' = track]", "['cycleway:both' = track]"],
            ["[cycleway = track][~'^parking:.*$'~'.']", "['cycleway:left' = track][~'^parking:.*$'~'.']", "['cycleway:right' = track][~'^parking:.*$'~'.']", "['cycleway:both' = track][~'^parking:.*$'~'.']"],
            ["[cycleway = opposite_track]", "['cycleway:left' = opposite_track]", "['cycleway:right' = opposite_track]", "['cycleway:both' = opposite_track]"],
            ["[cycleway = share_busway]", "['cycleway:left' = share_busway]", "['cycleway:right' = share_busway]", "['cycleway:both' = share_busway]"],
            ["[cycleway = opposite_share_busway]", "['cycleway:left' = opposite_share_busway]", "['cycleway:right' = opposite_share_busway]", "['cycleway:both' = opposite_share_busway]"],
            ["[cycleway = shared_lane]", "['cycleway:left' = shared_lane]", "['cycleway:right' = shared_lane]", "['cycleway:both' = shared_lane]"],
            "[bicycle = designated]", "[bicycle_road = yes]", "[highway = cycleway]",
            "[bicycle = designated][segregated = yes]",
            "[busway = lane]",
            "[highway = construction]"
        ]


class Highway:

    def query_area(country="Deutschland", city="Berlin"):
        pool = Pool(cpu_count())
        features = pool.map(Highway.queries, [(hw, country, city) for hw in highway])

        pool.close()
        pool.join()

        return {"features": features}

    def queries(args):
        infra_types = args[0]
        country = args[1]
        city = args[2]
        if isinstance(infra_types, list):
            elements = []
            for infra_type in infra_types:
                query = "area[name = " + country + "]->.country; area[name = " + city + "]->.city; way" + infra_type + "(area.city)(area.country);"
                elements += api.get(query, responseformat="json")["elements"]
            return {infra_types[0]: elements}
        else:
            res = api.get(
                "area[name = " + country + "]->.country; area[name = " + city + "]->.city; way" + infra_types + "(area.city)(area.country);",
                responseformat="json")
            return {infra_types: res["elements"]}


if __name__ == '__main__':
    print(Highway.query_area())