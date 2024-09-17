import json
# import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        self.vertices[vertex] = {}

    def add_edge(self, start, end, cost):
        self.vertices[start][end] = cost

    def get_neighbors(self, vertex):
        return self.vertices[vertex]
def json_to_graph(json_data):
    graph = Graph()
    data = json.loads(json_data)

    for zone in data["zones"]:
        for node in zone["nodes"]:
            node_id = node[id]
            graph.add_vertex(node_id)
    
    for zone in data["zones"]:
        for node in zone["nodes"]:
            node_id = node["id"]
            for connection in node["connections"]:
                connect_to = connection["connects_to"]
                cost = 1
                graph.add_edge(node_id, connect_to, cost)

    return graph