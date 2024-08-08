# COMP.CS.350 Data Structures and Algorithms 2, spring 2023
# Exercise round 4: Segment tree
# Segment tree data structure for summing list of integers
# 19.4.2023

import sys
import copy


class Segtree:

    def __init__(self, filename):

        self.tree = []
        self.intlist = []
        self.off = 0
        self.height = 0
        # Reading segment tree from file
        if filename:
            self.read_integer_file(filename)

    # Size of tree is amount of nodes in it
    def __len__(self):
        return len(self.tree)

    def __str__(self):
        s = "\n"
        s += "Segment tree -object:\n"
        s += " - Numbers in the original array: " + str(len(self.intlist)) +\
            "\n"
        s += " - Size of the tree-array: " + str(len(self)) + "\n"
        s += " - Height of the tree: " + str(self.height) + "\n"
        s += " - In the array value at index 0 is always 0 and it's not " \
             "printed!!!\n"
        s += " - Tree:\n"
        toprint = copy.copy(self.tree)
        # pop first zero
        toprint.pop(0)
        rowlen = 1
        while toprint:
            for j in range(rowlen):
                s += str(toprint[j])
                s += "  "
            del toprint[0:rowlen]
            rowlen = rowlen * 2
            s += "\n"

        return s

    def print_in_task_mode(self):
        s = "Segment tree levels:\n"
        toprint = copy.copy(self.tree)
        # pop first zero
        toprint.pop(0)
        rowlen = 1
        while toprint:
            s += " "
            for j in range(rowlen):
                s += str(toprint[j])
                s += " "
            del toprint[0:rowlen]
            rowlen = rowlen * 2
            s = s.rstrip()
            s += "\n"

        #s = s.rstrip()
        # Alla virheellisen esimerkkitiedoston mukainen tapa
        #s = " ".join([str(i) for i in self.tree])
        print(s)
        return s

    # Updates the whole tree as leaf value is modified
    def update_value(self, ind, val):
        """
        :param ind: index in the original int array (stored in self.intlist(
        :param val: new value of the corresponding index
        :return:
        """
        # Update intlist
        self.intlist[ind] = val
        # Update leaf
        self.tree[ind + self.off] = val

        # Parents
        for i in range(int(len(self.tree) / 2)):
            #print("i: ", i)
            j = len(self.tree) - i * 2 - 1
            #print("j: ", j)
            s = self.tree[j] + self.tree[j - 1]
            ind = j // 2
            self.tree[ind] = s

        return True

    def create_tree(self):

        # Find off a.k.a. array size
        self.off = 1
        self.height = 1
        while self.off < len(self.intlist):
            self.off = self.off * 2
            self.height += 1

        # Initialize to zeros
        self.tree = [0] * 2 * self.off

        # Update all parents when adding new leaf value
        for ind, i in enumerate(self.intlist):
            self.update_value(ind, i)

        return True

    def read_integer_file(self, filename):

        with open(filename, 'r') as f:
            line = f.readline().rstrip().split(' ')
            self.intlist = [int(i) for i in line]

        self.create_tree()
        return True

    def query(self, ind1, ind2):
        print()
        print("Querying interval " + str(ind1) + "..." + str(ind2))

        # Left and right pointers in intlist space=> change to tree-array world
        l = ind1 + self.off
        r = ind2 + self.off

        res = 0
        different_pointers = True
        while different_pointers:

            print("  left and right positions: " + str(l) + " " + str(r))

            # Even index refers to left child, uneven to right
            if l % 2 == 1:    # in root case l == 1 i.e. l % 2 == 1 as well
                print("    updated result from " + str(res) + " to " +
                      str(res + self.tree[l]) + " using S[" + str(l) + "]="
                      + str(self.tree[l]))
                res += self.tree[l]

            if r % 2 == 0:
                print("    updated result from " + str(res) + " to " +
                      str(res + self.tree[r]) + " using S[" + str(r) + "]="
                      + str(self.tree[r]))
                res += self.tree[r]

            # Change pointers
            l = (l + 1) // 2
            r = (r - 1) // 2

            #if l - r == 1 or r - l == 1 or l == r:
            if l >= r:  # Equal or in wrong order
                different_pointers = False

        #  If pointers are same, adding the last node where looping ends
        if l == r:
            print("  left and right positions: " + str(l) + " " + str(r))
            print("    updated result from " + str(res) + " to " +
                  str(res + self.tree[l]) + " using S[" + str(l) + "]="
                  + str(self.tree[l]))
            res += self.tree[l]

        print()
        print("Sum(" + str(ind1) + "..." + str(ind2) + ") = " + str(res))

        return res

    def read_command_file(self, filename):
        with open(filename, 'r') as f:
            # Each command is done separately in the loop
            for line in f:
                #print(self)
                command = line.rstrip().split(' ')
                par1 = int(command[1])
                par2 = int(command[2])
                if command[0] == "query":
                    #res = 0
                    #for i in range(par1+1, par2+1):
                    #    res += self.intlist[i - 1]
                    #    print(res)
                    self.query(par1, par2)

                elif command[0] == "set":
                    print()
                    print("Updating V[" + str(par1) + "] = " + str(par2))
                    self.update_value(par1, par2)

        return True


def main():

    #f = sys.argv[1]
    #c = sys.argv[2]
    f = "segment_tree_data/input1.txt"
    c = "segment_tree_data/commands1.txt"

    seg = Segtree(f)
    #print(seg)

    seg.print_in_task_mode()
    seg.read_command_file(c)


main()


