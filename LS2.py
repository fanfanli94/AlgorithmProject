'''
The code below is implemented based on the idea of Hill Climbing,
which read the input graph file and find an approximate optimum solution
within the given cutoff time.
Author: Judu Xu
Date: 12/04/2022
'''

import random
import time
import os

class graph:

    #initialize the graph
    def __init__(self):
        self.num_of_edges = 0
        self.num_of_vertex = 0
        self.g = {}
        self.vertex = set()

    def get_the_graph(self, filename):

        # get the data of the file
        f = open(filename, "r")
        lines = f.readlines()

        # get the data of the first line
        l = list(map(int, lines[0].split()))
        self.num_of_vertex = l[0]
        self.num_of_edges = l[1]

        # get the all the edges and the vertexes
        for i in range(1, self.num_of_vertex + 1):
            line = list(map(int, lines[i].split()))
            self.vertex.add(i)
            # check if this vertex is in the dict
            if i not in self.g:
                self.g[i] = set()

            for n in line:
                self.g[i].add(n)
                if n not in self.g:
                    self.g[n] = set()
                self.g[n].add(i)

        f.close()

    def copy(self):
        copy = graph()
        copy.num_of_edges = self.num_of_edges
        copy.num_of_vertex = self.num_of_vertex

        for v in self.vertex:
            copy.vertex.add(v)

        for key in self.g:
            copy.g[key] = set()
            for i in self.g[key]:
                copy.g[key].add(i)

        return copy

#add a vertex into a graph
def add(C, i):

    if i in C.vertex:
        return

    C.vertex.add(i)
    C.num_of_vertex += 1

    for j in C.g[i]:
        if j not in C.vertex:
            C.num_of_edges += 1

#remove a vertex from a graph
def remove(C, i):
    # check if this node is still in the graph
    if i not in C.vertex:
        return

    C.vertex.remove(i)
    C.num_of_vertex -= 1

    for j in C.g[i]:
        if j not in C.vertex:
            C.num_of_edges -= 1

#check the number of cover edges to see whether it is vertex cover
def is_vertex_cover(G, C):
    return G.num_of_edges == C.num_of_edges


def Local_Search(file, G, cutoff, seed):

    # get an initial solution
    C = G.copy()
    # start_time
    start_time = time.time()
    # using hill_climb to get the answer
    return Hill_Climbing(file, G, C, start_time, cutoff, seed)


def Hill_Climbing(file, G, C, start_time, cutoff, random_seed):
    
    #write answer
    f = open('Output\\' + file +  "_LS2_" +   str(cutoff) + "_" + str(random_seed) + ".trace", "w")
    f.write("0, " + str(C.num_of_vertex))
    f.write('\n')
    # set random seed
    random.seed(random_seed)

    C_ans = C.copy()
    # get sorted node dict
    node_dict = {}
    for i in range(1, G.num_of_vertex + 1):
        if len(G.g[i]) not in node_dict:
            node_dict[len(G.g[i])] = set()
        node_dict[len(G.g[i])].add(i)

    degree_list = sorted(node_dict.keys())

    # start hill climbing search
    while time.time() - start_time < cutoff and len(degree_list) > 0:

        # randomly choose a node that has the minimum degree
        v = random.choice(list(node_dict[degree_list[0]]))
        node_dict[degree_list[0]].remove(v)
        if not len(node_dict[degree_list[0]]):
            degree_list.pop(0)

        remove(C, v)
        if not is_vertex_cover(G, C):
            add(C, v)

        if C_ans.num_of_vertex > C.num_of_vertex:
            C_ans = C.copy()
            f.write(str(round(time.time() - start_time, 4)) + ", " + str(C_ans.num_of_vertex))
            f.write('\n')

    # return the answer
    f.close()
    return C_ans

def write_sol(file, cutoff, random_seed, output):
    
    f = open("Output//" + file + "_LS2_" +   str(cutoff) + "_" + str(random_seed) + ".sol", "w")
    f.write(str(output.num_of_vertex))
    f.write('\n')
    l = sorted(list(output.vertex))
    for i in range(len(l)):
        if i != len(l) - 1:
            f.write(str(l[i]) + ',')
        else:
            f.write(str(l[i]))
    f.close


# the main function of LS2
def LS2(file_name, outputPath, cutoff, random_seed):

    g = graph()
    g.get_the_graph(file_name)
    output = Local_Search(file_name[5:], g, cutoff, random_seed)
    write_sol(file_name[5:], cutoff, random_seed, output)

    
    
    
    

    
    
