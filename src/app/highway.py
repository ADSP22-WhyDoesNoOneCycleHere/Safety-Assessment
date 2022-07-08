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

    def query_area(sw = "52.51326008267224, 13.322514165234397", ne = "52.51681153023918, 13.335043884715132"):
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
        return elements
