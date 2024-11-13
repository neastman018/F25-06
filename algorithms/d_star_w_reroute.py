import heapq
import numpy as np

def calculate_heuristic(start, goal):
    (x1, y1) = start
    (x2, y2) = goal
    x_val = (x1-x2)**2
    y_val = (y1-y2)**2
    return np.sqrt(x_val + y_val)

def d_star(json_graph, start, goal, reservation_table):
    graph = json_graph.vertices
    open_list = [(calculate_heuristic(json_graph.get_coords(start), json_graph.get_coords(goal)), start, 0)]
    g_values = {(start, 0): 0}
    predecessors = {}
    visited = set()

    while open_list:
        current_cost, current, current_time = heapq.heappop(open_list)
        print(f"Current node: {current}, Time: {current_time}, Cost: {current_cost}")

        if (current) in visited:
            continue

        visited.add((current))

        if current == goal:
            return reconstruct_path(predecessors, current, current_time)

        for neighbor, cost in graph[current].items():
            tentative_g_score = g_values[(current, current_time)] + cost
            neighbor_time = current_time + 1

            if (neighbor, neighbor_time) not in g_values or tentative_g_score < g_values[(neighbor, neighbor_time)]:
                if not is_occupied(neighbor, neighbor_time, reservation_table):
                    g_values[(neighbor, neighbor_time)] = tentative_g_score
                    heapq.heappush(open_list, (tentative_g_score + calculate_heuristic(json_graph.get_coords(neighbor), json_graph.get_coords(goal)), neighbor, neighbor_time))
                    predecessors[(neighbor, neighbor_time)] = (current, current_time)

                    # Prune the open list if it becomes too large
                    if len(open_list) > 1000:  # Example threshold
                        open_list = prune_open_list(open_list)

    return None

def prune_open_list(open_list):
    N = 100  # Example threshold
    open_list.sort(key=lambda x: x[0])
    return open_list[:N]

def is_occupied(node, time, reservation_table):
    return node in reservation_table and time in reservation_table[node]

def reconstruct_path(predecessors, current, current_time):
    total_path = {'path':[current], 'time': [current_time]}
    while (current, current_time) in predecessors:
        current, current_time = predecessors[(current, current_time)]
        total_path['path'].append(current)
        total_path['time'].append(current_time)
    total_path['path'].reverse()
    total_path['time'].reverse()
    return total_path

def d_star_search(json_graph, src, dest):
    path = d_star(json_graph, src, dest, {})
    print("Path: (", src + ", " + dest + "):")
    print("Path found:", path)

def run_d_star(json_graph, agents):
    paths = {}
    reservation_table = {}
    for agent, routes in agents.items():
        paths[agent] = []
        for route in routes:
            src, dest = route
            path = d_star(json_graph, src, dest, reservation_table)
            paths[agent].append(path['path'])
            # print("Agent: " + str(agent) + ": Path found:", path)

    return paths

# # Example usage
# graph = Graph()
# graph.add_vertex((0, 0))
# graph.add_vertex((0, 1))
# graph.add_vertex((1, 0))
# graph.add_vertex((1, 1))
# graph.add_edge((0, 0), (0, 1), 1)
# graph.add_edge((0, 1), (1, 1), 1)
# graph.add_edge((1, 1), (1, 0), 1)
# graph.add_edge((1, 0), (0, 0), 1)

# agents = [((0, 0), (1, 1)), ((0, 1), (1, 0))]
# paths = multi_agent_path_planning(graph, agents)
# for agent, path in paths.items():
#     print(f"Agent {agent} path: {path}")