# file for running algorithms

import a_star_w_reroute as a_star
import d_star_w_reroute as d_star
import json_to_graph as jtg
# Driver Code



def main():
    # Define the graph from the interperter
    graph = jtg.json_to_graph('test_json/test1.json')

    # Define the source and destination
    src = 1
    dest = 8

    
    # Run the search algorithm requested by the user
    d_star.d_star_search(graph, src, dest)
    a_star.a_star_search(graph, src, dest)

if __name__ == "__main__":
    main()