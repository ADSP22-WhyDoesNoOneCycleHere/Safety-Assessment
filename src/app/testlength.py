from requests import request
import requests as req
import osmapi as osm

api = osm.OsmApi()
API_KEY = "3e9d076d-594f-4be2-96da-71368a80ac24"
BASE_URL = "https://graphhopper.com/api/1/route"

# get start and endnode from a way by its osm way id
def get_nodes(way_id):
    nodes = api.WayGet(way_id)["nd"]
    
    return nodes[0], nodes[1]

# get lat and lon coordinates from osm node is
def get_node_coordinates(node): 
    node_dict = api.NodeGet(node)
    lat = node_dict["lat"]
    lon = node_dict["lon"]
    #print(f'lat: {node_dict["lat"]}')
    #print(f'lon: {node_dict["lon"]}')
    
    return lat, lon

# get length between two coordinates
# graphhopper
def get_length_between_coordinates(from_lat, from_lon, to_lat, to_lon): 
    response = req.get(f'{BASE_URL}?key={API_KEY}&point={from_lat},{from_lon}&point={to_lat},{to_lon}')
    length = response.json()["paths"][0]["distance"]

    return length

# input: osmId from database
# return: length of way in meters
def get_length(osm_id):
    #print(f'try to get length from id: {osm_id}')
    node_from, node_to = get_nodes(osm_id)
    node_from_lat, node_from_lon =  get_node_coordinates(node_from)
    node_to_lat, node_to_lon =  get_node_coordinates(node_to)
    way_length = get_length_between_coordinates(node_from_lat, node_from_lon, node_to_lat, node_to_lon)

    return way_length

""" # for testing
if __name__ == "__main__":
    
    ways = [4609242, 72183527, 335462896, 335462901]

    #node_1_lat, node_1_lon =  get_node_coordinates(27537748)
    #node_2_lat, node_2_lon =  get_node_coordinates(27537747)
    #get_length_between_coordinates(node_1_lat, node_1_lon, node_2_lat, node_2_lon)

    #print(get_nodes(4609242))

    for way in ways:
        node_from, node_to = get_nodes(way)
        node_from_lat, node_from_lon =  get_node_coordinates(node_from)
        node_to_lat, node_to_lon =  get_node_coordinates(node_to)
        way_length = get_length_between_coordinates(node_from_lat, node_from_lon, node_to_lat, node_to_lon)
        
        print(f'way with id: {way}')
        print(f'with nodes: {node_from} -> {node_to}')
        print(f'and length {way_length}m') """
