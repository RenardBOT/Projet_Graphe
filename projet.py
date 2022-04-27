import copy

class Graph:
    def __init__(self):
        self.edges = []

    def __str__(self):
        res=""
        for edge in self.edges:
            res+=str(edge)+"\n"
        return res
    
    # Return number of vertex
    def __len__(self):
        unique = []
        for edge in self.edges:
            for vertex in edge:
                if vertex not in unique:
                    unique.append(vertex)
        return len(unique)

    # List all vertex
    def listVertices(self):
        unique = []
        for edge in self.edges:
            for vertex in edge:
                if vertex not in unique:
                    unique.append(vertex)
        return unique
    
    # Return an array which contain the degree for each vertex
    # Ex : index = 0, value = 4 mean the first vertex as a degree of 4
    def degreeByVertex(self):
        degrees = []
        vertices = self.listVertices()
        for vertex in vertices:
            degrees.append(self.degree(vertex))
        return degrees
                
    # Add one edge with the value v
    def addEdge(self,v):
        self.edges.append(v)

    # Return all neighbours
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
        for dontCare in range(0,len(d)):
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
    
    def getBucketPriorityQueue(self, degreeByVertex):
        D = []
        for i in range(0,len(self)-1) :
            D.append([])
        vertex = 1
        for degree in degreeByVertex:
            D[degree].append(vertex)
            vertex+=1
        return D     

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

def readGraph(path):
    g = Graph()
    file = open(path,"r")
    lines = file.readlines()
    g.vertices = int(lines[1].split()[3])
    for line in lines:
        if line[0] != "%":
            g.addEdge([int(i) for i in line.split()])
    return g

z = readGraph("./graphes/ucidata-zachary/dataset1")

(degen,dic) = z.degeneracy()
print("Degenerancy :",str(degen))
print("Centres :",dic)
(degenMB,verticesMB) = z.matulaBeckDegeneracy()
print("Matula & Beck degenerancy :",degenMB,"\nMatula & Beck output vertices :",verticesMB)
(chromaticNb,colors) = z.dsatur()
print("Nombre chromatique :",chromaticNb,"\nCouleurs :",colors)