import sys
import networkx as nx


def parse(file_path):

	file = open(file_path, "r")

	first_line = file.readline().strip()

	if first_line == "EDGELIST":

		second_line = file.readline().strip().split(" ")

		n = int(second_line[0])
		m = int(second_line[1])
		k = int(second_line[2])
		L = int(second_line[3])

		G = nx.Graph()

		for line in file:
			line = line.strip().split(" ")
			G.add_edge(int(line[0]), int(line[1]), weight=int(line[2]))

		G = add_dummy_edges(G)

		return G

	elif first_line == "COORDS":

		second_line = file.readline().strip().split(" ")

		n = int(second_line[0])
		k = int(second_line[1])
		L = int(second_line[2])

		# todo: parse vertices and edges from COORDS files

	else:

		print("Invalid instance format")
		sys.exit()


def add_dummy_edges(G):
	M = big_M(G)
	for i in range (G.number_of_nodes()):
		for j in range(i+1, G.number_of_nodes()):
			if not G.has_edge(i,j):
				G.add_edge(i, j, weight=M)
	return G

def big_M(G):
	return edge_weight_sum(G) + 1 # we need something better here

def max_edge_weight(G):
	max_weight = 0
	for edge in G.edges.data('weight'):
		weight = edge[2]
		if weight > max_weight:
			max_weight = weight
	return max_weight

def edge_weight_sum(G):
	weight_sum = 0
	for edge in G.edges.data('weight'):
		weight = edge[2]
		weight_sum += weight
	return weight_sum


