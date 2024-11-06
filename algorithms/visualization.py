from matplotlib.animation import FuncAnimation
import numpy as np
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import time
import copy


# class for visualizing the results of the algorithms
class Visualization:
    # graph object
    graph = None
    # create metrics for the algorithms
    metrics = {}
    metrics['agent_distance'] = {}
    metrics['total_estops'] = 0
    metrics['total_replan'] = 0
    metrics['total_dropoffs'] = 0

    def __init__(self) -> None:
        pass
    
    def update_metrics(self, paths, graph):
        
        self.nx_graph = self.convert_to_nx_graph(graph)
        self.pos = nx.get_node_attributes(self.nx_graph, 'pos')
        # todo: implement time and space complexity analysis and find metrics for the algorithms
        
        agents_paths = {}
        agent_info = {}
        frame = 0
        current_reservations = {}

        for agent in paths:
                agents_paths[agent] = list(itertools.chain(*paths[agent]))
                agent_info[agent] = 0
                self.metrics['agent_distance'][agent] = 0

        frame = 0
        done = False
        prev_reservations = {}

        while not done:  
            for agent, path in agents_paths.items():
                if path and (frame - agent_info[agent]) < len(path):
                    node = path[frame - agent_info[agent]]
                    x, y = self.pos[node]

                    if frame > 0 and node == path[frame - agent_info[agent] - 1]:
                        self.metrics['total_dropoffs'] += 1

                    # Check if the node is reserved
                    if frame > 0 and node in current_reservations and node != path[frame - agent_info[agent] - 1]:
                        # check if the reservation is try to switch
                        conflict_agent = current_reservations[node][0]
                        if agents_paths[conflict_agent][frame - agent_info[conflict_agent] + 1] == path[frame - agent_info[agent] - 1]:
                            # allow for the agents to switch
                            current_reservations[node].pop(0)
                            current_reservations[path[frame - agent_info[agent] - 1]].pop(0)
                            current_reservations[node].insert(0, agent)
                            if len(current_reservations[path[frame - agent_info[agent] - 1]]) == 0:
                                del current_reservations[path[frame - agent_info[agent] - 1]]
                            
                        else:
                            # If the node is reserved, wait for the other agent to move
                            agent_info[agent] += 1
                            prev_node = path[frame - agent_info[agent]]
                            x, y = self.pos[prev_node]
                    else:
                        # Reserve the node using a stack of reservations
                        if node not in current_reservations:
                            current_reservations[node] = []

                        current_reservations[node].append(agent)

                        if frame > 0:
                            prev_node = path[frame - agent_info[agent] - 1]
                            if prev_node in current_reservations and current_reservations[prev_node]:
                                old_node_agent = current_reservations[prev_node].pop(0)
                                if len(current_reservations[prev_node]) == 0:
                                    del current_reservations[prev_node]
                                if old_node_agent != agent:
                                    # print(f"Agent {agent} is waiting for Agent {old_node_agent} to move")
                                    self.metrics['total_estops'] += 1

                    # Update the agent's distance
                    prev_node = path[frame - agent_info[agent]-1]
                    self.metrics['agent_distance'][agent] += np.sqrt((x - self.pos[prev_node][0])**2 + (y - self.pos[prev_node][1])**2)
                else:
                    if path[len(path)-1] in current_reservations:
                        del current_reservations[path[len(path)-1]]

            
            done = True
            for agent in agents_paths:
                # check that all agents have reached their destination
                if (frame - agent_info[agent] - 1) < len(agents_paths[agent]):
                    done = False
                    break

            if frame > 0 and prev_reservations == current_reservations:
                    done = True
                    break   

            prev_reservations = copy.deepcopy(current_reservations)
            frame += 1
        
            
                
        return self.metrics


    def convert_to_nx_graph(self, graph):
        nx_graph = nx.Graph()
        for vertex in graph.vertices:
            nx_graph.add_node(vertex, pos=graph.vert_coord[vertex])
            for neighbor in graph.get_neighbors(vertex):
                nx_graph.add_edge(vertex, neighbor)
        return nx_graph

    def draw_graph(self, graph):
        self.nx_graph = self.convert_to_nx_graph(graph)
        self.pos = nx.get_node_attributes(self.nx_graph, 'pos')
        nx.draw(self.nx_graph, self.pos, with_labels=False)
        plt.show()

    
    
    def animate_paths(self, planners_paths, graph):
        self.nx_graph = self.convert_to_nx_graph(graph)
        self.pos = nx.get_node_attributes(self.nx_graph, 'pos')
        
        agents = list(planners_paths.keys())

        # Plot the second figure for the animation
        fig, ax = plt.subplots()
        nx.draw(self.nx_graph, nx.get_node_attributes(self.nx_graph, 'pos'), with_labels=False, node_size=75, node_color='skyblue')
        plt.title("Agent Paths Animation")

        # Initialize the animation
        lines = {agent: ax.plot([], [], marker='o', markersize=10, label=f"Agent {i+1}")[0] for i, agent in enumerate(agents)}
        trails = {agent: ax.plot([], [], linestyle='-', color=lines[agent].get_color())[0] for agent in agents}

        
        # Initialize the reservation table for the current frame
        current_reservations = {}
        agents_paths = {}
        agent_info = {}

        # Initialize the reservation table
        def init():
            for agent in planners_paths:
                agents_paths[agent] = list(itertools.chain(*planners_paths[agent]))
                agent_info[agent] = {'delay': 0, 'offset': 0}
                
            for line in lines.values():
                line.set_data([], [])
            for trail in trails.values():
                trail.set_data([], [])

            return list(lines.values())+list(trails.values())

        def update(frame):
            # something to break at
            for agent, path in agents_paths.items():
                if path and (frame - agent_info[agent]['delay']) < len(path):
                    node = path[frame - agent_info[agent]['delay']]
                    x, y = self.pos[node]

                    # Check if the node is reserved
                    if frame > 0 and node in current_reservations and node != path[frame - agent_info[agent]['delay'] - 1]:
                        # If the node is reserved, wait for the other agent to move
                        agent_info[agent]['delay'] += 1
                        prev_node = path[frame - agent_info[agent]['delay']]
                        x, y = self.pos[prev_node]
                        agent_info[agent]['offset'] = 0.05
                    else:
                        # Reserve the node using a stack of reservations
                        if node not in current_reservations:
                            current_reservations[node] = []
                        elif node == path[frame - agent_info[agent]['delay'] - 1]:
                            # restart the trail for the agent
                            trails[agent].set_data([], [])

                        current_reservations[node].append(agent)

                        if frame > 0:
                            prev_node = path[frame - agent_info[agent]['delay'] - 1]
                            if prev_node in current_reservations and current_reservations[prev_node]:
                                old_node_agent = current_reservations[prev_node].pop(0)
                                if len(current_reservations[prev_node]) == 0:
                                    del current_reservations[prev_node]
                                if old_node_agent != agent:
                                    print(f"Agent {agent} is waiting for Agent {old_node_agent} to move")

                    # Update the agent's distance
                    prev_node = path[frame - agent_info[agent]['delay']-1]
                    
                    # apply offset to the agent's trail
                    offset = agent_info[agent]['offset']
                    offset_x = x + offset
                    offset_y = y + offset

                    # Update the path
                    lines[agent].set_data([x], [y])
                    # Update the trail
                    trail_x, trail_y = trails[agent].get_data()
                    trail_x = np.append(trail_x, offset_x)
                    trail_y = np.append(trail_y, offset_y)
                    trails[agent].set_data(trail_x, trail_y)
            return list(lines.values()) + list(trails.values())

        # Animate the paths
        num_frames = 0
        for paths in planners_paths.values():
            for path in paths:
                if path and len(path) > num_frames:
                    num_frames = len(path)
        num_frames = num_frames * 4
        self.metrics['total_time'] = num_frames
        anim = FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True, repeat=True, interval=1000)

        # save the animation as a gif
        anim.save('C:/Users/HP/Documents/0. Fall 24/senior design/test/testing_' + str(time.time()) +'.gif', writer='Pillow', fps=1)

        # plt.legend(loc='lower left')
        plt.show()

        return self.metrics

    def show_path(self, path, graph):
        self.nx_graph = self.convert_to_nx_graph(graph)
        self.pos = nx.get_node_attributes(self.nx_graph, 'pos')
        # Draw the graph
        nx.draw(self.nx_graph, self.pos, with_labels=False, node_size=200, node_color='skyblue')
        
        # Extract the coordinates of the path
        agents_paths = {}
        for agent in path:
            agents_paths[agent] = list(itertools.chain(*path[agent]))
        for agent, path in agents_paths.items():
            path_coords = [self.pos[node] for node in path]
            path_x, path_y = zip(*path_coords)
            
        plt.plot(path_x, path_y, marker='o', markersize=10, label=f"Agent {agent}")
        
        plt.title("Path from Start to Goal")
        plt.legend()
        plt.show()