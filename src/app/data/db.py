import psycopg2

# Adapted from https://www.postgresqltutorial.com/postgresql-python/connect/


def connect():
    """ Connect to the PostgreSQL database server """
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