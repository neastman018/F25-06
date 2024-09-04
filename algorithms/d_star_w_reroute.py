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
    # Calculate the heuristic value between two vertices (e.g., Euclidean distance)
    # Replace this with your own heuristic function
    return 0

def d_star(graph, start, goal):
    open_list = [(calculate_heuristic(start, goal), start)]
    g_values = {start: 0}
    predecessors = {}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in predecessors:
                path.insert(0, current)
                current = predecessors[current]
            path.insert(0, start)
            return path

        for neighbor, cost in graph.get_neighbors(current).items():
            new_g = g_values[current] + cost

            if neighbor not in g_values or new_g < g_values[neighbor]:
                g_values[neighbor] = new_g
                f_value = new_g + calculate_heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_value, neighbor))
                predecessors[neighbor] = current

    return None

# Example usage
graph = Graph()
graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')
graph.add_vertex('D')
graph.add_edge('A', 'B', 1)
graph.add_edge('B', 'C', 2)
graph.add_edge('C', 'D', 3)
graph.add_edge('A', 'D', 10)

start_vertex = 'A'
goal_vertex = 'D'
path = d_star(graph, start_vertex, goal_vertex)
print(path)