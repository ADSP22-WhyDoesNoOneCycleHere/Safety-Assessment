#!/usr/bin/python
import itertools
import time
from threading import Thread

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

# function to fetch data from database for a specific part of the infrastructure types
def database_query(infra_types_part, cur, conn) :
    #print("--------------------------------")
    #print("data processed by " + conn.dsn + ":")
    for infra_type, osm_ids in infra_types_part.items():

        #print(infra_type, osm_ids)

        for osm_id in osm_ids:
            execute_queries(cur, conn, osm_id, infra_type)
    #print("--------------------------------")

if __name__ == '__main__':
    # connect databases services
    conn1, cur1 = db.connect(DB_PORT_1)
    conn2, cur2 = db.connect(DB_PORT_2)
    conn3, cur3 = db.connect(DB_PORT_3)

    # setup new table for each database service
    scores.initialize_score_table(cur1, conn1)
    scores.initialize_score_table(cur2, conn2)
    scores.initialize_score_table(cur3, conn3)

    print("Create infrastructure types.")
    infrastructure_osm_ids = osm_ids_per_infrastructure()
    print("Created infrastructure types successfully.")

    start = time.time()

    infra_types = infrastructure_osm_ids.items()
    #print("--------------------------------")
    #print("All infrastructure types:")
    #print(infra_types.mapping.keys())
    #print("--------------------------------")
    part_size = int(len(infra_types) / NUMBER_OF_DB_SERVICES)

    # create threads
    threads = []

    # append thread that queries the data for the first part of infrastructure types
    threads.append(Thread(target=database_query(dict(itertools.islice(infra_types, 0, part_size)), cur1, conn1)))
    # append Thread that queries the data for the second part of infrastructure types
    threads.append(Thread(target=database_query(dict(itertools.islice(infra_types, part_size, 2 * part_size)), cur2, conn2)))
    # append Thread that queries the data for the third part of infrastructure types
    threads.append(Thread(target=database_query(dict(itertools.islice(infra_types, 2 * part_size, len(infra_types))), cur3, conn3)))

    print("Add infrastructure type to legs and store computed scores inside the database")
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time.time()

    print(f'Time taken python: {end - start}')

    # disconnect from database services
    db.close_connection(conn1, cur1, DB_PORT_1)
    db.close_connection(conn2, cur2, DB_PORT_2)
    db.close_connection(conn3, cur3, DB_PORT_3)
