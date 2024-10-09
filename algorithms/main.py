# file for running algorithms

import a_star_w_reroute as a_star
import d_star_w_reroute as d_star
import json_to_graph as jtg
import networkx as nx
import matplotlib.pyplot as plt
import json_to_multi as jtm
from matplotlib.animation import FuncAnimation
import numpy as np
# Driver Code

def convert_to_nx_graph(graph):
    nx_graph = nx.Graph()
    for vertex in graph.vertices:
        nx_graph.add_node(vertex, pos=graph.vert_coord[vertex])
        for neighbor in graph.get_neighbors(vertex):
            nx_graph.add_edge(vertex, neighbor)
    return nx_graph

def main():
    # TODO: implement time and space complexity analysis and find metrics for the algorithms

    # Define the graph from the interperter
    j_graph = jtg.json_to_graph('algorithms/test_json/test2.json')
    #j_graph = jtm.json_to_graph('algorithms/test_json/test3.json')
    #j_graph = jtm.json_to_graph('algorithms/test_json/test4.json')

    # Define the source and destination
    agents = {1:("node_008", "node_006"), 2:("node_002", "node_007"), 3:("node_003", "node_005"), 4:("node_001","node_009")}

    # Run the search algorithm requested by the user
    src = agents[1][0]
    dest = agents[1][1]
    d_star.d_star_search(j_graph, src, dest)
    a_star_paths = a_star.run_a_star(j_graph, agents)

    # Convert the graph to a networkx graph and plot it
    # plt.figure(1)
    nx_graph = convert_to_nx_graph(j_graph)
    pos = nx.get_node_attributes(nx_graph, 'pos') # or pos = nx.spring_layout(nx_graph)
    # nx.draw(nx_graph, pos, with_labels=True, node_size=500, node_color='skyblue')
    # plt.title("NetworkX Graph")

    # Plot the second figure for the animation
    fig, ax = plt.subplots()
    nx.draw(nx_graph, nx.get_node_attributes(nx_graph, 'pos'), with_labels=True, node_size=500, node_color='skyblue')
    plt.title("Agent Paths Animation")

    # Initialize the animation
    lines = {agent: ax.plot([], [], marker='o', markersize=10, label=f"Agent {i+1}")[0] for i, agent in enumerate(agents)}
    trails = {agent: ax.plot([], [], linestyle='-', color=lines[agent].get_color())[0] for agent in agents}

    # Initialize the reservation table
    reservation_table = {}

    def init():
        for line in lines.values():
            line.set_data([], [])
        for trail in trails.values():
            trail.set_data([], [])

        return list(lines.values())+list(trails.values())

    def update(frame):
        for agent, path in a_star_paths.items():
            if path and frame < len(path):
                node, time = path[frame]
                x, y = pos[node]

                # Check for collisions
                if time in reservation_table and node in reservation_table[time]:
                    print(f"Collision detected at time {time} at node {node}")
                else:
                    if time not in reservation_table:
                        reservation_table[time] = set()
                    reservation_table[time].add(node)

                # Update the path
                lines[agent].set_data([x], [y])
                # Update the trail
                trail_x, trail_y = trails[agent].get_data()
                trail_x = np.append(trail_x, x)
                trail_y = np.append(trail_y, y)
                trails[agent].set_data(trail_x, trail_y)
        return list(lines.values()) + list(trails.values())

    # Animate the paths
    num_frames = max(len(path) for path in a_star_paths.values())
    anim = FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, repeat=True, interval=1000)

    # save the animation as a gif
    anim.save('C:/Users/HP/Documents/0. Fall 24/senior design/agent_paths.gif', writer='imagemagick')
    # plt.legend(loc='lower left')
    plt.show()


if __name__ == "__main__":
    main()