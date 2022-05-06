import utils
import copy
import sys

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
        return len(self.listVertices())

    # Lists all vertices
    def listVertices(self):
        unique = set()
        for edge in self.edges:
            for vertex in edge:
                unique.add(vertex)
        return list(unique)
    
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


    # NAIVE DEGENERACY

    # Degeneracy algorithm as seen in class
    def degeneracy(self):
        k = 0
        g = copy.deepcopy(self)
        vertices = g.listVertices() # Copying the graph. Deleting a vertex = Marking a vertex in the original graph.
        cores = {} # Dictionnary containing K-Cores.
        
        while(len(g) > 0 and k < 300):
            rec = True
            k = k+1
            cores[k] = []
            while rec is True:
                rec = False
                for vertex in vertices:
                    if g.degree(vertex) <= k:
                        g.remove(vertex)
                        vertices.remove(vertex)
                        cores[k].append(vertex)
                        rec = True   

        if k >= 300:
            sys.exit(utils.errorMessage(utils.Error.TOO_MANY_KCORES))

        return (k,cores)
    

    ## MATULA & BECK

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
            i = utils.twoDimArrayIndexHelper(D)
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
        return D

    # Returns all the neighbours of vertex v
    def neighbours(self,v):
        neighbours = []
        for edge in self.edges:
            if edge[0] == v:
                neighbours.append(edge[1])
            elif edge[1] == v:
                neighbours.append(edge[0])
        return neighbours    



    ## DSATUR 

    def dsatur(self):
        maxColor = -1
        verticesLength = len(self)

        DSAT = [0] * verticesLength
        vertexColor = [-1] * verticesLength

        counter = 0
        while(counter < verticesLength) :
            dsatVertex = self.dsaturGetVertex(DSAT,vertexColor)
            color = self.dsaturGetColor(DSAT, vertexColor, dsatVertex)
            
            vertexColor[dsatVertex-1] = color
            if color > maxColor :
               maxColor = color

            counter+=1
        return (maxColor+1,vertexColor)
    
    def dsaturGetVertex(self, DSAT, vertexColor):
        dsatVertex = 0
        dsatDegree = 0
        dsatMax = -1
        for vertex in range(1,len(self)+1) :
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

    def dsaturGetColor(self, DSAT, vertexColor, dsatVertex):
        colorIsUsed = [False] * len(self)

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
