import random
import math

# JORDA ER FLAT!#

### GLOBALS ###
MAXPHEROMONES = 100000
MINPHEROMONES = 1
MAXCOST = math.sqrt(200**2 + 200**2)


### CLASSES ###

class Node:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinate_x = coordinates[0]
        self.coordinate_y = coordinates[1]
        self.edges = {}

    def distance_to(self, toNode):
        return math.sqrt((self.coordinate_x - toNode.coordinate_x)**2 + (self.coordinate_y - toNode.coordinate_y)**2)

    def rouletteWheel(self, visitedEdges, startNode, endNode):
        visitedNodes = [oneEdge.toNode for oneEdge in visitedEdges.values()]
        viableEdges = [oneEdge for oneEdge in self.edges.values()
                       if not oneEdge.toNode in visitedNodes and oneEdge.toNode != startNode and oneEdge.toNode != endNode]
        # If all nodes are visited, get back to the starting node
        if not viableEdges:
            viableEdges = [oneEdge for oneEdge in self.edges if not oneEdge.toNode in visitedNodes]
        allPheromones = sum([oneEdge.pheromones for oneEdge in viableEdges])
        num = random.uniform(0, allPheromones)
        s = 0
        i = 0
        selectedEdge = viableEdges[0]
        while (s <= num):
            selectedEdge = viableEdges[i]
            s += selectedEdge.pheromones
            i += 1
        return selectedEdge

    def __repr__(self):
        return self.name



class Edge:
    def __init__(self, fromNode, toNode):
        self.fromNode = fromNode
        self.toNode = toNode
        self.key = str(fromNode.name + toNode.name)
        self.cost = fromNode.distance_to(toNode)
        self.pheromones = 1

    def __repr__(self):
        return self.fromNode.name + "--(" + str(self.cost) + ")--" + self.toNode.name

    def checkPheromones(self):
        if(self.pheromones>MAXPHEROMONES):
            self.pheromones = MAXPHEROMONES
        if(self.pheromones<MINPHEROMONES):
            self.pheromones = MINPHEROMONES

class ANT:
    def __init__(self, ):
        self.visitedEdges = {}

    def walk(self,  startNode: Node, endNode: Node, nodesToVisit: int):
        """
        Walks from 'startNode', visits an amount of nodes equal to 'nodesToVisit', then walks to endNode
        The graph defines the network of nodes in witch the ant will walk.
        """
        currentNode = startNode
        while (len(self.visitedEdges) < nodesToVisit ):
            #Choose next edge to travel
            currentEdge = currentNode.rouletteWheel(self.visitedEdges, startNode, endNode)
            currentNode = currentEdge.toNode
            self.visitedEdges[currentEdge.key] = currentEdge

        last_edge_key = str(currentNode.name + endNode.name)
        n = allEdges[last_edge_key]



### HARD KODA TING ###
nodes_example = {
    'node1': Node('node1', (-89.456, 50.726)),
    'node2': Node('node2', (-50.000, -40.543)),
    'node3': Node('node3', (10.435, -10.685)),
    'node4': Node('node4', (60.124, 60.478)),
    'node5': Node('node5', (90.096, -60.729)),
    'node6': Node('node6', (2, -88.789)),
    'node7': Node('node7', (-5.111, -47.426)),
    'node8': Node('node8', (-76.824, -99.009)),
    'node9': Node('node9', (-2.131, 2.858)),
    'node10': Node('node10', (25.959, 88.903))
}

edges_example = {
    'node1node2': Edge(nodes_example['node1'], nodes_example['node2'])
}
### "Main" - aka. run the algorithm ###

allNodes = nodes_example
allEdges = {}

#Assign edges between all nodes

def run(n):
    for fromNode in allNodes.values():
        for toNode in allNodes.values():
            if toNode != fromNode:
                eddie = Edge(fromNode, toNode)
                key = str(fromNode.name + toNode.name)
                print(key)
                fromNode.edges[key] = eddie
                allEdges[key] = eddie

    for i in range(10):
        annie = ANT()
        annie.walk(nodes_example['node1'], nodes_example['node10'], n)

run(8)






