import sys
from queue import PriorityQueue
from graph_old import Graph

# Class for priority queue,
# contains edges of graph in mode (u, v)

class PQ:
    def __init__(self):
        self.H = []
        self.Index = {}

    def __contains__(self, key):
        if key in self.Index and self.Index[key] > 0:
            return True
        return False

    def is_empty(self):
        return len(self.H) == 0

    def done(self, value):
        if value in self.Index and self.Index[value] < 0:
            return True
        return False

    def push(self, a):
        if a[1] in self:
            self.update(a)
        i = len(self.H)
        self.H.append(a)
        while i > 0:
            j = (i - 1) / 2
            if self.H[j] > a:
                self.H[i] = self.H[j]
                self.H[j] = a
                i = j
            else:
                break
        self.Index[a[1]] = i

    def pop(self):
        togo = self.H[0]
        a = self.H.pop()
        if a == togo:
            self.Index[a[1]] = -1
            return togo
        self.H[0] = a
        i = 0
        while (2 * i + 1) < len(self.H):
            left = 2 * i + 1
            right = 2 * i + 2
            if self.H[left] < a:
                if right >= len(self.H) or self.H[right] > self.H[left]:
                    self.H[i] = self.H[left]
                    self.H[left] = a
                    i = left
                    self.Index[self.H[i][1]] = i
                    continue
            if right < len(self.H) and self.H[right] < a:
                self.H[i] = self.H[right]
                self.H[right] = a
                i = right
                continue
            break
        self.Index[a[1]] = i
        self.Index[togo[1]] = -1
        return togo

    def update(self, a):
        value = a[0]
        oldvalue = self.H[a][0]
        key = a[1]
        i = self.Index[key]
        self.H[i] = a
        # Decrease priority, i.e., move up
        if oldvalue > value:
            while i > 0:
                j = (i - 1) / 2
                if self.H[j] <= a:
                    self.Index[key] = i
                    return
                self.H[i] = self.H[j]
                self.H[j] = a
                i = j
            self.Index[key] = 0
        # Increase priority: Not allowed
        else:
            raise Exception("key value increase not allowed")


# Class for graph
# Currently this doesn't allow directed graphs or graphs with loops

class Graph2:

    def __init__(self, filename=None, isdirected=False, isweighted=True):
        # initialize to empty graph
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
        # placeholder for weights
        self.W = {}
        if filename:
            self.read_graph_file(filename)

    # Printing graph prints its nodes and edges
    def __str__(self):
        return ("Graph-object:\n" + " - Nodes: " + ', '.join([str(v) for v in self.V]) +
                "\n - Edges: " + ', '.join([str(e) + ": " + str(w) for e, w in self.W.items()]))

    def add_vertex(self, k):
        if k in self.V:
            return
        # Add an element to the vertex set
        self.AL[k] = []
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
        # if graph is not directed, neighboring works both ways
        if not self.isdirected:
            self.AL[v].append(u)

        # Adjust the weight
        if w is not None and self.isweighted:
            self.W[(u, v)] = w
            #if not self.isdirected:
                # again if graph is not directed, neighboring works both ways
                #self.W[(v, u)] = w

        # Marking weight as 1
        #elif not self.isweighted:
        #    self.W[(u, v)] = 1
        #    # again if graph is not directed, neighboring works both ways
        #    self.W[(v, u)] = 1

    def adj(self, u):
        return self.AL[u]

    def is_adj(self, u, v):
        return v in self.AL[u]

    def read_graph_file(self, filename):
        f = open(filename, 'r')
        for line in f:

            # Splitting and rstripping into list
            e = line.rstrip().split(' ')

            # To ints
            e = [int(i) for i in e]
            u = e[0]
            v = e[1]
            w = e[2]

            # Creating edge so that the smaller node is the first
            if u < v:
                self.add_edge(u, v, w)
            else:
                self.add_edge(v, u, w)


# The actual Prim algorithm, hardcoded from the task description
def prim(g, s):

    mst = Graph()
    mst.add_vertex(s)
    pq = PriorityQueue()
    for u in g.adj(s):
        # Order check
        if s < u:
            e = (s, u)
        else:
            e = (u, s)
        pq.put((g.get_w(e), e))

    it = 1
    while not pq.empty():
        print("** Iteration " + str(it) + " **")
        it += 1
        we = pq.get()
        w = we[0]
        e = we[1]
        u = e[0]
        v = e[1]
        # Finding which of these is not yet in mst
        if v not in mst.V:
            new = v
            old = u
        elif u not in mst.V:
            new = u
            old = v
        # Both are already seen
        else:
            continue

        # Adding the new edge
        if old < new:
            mst.add_edge(old, new, w)
        else:
            mst.add_edge(new, old, w)

        # Printing order is again important
        if new < old:
            print("Adding the edge (" + str(new) + ", " + str(old) + ", "
                  + str(w) +") with the new node " + str(new))
        else:
            print("Adding the edge (" + str(old) + ", " + str(new) + ", "
                  + str(w) + ") with the new node " + str(new))

        # Adding new neighbors of the new into pq
        for i in g.adj(new):
            if i not in mst.V:
                # This is needed because (new, i) != (i, new) even though graph is undirected
                if new < i:
                    pq.put((g.W[(new, i)], (new, i)))
                else:
                    pq.put((g.W[(i, new)], (i, new)))

    # Calculating total cost
    cost = 0
    for e, w in mst.W.items():
        cost += w
    # Creating edgelist in printable form
    eprint = []
    for e in mst.W.keys():
        eprint.append(e)
    eprint.sort()
    eprint = [str(e[0]) + "-" + str(e[1]) for e in eprint]
    print("MST(" + str(cost) + "): " + " ".join(eprint))

    return mst


def main():
    #filename = sys.argv[1]
    #s = int(sys.argv[2])
    filename = "ex1_input2.txt"
    s = 13
    G = Graph(filename)
    print(G)
    mst = prim(G, s)
    #print(mst)


main()

