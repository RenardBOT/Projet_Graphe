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
        delete = []
        for edge in self.edges:
            if edge[0] == v or edge[1] == v:
                delete.append(edge)
        for edge in delete:
            self.edges.remove(edge)


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
            

def readGraph(path):
    g = Graph()
    file = open(path,"r")
    lines = file.readlines()
    g.vertices = int(lines[1].split()[3])
    for line in lines:
        if line[0] != "%":
            g.addEdge([int(i) for i in line.split()])
    return g

#A1 B2 C3 D4 E5 F6 G7 H8 I9 J10
g = readGraph("./ucidata-zachary/dataset1")
z = Graph()
print(len(z))
z.edges = [
    [1,2],
    [1,3],
    [1,4],
    [1,5],
    [1,6],
    [2,7],
    [3,4],
    [3,5],
    [4,6],
    [5,6],
    [5,7],
    [6,7],
    [6,8],
    [6,9],
    [6,10],
    [7,8],
    [8,9]
]
(degen,dic) = z.degeneracy()
print("Degenerancy : "+str(degen))
print("Centres : ")
print(dic)
