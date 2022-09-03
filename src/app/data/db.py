import os
from dotenv import load_dotenv
import psycopg2

# Adapted from https://www.postgresqltutorial.com/postgresql-python/connect/


def connect():
    """ Connect to the PostgreSQL database server """

    load_dotenv()

    conn = None
    try:
        print("Connecting to db...")
        # connect to the PostgreSQL server
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database="simra",
            user="simra",
            password="simra12345simra")

        # create a cursor
        cur = conn.cursor()

        return conn, cur

    except (Exception, psycopg2.DatabaseError) as error:
        print("Did you specify the correct adress in the .env file?\n", error)


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
