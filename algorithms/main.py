# file for running algorithms

import a_star_w_reroute as a_star
import d_star_w_reroute as d_star
import a_star_multi as a_star_multi
import json_to_graph as jtg
import networkx as nx
import matplotlib.pyplot as plt
import json_to_multi as jtm
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import visualization as vis
import json
import time


def test_validation(test_plan="Testing_1", num_agents=10, num_packages=2, algorithm="A*", floor_plan="Complex"):

    # Define the graph from the interperter
    simple_graph = jtg.json_to_graph('algorithms/test_json/test_simple.json')
    #j_graph = jtm.json_to_graph('algorithms/test_json/test3.json')
    multi_graph = jtm.json_to_multi('algorithms/test_json/test_complex.json')

    # Define the graph from the json file
    graph = simple_graph if floor_plan == "Simple" else multi_graph

    # Define the source and destination nodes
    graph_nodes = {}
    if graph == simple_graph:
        for node in graph.vert_type:
            if graph.vert_type[node] == 'input':
                graph_nodes[node] = []
            elif graph.vert_type[node] == 'bin':
                for input in graph_nodes:
                    if node.startswith(input):
                        graph_nodes[input].append(node)
                        break
    else:
        list_of_bins = []
        for node, type in graph.vert_type.items():
            if type == 'input':
                graph_nodes[node] = []
            elif type == 'bin':
                list_of_bins.append(node)
        for node in graph_nodes:
            graph_nodes[node] = list_of_bins

            

    # randomly selected bin nodes for 10 agents to go to from the input nodes
    agents = {}
    for i in range(1, num_agents + 1):
        agents[i] = []
        src = random.choice(list(graph_nodes.keys()))
        for _ in range(1, num_packages + 1):
            dest = graph_nodes[src][random.randint(0, len(graph_nodes[src]) - 1)]
            agents[i].append((src, dest)) # from input to bin
            agents[i].append((dest, src)) # from bin to input

            # print(f"Agent {i}: {src} -> {dest}")

    # Genaric: agents = {1:[("node_1", "node_1005"), ("node_1005", "node_1")], 2:[("node_2", "node_2009"), ("node_2009", "node_2")], 3:[("node_3", "node_3015"), ("node_3015", "node_3")], 4:[("node_4","node_4011"), ("node_4011", "node_4")]}
    # agents[1] = [("qwer", "node_x001"), ("node_x001", "qwer"), ("qwer", "node_x002"), ("node_x002", "qwer")]

    # Run the search algorithm requested by the user
    planner_paths = a_star.run_a_star(graph, agents) if algorithm == "A*" else d_star.run_d_star(graph, agents)


    # Visualize the results of the search algorithm
    vis_obj = vis.Visualization()
    vis_obj.animate_paths(planner_paths, graph)
    #vis_obj.show_path(planner_paths, graph)
    metrics = None
    metrics = vis_obj.update_metrics(planner_paths, graph)
    
    # exract the metrics from the visualization object
    max_dist = max(metrics['agent_distance'].values())
    speed = 1 # m/s
    delay = metrics['total_estops'] + metrics['total_dropoffs'] # seconds
    metrics['time'] = (max_dist / speed) + delay
    # print(f"Time: {metrics['time']} seconds")
    # print(f"Agents: {len(agents)}")
    # print(f"Total distance: {sum(metrics['agent_distance'].values())}")
    print(f"Total dropoffs: {metrics['total_dropoffs']}")

    full_metrics = {
        "Simulation Name": "2_Test Simulation", 
        "Simulation Conducted": test_plan, 
        "Algorithm": algorithm,
        "Floor Plan": floor_plan, 
        "Number of Robots": num_agents, 
        "Number of Nodes": graph.get_vertices_count(), 
        "simulation results": {
            "Time": metrics['time'], 
            "Total Distance": sum(metrics['agent_distance'].values()), 
            "Total Dropoffs": metrics['total_dropoffs'],
            "Total Planned Drops": num_agents * (num_packages + 1)
        }
    }

    # write a json file with the metrics
    json_metrics = json.dumps(full_metrics, indent=4)
    
    if full_metrics['simulation results']['Total Dropoffs'] == full_metrics['simulation results']['Total Planned Drops']:
        with open("c" + "metrics_D_" + str(time.time()) + ".json", 'w') as outfile:
            outfile.write(json_metrics)
        print("Simulation Passed")
    else:
        with open("metrics_" + str(time.time()) + ".json", 'w') as outfile:
            outfile.write(json_metrics)
   


if __name__ == "__main__":
    test_validation(algorithm="D*")