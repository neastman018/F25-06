import json_to_graph as jtg
from math import sqrt

def euclidean_distance(coord1, coord2):
    return sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def json_to_multi(json_data):
    graph = jtg.Graph()
    with open(json_data,'r') as file:
        data = jtg.json.load(file)

    node_coords_map = {}

    for zone in data["zones"]:
        for node in zone["nodes"]:
            node_id = node["id"]
            node_coords = (node["pose"][0], node["pose"][1])
            graph.add_vertex(node_id, node_coords)
            node_coords_map[node_id] = node_coords

    for zone in data["zones"]:
        for node in zone["nodes"]:
            node_id = node["id"]
            for connection in node["connections"]:
                connect_to = connection["connects_to"]
                cost = euclidean_distance(node_coords_map[node_id], node_coords_map[connect_to])
                graph.add_edge(node_id, connect_to, cost)

    # Calculate the maximum distance as the norm of all distances
    distances = []
    for node_id, coords1 in node_coords_map.items():
        for other_node_id, coords2 in node_coords_map.items():
            if node_id != other_node_id:
                distance = euclidean_distance(coords1, coords2)
                distances.append(distance)
    
    max_distance = sum(distances) / len(distances) if distances else 0

    for node_id, coords1 in node_coords_map.items():
        for other_node_id, coords2 in node_coords_map.items():
            if node_id != other_node_id:
                distance = euclidean_distance(coords1, coords2)
                if distance <= max_distance:
                    graph.add_edge(node_id, other_node_id, distance)
    
    return graph

if __name__ == "__main__":
    graph = json_to_multi('algorithms/test_json/test3.json')

    # Test the graph
    print(graph.get_neighbors("node_001"))
    print(graph.get_coords("node_001"))
    print(graph.get_neighbors("node_002"))
    print(graph.get_coords("node_002"))
    print(graph.get_neighbors("node_003"))
    print(graph.get_coords("node_003"))