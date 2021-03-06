#!/opt/local/bin/python2.7
"""
What does this do?
"""

import os
#import sys
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
	open_file = open(file_name)
	for line in open_file:
		fields = line.split()
		cleaned = clean(fields)
		gene1, gene2, value = cleaned[1], cleaned[3], cleaned[4]
		G.add_node(gene1)
		G.add_edge(gene1, gene2, confidence = float(value))
	open_file.close()
	return G


def calculate_degree(graph):
	graph.counts = {}
	for (node1, node2, edge) in graph.edges(data=True):
		if node1 in graph.counts:
			graph.counts[node1] += 1
		else:
			graph.counts[node1] = 1
	for (node1, node2, edge) in graph.edges(data=True):
		if node2 in graph.counts:
			graph.counts[node2] += 1
		else:
			graph.counts[node2] = 1
	return graph.counts


def filter_by_confidence(graph, confidence_threshold):
	filtered_graph = nx.Graph()
	for (node1, node2, edge) in graph.edges(data=True):
		if edge['confidence'] > confidence_threshold:
			inverse_confidence = float(1/edge['confidence'])
			filtered_graph.add_edge(node1, node2, length = inverse_confidence)
		else:
			pass
	return filtered_graph

def filter_by_degree(graph, degree_threshold):
	filtered_graph = nx.Graph()
	node_degree = calculate_degree(graph)
	for (node1, node2, edge) in graph.edges(data=True):
		if node_degree[node1] > degree_threshold:
			filtered_graph.add_edge(node1, node2, edge)
		else:
			pass
	return filtered_graph


def highlight_targets(graph, targets):
	node_color = {}
	open_file = open(targets)
	for line in open_file:
		fields=line.split()
		cleaned=clean(fields)
		for (node1, node2, edge) in graph.edges(data=True):
			if node1 == cleaned[0]:
				node_color[node1] = 'b'
			elif node2 == cleaned[0]:
				node_color[node2] = 'b'
			else:
				pass
		for (node1, node2, edge) in graph.edges(data=True):
			if node1 not in node_color:
				node_color[node1] = 'r'
			elif node2 not in node_color:
				node_color[node2] = 'r'
			else:
				pass
	open_file.close()
	return node_color

def label_by_degree(graph, degree_threshold):
	node_label = {}
	node_degree = calculate_degree(graph)
	for (node1, node2, edge) in graph.edges(data=True):
		if int(node_degree[node1]) > degree_threshold:
			node_label[node1] = node1
		else:
			node_label[node1] = ''
		if int(node_degree[node2]) > degree_threshold:
			node_label[node2] = node2
		else:
			node_label[node2] = ''
	return node_label

def label_by_target(graph, target):
	node_label = {}
	open_file = open(target)
	for line in open_file:
		fields=line.split()
		cleaned=clean(fields)
		for (node1, node2, edge) in graph.edges(data=True):
			if node1 == cleaned[0]:
				node_label[node1] = node1
			elif node2 == cleaned[0]:
				node_label[node2] = node2
			else:
				pass
		for (node1, node2, edge) in graph.edges(data=True):
			if node1 not in node_label:
				node_label[node1] = ''
			elif node2 not in node_label:
				node_label[node2] = ''
			else:
				pass
	open_file.close()
	return node_label


def label_custom(graph, position, degree_threshold, target):
	threshold_labels = label_by_degree(graph, degree_threshold)
	target_labels = label_by_target(graph, target)
	red_labels = nx.draw_networkx_labels(graph,pos=position, 
											labels=threshold_labels, 
											font_color='r')
	blue_labels = nx.draw_networkx_labels(graph,pos=position, 
											labels=target_labels, 
												font_color='b')
	return red_labels, blue_labels


def main():
	bacteriome = os.getcwd() + os.sep + 'bacteriome_combined.txt'
	create_targets = os.getcwd() + os.sep + 'genetargets.txt'
	
	G = generate_graph(bacteriome)
	print("network has %d nodes with %d edges" %(nx.number_of_nodes(G), nx.number_of_edges(G)))
	
	confidence_threshold = float(input("Enter the confidence threshold cutoff (0 - 1.0). "))
	G = filter_by_confidence(G, confidence_threshold)
	print("network filtered by confidence %.2f has %d nodes with %d edges" %(confidence_threshold, nx.number_of_nodes(G), nx.number_of_edges(G)))
	
	node_threshold = int(input("Enter the minimum degree for each node displayed in the network. "))
	G = filter_by_degree(G, node_threshold)
	print("network filtered by nodes with more than %s connections has %d nodes with %d edges" %(node_threshold, nx.number_of_nodes(G), nx.number_of_edges(G)))
	
	label_threshold = int(input("Enter the minimum degree for each node labeled in the network. "))

	node_degree = calculate_degree(G)
	node_color = highlight_targets(G, create_targets)
	#node_label = label_by_degree(G, 40)
	#node_label = label_by_target(G, create_targets)
	pos = nx.spring_layout(G)

	plt.figure(figsize=(8,8))
	nx.draw(G,
		pos=pos,
		node_color=[node_color[node] for node in G], 
		node_size=[node_degree[node] for node in G],
		#labels=node_label,
		#with_labels=True,
		#font_color='m',
		#font_weight='bold',
		width=0.1)
	blue_labels_threshold, red_labels_targets = label_custom(G, pos, label_threshold, create_targets)
	plt.draw()

	plt.savefig('output.png')

main()


















