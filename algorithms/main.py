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
    planner_paths = a_star_multi.run_a_star_multi(graph, agents)
    # a_star.run_a_star(graph, agents) if algorithm == "A*" else d_star.run_d_star(graph, agents)
    # a_star_multi.run_a_star_multi(graph, agents)

    # Visualize the results of the search algorithm
    vis_obj = vis.Visualization()
    # vis_obj.animate_paths(planner_paths, graph)
    # vis_obj.show_path(planner_paths, graph)
    metrics = None
    metrics = vis_obj.update_metrics(planner_paths, graph)
    
    # exract the metrics from the visualization object
    max_dist = max(metrics['agent_distance'].values())
    speed = 1 # m/s
    delay = metrics['total_estops'] + metrics['total_dropoffs'] # seconds
    metrics['total_time'] = (max_dist / speed) + delay
    metrics['agent_time'] = {}
    metrics['agent_parcles_hour'] = {}

    for agent, value in metrics['agent_distance'].items():
        metrics["agent_time"][agent] = (value / speed) + metrics['estop'][agent] + (num_packages*2)-1
        metrics['agent_parcles_hour'][agent] = (num_packages / metrics["agent_time"][agent]) * 3600

    metrics['avg_parcels_hour'] = sum(metrics['agent_parcles_hour'].values()) / num_agents
    metrics['avg_time'] = sum(metrics['agent_time'].values()) / num_agents
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
            "Total Time": metrics['total_time'], 
            "Total Distance": sum(metrics['agent_distance'].values()), 
            "Total Dropoffs": metrics['total_dropoffs'],
            "Total Planned Drops": num_agents * ((2*num_packages) - 1),
            "Total E-Stops": metrics['total_estops'],
            "Average Parcels per Hour": metrics['avg_parcels_hour'],
            "Average Time per Agent": metrics['avg_time']
        }
    }

    print(full_metrics['simulation results']["Total Planned Drops"])
    # write a json file with the metrics
    json_metrics = json.dumps(full_metrics, indent=4)
    
    if full_metrics['simulation results']['Total Dropoffs'] == full_metrics['simulation results']['Total Planned Drops']:
        with open("metrics_" + algorithm + "_" + str(num_agents) + "_" + str(num_packages) + "__" + str(time.time()) + ".json", 'w') as outfile:
            outfile.write(json_metrics)
        print("Simulation Passed")
    else:
        with open("metrics_" + str(time.time()) + ".json", 'w') as outfile:
            outfile.write(json_metrics)
   


if __name__ == "__main__":
    test_validation(algorithm="Multi_A-star", num_agents=15, num_packages=2)