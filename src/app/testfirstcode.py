#!/usr/bin/python
from pprint import pprint

import requests as req
import db
import area


def execute_queries(cur, osm_id):
    query = f'Select "avoidedCount" from "SimRaAPI_osmwayslegs" where "osmId"={osm_id}'
    cur.execute(query)
    print(f"for the legs with the OSM id {osm_id} we got the following avoided counts")
    print(cur.fetchall())


def query_area(north, east, south, west):
    body = {
        "ne": str(north) + "," + str(east),
        "sw": str(north-0.1) + "," + str(east-0.1)
    }
    response = req.post("http://127.0.0.1:8000/area", json=body)

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

    requested_data = query_area(north, east, south, west)

    print(requested_data)

    for infrastructure_dict in requested_data["features"]:
        for infra_type, streets in infrastructure_dict.items():
            print(infra_type)
            osm_ids = []
            for street_data in streets:
                osm_ids.append(street_data["id"])
                osm_ids_per_infrastructure[infra_type] = osm_ids

    return osm_ids_per_infrastructure


if __name__ == '__main__':
    conn, cur = db.connect()

    osm_ids_per_infrastructure = test_api()

    print(osm_ids_per_infrastructure)

    for infra, osm_ids in osm_ids_per_infrastructure.items():
        print(f"WORKING ON ALL OSM_IDS WITH INFRASTRUCTURE TYPE {infra}. THERE ARE {len(osm_ids)} IDS FOR THIS "
              f"INFRASTRUCTURE TYPE")
        for osm_id in osm_ids:
            execute_queries(cur, osm_id)

    db.close_connection(conn, cur)
