# COMP.CS.350 Data Structures and Algorithms 2, spring 2023
# Exercise round 3: Dinitz' algorithm
# Dinitz' algorithm to find maximum flow of directed weighted graph
# 13.4.2023


import copy
import sys
#from graph import Graph


""" Class for graph-objects.
Created to use in Data Structures and Algorithms 2 -course, spring 2023

Graph can be weighted or unweighted, directed or undirected.

Vertices and edges can be added and removed.

Graph can be read from .txt-file. If read from file, nodes must be integers and
the file should consist of lines in the following form:
u v w
where u and v are vertices connected by edge and w is the weight of the edge.
"""


class Graph:
    # As default, undirected and unweighted graph
    def __init__(self, filename=None, isdirected=False, isweighted=False, weirdinput=False):
        # if the graph is directed
        self.isdirected = isdirected
        # if the graph is weighted
        self.isweighted = isweighted

        self.weirdinput = weirdinput
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
        # for some flow algorithms
        self.sourcenode = None
        self.targetnode = None
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

    def get_sourcenode(self):
        return self.sourcenode

    def get_targetnode(self):
        return self.targetnode

    def get_adjacency_dict(self):
        return self.AL

    def get_adjacency_matrix(self):
        return self.AM

    def get_vertex_set(self):
        return self.V

    def get_visited_list(self):
        return self.visited

    def get_weight(self, u, v):
        return self.W[(u, v)]

    def get_weight_dict(self):
        return self.W

    def adj(self, u):
        return self.AL[u]

    def to_adj(self, u):
        return self.to_AL[u]

    def is_adj(self, u, v):
        return v in self.AL[u]

    def add_vertex(self, k):
        # Adding already existing node doesn't change anything
        if k in self.V:
            return False
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

    # changes edge weight between u and v. if no such edge, does nothing
    def change_weight(self, u, v, new_w):

        if not self.has_edges([(u, v)]):
            return False
        self.W[(u, v)] = new_w

        if not self.isdirected:
            self.W[(v, u)] = new_w

        return True

    # This is original read_graph_file -method, below is worse but needed
    # version for weird input data
    """
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

        f.close()

        return True
    """

    def read_graph_file(self, filename):
        try:
            f = open(filename, 'r')
        except OSError:
            print("Can't open the file!")
            return

        linenum = 0
        for line in f:
            linenum += 1

            if self.weirdinput and linenum == 1:
                # 1. row
                st = line.rstrip().split(' ')
                self.sourcenode = int(st[0])
                self.targetnode = int(st[1])

            else:
                # Splitting and rstripping into list
                e = line.rstrip().split(' ')

                # To ints and adding edge
                e = [int(i) for i in e]
                if self.isweighted:
                    self.add_edge(e[0], e[1], e[2])
                else:
                    self.add_edge(e[0], e[1])

        f.close()

        return True


# function to read weird input files of this dinitz task. Later implemented
# straight into graph class method
def handle_weird_input_file(filename, newfilename):
    """
    The input file here is annoingly different than in the previous tasks: first
    line is in the form s t where s is the source node and t is the sink node of
    flow graph. Thus read_graph_file -method implemented in Graph-class cannot
    handle these input files. In order to overcome this issue, we create this separate
    function to remove the first line of the file and save these as source and sink
    nodes.
    :return: source node s, sink (target) node t
    """
    s, t = 0, 0

    with open(filename, 'r') as f:
        lines = f.readlines()

        # 1. row
        st = lines[0].rstrip().split(' ')
        s = int(st[0])
        t = int(st[1])

    # Creating new file to store the actual graph if the file doesn't already
    # exist. If it does, this overwrites it.
    with open(newfilename, 'w') as fnew:
        # writing everything except 1. line back
        fnew.writelines(lines[1:])

    return s, t


# Apuprinttaufunktio
def print_levels(g, f, leveld, it):

    print("Edges of the level graph for iteration " + str(it) + ":")
    # Max level, skipping nones
    maxlev = max([v for v in leveld.values() if v is not None])
    lev = 0
    # Looping until max level
    while lev < maxlev:

        print(" level " + str(lev + 1) + ":", end="")
        edges = []  # Edges are collected into list
        for u in sorted(leveld.keys()):

            # Edges connecting to node on level i, source level is 0
            if leveld[u] == lev:
                # Normal edges
                for v in g[u]:
                    if (leveld[v] == lev + 1 and g.get_weight(u, v) >
                            f.get_weight(u, v)):
                        edges.append((u, v))
                # Reverse edges
                for v in g.to_adj(u):
                    if leveld[v] == lev + 1 and f.get_weight(v, u) > 0:
                        edges.append((v, u))

        edges = sorted(edges)
        for e in edges:
            print(" " + str(e[0]) + "-" + str(e[1]), end="")

        lev += 1
        print()

    return True


# Steps printing helper function
def print_dfs_steps(g, f, prevd, s, u):

    # Normal edge
    if g.is_adj(prevd[u], u):
        freecapa = g.get_weight(prevd[u], u) - f.get_weight(prevd[u], u)
        print("DFS steps from", prevd[u], "to", u,
              "with available capacity", freecapa)

    # Reverse edge
    elif g.is_adj(u, prevd[u]):
        freecapa = f.get_weight(u, prevd[u])
        print("DFS steps from " + str(prevd[u]) + " to " + str(u) +
              " with available reverse capacity " + str(freecapa))


# Path printing helper function
def print_path(bneck, path):
    print("Found a path with capacity " + str(bneck) + ": " + " ".join(
        [str(v) for v in path]))


# Helper function for dfs
def add_aug_path(g, f, prevd, t, bneck):

    # finding bottleneck flow, adding nodes on path to list
    path = [t]
    v = t
    while prevd[v] is not None:

        # Normal edge case
        if (prevd[v], v) in g.get_weight_dict():
            freecapa = g.get_weight(prevd[v], v) - f.get_weight(prevd[v], v)
            bneck = min(bneck, freecapa)
            v = prevd[v]
            path.append(v)

        # Reverse edge
        else:
            freecapa = f.get_weight(v, prevd[v])
            bneck = min(bneck, freecapa)
            v = prevd[v]
            path.append(v)

    # adding bottleneck flow to f's edge weights OR substracting it in
    # reverse edge case
    v = t
    while prevd[v] is not None:

        # Normal edge case
        if (prevd[v], v) in g.get_weight_dict():
            f.change_weight(prevd[v], v, f.get_weight(prevd[v], v) + bneck)
            v = prevd[v]

        # Reverse edge
        else:
            f.change_weight(v, prevd[v], f.get_weight(v, prevd[v]) - bneck)
            v = prevd[v]

    path.reverse()
    print_path(bneck, path)

    # Only modified thing is the flow graph
    return f


def bfs(g, f, s, t):
    """
    Derives the current level graph from BFS. Finds only nodes that are
    connected to source via forward edges with capacity left OR reverse edges
    with flow
    :param g: original graph or capacity graph
    :param f: current flow graph
    :param s: source node
    :param t: target node, only used to stop looping
    :return: levels of the nodes in dict, source is 0 and unfound nodes are not
    in the dict
    """
    queue = [s]
    # initialize levels to dict
    leveld = {v: None for v in g.get_vertex_set()}
    leveld[s] = 0    # source is at level 0
    while queue:
        u = queue.pop(0)

        # Tämä on paska tapa... menee läpi myös 5. testidatalla, mutta on
        # epäloogista. Miksei leveleitä voisi olla myös sinkistä/targetista
        # eteenpäin???
        if u == t:
            return leveld

        # Add forward edges that have capacity left
        for v in g.adj(u):
            if leveld[v] is None and g.get_weight(u, v) > f.get_weight(u, v):
                leveld[v] = leveld[u] + 1
                queue.append(v)

        # Add reverse edges that have flow
        for v in g.to_adj(u):
            if leveld[v] is None and f.get_weight(v, u) > 0:
                leveld[v] = leveld[u] + 1
                queue.append(v)

    return leveld


def dfs(g, f, leveld, s, t):

    invalid = {v: False for v in g.get_vertex_set()}
    stack = [s]

    # Making bottleneck big enough
    bneck = 0
    for w in g.get_weight_dict().values():
        bneck += w

    # This collects the previous node in dfs path
    prevd = {s: None}
    backtracked = False

    while stack:

        # Remove from main dfs stack
        u = stack.pop()

        toadd = []  # list for nodes to add into main stack later

        if not backtracked and u != s:
            print_dfs_steps(g, f, prevd, s, u)

        backtracked = False  # As default, false

        # If target has been found
        if u == t:
            f = add_aug_path(g, f, prevd, t, bneck)
            # Starting dfs again from the source node
            stack = [s]
            prevd = {s: None}

        # Most of the cases lead under this condition
        elif (any([not invalid[v] and leveld[v] == leveld[u] + 1 and
                   f.get_weight(u, v) < g.get_weight(u, v) for v in g[u]]) or
              any([not invalid[v] and leveld[v] == leveld[u] + 1 and
                   f.get_weight(v, u) > 0 for v in g.to_adj(u)])):

            # Get all adjacent nodes of the popped node
            for v in f[u]:
                fw = f.get_weight(u, v)
                gw = g.get_weight(u, v)
                # go forward if possible
                if (leveld[v] == leveld[u] + 1) and (fw < gw) and (not invalid[v]):
                    prevd[v] = u
                    toadd.append(v)

            # Same to reverse edges
            for v in f.to_adj(u):
                fw = f.get_weight(v, u)
                # go forward (in reverse direction) if possible
                if ((leveld[v] == leveld[u] + 1) and (fw > 0)
                        and (not invalid[v])):
                    prevd[v] = u
                    toadd.append(v)

        # No valid neighbors and not a target node
        else:
            backtracked = True
            if u == s:
                # Backtracked into source node. This ends the whole while-loop
                stack = []
                print()
            else:
                # Can't go forward so backtrack: Make current invalid and
                # add previous node back to main stack
                stack.append(prevd[u])
                invalid[u] = True
                print("DFS backtracks from " + str(u) + " to " + str(prevd[u]))

        # Adding neighboring nodes (if any)
        if toadd:
            toadd.sort(reverse=True)
            for v in toadd:
                stack.append(v)

    # The only relevant modified thing
    return f


def maxflow(g, s, t):

    # initialize flow graph f: all weights to 0
    f = copy.deepcopy(g)

    # Changing all f's weights to 0
    for u in f.get_vertex_set():
        neighs = f[u].copy()
        for v in neighs:
            f.change_weight(u, v, 0)

    it = 0
    leveld = bfs(g, f, s, t)
    # bfs returns dict of levels, t is None if it wasn't found
    while leveld[t]:
        it += 1
        print_levels(g, f, leveld, it)
        f = dfs(g, f, leveld, s, t)
        leveld = bfs(g, f, s, t)

    # Maximum flow from graph f
    flow = 0
    for v in f.to_adj(t):
        flow += f.get_weight(v, t)

    return flow


def main():

    #f = sys.argv[1]
    f = "dinitz_data/input1.txt"
    g = Graph(filename=f, isweighted=True, isdirected=True, weirdinput=True)

    s = g.get_sourcenode()
    t = g.get_targetnode()

    maxf = maxflow(g, s, t)
    print("Maximum flow: " + str(maxf))


main()
