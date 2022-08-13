import time
import random
import data.db

if __name__ == '__main__':
    conn, cur = data.db.connect()

    query = f'SELECT * INTO public."SimRaAPI_osmwayslegsused" FROM public."SimRaAPI_osmwayslegs" WHERE count > 0 or "avoidedCount" > 0;'

    cur.execute(query)
    conn.commit()

    #print(len(cur.fetchall()))
