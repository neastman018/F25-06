import heapq


"""
A* algorithm implementation for finding the shortest path in a graph.
Args:
    graph (dict): The graph represented as a dictionary where the keys are nodes and the values are lists of tuples representing the neighbors and their associated costs.
    start (tuple): The starting node.
    goal (tuple): The goal node.
    heuristic (function): The heuristic function used to estimate the cost from a node to the goal.
Returns:
    list or None: The shortest path from the start node to the goal node as a list of nodes. If no path is found, returns None.
"""
import heapq

def new_a_star(json_graph, start, goal, heuristic, blocked_nodes, time_step):
    graph = json_graph.vertices
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(json_graph.get_coords(start), json_graph.get_coords(goal))
    visited = set()

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            return reconstruct_path(came_from, current)
        
        if current in blocked_nodes or current in visited:
            #print(f"Node {current} is blocked, skipping.")
            continue

        visited.add(current)

        for neighbor, cost in graph[current].items():
            # Check if the neighbor is blocked at the current time step
            if neighbor in blocked_nodes or neighbor in visited:
                #print("blocked node")
                continue
            
            tentative_g_score = g_score[current] + cost
            
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(json_graph.get_coords(neighbor), json_graph.get_coords(goal))
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None

def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path

def heuristic(node, goal):
    # Example heuristic function (Manhattan distance for grid-based graph)
    (x1, y1) = node
    (x2, y2) = goal
    return abs(x1 - x2) + abs(y1 - y2)

def run_a_star_multi(json_graph, agents):
    paths = {}
    time_step = 0
    blocked_nodes = {}

    while agents:
        new_agents = {}
        for agent, routes in agents.items():
            if agent not in paths:
                paths[agent] = []
            for route in routes:
                src, dest = route
                path = new_a_star(json_graph, src, dest, heuristic, blocked_nodes, time_step)
                if path:
                    blocked_node = check_conflict(paths, path, time_step, blocked_nodes, agent)
                    while blocked_node != -1:
                        # blocked node has the name of the node in the way
                        path = new_a_star(json_graph, src, dest, heuristic, blocked_nodes, time_step)
                        if not path:
                            time_step += 1
                            blocked_nodes = {}
                            continue
                        blocked_node = check_conflict(paths, path, time_step, blocked_nodes, agent) 

                    paths[agent].append(path)
                    blocked_nodes = {}
                else:
                    new_agents[agent] = []
                    new_agents[agent].append((src,dest))
            time_step += 1

        # for node in list(blocked_nodes.keys()):
        #     blocked_nodes[node] = [t for t in blocked_nodes[node] if t > time_step]
        #     if not blocked_nodes[node]:
        #         del blocked_nodes[node]
        agents = new_agents

    return paths

def check_conflict(paths, new_path, time_step, blocked_nodes, curr_agent):
    for agent_num, path in paths.items():
        bottom_path = []
        if agent_num == curr_agent:
            continue
        else:
            start_time = 0
            for path in paths[curr_agent]:
                start_time += len(path)
            curr_time = time_step + start_time

            for path in paths[agent_num]:
                bottom_path += path

        

        if(path != []):
            length = min(len(bottom_path)-curr_time+agent_num-1, len(new_path))
        else:
            length = len(new_path)
        # if the length is negative, the bottom path is shorter than the start of the new path
        if length < 0:
            continue
        for i in range(length):
            # check if bottom path exists and if the node is the same as the new path
            if bottom_path != []:
                # other path's node
                other_node = bottom_path[i+curr_time-agent_num + 1]
                curr_node = new_path[i]
                if other_node == curr_node and i != (len(new_path)-1) and i != 0:
                    if curr_node not in blocked_nodes:
                        blocked_nodes[curr_node] = []
                        blocked_nodes[curr_node].append(curr_time + 2)
                    else:
                        blocked_nodes[curr_node].append(curr_time + 2)
                    return curr_node
                # Check for edge conflicts (swapping places)
                if  i>0 and bottom_path[i+curr_time-agent_num] == curr_node and other_node == new_path[i-1] and i != (len(new_path)-1) and i != 0:
                    print("edge conflict")
                    if curr_node not in blocked_nodes:
                        blocked_nodes[bottom_path[i+curr_time-agent_num]] = []
                        blocked_nodes[bottom_path[i+curr_time-agent_num]].append(curr_time + 2)
                    if new_path[i - 1] not in blocked_nodes:
                        blocked_nodes[other_node] = []
                        blocked_nodes[other_node].append(curr_time + 2)
                    return curr_node
            # if bottom_path and bottom_path[i + time_step - agent_num + 1] == new_path[i]:
            #     print("headon conflict")
            #     if new_path[i] not in blocked_nodes:
            #         blocked_nodes[new_path[i]] = []
            #         blocked_nodes[new_path[i]].append(time_step + 2)
            #     return new_path[i]
    return -1

class SimpleGraph:
    def __init__(self):
        self.vertices = {
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1}
        }
        self.coords = {
            'A': (0, 0),
            'B': (1, 0),
            'C': (1, 1),
            'D': (2, 1)
        }

    def get_coords(self, node):
        return self.coords[node]

# Create a simple graph
simple_graph = SimpleGraph()

# Define agents with their start and goal positions
# agents = [
#     ('A', 'D'),
#     ('B', 'C')
# ]

# Run the A* algorithm for multiple agents
# run_a_star_multi(simple_graph, agents)
