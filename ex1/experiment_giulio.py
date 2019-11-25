from hot_instance import *
from hot_solution import *
from construction_heuristics import *


inst = HotInstance("instances/0010_k2.txt")

#print(i.k, i.L, i.n, i.m)
#print(i.G.edges().data())

sol = HotSolution(inst)

print("neighbourhood_search_driver_flip")
for i in range(5):
    if sol.neighbourhood_search_driver_flip(step_function="next_improvement"):
        print(sol)
        print(round(sol.calc_objective(),2))
        print()
    else:
        print("No improvement found")


print("neighbourhood_search_tour_swap")
for i in range(5):
    if sol.neighbourhood_search_tour_swap(step_function="random_improvement"):
        print(sol)
        print(round(sol.calc_objective(),2))
        print()
    else:
        print("No improvement found")
        print()
