'''
The code below is implemented based on the idea of Simulated Annealing (SA),
which read the input graph file and find an approximate optimum solution
within the given cutoff time.

Author: Mengzhen Chen
Date: 11/28/2022
'''

import networkx as nx
import time
import os
import random
import math
import argparse

def read_input(graphFileName):
    G = nx.Graph()
    with open(graphFileName, 'r') as gf:
        numOfVertex, numOfEdges, _ = gf.readline().split()
        adjInfo = gf.readlines()
        for index, value in enumerate(adjInfo):
            for vertex in value.split():
                G.add_edge(index+1, int(vertex))
    
    return G, int(numOfVertex), int(numOfEdges)


def create_ini_sol(G, startTime, cutoff, outputFile):
    G_ini = list(G.nodes())
    G_pair = zip(list(dict(G.degree(G_ini)).values()), G_ini)
    sortedVertexCoverList = sorted(list(G_pair), reverse=False)
    count = 0

    '''
    Remove as much nodes as possible to create an initial solution 
    of the vertex cover
    '''
    while (count < len(sortedVertexCoverList) and (time.time() - startTime < cutoff)):
        needToCheck = True
        for vertex in G.neighbors(sortedVertexCoverList[count][1]):
            if vertex not in G_ini:
                needToCheck = False
        if needToCheck:
            '''
            If all the neighbors of current node is in the initial
            solution, it will be removed from the solution
            ''' 
            G_ini.remove(sortedVertexCoverList[count][1])
        count += 1
    
    # Output the time to generate the initial solution
    outputFile.write(str(time.time() - startTime) + "," + str(len(G_ini)) + "\n")
    return G_ini


def simulate_annealing(G, outputFile, Sol_ini, cutoff, startTime):
    Temp = 0.8   
    Sol = Sol_ini.copy()
    # Initialize the Sol_best as empty list
    Sol_best = []
    while ((time.time() - startTime) < cutoff):
        Temp = 0.95 * Temp 

        # Searching for a solution with less vertices
        while not Sol_best:
            Sol = Sol_ini.copy()
            # Store the current improved vertex cover solution
            outputFile.write(str(time.time()-startTime) + "," + str(len(Sol)) + "\n")
            
            # Randomly remove a vertex in the solution
            rmVertex = random.choice(Sol_ini)

            # Check whether the neighbors of current node are in the solution or not
            for vertex in G.neighbors(rmVertex):
                if vertex not in Sol_ini:
                    '''
                    If the neighbors are not in the current solution,
                    both the vertex and that neighbor will be added
                    into the Sol_best list
                    '''
                    Sol_best.append(vertex)
                    Sol_best.append(rmVertex)
            Sol_ini.remove(rmVertex)     

        # Randomly delete a vertex from the current solution
        Sol_cur = Sol_ini.copy()

        # uncoveredSet is the list to store vertices haven't been covered by the solution
        uncoveredSet = Sol_best.copy()
        rmVertex = random.choice(Sol_ini)
        for vertex in G.neighbors(rmVertex):
            if vertex not in Sol_ini:
                Sol_best.append(vertex)
                Sol_best.append(rmVertex)         
        Sol_ini.remove(rmVertex)   

        # Randomly add a vertex from the Sol_best vertex set
        addVertex = random.choice(Sol_best)
        Sol_ini.append(addVertex)
        for vertex in G.neighbors(addVertex):
            if vertex not in Sol_ini:
                '''
                If the neighbors are not in the current solution,
                both the vertex and that neighbor will be removed
                from the Sol_best list
                '''
                Sol_best.remove(vertex)
                Sol_best.remove(addVertex)

        '''
        Accept a new solution based on the probability which is 
        proportional to the difference between the quality of 
        the best solution and the current solution, and the temperature.
        ''' 
        if len(uncoveredSet) < len(Sol_best): 
            '''
            P is the expression for the probability to either accept 
            or deny the solution
            '''
            P = math.exp(float(len(uncoveredSet) - len(Sol_best))/Temp)
            
            # Randomly pick a number between 0 and 1
            alpha = random.uniform(0, 1)
            
            if alpha > P:
                '''
                If the solution is 
                '''    
                Sol_ini = Sol_cur.copy()
                Sol_best = uncoveredSet.copy()
    return Sol


def LS1(inputFile, outputPath, cutoff, sd):
    # Setup random seed
    random.seed(sd)
    
    # Get input file name
    inputFileName = inputFile.split('/')[-1].split('.')[0]

    # Set output file name and location 
    SolFileName = "_".join([inputFileName, "SA", str(cutoff), str(sd)]) + '.sol'
    TraceFileName = "_".join([inputFileName, "SA", str(cutoff), str(sd)]) + '.trace'

    # Record computation start time
    startTime = time.time()

    # Check output path existence
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    
    # Record the trace of the solution
    with open(os.path.join(outputPath, TraceFileName), 'w') as traceFile:
        # Read the input graph file
        G, numOfVertex, numOfEdges = read_input(inputFile)

        # Initialize the solution
        G_ini = G.copy()
        Sol_ini = create_ini_sol(G_ini, startTime, cutoff, traceFile)

        # Apply the simulation annealing algorithm to seek the best solution
        Sol = simulate_annealing(G, traceFile, Sol_ini, cutoff, startTime)

        print('The SA Solution of the MVC problem is: {}.'.format(Sol))
        print('The number of minimum vertices is: {}.'.format(len(Sol)))
    
        # Write solution to file  
        with open(os.path.join(outputPath, SolFileName), 'w') as solFile:
            solFile.write(str(len(Sol)) + '\n')
            solFile.write(','.join([str(n) for n in sorted(Sol)]))


# if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Run the Minimum Vertex Problem with different algorithms')
    # parser.add_argument('-inst', type=str, required=True, help='inputFile')
    # parser.add_argument('-alg', type=str, required=True, help='algorithm to be used')
    # parser.add_argument('-time', type=float, default=500, required=False, help='cutoff time')
    # parser.add_argument('-seed', type=int, default=1, required=False, help='random seed')
    # args = parser.parse_args()

    # '''
    # Example command:
    # python LS1.py -inst ./DATA/jazz.graph -alg SA -time 10 -seed 1
    # '''

    # main(args.alg, args.inst, args.time, args.seed)
    
    # for rd in range(2, 11):
    #     main("SA", 'DATA/star.graph', 1000.0, rd)