# Tietorakenteet ja algoritmit 2, kevät 2023
# Exercise round 2
# Algorithm to find topological order of DAG. If graph has cycle
# (and thus is not DAG), finds one cycle
# 28.3.2023


import sys
#from graph import Graph
import math


""" Class for graph-objects
Created to use in Data Structures and Algorithms 2 -course, spring 2023

Graph can be weighted or unweighted, directed or undirected.

Vertices and edges can be added and removed.

Graph can be read from .txt-file. If read from file, nodes must be integers and
the file should consist of lines in the following form:
u v w
where u and v are vertices connected by edge and w is the weight of the edge.
"""


class Graph:
    # As default, undirected and weighted graph
    def __init__(self, filename=None, isdirected=False, isweighted=False):
        # if the graph is directed
        self.isdirected = isdirected
        # if the graph is weighted
        self.isweighted = isweighted
        # placeholder for keys to vertices
        self.V = set([])
        # Placeholder for adjacency matrix
        self.AM = {}
        # Dictionary for adjacency lists
        self.AL = {}
        # Dictionary for incoming neighbors
        self.to_AL = {}
        # placeholder for weights. if unweighted, stays always empty
        self.W = {}
        # list for some graph algorithms
        self.visited = [False] * len(self)
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
            txt += " - Nodes: " + ', '.join([str(v) for v in self.V]) + \
                   "\n - Edges: " + ', '.join([str(e) + ": " + str(w)
                                               for e, w in self.W.items()])
        else:
            txt += " - Unweighted\n"
            txt += " - Nodes: " + ', '.join([str(v) for v in self.V]) + \
                   "\n - Edges: " + ', '.join([str(e) for e in self.W.keys()])

        return txt

    def __len__(self):
        return len(self.V)

    def __getitem__(self, v):
        return self.adj(v)

    # returns amount of vertices and edges
    def size(self):
        if self.isdirected:
            return len(self.V), len(self.W)
        return len(self.V), len(self.W)/2

    def has_vertices(self, vlist):
        notnodes = []
        for v in vlist:
            if v not in self.V:
                notnodes.append(str(v))
        if notnodes:
            print("ERROR!!! The following vertices do not exist: " +
                  ", ".join(notnodes))
            return False
        return True

    def has_edges(self, elist):
        notedges = []
        for e in elist:
            if e not in self.W:
                notedges.append(str(e))
        if notedges:
            print("ERROR!!! The following edges do not exist: " +
                  ", ".join(notedges))
            return False
        return True

    def get_adjacency_dict(self):
        return self.AL

    def get_vertex_set(self):
        return self.V

    def get_visited_list(self):
        return self.visited

    def get_weight(self, u, v):
        return self.W[(u, v)]

    def adj(self, u):
        return self.AL[u]

    def to_adj(self, u):
        return self.to_AL[u]

    def is_adj(self, u, v):
        return v in self.AL[u]

    def add_vertex(self, k):
        # Adding already existing node doesn't change anything
        if k in self.V:
            return
        # Add an element to the vertex set and create adjacency lists
        self.AL[k] = []
        self.to_AL[k] = []
        self.V.add(k)

        return True

    # for unweighted graph the weights are marked as None
    def add_edge(self, u, v, w=None):
        # if u or v is not a vertex, they are added before edge creation
        # actually it doesn't matter because you can try to add new vertex
        # even though if exists already
        self.add_vertex(u)
        self.add_vertex(v)

        # if edge already exists, don't change anything
        # this ain't no multigraph
        if (u, v) in self.W:
            print("Edge between nodes " + str(u) + " and " + str(v) +
                  " already exists!!!")
            return False

        # Adjacency lists updated
        self.AL[u].append(v)
        self.to_AL[v].append(u)

        # if graph is not directed, neighboring works both ways
        if not self.isdirected:
            self.AL[v].append(u)
            self.to_AL[u].append(v)

        # Adjust the weight
        self.W[(u, v)] = w
        # the other direction also
        if not self.isdirected:
            self.W[(v, u)] = w

        return True

    # Removing node removes it and all edges connected to it from the graph
    def remove_vertex(self, toremove):

        # If the node doesn't exist
        if not self.has_vertices([toremove]):
            return False

        # First removing edges connecting to toremove
        edges_toremove = []
        for e in self.W.keys():
            if e[0] == toremove or e[1] == toremove:
                edges_toremove.append(e)
        for e in edges_toremove:
            self.remove_edge(e[0], e[1])

        # Actually removing the node
        self.AL.pop(toremove)
        self.to_AL.pop(toremove)
        self.V.remove(toremove)

        return True

    # Removing edge removes only the edge between nodes u and v. The nodes
    # themselves stay as they are
    def remove_edge(self, u, v):

        # If either of the nodes don't exist
        if not self.has_vertices([u, v]):
            return False
        # If edge doesn't exist
        if not self.has_edges([(u, v)]):
            return False

        # Remove from Wdict and adjacency lists
        self.W.pop((u, v))
        self.AL[u].remove(v)
        self.to_AL[v].remove(u)

        if not self.isdirected:
            self.W.pop((v, u))
            self.AL[v].remove(u)
            self.to_AL[u].remove(v)

        return True

    def read_graph_file(self, filename):
        try:
            f = open(filename, 'r')
        except OSError:
            print("Can't open the file!")
            return

        for line in f:
            # Splitting and rstripping into list
            e = line.rstrip().split(' ')

            # To ints and adding edge
            e = [int(i) for i in e]
            if self.isweighted:
                self.add_edge(e[0], e[1], e[2])
            else:
                self.add_edge(e[0], e[1])

        return True



# This is modified from the Bellman-Ford algorithm task
def find_cycle(g):
    vset = g.get_vertex_set()
    # Adding previous nodes to dict for easier usage
    prev = {}
    for v in vset:
        prev[v] = min(g.to_adj(v))

    s = min(vset)
    cycle = [s]
    v = s
    # Loop to find the cycle
    while prev[v] not in cycle:
        v = prev[v]
        cycle.append(v)
    v = prev[v]

    # v is now the start (and end) of the cycle
    # Collecting the cycle into list
    cycle = []
    u = v
    while v not in cycle:
        cycle.append(prev[u])
        u = prev[u]
    cycle.reverse()  # Reversing order
    cycle.append(v)  # First also to last element

    return cycle


def topological_sort(g):

    # Look for source nodes
    sources = []
    for v in g.get_vertex_set():
        if not g.to_adj(v):  # empty list, no incoming edges
            sources.append(v)

    ord = []
    # sources should be now non-empty list
    # if it is empty already => jump to find cycle
    while sources:
        sources.sort(reverse=True)
        s = sources.pop()
        ord.append(s)
        adjlist = g.adj(s).copy()
        g.remove_vertex(s)
        for v in adjlist:  # looping through outgoing neighbours
            if not g.to_adj(v):  # empty list, no incoming edges
                sources.append(v)

    # if now the graph is not empty, it is acyclic
    if len(g):  # len non-zero
        cycle = find_cycle(g)
        txt = "The graph is not acyclic, found a cycle: " + \
              " ".join([str(v) for v in cycle])
        print(txt)
        return False

    print("Found a topological order: " + " ".join([str(v) for v in ord]))
    return True


def main():
    #f = sys.argv[1]
    f = "topologicalorder_data/input4.txt"
    g = Graph(filename=f, isdirected=True, isweighted=False)

    topological_sort(g)


main()
