#!/opt/local/bin/python2.7
"""
What does this do?
"""

import os
import re
import sys
import networkx as nx
import matplotlib.pyplot as plt

#input_file = sys.argv[1]

def clean(lines):
    cleaned = []
    for field in lines:
        cleaned.append(field.strip())  # strip() takes out anything that is white space
    return(cleaned)

def generate_graph(file_name):
	G = nx.Graph()
	G.gene = {}
	G.confidence = {}
	gene = []

	for line in open(file_name):
		fields = line.split()
		cleaned = clean(fields)
		gene1, gene2, confidence = cleaned[1], cleaned[3], cleaned[4]
		G.add_node(gene1)
		G.add_edge(gene1, gene2, weight = float(confidence))

	return G




### file = open("/Users/Andrea/Desktop/CSCI_1310/students.txt", "r")
### new_file = open("/Users/Andrea/Desktop/CSCI_1310/students_list.txt", "w")
### for line in file:
### 	first, last, student_id = line.replace(" ", "").split(",")
### 	new_file.write('\t'.join((last, first, student_id)))
### new_file.close()
### file.close()


def main():
	G = generate_graph(os.getcwd() + os.sep + 'bacteriome_combined.txt')
	print("digraph has %d nodes with %d edges" %(nx.number_of_nodes(G), nx.number_of_edges(G)))
	#nx.draw(G)
	#plt.draw()


	H = nx.Graph()
	create_list = open(os.getcwd() + os.sep + 'CREATE_genetargets.txt')
	for line in create_list:
		fields=line.split()
		cleaned=clean(fields)
		for v in G:
			if cleaned[0] == v:
				G.gene[v] = 200
			else:
				G.gene[v] = 5
	#print G.gene

	G.counts = {}

	counts = {}
    for character in text:
        if character in counts:
            counts[character] += 1
        else:
            counts[character] = 1
    return(counts)


	for v in G:
		G.counts[v] = 0
		G.counts[v] += 1
	print G.counts
	if G.counts[v] >= 20:
		H.add_node(v)
	else:
		pass
	for(u,v,d) in G.edges(data=True):
		if d['weight'] > 0.8:
			H.add_edge(u,v)

	plt.figure(figsize=(8,8))
	#node_color = [float(H.degree(v)) for v in H]
	nx.draw(H, 
		node_size=[G.gene[v] for v in H],
		with_labels=False)
	plt.draw()

	plt.savefig('bla.png')





main()
