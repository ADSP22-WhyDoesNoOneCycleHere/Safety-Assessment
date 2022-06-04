#!/usr/bin/python
import psycopg2
from fastapi import FastAPI
import requests as req


def connect():
    """ Connect to the PostgreSQL database server """
    # from some website
    conn = None
    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="localhost",
            database="simra",
            user="simra",
            password="simra12345simra")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        return conn, cur

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def close_connection(conn, cur):
    # from some website. Originally in connect() function
    try:
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def execute_queries(cur, osm_id):
    query = f'Select "avoidedCount" from "SimRaAPI_osmwayslegs" where "osmId"={osm_id}'
    cur.execute(query)
    print(f"for the legs with the OSM id {osm_id} we got the following avoided counts")
    print(cur.fetchall())


def testApi():
    # Structure of the json we get atm:
    # Json dict contains one key "features"
    # "Features" values is a list with one dict for every infrastructure type
    # Each of these dicts have their identifier as a key (Example key: '[highway = trunk]') and the value of this key is
    # a list with a dict for every street that corresponds to this type
    # This dict has the osm-id under the key "id"

    request = req.get("http://127.0.0.1:8000")
    requested_data = request.json()["features"]

    osm_ids_per_infrastructure = {}
    for infrastructure_dict in requested_data:

        for infra_type, streets in infrastructure_dict.items():
            osm_ids = []
            for street_data in streets:
                osm_ids.append(street_data["id"])
            osm_ids_per_infrastructure[infra_type] = osm_ids

    return osm_ids_per_infrastructure


if __name__ == '__main__':
    conn, cur = connect()

    osm_ids_per_infrastructure = testApi()

    for infra, osm_ids in osm_ids_per_infrastructure.items():
        print(f"WORKING ON ALL OSM_IDS WITH INFRASTRUCTURE TYPE {infra}. THERE ARE {len(osm_ids)} IDS FOR THIS "
              f"INFRASTRUCTURE TYPE")
        for osm_id in osm_ids:
            execute_queries(cur, osm_id)

    close_connection(conn, cur)

