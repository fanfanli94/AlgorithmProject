"""
Main Function Codes Group22
Main function to call the algorithm executables
Availabel algorithm options:
	[BnB|Approx|LS1|LS2]

Sample Execution:
	got to the current folder 
	cd CSE6140_Project_Group22
	python CS6140_project/main.py -inst email.graph -alg Approx -time 600 -seed 1045

"""
from Approx import Approx
from LS1 import LS1
from LS2 import LS2
from BnB import BnB
import sys
from sys import argv
import argparse

	
if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Wrapper Function for Vertex Cover Graphs')
    parser.add_argument('-inst',action='store',type=str,required=True,help='Enter graph datafile Data/name')
    parser.add_argument('-alg',action='store',type=str,required=True,help='Enter Algorithm name  [BnB|Approx|LS1|LS2]')
    parser.add_argument('-time',action='store',default=600,type=float,required=False,help='Cutoff in Seconds')
    parser.add_argument('-seed',action='store',default=10,type=int,required=False,help='Random Seed')
    args=parser.parse_args()

    algorithm = args.alg
    graph_file = 'DATA/' + args.inst
    output_dir = 'Output/'
    cutoff = args.time
    randSeed = args.seed

    if algorithm == 'Approx':
        Approx(graph_file, output_dir, cutoff, randSeed)

    elif algorithm == 'LS1':
        LS1(graph_file, output_dir, cutoff, randSeed)

    elif algorithm == 'LS2':
        LS2(graph_file, output_dir, cutoff, randSeed)

    elif algorithm == 'BnB':
        BnB(graph_file, output_dir, cutoff, randSeed)
		
    else:
        print('Please enter correct algorithm option from any of: [BnB|Approx|LS1|LS2]') #Error message
