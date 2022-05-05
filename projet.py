import copy

import sys

if(len(sys.argv) != 1):
    PATH_GRAPH = "./graphes/ucidata-zachary/dataset1"
else:
    PATH_GRAPH = sys.argv[1]

# A graph is an object that only contains an array of edges : 
class Graph:
    def __init__(self):
        self.edges = []

    # String allowing to print the graph
    def __str__(self):
        res=""
        for edge in self.edges:
            res+=str(edge)+"\n"
        return res
    
    # Returns the amount of vertices
    def __len__(self):
        unique = []
        for edge in self.edges:
            for vertex in edge:
                if vertex not in unique:
                    unique.append(vertex)
        return len(unique)

    # Lists all vertices
    def listVertices(self):
        unique = []
        for edge in self.edges:
            for vertex in edge:
                if vertex not in unique:
                    unique.append(vertex)
        return unique
    
    # Returns an array containing the degree of each vertex
    # Ex : index = 0, value = 4 mean the first vertex has a degree of 4
    def degreeByVertex(self):
        degrees = []
        vertices = self.listVertices()
        for vertex in vertices:
            degrees.append(self.degree(vertex))
        return degrees
                
    # Adds one edge with the value v
    def addEdge(self,v):
        self.edges.append(v)

    # Return all v neighbours
    def neighbours(self,v):
        neighbours = []
        for edge in self.edges:
            if edge[0] == v:
                neighbours.append(edge[1])
            elif edge[1] == v:
                neighbours.append(edge[0])
        return neighbours
    
    #  Remove edge with the value v
    def remove(self,v):
        delete = []
        for edge in self.edges:
            if edge[0] == v or edge[1] == v:
                delete.append(edge)
        for edge in delete:
            self.edges.remove(edge)

    # Return degree of vertex v
    def degree(self,v):
        return len(self.neighbours(v))

    # Degeneracy algorithm as seen in class
    def degeneracy(self):
        k = 0
        g = copy.deepcopy(self)
        vertices = g.listVertices()
        centres = {}
        
        while(len(g) > 0 and k < 500):
            rec = True
            k = k+1
            centres[k] = []
            while rec is True:
                rec = False
                for vertex in vertices:
                    if g.degree(vertex) <= k:
                        g.remove(vertex)
                        vertices.remove(vertex)
                        centres[k].append(vertex)
                        rec = True    
        return (k,centres)
    
    # At the end of the algorithm, any vertex L[i] will have at most k edges
    def matulaBeckDegeneracy(self):
        # https://en.wikipedia.org/wiki/Degeneracy_(graph_theory)#Algorithms
        # https://schulzchristian.github.io/thesis/thesis_huebner.pdf Page 16
        L = []
        d = self.degreeByVertex()
        D = self.getBucketPriorityQueue(d)
        k = 0
        i = 0
        for _ in range(0,len(d)):
            i = twoDimArrayIndexHelper(D)
            k = max(k,i)
            v = D[i].pop(0)
            L.insert(0,v)
            for neighbour in self.neighbours(v):
                if neighbour not in L:
                    indexNeighbour = neighbour-1 # neighbour-1 because array don't start at 1. So vertex number 4 is located at index 3 
                    D[d[indexNeighbour]].remove(neighbour)
                    d[indexNeighbour]-=1
                    D[d[indexNeighbour]].append(neighbour)
        return (k,L)

    # Puts vertex of degree i in D[i] 
    def getBucketPriorityQueue(self, degreeByVertex):
        D = []
        for i in range(max(degreeByVertex)+1) :
            D.append([])
        vertex = 1
        for degree in degreeByVertex:
            D[degree].append(vertex)
            vertex+=1
        print("\n\n",degreeByVertex,"\n\n",D,"\n\n")
        return D    


    #DSATUR 


    def dsatur(self):
        maxColor = -1
        verticesLength = len(self)

        DSAT = [0] * verticesLength
        vertexColor = [-1] * verticesLength

        counter = 0
        while(counter < verticesLength) :
            dsatVertex = self.dsaturGetVertex(DSAT,vertexColor,verticesLength)
            color = self.dsaturGetColor(DSAT, vertexColor, verticesLength, dsatVertex)
            
            vertexColor[dsatVertex-1] = color
            if color > maxColor :
               maxColor = color

            counter+=1
        return (maxColor+1,vertexColor)
    
    def dsaturGetVertex(self, DSAT, vertexColor, verticesLength):
        dsatVertex = 0
        dsatDegree = 0
        dsatMax = -1
        for vertex in range(1,verticesLength+1) :
            vertexIndex = vertex - 1
            if vertexColor[vertexIndex] == -1 :
                if DSAT[vertexIndex] > dsatMax :
                    dsatMax = DSAT[vertexIndex]
                    dsatVertex = vertex
                    dsatDegree = self.degree(vertex)
                elif DSAT[vertexIndex] == dsatMax :
                    currentDegree = self.degree(vertex)
                    if currentDegree > dsatDegree :
                        dsatDegree = currentDegree
                        dsatVertex = vertex
        return dsatVertex    

    def dsaturGetColor(self, DSAT, vertexColor, verticesLength, dsatVertex):
        colorIsUsed = [False] * verticesLength

        neighbours = self.neighbours(dsatVertex)
        for neighbour in neighbours :
            neighbourIndex = neighbour - 1
            if vertexColor[neighbourIndex] != -1:
                colorIsUsed[vertexColor[neighbourIndex]] = True
                DSAT[neighbourIndex]+=1

        color = 0
        while colorIsUsed[color] :
            color+=1
        return color

    
# Return the index of the first array which is not empty inside of a two dim array
# Ex : [[],[],[5],[5,6,7]] return 2
# Ex : [[]] return -1
def twoDimArrayIndexHelper(twoDimArray):
    index = 0
    empty = True
    while(empty):
        empty = len(twoDimArray[index]) == 0
        index+=1
    index-=1
    if empty:
        return -1
    else:
        return index

# Reads from a file and makes a graph object out of it.
def readGraph(path):
    g = Graph()
    file = open(path,"r")
    lines = file.readlines()
    g.vertices = int(lines[1].split()[3])
    for line in lines:
        if line[0] != "%":
            g.addEdge([int(i) for i in line.split()])
    return g

z = readGraph(PATH_GRAPH)
e= [[1,2],[1,3],[3,4],[2,3]]
g = Graph()
g.edges = e
print(str(g))
print("voisin:",g.neighbours(1))

(degen,centres) = z.degeneracy()
print("Degenerancy :",str(degen))
print("Centres :",centres)
(degenMB,verticesMB) = z.matulaBeckDegeneracy()
print("Matula & Beck degenerancy :",degenMB,"\nMatula & Beck output vertices :",verticesMB)
(chromaticNb,colors) = z.dsatur()
print("Nombre chromatique :",chromaticNb,"\nCouleurs :",colors)
if(len(sys.argv) > 0):
    print("argument : ",sys.argv[1])