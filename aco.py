import random
import math
MAXPHEROMONES = 100000
MINPHEROMONES = 1
MAXCOST = math.sqrt(200**2 + 200**2)

#Node
 #ANNIKA
#Hardkoda noder
# ANNIKA

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

