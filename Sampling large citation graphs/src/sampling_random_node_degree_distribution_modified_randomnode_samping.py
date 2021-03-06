# To Run this script: python sampling_random_node_degree_distribution_modified_randomnode_samping.py <year>

import networkx as nx
import matplotlib.pyplot as plt
import sys
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.font_manager import FontProperties
import random
import math
from scipy.stats import ks_2samp
import numpy as np
'''
samplepercent = .50
samplepercents = [.10,.20,.30,.40,.50]
samplepercents100 = [10,20,30,40,50]
biases = []
avgdvalues = []
n = 1
'''
samplepercent = .50
samplepercents = [.10,.20,.30,.40,.50]
samplepercents100 = [10,20,30,40,50]
biases = []
avgdvalues = []
n = 1
curyear = int(sys.argv[1])
for samplepercent in samplepercents:
	avgdvalue = 0
	avgbiasforsample = 0
	for iteration in range(0,n):
		year = []
		largestcomponent = []
		randomnodes = []
		print "Year", curyear,":"
		for x in range(curyear, curyear+1):
			fh1 = open("../data/adjlistfile_till_year_"+str(x))
			fh2 = open("../data/adjlistfile_largestcomponent_till_year_"+str(x))
			G1 = nx.read_adjlist(fh1)
			avgclusteringcoefofnetwork = nx.average_clustering(G1)
			G2 = nx.read_adjlist(fh2, create_using=nx.DiGraph())
			samplesize = int(samplepercent*G2.number_of_nodes())
			
			source = random.choice(G2.nodes()) # sources
			randomnodes.append(source)
			i = 0
			while len(randomnodes)<=samplesize:
				for inn in range(0, int(len(G2.predecessors(randomnodes[i]))*1)):
					indegreenode = random.choice(G2.predecessors(randomnodes[i]))
					if (randomnodes.count(indegreenode)==0):
						randomnodes.append(indegreenode) # append indegree neighbors randomly
				for outt in range(0, int(len(G2.neighbors(randomnodes[i]))*1)):
					outdegreenode = random.choice(G2.neighbors(randomnodes[i]))
					if (randomnodes.count(outdegreenode)==0):
						randomnodes.append(outdegreenode) # append outdegree neighbors randomly
				i = i+1
				print "Number of nodes in",int(samplepercent*100),"% random sample:",len(randomnodes),'of',samplesize,'nodes.'
			
			G3 = G2.subgraph(randomnodes)
			G3 = G3.to_undirected()
			degrees1 = G1.degree() # dictionary node:degree
			values1 = sorted(set(degrees1.values()))
			hist1 = [degrees1.values().count(x) for x in values1]
			nodes1 = G1.number_of_nodes()
			newhist1 = [float(x)/nodes1 for x in hist1]

			degrees2 = G3.degree() # dictionary node:degree
			values2 = sorted(set(degrees2.values()))
			hist2 = [degrees2.values().count(x) for x in values2]
			nodes2 = G3.number_of_nodes()
			newhist2 = [float(x)/nodes2 for x in hist2]
			
			plt.figure()
			ax = plt.subplot(111)
			box = ax.get_position()
			ax.set_position([box.x0, box.y0 + box.height * 0.10, box.width, box.height * .90])
			plt.yscale('log')
			plt.xscale('log')
			fontP = FontProperties()
			fontP.set_size('small')
			line1, = plt.plot(values1,newhist1,'bo',label='Original network')
			plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=2, handler_map={line1: HandlerLine2D(numpoints=2)}, prop = fontP)
			line2, = plt.plot(values2,newhist2,'ro',label='Random node sample network (via modified random node sampling)')
			plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=2, handler_map={line2: HandlerLine2D(numpoints=2)}, prop = fontP)
			plt.suptitle('Degree Distribution plot for '+str(int(samplepercent*100))+'% random node sample (via modified random node sampling) till year '+str(curyear), fontsize=11)
			plt.xlabel('Degree')
			plt.ylabel('Fraction of nodes')
			plt.savefig('../graphs/Degree Distribution plot for '+str(int(samplepercent*100))+'% random node sampling (via modified random node sampling) till year '+str(curyear)+'.png')
			plt.close()
	print
