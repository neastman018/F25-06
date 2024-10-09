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
def a_star(json_graph, start, goal, heuristic):
    graph = json_graph.vertices
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(json_graph.get_coords(start), json_graph.get_coords(goal))
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            return reconstruct_path(came_from, current)
        
        for neighbor, cost in graph[current].items():
            tentative_g_score = g_score[current] + cost
            
            if tentative_g_score < g_score[neighbor]:
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


def run_a_star(json_graph, agents):
    paths = {}
    for agent, route in agents.items():
        src, dest = route
        path = a_star(json_graph, src, dest, heuristic)
        paths[agent] = path, list(range(len(path)+1))
        print("Agent: " + str(agent) + ": Path found:", path)

    return paths



# # Example usage
# graph = {
#     (0, 0): [((0, 1), 1), ((1, 0), 1)],
#     (0, 1): [((0, 0), 1), ((1, 1), 1)],
#     (1, 0): [((0, 0), 1), ((1, 1), 1)],
#     (1, 1): [((1, 0), 1), ((0, 1), 1)]
# }

# start = (0, 0)
# goal = (1, 1)
# path = a_star(graph, start, goal, heuristic)
# print("Path found:", path)  # Output: Path found: [(0, 0), (1, 0), (1, 1)]

