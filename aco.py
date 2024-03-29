import random
import math
import csv
from pathlib import Path

# JORDA ER FLAT!#

### GLOBALS ###
MAXPHEROMONES = 100000
MINPHEROMONES = 1
MAXCOST = 1500

bestScore = 0
bestSolution = {}


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
        Walks from 'startNode', visits an amount of nodes equal to 'nodesToVisit', then walks
        to endNode. The graph defines the network of nodes in witch the ant will walk.
        """
        currentNode = startNode
        while (len(self.visitedEdges) < nodesToVisit ):
            #Choose next edge to travel
            currentEdge = currentNode.rouletteWheel(self.visitedEdges, startNode, endNode)
            currentNode = currentEdge.toNode
            self.visitedEdges[currentEdge.key] = currentEdge

        last_edge_key = str(currentNode.name + endNode.name)
        self.visitedEdges[last_edge_key] = allEdges[last_edge_key]
    def getSum(self):
        sum = 0
        for e in self.visitedEdges.values():
            sum += e.cost
        print('SUM: ', sum)
        return sum
    def pheromonesWithoutMMAS(self):
        # currentCost = sum(e.cost for e in self.visitedEdges)
        currentCost = self.getSum()
        #Score
        score = 10**(1-float(currentCost)/MAXCOST)
        for oneEdge in self.visitedEdges.values():
            oneEdge.pheromones += score
    def pheromones(self):
        currentCost = self.getSum()
        # Score
        score = 10 ** (1 - float(currentCost) / MAXCOST)  # 1
        global bestScore
        global bestSolution
        if (score > bestScore):
            bestScore = score
            bestSolution = self.visitedEdges

        for oneEdge in bestSolution.values():  # self.visitedEdges:
            oneEdge.pheromones += score


## HARD KODA TING ###
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

# edges_example = {
#     'node1node2': Edge(nodes_example['node1'], nodes_example['node2'])
# }
### Other functions ###

def evaporation():
    for edge in allEdges.values():
        edge.pheromones *= 0.99

### "Main" - aka. run the algorithm ###

def dict_from_cvs_file(startNode, endNode):
    path = Path('position.csv')
    dict = {}

    sNode = None
    eNode = None
    with open(path, mode='r') as infile:
        reader = csv.reader(infile, delimiter=';')
        reader.__next__() #Remove header
        for row in reader:
            if row[0] == startNode:
                sNode = Node(row[0], (int(row[2]),int(row[3])))
            if row[0] == endNode:
                eNode = Node(row[0], (int(row[2]),int(row[3])))

    if sNode == None or eNode == None:
        print('Nodes not found')
        return None

    x = (eNode.coordinate_x + sNode.coordinate_x) / 2
    y = (eNode.coordinate_y + sNode.coordinate_y)/2
    midtpoint = Node('M', (x,y))
    distance_start_end = sNode.distance_to(eNode)*1.1

    with open(path, mode='r') as infile:
        reader = csv.reader(infile, delimiter=';')
        reader.__next__() #Remove header
        for row in reader:
            if row[3] != '':
                n = Node(row[0], (int(row[2]),int(row[3])))
                if midtpoint.distance_to(n) < distance_start_end:
                    print(n)
                    dict[row[0]] = n
    return dict

def make_node_connections():
    for fromNode in allNodes.values():
        for toNode in allNodes.values():
            if toNode != fromNode:
                eddie = Edge(fromNode, toNode)
                key = str(fromNode.name + toNode.name)
                fromNode.edges[key] = eddie
                allEdges[key] = eddie

#allNodes = dict_from_cvs_file('25355', '22477')
allNodes = nodes_example

allEdges = {}
make_node_connections()


def run(startNode, endNode, n_cities):

    for i in range(100):
        evaporation()
        annie = ANT()
        annie.walk(allNodes[startNode], allNodes[endNode], n_cities)
        annie.pheromones()


    print('---------------')
    for e in annie.visitedEdges.values():
        print(e.fromNode, e.pheromones)
    print('node10')
    print(annie.getSum())
    print('---------------')




run('21326', '21341', 8 )






