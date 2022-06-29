from multiprocessing import Pool, cpu_count
import overpass

api = overpass.API(endpoint="https://vm3.mcc.tu-berlin.de:8088/api/interpreter", timeout=90)

#highway = [
#            "[highway = trunk]",
#            "[highway = primary]",
#            "[highway = secondary]",
#            "[highway = tertiary]",
#            "[highway = unclassified]",
#            "[highway = residential]", "[highway = residential][~'^parking:.*$'~'.'][!cycleway]",
#            "[highway = motorway_link]",
#            "[highway = trunk_link]",
#            "[highway = primary_link]",
#            "[highway = secondary_link]",
#            "[highway = tertiary_link]",
#            "[highway = living_street]",
#            "[highway = service]",
#            "[highway = pedestrian]",
#            "[highway = track]",
#            "[highway = bus_guideway]",
#            "[highway = escape]",
#            "[highway = road]",
#            "[highway = busway]",
#            "[highway = footway][bicycle = yes]", "[highway = footway][bicycle = no]", "[highway = footway]",
#            "[highway = bridleway]",
#            "[highway = steps]",
#            "[highway = corridor]",
#            "[highway = path]",
#            "[footway = sidewalk][bicycle = yes]", "[footway = sidewalk][bicycle = no]", "[footway = sidewalk]",
#            "[footway = crossing][bicycle = yes]", "[footway = crossing][bicycle = no]", "[footway = crossing]",
#            "[highway = cycleway]",
#            [ "[cycleway = lane]", "['cycleway:left' = lane]", "['cycleway:right' = lane]", "['cycleway:both' = lane]" ],
#            [ "[cycleway = opposite]", "['cycleway:left' = opposite]", "['cycleway:right' = opposite]", "['cycleway:both' = opposite]" ],
#            [ "[cycleway = opposite_lane]", "['cycleway:left' = opposite_lane]", "['cycleway:right' = opposite_lane]", "['cycleway:both' = opposite_lane]" ],
#            [ "[cycleway = separate]", "['cycleway:left' = separate]", "['cycleway:right' = separate]", "['cycleway:both' = separate]", "[cycleway = track]", "['cycleway:left' = track]", "['cycleway:right' = track]", "['cycleway:both' = track]" ],
#            [ "[cycleway = opposite_track]", "['cycleway:left' = opposite_track]", "['cycleway:right' = opposite_track]", "['cycleway:both' = opposite_track]" ],
#            [ "[cycleway = share_busway]", "['cycleway:left' = share_busway]", "['cycleway:right' = share_busway]", "['cycleway:both' = share_busway]" ],
#            [ "[cycleway = opposite_share_busway]", "['cycleway:left' = opposite_share_busway]", "['cycleway:right' = opposite_share_busway]", "['cycleway:both' = opposite_share_busway]" ],
#            [ "[cycleway = shared_lane]", "['cycleway:left' = shared_lane]", "['cycleway:right' = shared_lane]", "['cycleway:both' = shared_lane]" ],
#            "[busway = lane]",
#            "[highway = construction]"
#        ]

highway = [ "[highway = trunk]" ]

class Highway:

    def query_area(name = "Berlin"):
        pool = Pool(cpu_count())
        features = pool.map(Highway.queries, [ (hw, name) for hw in highway ])
        
        pool.close()
        pool.join()

        return  { "features": features }

    def queries(args):
        infra_types = args[0]
        name = args[1]
        if isinstance(infra_types, list):
            elements = [ ]
            for infra_type in infra_types:
                query = "area[name = " + name + "]; way" + infra_type + ";"
                elements.append(api.get(query, responseformat="json")["elements"])
            return { infra_types[0]: elements }
        else:
            res = api.get("area[name = " + name + "]; way" + infra_types + ";", responseformat="json")
            return { infra_types: res["elements"] }


if __name__ == '__main__':
    print(Highway.query_area())
