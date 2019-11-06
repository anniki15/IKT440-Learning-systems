import random
import math
MAXPHEROMONES = 100000
MINPHEROMONES = 1
MAXCOST = math.sqrt(200**2 + 200**2)

#Node
class Node:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinate_x = coordinates[0]
        self.coordinate_y = coordinates[1]

nodes = {
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

# node1 = Node('node1', nodes['node1'])
# node2 = Node('node2', nodes['node2'])
# node3 = Node('node3', nodes['node3'])
# node4 = Node('node4', nodes['node4'])
# node5 = Node('node5', nodes['node5'])
# node6 = Node('node6', nodes['node6'])
# node7 = Node('node7', nodes['node7'])
# node8 = Node('node8', nodes['node8'])
# node9 = Node('node9', nodes['node9'])
# node10 = Node('node10', nodes['node10'])



# Edge class
class Edge:
   def __init__(self,fromNode,toNode,cost):
        self.fromNode = fromNode
        self.toNode = toNode
        self.cost = cost
        self.pheromones = 1

   def __repr__(self):
       return self.fromNode.name + "--(" + str(self.cost) + ")--" + self.toNode.name

   def checkPheromones(self):
       if(self.pheromones>MAXPHEROMONES):
           self.pheromones = MAXPHEROMONES
       if(self.pheromones<MINPHEROMONES):
           self.pheromones = MINPHEROMONES

def evaporation(egdes):
    for edge in egdes:
        edge.pheromones *= 0.99

def checkAllEdges(edges):
    for edge in edges:
        edge.checkPheromones()


class ANT:
    def __init__(self):
        self.visitedEdges = []

    def walk(self, startNode):
        currentNode = startNode
        currentEdge = None
        while (not checkAllNodesPresent(self.visitedEdges)):
            currentEdge = currentNode.rouletteWheel(self.visitedEdges, startNode)
            # currentEdge = currentNode.roluetteWheelSimple()
            currentNode = currentEdge.toNode
            self.visitedEdges.append(currentEdge)

    def pheromonesWitoutMMAS(self):
        currentCost = getSum(self.visitedEdges)
        # Score
        score = 10 ** (1 - float(currentCost) / MAXCOST)  # 1
        for oneEdge in self.visitedEdges:
            oneEdge.pheromones += score

    def pheromones(self):
        currentCost = getSum(self.visitedEdges)
        # Score
        score = 10 ** (1 - float(currentCost) / MAXCOST)  # 1
        global bestScore
        global bestSolution
        if (score > bestScore):
            bestScore = score
            bestSolution = self.visitedEdges

        for oneEdge in bestSolution:  # self.visitedEdges:
            oneEdge.pheromones += score

edges = {}

