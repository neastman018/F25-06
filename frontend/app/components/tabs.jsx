import * as React from 'react';
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import { TabContext, TabList, TabPanel } from '@mui/lab';
import CodeBlock from './codeblock';



const a_star_code = `
    # A* Search Algorithm
    def a_star(start, goal, h):
        # The set of nodes already evaluated
        closed_set = set()

        # The set of currently discovered nodes that are not evaluated yet.
        # Initially, only the start node is known.
        open_set = {start}

        # For each node, which node it can most efficiently be reached from.
        # If a node can be reached from many nodes, came_from will eventually
         contain the most efficient previous step.
        came_from = {}

        # For each node, the cost of getting from the start node to that node.
        g_score = {start: 0}

        # For each node, the total cost of getting from the start node to the goal
        # by passing by that node. That value is partly known, partly heuristic.
        f_score = {start: h(start)}

        while open_set:
            # The node in open_set having the lowest f_score[] value
            current = min(open_set, key=lambda node: f_score.get(node, float('inf')))

            if current == goal:
                return reconstruct_path(came_from, current)

            open_set.remove(current)
            closed_set.add(current)

            for neighbor in get_neighbors(current):
                if neighbor in closed_set:
                    continue  # Ignore the neighbor which is already evaluated.

                # The distance from start to a neighbor
                tentative_g_score = g_score[current] + dist_between(current, neighbor)

                if neighbor not in open_set:  # Discover a new node
                    open_set.add(neighbor)
                elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                    continue  # This is not a better path.

                # This path is the best until now. Record it!
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor)

        # Open set is empty but goal was never reached
        return False

    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path

    def dist_between(node_a, node_b):
        # This function should return the distance between node_a and node_b
        # Implement this based on your specific use case
        pass

    def get_neighbors(node):
        # This function should return the neighbors of a node
        # Implement this based on your specific use case
        pass
    `;

const d_star_code = `
    # D* Search Algorithm
    def d_star(start, goal, h):
        # Initialize the open and closed sets
        open_set = {start}
        closed_set = set()

        # Initialize the g_score and rhs_score dictionaries
        g_score = {start: float('inf')}
        rhs_score = {start: 0}

        # Initialize the priority queue with the start node
        priority_queue = PriorityQueue()
        priority_queue.put((h(start), start))

        while not priority_queue.empty():
            # Get the node with the lowest priority
            current = priority_queue.get()[1]

            if current == goal:
                return reconstruct_path(came_from, current)

            open_set.remove(current)
            closed_set.add(current)

            for neighbor in get_neighbors(current):
                if neighbor in closed_set:
                    continue

                tentative_rhs_score = rhs_score[current] + dist_between(current, neighbor)

                if tentative_rhs_score < rhs_score.get(neighbor, float('inf')):
                    rhs_score[neighbor] = tentative_rhs_score
                    g_score[neighbor] = min(g_score.get(neighbor, float('inf')), rhs_score[neighbor] + h(neighbor))
                    priority_queue.put((g_score[neighbor], neighbor))
                    open_set.add(neighbor)

        return False

    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path

    def dist_between(node_a, node_b):
        # This function should return the distance between node_a and node_b
        # Implement this based on your specific use case
        pass

    def get_neighbors(node):
        # This function should return the neighbors of a node
        # Implement this based on your specific use case
        pass

        `;

const random_tree_code = `
    # Random Tree Pathing Algorithm
    def random_tree_path(start, goal):
        # Initialize the tree with the start node
        tree = {start: None}
        
        # Initialize the set of visited nodes
        visited = set()
        
        # While the goal is not reached
        while goal not in tree:
            # Select a random node from the tree
            current = select_random_node(tree)
            
            # Get the neighbors of the current node
            neighbors = get_neighbors(current)
            
            # For each neighbor
            for neighbor in neighbors:
                # If the neighbor has not been visited
                if neighbor not in visited:
                    # Add the neighbor to the tree
                    tree[neighbor] = current
                    
                    # Mark the neighbor as visited
                    visited.add(neighbor)
                    
                    # If the goal is reached, break
                    if neighbor == goal:
                        break
        
        # Reconstruct the path from start to goal
        path = reconstruct_path(tree, goal)
        
        return path

    def select_random_node(tree):
        # This function should return a random node from the tree
        # Implement this based on your specific use case
        pass

    def get_neighbors(node):
        # This function should return the neighbors of a node
        # Implement this based on your specific use case
        pass

    def reconstruct_path(tree, goal):
        # This function should reconstruct the path from start to goal
        # Implement this based on your specific use case
        pass`;


export default function AlgorithmTabs() {
    const [value, setValue] = React.useState('1');

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <Box sx={{ width: '100vw', typography: 'body1', display: 'flex', justifyContent: 'right', alignItems: 'center', flexDirection: 'column' }}>
                <TabContext value={value}>
                    <Box sx={{ borderBottom: 2, borderColor: 'divider', width: '100%' }}>
                        <TabList onChange={handleChange} aria-label="lab API tabs example" centered>
                            <Tab label="A*" value="1" />
                            <Tab label="D*" value="2" />
                            <Tab label="Random Tree" value="3" />
                        </TabList>
                    </Box>
                    <TabPanel value="1" sx={{ width: '60%', transform: 'rotateY(5deg) translateZ(10px)', transition: 'transform 0.5s' }}>
                    <CodeBlock code={a_star_code} language="python" />
                    </TabPanel>
                    <TabPanel value="2" sx={{ width: '60%', transform: 'rotateY(5deg) translateZ(10px)', transition: 'transform 0.5s' }}>
                    <CodeBlock code={d_star_code} language="python" />
                    </TabPanel>
                    <TabPanel value="3" sx={{ width: '60%', transform: 'rotateY(5deg) translateZ(10px)', transition: 'transform 0.5s' }}>
                    <CodeBlock code={random_tree_code} language="python" />
                    </TabPanel>
                </TabContext>
        </Box>

    );
}