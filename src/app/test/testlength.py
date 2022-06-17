import requests as req
import overpass
import geopy.distance

API_KEY = "3e9d076d-594f-4be2-96da-71368a80ac24"
BASE_URL = "https://graphhopper.com/api/1/route"


# get start and endnode from a way by its osm way id
def get_nodes(way_id):
    api_overpass = overpass.API(endpoint="http://vm3.mcc.tu-berlin.de:8088/api/interpreter", timeout=90)
    nodes = api_overpass.get(f"way({way_id});out body;>", verbosity='skel', responseformat='json')["elements"]

    print(nodes[1:])
    
    return nodes[1:]


# get length between two coordinates
# graphhopper
def get_length_between_coordinates(from_lat, from_lon, to_lat, to_lon): 
    response = req.get(f'{BASE_URL}?key={API_KEY}&point={from_lat},{from_lon}&point={to_lat},{to_lon}')
    length = response.json()["paths"][0]["distance"]

    return length


def get_length(osm_id):
    way_length = 0
    nodes = get_nodes(osm_id)
    for i in range(len(nodes)-1):
        c1 = (nodes[i]["lat"], nodes[i]["lon"])
        c2 = (nodes[i+1]["lat"], nodes[i+1]["lon"])
        way_length += geopy.distance.distance(c1, c2).km

    return way_length


if __name__ == "__main__":
    print(get_length(25184342))
