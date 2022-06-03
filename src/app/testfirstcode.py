#!/usr/bin/python
import psycopg2
from fastapi import FastAPI
import requests as req

# from config import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        # params = config()

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
    print(f"for the OSM id {osm_id} we got the following avoided counts")
    print(cur.fetchall())


def testApi():
    test = req.get("http://127.0.0.1:8000")
    intermediary = test.json()["elements"]

    osm_ids = []
    for item in intermediary:
        osm_ids.append(item["id"])

    return osm_ids


if __name__ == '__main__':
    osm_ids = testApi()

    conn, cur = connect()

    for osm_id in osm_ids:
        print(f"Working on osm_id {osm_id}: ############################")
        execute_queries(cur, osm_id)

    close_connection(conn, cur)

