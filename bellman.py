# Tietorakenteet ja algoritmit 2, kevät 2023
# Exercise round 2
# Bellman-Ford algorithm for directed weighted graph
# 27.3.2023


import sys
#from graph import Graph
import math


# Class for graph for tiraka2 course
# Aapo Hetemaa 24.3.2023


# if read from file, nodes must be integers
# file should be in the following form
# u v w
# where u and v are nodes connected by edge and w is edges weight
class Graph:
    # As default, undirected and weighted graph
    def __init__(self, filename=None, isdirected=False, isweighted=False):
        # if the graph is directed
        self.isdirected = isdirected
        # if the graph is weighted
        self.isweighted = isweighted
        # placeholder for keys to vertices
        self.V = set([])
        # number of vertices
        self.nV = 0
        # number of edges
        self.nE = 0
        # Placeholder for adjacency matrix
        self.AM = {}
        # Dictionary for adjacency lists
        self.AL = {}
        # Dictionary for incoming neighbors
        self.to_AL = {}
        # placeholder for weights. if unweighted, stays always empty
        self.W = {}
        # list for some graph algorithms
        self.visited = [False] * self.nV
        # Reading graph from file
        if filename:
            self.read_graph_file(filename)

    # Printing graph prints its nodes and edges
    def __str__(self):
        txt = "Graph-object:\n"
        if self.isdirected:
            txt += " - Directed\n"
        else:
            txt += " - Undirected\n"
        if self.isweighted:
            txt += " - Weighted\n"
        else:
            txt += " - Unweighted\n"
        txt += " - Nodes: " + ', '.join([str(v) for v in self.V]) + \
               "\n - Edges: " + ', '.join([str(e) + ": " + str(w) for e, w in
                                           self.W.items()])
        return txt

    def __len__(self):
        return len(self.V)

    def __getitem__(self, v):
        return self.adj(v)

    def get_adjacency_dict(self):
        return self.AL

    def get_vertex_set(self):
        return self.V

    def get_visited_list(self):
        return self.visited

    def get_weight(self, u, v):
        return self.W[(u, v)]

    def add_vertex(self, k):
        # Adding already existing node doesn't change anything
        if k in self.V:
            return
        # Add an element to the vertex set
        self.AL[k] = []
        self.to_AL[k] = []
        self.V.add(k)
        self.nV += 1

    def add_edge(self, u, v, w=None):
        # if u or v is not a vertex, they are added before edge creation
        # actually it doesn't matter because you can try to add new vertex
        # even though if exists already
        self.add_vertex(u)
        self.add_vertex(v)
        self.nE += 1

        # Adjacency lists updated
        self.AL[u].append(v)
        self.to_AL[v].append(u)

        # if graph is not directed, neighboring works both ways
        if not self.isdirected:
            self.AL[v].append(u)
            self.to_AL[u].append(v)

        # Adjust the weight
        if self.isweighted:  # is not None and self.isweighted:
            self.W[(u, v)] = w
            # the other direction also
            if not self.isdirected:
                self.W[(v, u)] = w

        # Marking weight as 1
        # elif not self.isweighted:
        #    self.W[(u, v)] = 1
        #    # again if graph is not directed, neighboring works both ways
        #    self.W[(v, u)] = 1

    def adj(self, u):
        return self.AL[u]

    def to_adj(self, u):
        return self.to_AL[u]

    def is_adj(self, u, v):
        return v in self.AL[u]

    def read_graph_file(self, filename):
        try:
            f = open(filename, 'r')
        except OSError:
            print("Can't open the file!")
            return

        for line in f:
            # Splitting and rstripping into list
            e = line.rstrip().split(' ')

            # To ints
            e = [int(i) for i in e]
            self.add_edge(e[0], e[1], e[2])

            # Creating edge so that the smaller node is the first
            # if u < v:
            #    self.add_edge(u, v, w)
            # else:
            #    self.add_edge(v, u, w)


def find_neg_cycle(g, prev, changed):
    v = min(changed)
    cycle = [v]
    # Loop to find the cycle
    while prev[v] not in cycle:
        v = prev[v]
        cycle.append(v)
    v = prev[v]

    # v is now the start (and end) of the cycle
    # # Collecting the cycle into list
    cycle = []
    cost = 0
    u = v
    while v not in cycle:
        cycle.append(prev[u])
        cost += g.get_weight(prev[u], u)
        u = prev[u]
    cycle.reverse()  # Reversing order
    cycle.append(v)  # First also to last element

    txt = "A negative cycle with cost " + str(cost) + " detected: "
    txt += " ".join([str(v) for v in cycle])
    print(txt)
    return False


def print_changes(it, d, changed):
    changed.sort()
    t = "Improvements in iteration " + str(it) + ": "
    for u in changed:
        t += "d(" + str(u) + ") = " + str(d[u]) + ", "
    t = t.rstrip(", ")
    print(t)
    return True


def print_outputs(s, it, d):

    print("No improvements in iteration " + str(it))
    txt = "Distances from " + str(s) + ": "
    for v in sorted(d.keys()):
        if d[v] == math.inf:
            txt += "d(" + str(v) + ") = INF, "
        else:
            txt += "d(" + str(v) + ") = " + str(d[v]) + ", "
    txt = txt.rstrip(", ")
    print(txt)
    return True



def bellmanford(g, s):

    d = {}
    prev = {}
    for v in g.get_vertex_set():
        d[v] = math.inf
        prev[v] = None
    d[s] = 0
    changed = [s]

    it = 0
    while changed:  # list is considered false if it is empty
        it += 1
        nextchanged = []

        for v in changed:

            for u in g[v]:
                prevd = d[u]
                d[u] = min(d[u], d[v] + g.get_weight(v, u))
                if d[u] < prevd:
                    prev[u] = v
                    # There can be situation that u is already changed from other v...
                    # in that case don't append it again
                    if u not in nextchanged:
                        nextchanged.append(u)

        changed = nextchanged
        if changed:
            print_changes(it, d, changed)
            # Checking for negative cycle after n th (amount of nodes) iteration
            # n - 1 is the maximum of needed iterations
            if it == len(g):
                find_neg_cycle(g, prev, changed)
                return False

    print_outputs(s, it, d)

    return True


def main():
    #f = sys.argv[1]
    #s = int(sys.argv[2])
    f = "bellmanford_data/ex3_input6.txt"
    s = 12
    g = Graph(filename=f, isweighted=True, isdirected=True)
    bellmanford(g, s)


main()


