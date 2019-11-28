from hot_instance import *
from hot_solution import *
from construction_heuristics import *
from neighbourhood_structures import *
from local_search import *
from grasp import *
from vnd import *
from simulated_annealing import *


inst = HotInstance("instances/0010_k2.txt")
#ns = DriverOneExchange()
ns = TourReversal()
#ns = OneBlockMove()
nsa = [TourReversal(), OneBlockMove(), DriverOneExchange()]

#---------------STUFF TO PLAY AROUND---------------
multiplier = 1  #variable to play around with temperature
alpha = 0.95
max_iterations = 100000
max_time = 10
#----------------------------------------------------

sol = construct_greedy(inst)
#sol = construct_random_greedy(inst, 0.25)
T = sol.inst.M * sol.inst.k *multiplier #temperature

#sol = construct_greedy(inst)
# sol = HotSolution(inst, drivers=[0,1,1,0,0,1,1,0,0,1])

print(sol)
print(sol.obj())
print()

simulated_annealing(sol, nsa, T, alpha, max_iterations, max_time)

print(sol)
print(sol.obj())
print()

