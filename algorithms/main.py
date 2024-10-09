# file for running algorithms

import a_star_w_reroute as a_star
import d_star_w_reroute as d_star
import json_to_graph as jtg
import networkx as nx
import matplotlib.pyplot as plt
import json_to_multi as jtm
# Driver Code

def convert_to_nx_graph(graph):
    nx_graph = nx.Graph()
    for vertex in graph.vertices:
        nx_graph.add_node(vertex, pos=graph.vert_coord[vertex])
        for neighbor in graph.get_neighbors(vertex):
            nx_graph.add_edge(vertex, neighbor)
    return nx_graph

def main():
    # Define the graph from the interperter
    #j_graph = jtg.json_to_graph('algorithms/test_json/test4.json')
    j_graph = jtm.json_to_multi('algorithms/test_json/test4.json')

    # Define the source and destination
    agents = [("node_1a", "node_1005")]

    # Run the search algorithm requested by the user
    d_star.d_star_search(j_graph, agents[0][0], agents[0][1])
    a_star.run_a_star(j_graph, agents)

    # Convert the graph to a networkx graph and plot it
    nx_graph = convert_to_nx_graph(j_graph)
    nx.draw(nx_graph, nx.get_node_attributes(nx_graph, 'pos'), with_labels=True, node_size=300, node_color='skyblue', font_size=5)
    plt.show()

if __name__ == "__main__":
    main()