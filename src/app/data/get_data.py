#!/usr/bin/python
import itertools
import time
from multiprocessing import Process

from src.app.data import db
from src.app.calculation import area
from src.app.calculation import scores
from src.app.data.highway import Highway

leg = {}  # Dict to which the different counts are saved

DB_PORT_1 = 5432
DB_PORT_2 = 5433
DB_PORT_3 = 5434
NUMBER_OF_DB_SERVICES = 3

def execute_queries(cur, conn, osm_id, infra_type):
    query = f'Select "id", "avoidedCount", "chosenCount", "normalIncidentCount", ' \
            f'"scaryIncidentCount", "count", ST_Length(geom::geography) as length' \
            f' from "SimRaAPI_osmwayslegs" where "osmId"={osm_id} and count > 0;'

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

        scores.calculate_scores_ways(leg, cur, conn)


def query_area(north, east, south, west):
    return Highway.query_area(str(south) + "," + str(west), str(north) + "," + str(east))


# Use this function when testing new features; query_area() queries ALL of Berlin
def test():
    return Highway.query_area()


def osm_ids_per_infrastructure():
    infrastructure_osm_ids = {}

    # Uncomment the lines below to query the whole relevant area (program takes ages to complete)
    # north, east, south, west = area.find_borders()
    # requested_data = query_area(north, east, south, west)

    requested_data = test()

    for infrastructure_dict in requested_data["features"]:
        for infra_type, streets in infrastructure_dict.items():
            osm_ids = []
            for street_data in streets:
                osm_ids.append(street_data["id"])
                infrastructure_osm_ids[infra_type] = osm_ids

    return infrastructure_osm_ids

def database_query(infra_types_part, port):
    # connect
    conn, cur = db.connect(port)
    # create table for scores
    scores.initialize_score_table(cur, conn)

    # query data and compute stores
    for infra_type, osm_ids in infra_types_part.items():
        for osm_id in osm_ids:
            execute_queries(cur, conn, osm_id, infra_type)

    # disconnect from database services
    db.close_connection(conn, cur, port)


if __name__ == '__main__':
    start = time.time()

    print("Create infrastructure types.")
    infra_types = osm_ids_per_infrastructure().items()
    print("Created infrastructure types successfully.")


    part_size = int(len(infra_types) / NUMBER_OF_DB_SERVICES)

    # array for processes
    processes = []

    # build processes, that connect to db, query and store the specific data and close connection
    processes.append(Process(target=database_query, args=(dict(itertools.islice(infra_types, 0, part_size)), DB_PORT_1)))
    processes.append(Process(target=database_query, args=(dict(itertools.islice(infra_types, part_size, 2 * part_size)), DB_PORT_2)))
    processes.append(Process(target=database_query, args=(dict(itertools.islice(infra_types, 2 * part_size, len(infra_types))), DB_PORT_3)))

    print("Add infrastructure type to legs and store computed scores inside the database")
    for process in processes:
        process.start()

    for process in processes:
        process.join()

    end = time.time()

    print(f'Time taken python: {end - start}')