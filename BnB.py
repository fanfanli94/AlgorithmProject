###########################Top Comments################################################
'''This code implements the Branch and Bound (BnB) Algorithm to find minimum vertex cover (MVC)
Author:Group 22_Fall2020 Xiao Jing

Language: Python 3
Run this code: Please see the README

The output will be two files: *.sol and *.trace automatically into the created output folder
'''
import time
import os
import argparse
import networkx as nx
import operator

########Main Execuation of this Algorithm################################
def BnB(inputfile, output_dir, cutoff, randSeed):
	#Call g to get all the edges and the vertextex to create graph
	g = get_the_graph(inputfile)
	
	print('Number of Nodes in Graph :', g.number_of_nodes(),
		  '\nNumber of Edges in Graph:', g.number_of_edges())

	Sol_VC, times_list = BnBalg(g, cutoff)

	#Remove incorrecr nodes (Binstate=0)
	for element in Sol_VC:
		if element[1]==0:
			Sol_VC.remove(element)
			
######Write Output files##############
	# Write Solution File
	inputdir, inputfile = os.path.split(inputfile)
	#Write Sol Files
	with open('./Output//' + inputfile.split('.')[0] + '_BnB_'+str(int(cutoff))+'.sol', 'w') as f:
		f.write('%i\n' % (len(Sol_VC)))
		f.write(','.join([str(x[0]) for x in Sol_VC]))

	#Write Trace Files
	with open('./Output//' + inputfile.split('.')[0] + '_BnB_'+str(int(cutoff))+'.trace', 'w') as f:
		for t in times_list:
			f.write('%.2f,%i\n' % ((t[1]),t[0]))


#############function-Get all the edges and the vertextex to create graph##############
def get_the_graph(filename):
	list_of_edges= []
	with open(filename) as f:
		num_of_vertex, num_of_edges, weight = map(int, f.readline().split())
		for i in range(num_of_vertex):
			list_of_edges.append(map(int, f.readline().split()))
	g = nx.Graph()
	for i in range(len(list_of_edges)):
		for k in list_of_edges[i]:
			g.add_edge(i + 1, k)
	return g

##########BnB Algorithm main function#########################
##########To find Minimum Vertex Cover of the Graph##############
def BnBalg(G, T):

 ######Initilize OptimalSolution, VCSETS AND CanSV SET TO EMPTY SET
	OptVC = []
	CVC = []
	CanSV = []
	NeighborNodes = []

	#Initial Upper_Bound UB
	UB = G.number_of_nodes()
	print('Initial UpperBound:', UB)

	SubCG = G.copy()  ##Make a copy of G as subproblem 
	
 	# Sort dict degree of nodes with max degree
	list_deg = SubCG.degree()
	list_deg_sorted = sorted(dict(list_deg).items(), reverse=True, key=operator.itemgetter(1))  #Sort in descending order
	v = list_deg_sorted[0]  # tuple - (node,degree)

	#Record running time
	StartTime = time.time()
	Endtime = StartTime
	Deltime = Endtime-StartTime
	Times_list=[]    #list of times when solution is here tuple=(VC size,Deltime)		
 
	# Append V(0&1) TO CanSV
	CanSV.append((v[0], 0, (-1, -1)))  # tuples of node
	CanSV.append((v[0], 1, (-1, -1)))	
 
	while CanSV!=[] and Deltime < T:
		(V_max,VertexCover,ParentNodes)=CanSV.pop() #set current node to last element in CanSV
		
		Backtracking = False
		if VertexCover == 0:  # if V_max is not selected, Binstate of all NeighborNodes=0
			NeighborNodes = SubCG.neighbors(V_max)  # store all RelError of V_max
			for node in list(NeighborNodes):
				CVC.append((node, 1))
				SubCG.remove_node(node)  # node is in CVC, remove NeighborNodes from SubCG
		elif VertexCover == 1:  # if V_max is selected, Binstate of all NeighborNodes=0
			SubCG.remove_node(V_max)  # V_max is in CVC and remove nodes from G
		else:
			pass

		CVC.append((V_max, VertexCover))
		#Get the size of CVC :No. of nodes with VertexCover=1
		VC_Size = 0 ##VC is a tuple list, vc_size is the number of nodes which has binstate == 1
		for item in CVC:
			VC_Size = VC_Size + item[1]
		CVC_size = VC_Size

		if SubCG.number_of_edges() == 0:  # Which means it is the end of exploring, optimal solution should be found
			if CVC_size < UB:
				OptVC = CVC.copy()
				print('Current Optimal VC size', CVC_size)
				UB = CVC_size
				Times_list.append((CVC_size,time.time()-StartTime))
			Backtracking = True
				
		else:  #Sub solution
			CurLB = LBfun(SubCG) + CVC_size

			if CurLB < UB:  # worth exploring
				####Find Vertex with Max degree in remianing Graph#####
				list_deg = SubCG.degree()
				list_deg_sorted = sorted(dict(list_deg).items(), reverse=True, key=operator.itemgetter(1))  #sort in descending order of node degree
				Vmaxdeg = list_deg_sorted[0]  # tuple - (node,degree)
	
				CanSV.append((Vmaxdeg[0], 0, (V_max, VertexCover)))#(V_max,state) is parent of vj
				CanSV.append((Vmaxdeg[0], 1, (V_max, VertexCover)))
			else:
				# End of path, it will return worse solution, backtracking to parent nodes
				Backtracking = True

		if Backtracking == True:
			if CanSV != []:	#otherwise no more candidates
				nextnode_parent = CanSV[-1][2]	#Parents of last element in CanSV turple

				# Backtracking to the level of nextnode_parent
				if nextnode_parent in CVC:
					
					ID = CVC.index(nextnode_parent) + 1
					while ID < len(CVC):	#undo changes from end of CurVC back up to parent nodes
						Cnode, binstate = CVC.pop()
						SubCG.add_node(Cnode)	
						
						# find all the edges connected to V_max in Graph G
						CVC_nodes = list(map(lambda t:t[0], CVC))
						for nd in G.neighbors(Cnode):
							if (nd in SubCG.nodes()) and (nd not in CVC_nodes):
								SubCG.add_edge(nd, Cnode)	#Append edges of V_max back to SubCG that were possibly removed

				elif nextnode_parent == (-1, -1):
					# Backtracking to the root nodes
					CVC.clear()
					SubCG = G.copy()
				else:
					print('Error in Backtracking Step!') ##Error Message

		Endtime=time.time()
		Deltime=Endtime-StartTime
		if Deltime>T:
			print('Reminder:Cutoff time reached!') ##Warning Message

	return OptVC,Times_list


#Calculate LowerBound
def LBfun(graph):
	list_deg = graph.degree()
	list_deg_sorted = sorted(dict(list_deg).items(), reverse=True, key=operator.itemgetter(1))  #sort in descending order of node degree
	find_maxdeg = list_deg_sorted[0]
	LB = graph.number_of_edges() / find_maxdeg[1]	
 	######Find the minimum integer bigger than current LB#################
	if LB > int(LB):
		LB = int(LB) + 1
	else:
		LB = int(LB)
		
	return LB

