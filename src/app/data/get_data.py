#!/usr/bin/python
import time
import json
from pprint import pprint

from src.app.data import db
from src.app.calculation import scores
from src.app.data.highway import Highway

leg = {}  # Dict to which the different counts are saved


def execute_queries(cur, conn, osm_id, infra_type):
    query = f'Select "id", "avoidedCount", "chosenCount", "normalIncidentCount", ' \
            f'"scaryIncidentCount", "count", (ST_Length(geom::geography) / 1000) as length' \
            f' from "SimRaAPI_osmwayslegs" where "osmId"={osm_id};'

    cur.execute(query)

    for count in cur.fetchall():
        leg["infra_type"] = infra_type
        leg["id"] = count[0]
        leg["a_count"] = count[1]
        leg["c_count"] = count[2]
        leg["normal_incident_count"] = count[3]
        leg["scary_incident_count"] = count[4]
        leg["count"] = count[5]
        leg["length"] = count[6]

        scores.calculate_scores_legs(leg, cur, conn)


def query_area(country, city):
    return Highway.query_area(country, city)


# Use this function when testing new features; query_area() queries ALL of Berlin
def test():
    return Highway.query_area()


def osm_ids_per_infrastructure(country, city):
    infrastructure_osm_ids = {}

    # Uncomment the lines below to query the whole relevant area (program takes ages to complete)‚
    # requested_data = query_area(country, city)

    requested_data = test()

    for infrastructure_dict in requested_data["features"]:
        for infra_type, streets in infrastructure_dict.items():
            osm_ids = []
            for street_data in streets:
                osm_ids.append(street_data["id"])
                infrastructure_osm_ids[infra_type] = osm_ids

    return infrastructure_osm_ids


def main():
    conn, cur = db.connect()
    scores.add_columns(cur, conn)
    scores.initialize_infra_table(cur, conn)

    with open("areas.json") as f: # for docker: ./app/areas.json
        areas = json.load(f)
        for area in areas["areas"]:

            infrastructure_osm_ids = osm_ids_per_infrastructure(area[0], area[1])

            start = time.time()

            for infra_type, osm_ids in infrastructure_osm_ids.items():
                print(f"++ Working on {infra_type} with {len(osm_ids)} osm_ids")
                print(f"-> Calculating leg scores for infra type: {infra_type}")
                for osm_id in osm_ids:
                    execute_queries(cur, conn, osm_id, infra_type)
                print(f"-> Calculating averaged scores for infra type: {infra_type}")
                scores.calculate_scores_infra_types(infra_type, cur, conn)

            end = time.time()

            print(f'Time taken python: {end - start}')

    db.close_connection(conn, cur)
