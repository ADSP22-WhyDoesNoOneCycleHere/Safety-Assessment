import overpass
import requests as req
import geopy.distance


HOPPER_URL = "http://vm3.mcc.tu-berlin.de:8980/route"


# get start and endnode from a way by its osm way id
def get_nodes(way_id):
    api_overpass = overpass.API(endpoint="http://vm3.mcc.tu-berlin.de:8088/api/interpreter", timeout=90)
    nodes = api_overpass.get(f"way({way_id});out body;>", verbosity='skel', responseformat='json')["elements"]

    return nodes[1:]


def get_graphhopper(from_lat, from_lon, to_lat, to_lon):
    r = req.get(f'{HOPPER_URL}?point={from_lat},{from_lon}&point={to_lat},{to_lon}')
    return r.json()["paths"][0]["distance"]


def get_length(osm_id, graphhopper):
    """
    Computes the length of a given osm way
    :param osm_id: the way id
    :param graphhopper: True if graphhopper is to be used to compute distance, false if geopy should be used
    :return: the length of the way
    """
    way_length = 0
    nodes = get_nodes(osm_id)
    for i in range(len(nodes)-1):
        c1 = (nodes[i]["lat"], nodes[i]["lon"])
        c2 = (nodes[i+1]["lat"], nodes[i+1]["lon"])

        if graphhopper:
            way_length += get_graphhopper(c1[0], c1[1], c2[0], c2[1])

        else:
            way_length += geopy.distance.distance(c1, c2).m

    return way_length


# for testing
if __name__ == "__main__":
    print(get_length(25184342, True))
    print(get_length(25184342, False))
