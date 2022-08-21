#!/usr/bin/python
import time
import json

from src.app.data import db
from src.app.calculation import scores
from src.app.data.highway import Highway

leg = {}  # Dict to which the different counts are saved


def execute_queries(cur, conn, osm_id, infra_type):
    """
    Imports relevant counts from the database and stores them in a dict for later calculation
    :param cur:
    :param conn: connection to postgresql db
    :param osm_id: the openstreetmap-id of the current street-segment
    :param infra_type: the infrastructure-type of the current street-segment
    :return:
    """
    query = f'Select "id", "avoidedCount", "chosenCount", "normalIncidentCount", ' \
            f'"scaryIncidentCount", "count", (ST_Length(geom::geography) / 1000) as length' \
            f' from "SimRaAPI_osmwayslegsused" where "osmId"={osm_id};'

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


def init_smaller_table(cur, conn):
    """
    Creates table SimRaAPI_osmwayslegsused if it does not already exist. The table is a sub-table of SimRaAPI_osmwayslegs
    where count or avoidedCount is greater than 0
    :param cur:
    :param conn: Connection to postgresql database
    :return:
    """
    query = "select exists (select from information_schema.tables where  table_schema = 'public' and " \
            "table_name = 'SimRaAPI_osmwayslegsused');"

    cur.execute(query)

    if not cur.fetchone()[0]:
        # The table does not exist yet, so we create it
        query = f'SELECT * ' \
                f'INTO public."SimRaAPI_osmwayslegsused" ' \
                f'FROM public."SimRaAPI_osmwayslegs" ' \
                f'WHERE count > 0 or "avoidedCount" > 0;'

        cur.execute(query)
        conn.commit()


def query_area(country, city):
    """
    Queries the specified city for all defined infrastructure-types
    :param country:
    :param city:
    :return:
    """
    return Highway.query_area(country, city)


def test():
    """
    Use this function when testing. Queries all of Berlin.
    :return:
    """
    return Highway.query_area()


def osm_ids_per_infrastructure(country, city):
    """
    Calls query_area and saves all openstreetmap-ids to each infrastructure-type they belong to
    :param country:
    :param city:
    :return:
    """
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
    
    init_smaller_table(cur, conn)
    
    scores.add_columns(cur, conn)
    scores.initialize_infra_table(cur, conn)

    # for docker use: ./app/areas.json
    with open("areas.json", "r", encoding='utf-8') as f:
        areas = json.load(f)

        # Loops through all areas defined in areas.json
        for country_city in areas["areas"]:
            scores.add_columns(cur, conn)
            scores.initialize_infra_table(cur, conn)

            infrastructure_osm_ids = osm_ids_per_infrastructure(country_city[0], country_city[1])

            start = time.time()

            for infra_type, osm_ids in infrastructure_osm_ids.items():
                print(f"++ Working on {infra_type} with {len(osm_ids)} osm_ids")
                print(f"-> Calculating leg scores for infra type: {infra_type}")
                for osm_id in osm_ids:
                    execute_queries(cur, conn, osm_id, infra_type)
                print(f"-> Calculating averaged scores for infra type: {infra_type}")
                scores.calculate_scores_infra_types(infra_type, cur, conn)

            scores.save_infra_type_scores(country_city[1])

            end = time.time()

            print(f'Time taken python: {end - start}')

    db.close_connection(conn, cur)
