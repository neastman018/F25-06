# file for running algorithms

import a_star_w_reroute as a_star
import d_star_w_reroute as d_star
import json_to_graph as jtg
import networkx as nx
import matplotlib.pyplot as plt
import json_to_multi as jtm
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import visualization as vis


def main():
    # TODO: implement time and space complexity analysis and find metrics for the algorithms

    # Define the graph from the interperter
    single_graph = jtg.json_to_graph('algorithms/test_json/test4.json')
    #j_graph = jtm.json_to_graph('algorithms/test_json/test3.json')
    multi_graph = jtm.json_to_multi('algorithms/test_json/test4.json')

    # Define the graph from the json file
    graph = multi_graph

    # Define the source and destination nodes
    graph_nodes = {}
    for node in graph.vert_type:
        if graph.vert_type[node] == 'input':
            graph_nodes[node] = []
        elif graph.vert_type[node] == 'bin':
            for input in graph_nodes:
                if node.startswith(input):
                    graph_nodes[input].append(node)
                    break

            

    # randomly selected bin nodes for 10 agents to go to from the input nodes
    agents = {}
    for i in range(1, 11):
        agents[i] = []
        src = random.choice(list(graph_nodes.keys()))
        for _ in range(1, 3):
            dest = graph_nodes[src][random.randint(0, len(graph_nodes[src]) - 1)]
            agents[i].append((src, dest)) # from input to bin
            agents[i].append((dest, src)) # from bin to input

            # print(f"Agent {i}: {src} -> {dest}")

    # Genaric: agents = {1:[("node_1", "node_1005"), ("node_1005", "node_1")], 2:[("node_2", "node_2009"), ("node_2009", "node_2")], 3:[("node_3", "node_3015"), ("node_3015", "node_3")], 4:[("node_4","node_4011"), ("node_4011", "node_4")]}

    # Run the search algorithm requested by the user
    d_star.d_star_search(graph, src, dest)
    a_star_paths = a_star.run_a_star(graph, agents)


    # Visualize the results of the search algorithm
    vis_obj = vis.Visualization()
    vis_obj.draw_graph(graph)
    vis_obj.animate_paths(a_star_paths, graph)
   


if __name__ == "__main__":
    main()