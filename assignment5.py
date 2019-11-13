import random
MAXPHEROMONES = 100000
MINPHEROMONES = 1

bestScore = 0
bestSolution = []

class Node:
    def __init__(self,name):
        self.name = name
        self.edges = []

    def roluetteWheelSimple(self):
        return random.sample(self.edges,1)[0]

    def rouletteWheel(self,visitedEdges,startNode):
        visitedNodes = [oneEdge.toNode for oneEdge in visitedEdges]
        viableEdges = [oneEdge for oneEdge in self.edges if not oneEdge.toNode in visitedNodes and oneEdge.toNode!=startNode]
        #If all nodes are visited, get back to the starting node
        if not viableEdges: 
               viableEdges = [oneEdge for oneEdge in self.edges if not oneEdge.toNode in visitedNodes]
        allPheromones = sum([oneEdge.pheromones for oneEdge in viableEdges])
        num = random.uniform(0,allPheromones)
        s = 0
        i = 0
        selectedEdge = viableEdges[0]
        while(s<=num):
            selectedEdge = viableEdges[i]
            s += selectedEdge.pheromones
            i += 1
        return selectedEdge

    def __repr__(self):
        return self.name

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

a = Node("A")
b = Node("B")
c = Node("C")
d = Node("D")
e = Node("E")

nodes = [a,b,c,d,e]

edges = [
   Edge(a,b,100),
   Edge(a,c,175),
   Edge(a,d,100),
   Edge(a,e,75),
   Edge(b,c,50),
   Edge(b,d,75),
   Edge(b,e,125),
   Edge(c,d,100),
   Edge(c,e,125),
   Edge(d,e,75)]


#Make symetrical
for oneEdge in edges[:]:
   edges.append(Edge(oneEdge.toNode,oneEdge.fromNode,oneEdge.cost))

#Assign to nodes
for oneEdge in edges:
    for oneNode in nodes:
        if(oneEdge.fromNode==oneNode):
            oneNode.edges.append(oneEdge)

def checkAllNodesPresent(edges):
    visitedNodes = [edge.toNode for edge in edges]
    return set(nodes).issubset(visitedNodes) #Checks that all the nodes is a subset of the visited which is the same as checking if all the nodes is the same as the visited

print(edges)

#Part of the cost function
def getSum(edges):
    return sum(e.cost for e in edges)

MAXCOST = getSum(edges)

class ANT:
    def __init__(self):
        self.visitedEdges = []

    #Walks to an unvisited node
    def walk(self,startNode):
        currentNode = startNode
        currentEdge = None
        while(not checkAllNodesPresent(self.visitedEdges)):
            currentEdge = currentNode.rouletteWheel(self.visitedEdges,startNode)
            #currentEdge = currentNode.roluetteWheelSimple()
            currentNode = currentEdge.toNode
            self.visitedEdges.append(currentEdge)

    def pheromonesWitoutMMAS(self):
        currentCost = getSum(self.visitedEdges)
        #Score
        score = 10**(1-float(currentCost)/MAXCOST)#1
        for oneEdge in self.visitedEdges:
            oneEdge.pheromones += score
    
    def pheromones(self):
        currentCost = getSum(self.visitedEdges)
        #Score
        score = 10**(1-float(currentCost)/MAXCOST)#1
        global bestScore
        global bestSolution
        if(score>bestScore):
            bestScore = score
            bestSolution = self.visitedEdges

        for oneEdge in bestSolution:#self.visitedEdges:
            oneEdge.pheromones += score

for i in range(100000):
    evaporation(edges)
    ant = ANT()
    ant.walk(a)
    ant.pheromones()
    checkAllEdges(edges)
    print(i,getSum(ant.visitedEdges))
