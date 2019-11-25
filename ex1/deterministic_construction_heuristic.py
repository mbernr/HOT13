import numpy as np


def deterministic_construction_heuristic(inst):

	# build tour array:
	# Step 1)	select edge closest to (L*k)/n
	# Step i+1)	select edge closest to (L*k - sum of weights of assigned edges) / (n - number of assigned edges) 

	# build driver array:
	# bin packing, exercise 1
	# drivers are bins, edges are items, L is capacity