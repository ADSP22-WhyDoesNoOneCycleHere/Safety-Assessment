from multiprocessing import Pool, cpu_count

import overpass

api = overpass.API(endpoint="https://overpass.kumi.systems/api/interpreter", timeout=90)

highway = [
            "[highway = primary]",
            "[highway = secondary]",
            "[highway = tertiary]",
            "[highway = unclassified]",
            "[highway = residential]",
            "[highway = primary_link]",
            "[highway = secondary_link]",
            "[highway = tertiary_link]",
            "[highway = living_street]",
        ]

parking = [
            "[highway = primary][~'^parking:.*$'~'.']",
            "[highway = secondary][~'^parking:.*$'~'.']",
            "[highway = tertiary][~'^parking:.*$'~'.']",
            "[highway = residential][~'^parking:.*$'~'.']",
            "[highway = living_street][~'^parking:.*$'~'.']",
        ]

cycleway = [
            ["[cycleway = lane][~'^parking:.*$'~'.']", "['cycleway:left' = lane][~'^parking:.*$'~'.']",
                "['cycleway:right' = lane][~'^parking:.*$'~'.']", "['cycleway:both' = lane][~'^parking:.*$'~'.']"],
            ["[cycleway = opposite][~'^parking:.*$'~'.']", "['cycleway:left' = opposite][~'^parking:.*$'~'.']",
                "['cycleway:right' = opposite][~'^parking:.*$'~'.']", "['cycleway:both' = oppposite][~'^parking:.*$'~'.']"],
            ["[cycleway = track][~'^parking:.*$'~'.']", "['cycleway:left' = track][~'^parking:.*$'~'.']",
                "['cycleway:right' = track][~'^parking:.*$'~'.']", "['cycleway:both' = track][~'^parking:.*$'~'.']"],


            ["[cycleway = track]", "['cycleway:left' = track]", "['cycleway:right' = track]",
                "['cycleway:both' = track]"],
            ["[cycleway = opposite_track]", "['cycleway:left' = opposite_track]", "['cycleway:right' = opposite_track]",
                "['cycleway:both' = opposite_track]"],
            ["[cycleway = lane]", "['cycleway:left' = lane]", "['cycleway:right' = lane]", "['cycleway:both' = lane]"],
            ["[cycleway = opposite]", "['cycleway:left' = opposite]", "['cycleway:right' = opposite]",
                "['cycleway:both' = oppposite]"],
            ["[cycleway = share_busway]", "['cycleway:left' = share_busway]", "['cycleway:right' = share_busway]",
                "['cycleway:both' = share_busway]"],
            ["[cycleway = opposite_share_busway]", "['cycleway:left' = opposite_share_busway]",
                "['cycleway:right' = opposite_share_busway]", "['cycleway:both' = opposite_share_busway]"],
            ["[cycleway = shared_lane]", "['cycleway:left' = shared_lane]", "['cycleway:right' = shared_lane]",
                "['cycleway:both' = shared_lane]"],
        ]

highway_and_cycleway = [
            ["[highway = primary][cycleway = track]", "[highway = primary]['cycleway:left' = track]",
             "[highway = primary]['cycleway:right' = track]", "[highway = primary]['cycleway:both' = track]"],
            ["[highway = secondary][cycleway = track]", "[highway = secondary]['cycleway:left' = track]",
             "[highway = secondary]['cycleway:right' = track]", "[highway = secondary]['cycleway:both' = track]"],
            ["[highway = tertiary][cycleway = track]", "[highway = tertiary]['cycleway:left' = track]",
             "[highway = tertiary]['cycleway:right' = track]", "[highway = tertiary]['cycleway:both' = track]"],
            ["[highway = residential][cycleway = track]", "[highway = residential]['cycleway:left' = track]",
             "[highway = residential]['cycleway:right' = track]", "[highway = residential]['cycleway:both' = track]"],

            ["[highway = primary][cycleway = lane]", "[highway = primary]['cycleway:left' = lane]",
             "[highway = primary]['cycleway:right' = lane]", "[highway = primary]['cycleway:both' = lane]"],
            ["[highway = secondary][cycleway = lane]", "[highway = secondary]['cycleway:left' = lane]",
             "[highway = secondary]['cycleway:right' = lane]", "[highway = secondary]['cycleway:both' = lane]"],
            ["[highway = tertiary][cycleway = lane]", "[highway = tertiary]['cycleway:left' = lane]",
             "[highway = tertiary]['cycleway:right' = lane]", "[highway = tertiary]['cycleway:both' = lane]"],
            ["[highway = residential][cycleway = lane]", "[highway = residential]['cycleway:left' = lane]",
             "[highway = residential]['cycleway:right' = lane]", "[highway = residential]['cycleway:both' = lane]"],
        ]

segregated = [
        ["[bicycle = designated][segregated = yes]", "[footway = sidewalk][segregated = yes]"]
    ]

other = [
            "[bicycle = designated][~'^parking:.*$'~'.']",
            "[bicycle_road = yes][~'^parking:.*$'~'.']",
            "[bicycle_road = yes]",
            "[highway = cycleway]",
            "[bicycle = designated]",
            "[highway = pedestrian]",
            "[highway = track]",
            "[highway = road]",
            "[highway = path]",
            "[footway = sidewalk]",
            "[highway = footway]",
            "[busway = lane]",
        ]


class Highway:

    def query_area(country = "Deutschland", city = "Berlin"):
        pool = Pool(cpu_count())
        features = pool.map(Highway.queries, [ (hw, country, city) for hw in segregated ])
        features += pool.map(Highway.queries_no_segregation, [ (hw, country, city) for hw in other ])
        features += pool.map(Highway.queries, [ (hw, country, city) for hw in cycleway ])
        features += pool.map(Highway.queries, [ (hw, country, city) for hw in highway_and_cycleway ])
        features += pool.map(Highway.queries_no_cycleway, [ (hw, country, city) for hw in parking ])
        features += pool.map(Highway.queries_no_cycleway_no_parking, [ (hw, country, city) for hw in highway ])

        pool.close()
        pool.join()

        return  { "features": features }

    def queries_no_segregation(args):
        """
        Removes segregation tags from queries and retrieves the query result
        """
        infra_types = args[0]
        country = args[1]
        city = args[2]
        res = api.get(
            "area[name = " + country + "]->.country; area[name = " + city + "]->.city; "
            "(way" + infra_types + "(area.city)(area.country); "
            "- "
            "way[~'^segregated.*$'~'.'](area.city)(area.country););",
            responseformat="json")
        return {f'{infra_types}[!segregated]': res["elements"]}

    def queries_no_cycleway(args):
        """
        Removes cycleway tags from queries and retrieves the query result
        """
        infra_types = args[0]
        country = args[1]
        city = args[2]
        res = api.get(
            "area[name = " + country + "]->.country; area[name = " + city + "]->.city; "
            "(way" + infra_types + "(area.city)(area.country); "
            "- "
            "(way[~'^cycleway.*$'~'.'](area.city)(area.country);"
            "way[~'^cycleway:.*$'~'.'](area.city)(area.country);););",
            responseformat="json")
        return {f'{infra_types}[!cycleway]': res["elements"]}

    def queries_no_cycleway_no_parking(args):
        """
        Removes cycleway tags from queries and retrieves the query result
        """
        infra_types = args[0]
        country = args[1]
        city = args[2]
        res = api.get(
            "area[name = " + country + "]->.country; area[name = " + city + "]->.city; "
            "(way" + infra_types + "(area.city)(area.country); "
            "- "
            "(way[~'^cycleway:.*$'~'.'](area.city)(area.country); "
            "way[~'^cycleway.*$'~'.'](area.city)(area.country);"
            "way[~'^parking:.*$'~'.'](area.city)(area.country);););",
            responseformat="json")
        return {f'{infra_types}[!cycleway][!parking]': res["elements"]}

    def queries(args):
        infra_types = args[0]
        country = args[1]
        city = args[2]
        if isinstance(infra_types, list):
            elements = [ ]
            for infra_type in infra_types:
                query = "area[name = " + country + "]->.country; area[name = " + city + "]->.city; way" + infra_type + "(area.city)(area.country);"
                elements += api.get(query, responseformat="json")["elements"]
            return { infra_types[0]: elements }
        else:
            res = api.get("area[name = " + country + "]->.country; area[name = " + city + "]->.city; way" + infra_types + "(area.city)(area.country);", responseformat="json")
            return { infra_types: res["elements"] }


if __name__ == '__main__':
    print(Highway.query_area())
