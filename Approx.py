'''
The following code implements the Approximation Algorithm for Vertex Cover

'''

import random
import time




def Approx(graph_file, output_dir, cutoff, randSeed):
    # Generates a random seed
    random.seed(randSeed)
    # Create Graph adjacency dictionary and set of Edges
    G,E = parse_edges(graph_file) 

    # create output folders with the requested names
    if 'DATA/' in graph_file:
        file_path = graph_file.replace('DATA/','')
        sol_file = output_dir+file_path+'_'+'Approx'+'_'+str(cutoff)+'_'+str(randSeed)+'.sol'
        trace_file = output_dir+file_path+'_'+'Approx'+'_'+str(cutoff)+'_'+str(randSeed)+'.trace'

    # call MinVerCover function that returns the minimum vertex cover set
    vertices = MinVerCover(E, cutoff, trace_file)

    # Write output data and store in the Output folder
    output = open(sol_file, 'w')
    output.write(str(len(vertices)) + "\n")

    # add the final number of vertices to the trace files
    i = 1
    for v in vertices:
        output.write(str(v))
        if i < len(vertices):
            output.write(",")
        i += 1

    output.write("\n")


# parse data files and create graph dictionary       
def parse_edges(filename):
    
    G = {}
    V = set()
    E = set()   
    Num_V = 0
    Num_E = 0

    
    f = open(filename, "r")
    firstln = True
    for i, ln in enumerate(f):
        
        line_list = ln.split(' ')

        if not firstln:
            
            if 'dummy' in filename:
                line_list = list(map(int, line_list)) 
                v = line_list.pop(0)
            else:
                
                # Input the line number as the vertex
                line_list.pop(-1)
                line_list = list(map(int, line_list)) 
                v = i
            # Add a new vertex to the Graph
            if v not in G.keys():
                G[v] = set()
                V.add(v)

            # Add the new edge to the graph
            for u in line_list:
                G[v].add(u)
                V.add(u)
                E.add((v, u))


                if u not in G.keys():
                    G[u] = {v}
                else:
                    G[u].add(v)

        else:
            # Parse the first line to get the number of vertices and edges
            firstln = False
            line_list = list(map(int, line_list)) 
            num_v, num_e, weight = line_list
            Num_V = num_v
            Num_E = num_e

    return G, E





def MinVerCover(E, time_limit, trace_file):
    st = time.perf_counter()

    output = open(trace_file, 'w')

    # All edges start with unselected
    edge_unselect = E.copy()
    node_set = set()

    # running time
    run_t = 0

    # iterate all edges until empty or cutoff time exceeds
    while run_t < time_limit and len(edge_unselect) != 0:

        # Randomly select any edges add to the selected set
        edge_rand = random.sample(edge_unselect, 1)[0]

        # remove the selected edges from the unselected set
        edge_unselect.remove(edge_rand)

        node_set.add(edge_rand[0])
        node_set.add(edge_rand[1])

        edges_removed = set()

        # delete all edge incident to either u or v
        for E1 in edge_unselect:
            if edge_rand[0] == E1[0] or edge_rand[0] == E1[1] or edge_rand[1] == E1[0] or edge_rand[1] == E1[1]:
                edges_removed.add(E1)
        for E2 in edges_removed:
            edge_unselect.remove(E2)

        curr_time = time.perf_counter()
        run_t = curr_time - st

    # run time
    curr_time = time.perf_counter()
    run_t = curr_time - st
    output.write(str(run_t) + ", " + str(len(node_set)) + "\n")

    return node_set
