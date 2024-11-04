import json
# import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.vertices = {}
        self.vert_coord = {}
        self.vert_type = {}

    def add_vertex(self, vertex, coords, vtype):
        self.vertices[vertex] = {}
        self.vert_coord[vertex] = coords
        self.vert_type[vertex] = vtype

    def add_edge(self, start, end, cost):
        self.vertices[start][end] = cost

    def get_neighbors(self, vertex):
        return self.vertices[vertex]
    
    def get_coords(self, vertex):
        return self.vert_coord[vertex]
    
    def get_vertex_type(self, vertex):
        return self.vert_type[vertex]
    
    def get_vertices_count(self):
        return len(self.vertices)
    
    def get_edge_count(self, vertex):
        if vertex in self.vertices:
            return len(self.vertices[vertex])
        else:
            return 0
        
    def get_vertices_count(self):
        return len(self.vertices)

def json_to_graph(json_data):
    graph = Graph()
    with open(json_data,'r') as file:
        data = json.load(file)

    node_coords_map = {}

    for zone in data["zones"]:
        for node in zone["nodes"]:
            node_id = node["id"]
            node_coords = (node["pose"][0], node["pose"][1])
            node_type = "init"
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

    return graph

if __name__ == "__main__":
    graph = json_to_graph('algorithms/test_json/test1.json')

    # Test the graph
    print(graph.get_neighbors("node_001"))
    print(graph.get_coords("node_001"))
    print(graph.get_neighbors("node_002"))
    print(graph.get_coords("node_002"))
    print(graph.get_neighbors("node_003"))
    print(graph.get_coords("node_003"))