import db


def find_borders():
    conn, cur = db.connect()

    cur.execute('SELECT ST_AsText(geom) FROM "SimRaAPI_osmwayslegs"')

    entries = cur.fetchall()

    north = 0.0
    south = 100.0
    east = 0.0
    west = 100.0

    for entry in entries:
        for ne in entry[0].split(",")[10:-1]:
            geom_list = [ne.split(" ")[1], ne.split(" ")[0]]

            if float(geom_list[0]) > north:
                north = float(geom_list[0])

            if float(geom_list[1]) > east:
                east = float(geom_list[1])

            if float(geom_list[0]) < south:
                south = float(geom_list[0])

            if float(geom_list[1]) < west:
                west = float(geom_list[1])

    db.close_connection(conn, cur)

    print(f"North: {north}, East: {east}, South: {south}, West: {west}")

    return north, east, south, west


if __name__ == '__main__':
    find_borders()
