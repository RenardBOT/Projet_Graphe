import copy

class Graph:
    def __init__(self):
        self.edges = []

    def __str__(self):
        res=""
        for edge in self.edges:
            res+=str(edge)+"\n"
        return res
    
    def __len__(self):
        unique = []
        for edge in self.edges:
            for vertex in edge:
                if vertex not in unique:
                    unique.append(vertex)
        return len(unique)

    def listVertices(self):
        unique = []
        for edge in self.edges:
            for vertex in edge:
                if vertex not in unique:
                    unique.append(vertex)
        return unique
    
    def addEdge(self,v):
        self.edges.append(v)

    def neighbours(self,v):
        neighbours = []
        for edge in self.edges:
            if edge[0] == v:
                neighbours.append(edge[1])
            elif edge[1] == v:
                neighbours.append(edge[0])
        return neighbours
    
    def remove(self,v):
        for edge in self.edges:
            if edge[0] == v or edge[1] == v:
                self.edges.remove(self)


    def degree(self,v):
        return len(self.neighbours(v))


    def degeneracy(self):
        k = 1
        g = copy.deepcopy(self)
        vert = g.listVertices()
        while(len(g) > 0 and k < 500):
            for vertex in vert:
                if g.degree(vertex) <= k:
                    vert.remove(vertex)
                    g.remove(vertex)
            k = k+1
        return k
            

def readGraph(path):
    g = Graph()
    file = open(path,"r")
    lines = file.readlines()
    g.vertices = int(lines[1].split()[3])
    for line in lines:
        if line[0] != "%":
            g.addEdge([int(i) for i in line.split()])
    return g


g = readGraph("./ucidata-zachary/dataset1")

print(g.degeneracy())
