import math
import networkx as nx


class HotInstance:

	def __init__(self, file_path: str):

		file = open(file_path, "r")

		first_line = file.readline().strip()

		if first_line == "EDGELIST":

			second_line = file.readline().strip().split(" ")

			n = int(second_line[0]) # number of vertices
			m = int(second_line[1]) # number of edges
			k = int(second_line[2]) # number of drivers
			L = int(second_line[3]) # desired travel distance

			G = nx.Graph()

			for i in range(n):
				G.add_node(i)

			for i in range(m):
				line = file.readline().strip().split(" ")
				G.add_edge(int(line[0]), int(line[1]), weight=int(line[2]))

			M = self.big_M(G, L, k)
			G = self.add_dummy_edges(G, L, k, M)

		elif first_line == "COORDS":

			second_line = file.readline().strip().split(" ")

			n = int(second_line[0]) # number of vertices
			k = int(second_line[1]) # number of drivers
			L = int(second_line[2]) # desired travel distance

			G = nx.Graph()

			for i in range(n):
				line = file.readline().strip().split(" ")
				G.add_node(i, x=int(line[0]), y=int(line[1]))

			for i in range(n):
				xi = G.nodes[i]["x"]
				yi = G.nodes[i]["y"]
				for j in range(i+1, n):
					xj = G.nodes[j]["x"]
					yj = G.nodes[j]["y"]
					distance = custom_round(euclidean_distance(xi,yi,xj,yj))
					G.add_edge(i, j, weight=distance)

			M = self.big_M(G, L, k)

		self.name = self.get_basename(file_path)
		self.n = n
		self.m = G.number_of_edges()
		self.k = k
		self.L = L
		self.G = G
		self.M = M


	def add_dummy_edges(self, G, L, k, dummy_weight):
		for i in range(G.number_of_nodes()):
			for j in range(i+1, G.number_of_nodes()):
				if not G.has_edge(i,j):
					G.add_edge(i, j, weight=dummy_weight)
		return G

	def big_M(self, G, L, k):
		S = self.edge_weight_sum(G) + 1
		if L <= S:
			return L + k*(S+1)
		else:
			return L + k*(L+1)

	def max_edge_weight(self, G):
		max_weight = 0
		for edge in G.edges.data('weight'):
			weight = edge[2]
			if weight > max_weight:
				max_weight = weight
		return max_weight

	def edge_weight_sum(self, G):
		weight_sum = 0
		for edge in G.edges.data('weight'):
			weight = edge[2]
			weight_sum += weight
		return weight_sum

	def euclidean_distance(self, x1,y1,x2,y2):
		return math.sqrt((x1-x2)**2 + (y1-y2)**2)

	def custom_round(self, x):
		frac = x - math.floor(x)
		if frac < 0.5:
			return math.floor(x)
		else:
			return math.ceil(x)

	def get_distance(self, a, b):
		if (a==b):
			print("a = b")
			print("a: ", a, " b: ", b)
		return self.G.get_edge_data(a,b)["weight"]

	def get_basename(self, file_path):
		path_array = file_path.split("/")
		filename_array = path_array[len(path_array)-1].split(".")
		return filename_array[0]