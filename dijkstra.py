'''
Names: Jakira Williams and Keiser Dallas
Date: 2/18/22
Section: 450-001
Assignment: Project 2
'''




import sys # Command Line arguments 
import csv # CSV reader



# Function to find edge costs from csv file
# Takes list of unvisiTED
def setDistance(nodes, disc, cost, graph, source):
    i = 0
    while(i < len(nodes) - 1):
        nxt_row = next(graph)
        j = 1
        while(j < len(nodes)):
            cost[(nodes[j], nxt_row[0])] = int(nxt_row[j])
            j += 1
        i += 1
    nodes.remove('')
    nodes.remove(source)
    disc.append(source)
    

# Dijkstra's Algorithm 
def dijkstra(source, unv_nodes, disc, shortDist, pre_node, edge):
    
    # Set distances of all nodes to inf and prev node to none 
    for vertex in unv_nodes:
        shortDist[vertex] = 9999
        pre_node[vertex] = None 
        
    # Set source shortest distance to 0
    shortDist[source] = 0
    
    while(len(unv_nodes) != 0):
        
        # Find the next unvisited node w/ shortest path
        v = unv_nodes[0]
        for vertex in unv_nodes:
            if (shortDist[vertex] < shortDist[v]):
                v = vertex
        unv_nodes.remove(v) # Mark v as explored
        disc.append(v)
        for(v,w) in edge:
            if(shortDist[v] + edge[(v,w)] < shortDist[w]):
                shortDist[w] = shortDist[v] + edge[(v,w)]
                pre_node[w] = v
    

# Bellman-Ford Equation
def bellmanford(source, unv_nodes, shortDist, pre_node, edge):
    
    # Set distances of all nodes to inf and prev node to none 
    for vertex in unv_nodes:
        shortDist[vertex] = 9999
        pre_node[vertex] = None 
        
    # Set source shortest distance to 0
    shortDist[source] = 0
    
    # Update the neighbor's distances using BF
    for i in range(len(unv_nodes) - 1):
        for(v,w) in edge:
            if(shortDist[v] + edge[(v,w)] < shortDist[w]):
                shortDist[w] = shortDist[v] + edge[(v,w)]


# Displays Distance-Vector for each node 
def disVec(unv_nodes,cost):
    print("")
    # Perform Bell-Man Ford for each node
    for node in unv_nodes:
        distV = {}
        prev2 = {}
        temp = unv_nodes
        bellmanford(node, temp, distV, prev2, cost)
        print("\nDistance vector for node {}:".format(node))
        for key in distV:
            i = distV[key]
            print(i, end=" ")


                
# Print shortest path and least cost path for each node for Dijkstra's Alg
def disPath(source,disc,shortDist, pre_node):
    
    # Display Shortest Path for each node
    print("Shortest path tree for {}: ".format(source))
    for node in disc:
        if(node != '' and node != source):
            j = disc.index(node)
            print(str(disc[:j]) + ", ")
    
    # Display the least cost path
    print("Least-cost path for {}:".format(source))
    for node in disc:
        i = "{}: {} ".format(node,dist[node])
        print(i, end=" ")
        
 

# MAIN

# Grab command line args and open CSV file
top_file = sys.argv[2] 
file = open(top_file) 
csvreader = csv.reader(file)



# Lists for explored and unvisited nodes
unvisited = next(csvreader)
unvisited2 = []
for index in unvisited:
    unvisited2.append(index)
unvisited2.remove('')
visited = []



# Dictionaries for shortest distance and prev node
dist = {}
prev = {} 
cost = {}


# Prompt for source node, set distances, and run algorithms 
source_node = input("Please, provide the source node: ")

# Construct the graph costs
setDistance(unvisited, visited, cost, csvreader, source_node)

# Perform Dijkstra's Alg and display
dijkstra(source_node, unvisited, visited, dist, prev, cost)
disPath(source_node, visited, dist, prev)

# Perform Distance-Vector for each node and display
disVec(unvisited2, cost)



