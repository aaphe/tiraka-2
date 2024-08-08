# COMP.CS.350 Data Structures and Algorithms 2, spring 2023
# Exercise round 6: Aho-Corasick algorithm
#
# 4.5.2023

import sys
import copy
from queue import PriorityQueue

""" Class for ACTrie -data structure. The class is mainly modified from the graph
class implementation and the original Trie-class. Mainly the methods reading text file are modified. In the
trie-graph, chars of the strings are stored as edges between vertices. The trie-
graph is actually a tree with rootnode 0. Most of the original graph class
methods are not meaningful in the trie context.
"""
class Trie:
    # As default, undirected and unweighted graph
    def __init__(self, filename=None, isdirected=True, isweighted=True, isACTrie=False):

        # Contains the original strings given to trie
        self.ogstrings = []
        # For each key (nodename) contains list of string indices going
        # through the node
        self.strings_in_node = {}
        self.rootname = 0
        # if the graph is directed
        self.isdirected = isdirected
        # if the graph is weighted
        self.isweighted = isweighted
        # placeholder for keys to vertices
        self.V = set([])
        # Dictionary for adjacency lists
        self.AL = {}
        # This is for trie; keeps the AL ordered with char (weight)
        self.orderedAL = {}
        # Dictionary for incoming neighbors
        self.to_AL = {}
        # placeholder for weights. if unweighted, stays always empty
        self.W = {}
        self.add_vertex(self.rootname)
        # Reading graph from file
        if filename and not isACTrie:
            self.read_trie_file(filename)

        # This is for ACTrie
        self.string_to_process = ""
        self.fac = {}
        if isACTrie and filename:
            self.read_actrie_file(filename)


    def __str__(self):
        s = "Trie levels:\n"
        level = [self.rootname]
        nextlev = []
        i = 1
        while level:
            s += " level " + str(i) + ": "
            for v in level:
                for c, u in self.orderedAL[v]:
                    s += "(" + str(v) + "-" + str(u) + ", " + c + ") "
                    nextlev.append(u)
            level = nextlev
            level = sorted(level)
            nextlev = []
            s = s.rstrip()
            s += "\n"
            i += 1

        s = s[:s.rfind('\n')]
        s = s[:s.rfind('\n')]
        return s

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
        self.orderedAL[k] = []
        self.strings_in_node[k] = []

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

        # Ordered updated
        self.orderedAL[u].append((w, v))

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

    def insert_string(self, s, ind):
        self.ogstrings.append(s)
        v = self.rootname
        for char in s:
            #print(char)
            found = False
            for u in self.adj(v):
                if self.W[(v, u)] == char:
                    found = True
                    self.strings_in_node[u].append(ind)
                    v = u
                    break

            if not found:
                u = len(self)
                self.add_vertex(u)
                self.add_edge(v, u, char)
                self.strings_in_node[u].append(ind)
                v = u

        # Ordering all
        for v in self.V:
            self.orderedAL[v] = sorted(self.orderedAL[v], key=lambda tup: tup[0])

    def read_trie_file(self, filename):

        with open(filename, 'r') as f:
            ind = 1
            for line in f:
                self.insert_string(line.rstrip(), ind)
                ind += 1

        return True

    def read_actrie_file(self, filename):

        with open(filename, 'r') as f:
            ind = 0
            for line in f:
                # 1. line is the string T
                if ind == 0:
                    self.string_to_process = line.rstrip()
                else:
                    self.insert_string(line.rstrip(), ind)
                ind += 1

        return True


    def precompute_fac(self):

        r = self.rootname
        self.fac[r] = None

        level = []
        for v in self.adj(r):
            self.fac[v] = r
            for u in self[v]:
                level.append(u)


        while level:
            level = sorted(level)
            nextlevel = []
            for u in level:

                for k in self.adj(u):
                    nextlevel.append(k)
                #"""
                w = self.to_adj(u)[0]   # Only one parent, tree
                v = self.fac[w]

                uin = self.W[(w, u)]

                v_outs = set()
                for k in self.adj(v):
                    v_outs.add(self.W[(v, k)])

                while v is not None and uin not in v_outs:
                    v = self.fac[v]
                    if v is None:
                        break
                    v_outs = set()
                    for k in self.adj(v):
                        v_outs.add(self.W[(v, k)])


                if v is not None:
                    for k in self.adj(v):
                        if self.W[(v, k)] == uin:
                            break
                    self.fac[u] = k
                #if v is not None:
                #    self.fac[u] = k
                else:
                    self.fac[u] = r
                #"""
            #print(level)
            level = nextlevel

        self.print_fac()





    def processText(self):

        string = self.string_to_process
        print()
        print("Processing the text '" + string + "':")
        index = 0
        current = self.rootname
        found = False
        prev = index - 1
        #for i in range(0, len(string)):
        i = 0
        while i < len(string):
            found = False
            if prev < i and i != 0:
                #print(end="")
                print()
                print(" " + string[i] + ": " +  str(current), end="")
            elif prev < i:
                print(" " + string[i] + ": " + str(current), end="")

            prev = i

            for out in self[current]:
                label = self.W[(current, out)]
                if (label == string[i]):
                    print("", out, end="")
                    current = out
                    found = True
                    i += 1
                    break

            if (found == False and self.fac[current] == None):
                prev = i
                i += 1
                continue

            while self.fac[current] != None and found == False:
                current = self.fac[current]
                print("", current, end="")
                for out in self[current]:
                    label = self.W[(current, out)]
                    if (label == string[i]):
                        print("", out, end="")
                        current = out
                        found = True
                        i += 1
                        break

                if found == False and self.fac[current] != None:
                    print(" " + str(self.fac[current]), end="")
                    current = self.fac[current]




    def print_fac(self):

        print("Suffix function:")
        level = [self.rootname]
        i = 0
        while level:
            nextlev = []
            s = " level " + str(i) + ":"
            for v in sorted(level):
                if v == self.rootname:
                    s += " <" + str(v) + ": " + "null" + ">"
                else:
                    s += " <" + str(v) + ": " + str(self.fac[v]) + ">"
                for u in self.adj(v):
                    nextlev.append(u)

            if nextlev:
                level = nextlev
            else:
                break
            i += 1
            print(s)

            if nextlev:
                level = nextlev
            else:
                break

        #s += " level " + str(i) + ":"
        #for v in sorted(level):
        #    s += " <" + str(v) + ": " + str(self.fac[v]) + ">"

        #s = s[:s.rfind('\n')]
        #s = s[:s.rfind('\n')]
        print(s)
        return s



    # Read patterns from file and return in list
    def read_pattern_file(self, filename):

        with open(filename, 'r') as f:
            return [line.rstrip() for line in f]



def main():

    f = "ac_data/input1.txt"

    f = sys.argv[1]
    #p = sys.argv[2]
    t = Trie(f, isdirected=True, isweighted=True, isACTrie=True)
    print(t)
    print()
    #ps = t.read_pattern_file(p)
    #t.find_patterns(ps)

    t.precompute_fac()

    t.processText()
    print()

main()