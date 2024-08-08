# COMP.CS.350 Data Structures and Algorithms 2, spring 2023
# Exercise round 4: 3-way quicksort for strings
# 3-way quicksort algorithm for sorting list of strings
# 19.4.2023


import sys
import copy

def read_string_file(filename):

    wordlist = []
    with open(filename, 'r') as f:
        for line in f:
            wordlist.append(line.rstrip())

    return wordlist


def quicksort3(wlist):

    print("Original: " + " ".join(wlist))
    #sortwlist = copy.copy(wlist)

    s = 0
    e = len(wlist) - 1
    d = 0
    p = wlist[(s + e) // 2]

    sort_recursive(wlist, s, e, 0)
    print("Sorted: " + " ".join(wlist))
    return wlist


def sort_recursive(wlist, s, e, d):

    if s < e:
        pi = (s + e) // 2
        p = wlist[pi]

        print("Sorting subarray " + str(s) + "..." + str(e) + " with depth " +
              str(d) + " and pivot " + str(p))

        # Swapping
        sv = wlist[s]
        wlist[s] = p
        wlist[pi] = sv

        eqs = s
        eqe = e
        i = s + 1
        while i <= eqe:
            if (len(wlist[i]) <= d and len(p) <= d):
                i += 1
            elif (len(wlist[i]) <= d and len(p) > d):
                # Swap
                veqs = wlist[eqs]
                vi = wlist[i]
                wlist[eqs] = vi
                wlist[i] = veqs

                eqs += 1
                i += 1
            elif (len(wlist[i]) > d and len(p) <= d):
                # Swap
                veqe = wlist[eqe]
                vi = wlist[i]
                wlist[eqe] = vi
                wlist[i] = veqe

                eqe -= 1
            elif wlist[i][d] < p[d]:
                # Swap
                veqs = wlist[eqs]
                vi = wlist[i]
                wlist[eqs] = vi
                wlist[i] = veqs

                eqs += 1
                i += 1
            elif wlist[i][d] > p[d]:
                # Swap
                veqe = wlist[eqe]
                vi = wlist[i]
                wlist[eqe] = vi
                wlist[i] = veqe

                eqe -= 1

            else:
                i += 1

        sort_recursive(wlist, s, eqs-1, d)
        if len(p) > d:
            sort_recursive(wlist, eqs, eqe, d+1)
        sort_recursive(wlist, eqe+1, e, d)

    else:
        print("Immediate return from subarray " + str(s) + "..." + str(e) + " with depth " + str(d))


def main():

    #f = sys.argv[1]
    f = "3wayquicksort_data/input1.txt"

    w = read_string_file(f)
    #print(len(w))
    #print(w)

    sw = quicksort3(w)
    #print(sw)

main()


