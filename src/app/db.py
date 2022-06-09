import psycopg2


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