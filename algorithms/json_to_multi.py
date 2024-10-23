import json_to_graph as jtg
from math import sqrt
import visualization as vis

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
            if(node["type"] != "target"):
                node_type = "init"
            elif(node["type"] == "target"):
                if "target_reservation_cost_linear" in node:
                    node_type = "input"
                else:
                    node_type = "bin"
            graph.add_vertex(node_id, node_coords, node_type)
            node_coords_map[node_id] = node_coords

    for zone in data["zones"]:
        for node in zone["nodes"]:
            node_id = node["id"]
            for connection in node["connections"]:
                connect_to = connection["connects_to"]
                if '/' in connect_to:
                    xx,zone_id, connect_to = connect_to.split('/')
                    connect_to_coords = None
                    for z in data["zones"]:
                        if z["id"] == zone_id:
                            for n in z["nodes"]:
                                if n["id"] == connect_to:
                                    connect_to_coords = (n["pose"][0], n["pose"][1])
                                    break
                            break
                    if connect_to_coords:
                        cost = 1
                        graph.add_edge(node_id, connect_to, cost)
                else:
                    cost = 1
                    graph.add_edge(node_id, connect_to, cost)

    # Calculate the maximum distance as the norm of all distances for connected nodes
    avg_distance = 0 
    counter = 0
    for zone in data["zones"]:
        for node in zone["nodes"]:
            node_id = node["id"]
            for connection in node["connections"]:
                connect_to = connection["connects_to"]
                if '/' in connect_to:
                    _, zone_id, connect_to = connect_to.split('/')
                distance = euclidean_distance(node_coords_map[node_id], node_coords_map[connect_to])
                counter += 1
                avg_distance = distance
    avg_distance /= counter
    avg_distance = 2.75
    # Add connections to nodes if other nodes are within the max distance
    for node_id1, coords1 in node_coords_map.items():
        for node_id2, coords2 in node_coords_map.items():
            if node_id1 != node_id2:
                distance = euclidean_distance(coords1, coords2)
                if distance <= avg_distance:
                    graph.add_edge(node_id1, node_id2, distance)
    #Calculate the maximum distance as the norm of all distances
    # max_distance = 0
    # for node_id1, coords1 in node_coords_map.items():
    #     for node_id2, coords2 in node_coords_map.items():
    #         if node_id1 != node_id2:
    #             distance = euclidean_distance(coords1, coords2)
    #             if distance > max_distance:
    #                 max_distance = distance
    #             if distance <= 2.5:  # Replace `arbitrary_distance` with your desired distance threshold
    #                 graph.add_edge(node_id1, node_id2, distance)
    return graph

if __name__ == "__main__":
    graph = json_to_multi('algorithms/test_json/test_complex.json')

    # Test the graph
    print(graph.get_neighbors("node_1001"))
    print(graph.get_vertex_type("node_1001"))
    print(graph.get_neighbors("node_1002"))
    print(graph.get_vertex_type("node_2"))
    vis_obj = vis.Visualization()
    vis_obj.draw_graph(graph)