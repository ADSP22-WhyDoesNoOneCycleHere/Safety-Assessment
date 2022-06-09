#!/usr/bin/python
from pprint import pprint

import pandas as pd
import requests as req
import db
import area
import testlength

infra_types = []
infra_dict = {}  # Dict to which the different counts are saved


def execute_queries(cur, osm_id, infra_type):

    # TODO: Look into what counts are actually important for the scores!
    query = f'Select "avoidedCount", "chosenCount", "normalIncidentCount", "scaryIncidentCount", "osmId", "count"' \
            f' from "SimRaAPI_osmwayslegs" where "osmId"={osm_id}'

    cur.execute(query)

    analysed_osm_ids = []

    for count in cur.fetchall():
        infra_dict[infra_type]["avoided_count"] += count[0]
        infra_dict[infra_type]["chosen_count"] += count[1]
        infra_dict[infra_type]["normal_incident_count"] += count[2]
        infra_dict[infra_type]["scary_incident_count"] += count[3]
        # the first time an unchecked id occurs -> add way length to the complete length
        # check for first time
        tmp_osm_id = count[4]
       
        if not tmp_osm_id in analysed_osm_ids:
            infra_dict[infra_type]["length"] += testlength.get_length(tmp_osm_id)
            analysed_osm_ids.append(tmp_osm_id)

        infra_dict[infra_type]["count"] += count[5]


def query_area(north, east, south, west):

    body = {
        "ne": str(north) + "," + str(east),
        "sw": str(south) + "," + str(west)
    }
    response = req.post("http://127.0.0.1:8000/area", json=body)

    return response.json()


# Use this function when testing new features; query_area() queries ALL of Berlin
def test():
    response = req.get("http://127.0.0.1:8000/")

    return response.json()


def test_api():
    # Structure of the json we get atm:
    # Json dict contains one key "features"
    # "Features" values is a list with one dict for every infrastructure type
    # Each of these dicts have their identifier as a key (Example key: '[highway = trunk]') and the value of this key is
    # a list with a dict for every street that corresponds to this type
    # This dict has the osm-id under the key "id"

    osm_ids_per_infrastructure = {}

    north, east, south, west = area.find_borders()

    # Uncomment the line below to query the whole relevant area (program takes ages to complete)
    # requested_data = query_area(north, east, south, west)

    requested_data = test()

    for infrastructure_dict in requested_data["features"]:
        for infra_type, streets in infrastructure_dict.items():
            osm_ids = []
            for street_data in streets:
                osm_ids.append(street_data["id"])
                osm_ids_per_infrastructure[infra_type] = osm_ids

    return osm_ids_per_infrastructure


if __name__ == '__main__':
    conn, cur = db.connect()

    osm_ids_per_infrastructure = test_api()

    for infra_type, osm_ids in osm_ids_per_infrastructure.items():

        infra_types.append(infra_type)

        infra_dict[infra_type] = {}
        infra_dict[infra_type]["avoided_count"] = 0
        infra_dict[infra_type]["chosen_count"] = 0
        infra_dict[infra_type]["normal_incident_count"] = 0
        infra_dict[infra_type]["scary_incident_count"] = 0
        infra_dict[infra_type]["leg_count"] = 0
        infra_dict[infra_type]["length"] = 0
        infra_dict[infra_type]["count"] = 0

        print(f"WORKING ON ALL OSM_IDS WITH INFRASTRUCTURE TYPE {infra_type}. THERE ARE {len(osm_ids)} IDS FOR THIS "
              f"INFRASTRUCTURE TYPE")

        for osm_id in osm_ids:
            execute_queries(cur, osm_id, infra_type)

        print(infra_dict[infra_type])

    df = pd.DataFrame.from_dict(infra_dict, orient="index")
    df.to_csv("../../test.csv")

    db.close_connection(conn, cur)
