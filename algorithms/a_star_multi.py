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

def run_a_star_multi(json_graph, agents):
    paths = {}
    time_step = 0

    while agents:
        new_agents = []
        for agent in agents:
            src, dest = agent
            path = a_star(json_graph, src, dest, heuristic)
            if path:
                if not check_conflict(paths, path, time_step):
                    paths[agent] = path
                    print(f"Agent: ({src}, {dest}): Path found: {path}")
                else:
                    new_agents.append(agent)
            else:
                new_agents.append(agent)
        agents = new_agents
        time_step += 1

def check_conflict(paths, new_path, time_step):
    for path in paths.values():
        if len(path) > time_step and path[time_step] == new_path[time_step]:
            return True
    return False

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
agents = [
    ('A', 'D'),
    ('B', 'C')
]

# Run the A* algorithm for multiple agents
run_a_star_multi(simple_graph, agents)
