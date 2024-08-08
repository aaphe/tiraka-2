# COMP.CS.350 Data Structures and Algorithms 2, spring 2023
# Exercise round 5: KMP string matching
# Knuth-Morris-Pratt algorithm to find pattern of characters in a given string
# 25.4.2023


import sys
import copy


def read_string_file(filename):

    with open(filename, 'r') as f:
        p = f.readline().rstrip()
        t = f.readline().rstrip()

    return p, t


def precompute_f(p):

    f = [0] * len(p)
    t = p[1:len(p)]
    i = 0
    j = 0
    while i < len(t):
        while i < len(t) and t[i] == p[j]:
            i += 1
            j += 1
            f[i] = j
        if j > 0:
            j = f[j-1]
        else:
            i += 1

    return f


def kmp(p, t):
    t2 = t.lower()
    p2 = p.lower()
    m = len(p)
    n = len(t)
    print("P: " + p)
    f = precompute_f(p)
    print("Suffix function f: " + " ".join([str(i) for i in f]))
    klist = []
    i, j = 0, 0
    ismatch = False
    matchw = ""

    # !!! T:tä indeksoidaan i:llä, P:tä vastaavasti j:llä!!!
    while i - j <= n - m:
        pos = i - j
        print("P at pos " + str(pos) + " with i = " + str(i) + " and j = " + str(j))
        prevj = j
        previ = i
        while j < m and t2[i] == p2[j]:
            i += 1
            j += 1
            ismatch = True
            matchw += p[j-1]

        if ismatch:
            print("  matched T[" + str(previ) + ".." + str(i-1) + "] = " +
                  t[previ:i] + " = P[" + str(prevj) + ".." + str(j-1) + "] = " +
                  matchw)

        if j == m:
            print("  found an occurrence of P")
            klist.append(i - m)
        else:
            print("  mismatch T[" + str(i) + "] = " + str(t[i]) + " != P[" + str(j) + "] = " + str(p[j]))
        if j > 0:
            print("  updated j from " + str(j) + " to f[" + str(j-1) + "] = " + str(f[j-1]))
            j = f[j - 1]
        else:
            print("  incremented i from " + str(i) + " to " + str(i+1))
            i += 1
        ismatch = False
        matchw = ""

    return klist


def main():

    f = "kmp_data/input3.txt"
    f = sys.argv[1]
    p, t = read_string_file(f)

    kmp(p, t)



main()

