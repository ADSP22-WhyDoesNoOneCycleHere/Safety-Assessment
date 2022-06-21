import psycopg2


def connect(port):
    """ Connect to the PostgreSQL database server """
    # from some website
    conn = None
    try:

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="localhost",
            port=str(port),
            database="simra",
            user="simra",
            password="simra12345simra")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        #print('PostgreSQL database version:')
        #cur.execute('SELECT version()')
        #db_version = cur.fetchone()
        #print(type(db_version))

        # display the PostgreSQL database server version and port
        print("Connected to database on port " + str(port))

        return conn, cur

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def close_connection(conn, cur, port):
    # from some website. Originally in connect() function
    try:
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Connection closed to database on port ' + str(port))