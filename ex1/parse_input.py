import sys
import networkx as nx
import math


def parse(file_path):

	file = open(file_path, "r")

	first_line = file.readline().strip()

	if first_line == "EDGELIST":

		second_line = file.readline().strip().split(" ")

		n = int(second_line[0]) # number of vertices
		m = int(second_line[1]) # number of edges
		k = int(second_line[2]) # number of drivers
		L = int(second_line[3]) # desired travel distance

		G = nx.Graph()

		for i in range(0,n):
			line = file.readline().strip().split(" ")
			G.add_edge(int(line[0]), int(line[1]), weight=int(line[2]))

		G = add_dummy_edges(G)

		return G

	elif first_line == "COORDS":

		second_line = file.readline().strip().split(" ")

		n = int(second_line[0]) # number of vertices
		k = int(second_line[1]) # number of drivers
		L = int(second_line[2]) # desired travel distance

		G = nx.Graph()

		for i in range(0,n):
			line = file.readline().strip().split(" ")
			G.add_node(i, x=int(line[0]), y=int(line[1]))

		for i in range(G.number_of_nodes()):
			xi = G.nodes[i]["x"]
			yi = G.nodes[i]["y"]
			for j in range(i+1, G.number_of_nodes()):
				xj = G.nodes[j]["x"]
				yj = G.nodes[j]["y"]
				distance = custom_round(euclidean_distance(xi,yi,xj,yj))
				G.add_edge(i, j, weight=distance)

		return G

	else:

		print("Invalid instance format")
		sys.exit()


def add_dummy_edges(G):
	M = big_M(G)
	for i in range(G.number_of_nodes()):
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

def euclidean_distance(x1,y1,x2,y2):
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def custom_round(x):
	frac = x - math.floor(x)
	if frac < 0.5: 
		return math.floor(x)
	else:
		return math.ceil(x)


# edgelist = "instances/0010_k1.txt"
# coords = "instances/kroB150_k3_2.txt"
# G = parse(edgelist)
