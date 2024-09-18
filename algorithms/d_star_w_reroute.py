import heapq

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        self.vertices[vertex] = {}

    def add_edge(self, start, end, cost):
        self.vertices[start][end] = cost

    def get_neighbors(self, vertex):
        return self.vertices[vertex]

def calculate_heuristic(start, goal):
    (x1, y1) = start
    (x2, y2) = goal
    return abs(x1 - x2) + abs(y1 - y2)

def d_star(graph, start, goal, reservation_table):
    open_list = [(calculate_heuristic(start, goal), start, 0)]
    g_values = {(start, 0): 0}
    predecessors = {}

    while open_list:
        current_cost, current, current_time = heapq.heappop(open_list)

        if current == goal:
            return reconstruct_path(predecessors, current, current_time)

        for neighbor, cost in graph.get_neighbors(current).items():
            tentative_g_score = g_values[(current, current_time)] + cost
            neighbor_time = current_time + 1

            if (neighbor, neighbor_time) not in g_values or tentative_g_score < g_values[(neighbor, neighbor_time)]:
                if not is_occupied(neighbor, neighbor_time, reservation_table):
                    g_values[(neighbor, neighbor_time)] = tentative_g_score
                    heapq.heappush(open_list, (tentative_g_score + calculate_heuristic(neighbor, goal), neighbor, neighbor_time))
                    predecessors[(neighbor, neighbor_time)] = (current, current_time)

    return None

def is_occupied(node, time, reservation_table):
    return node in reservation_table and time in reservation_table[node]

def reconstruct_path(predecessors, current, current_time):
    total_path = [(current, current_time)]
    while (current, current_time) in predecessors:
        current, current_time = predecessors[(current, current_time)]
        total_path.append((current, current_time))
    total_path.reverse()
    return total_path

def multi_agent_path_planning(graph, agents):
    reservation_table = {}
    paths = {}
    for agent in agents:
        start, goal = agent
        path = d_star(graph, start, goal, reservation_table)
        if path:
            paths[agent] = path
            for node, time in path:
                if node not in reservation_table:
                    reservation_table[node] = set()
                reservation_table[node].add(time)
        else:
            paths[agent] = None
    return paths

# Example usage
graph = Graph()
graph.add_vertex((0, 0))
graph.add_vertex((0, 1))
graph.add_vertex((1, 0))
graph.add_vertex((1, 1))
graph.add_edge((0, 0), (0, 1), 1)
graph.add_edge((0, 1), (1, 1), 1)
graph.add_edge((1, 1), (1, 0), 1)
graph.add_edge((1, 0), (0, 0), 1)

agents = [((0, 0), (1, 1)), ((0, 1), (1, 0))]
paths = multi_agent_path_planning(graph, agents)
for agent, path in paths.items():
    print(f"Agent {agent} path: {path}")