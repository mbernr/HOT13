
instance = "a280_k5_1.txt"
can_be_infeas = False

names = [
	"Det. constr.",
	"Rand. constr.",
	"LS (\\textit{driver-one-ex, best-improv})",
	"LS (\\textit{driver-one-ex, next-improv})",
	"LS (\\textit{driver-one-ex, random})",
	"LS (\\textit{one-block-move, best-improv})",
	"LS (\\textit{one-block-move, next-improv})",
	"LS (\\textit{one-block-move, random})",
	"LS (\\textit{tour-reversal, best-improv})",
	"LS (\\textit{tour-reversal, next-improv})",
	"LS (\\textit{tour-reversal, random})",
	"GRASP",
	"VND",
	"Simulated Annealing",
]

files = [
	"deterministic.txt",
	"random.txt",
	"local_search_driver_one_ex_best_improvement.txt",
	"local_search_driver_one_ex_next_improvement.txt",
	"local_search_driver_one_ex_random.txt",
	"local_search_one_block_best_improvement.txt",
	"local_search_one_block_next_improvement.txt",
	"local_search_one_block_random.txt",
	"local_search_tour_reversal_best_improvement.txt",
	"local_search_tour_reversal_next_improvement.txt",
	"local_search_tour_reversal_random.txt",
	"grasp.txt",
	"vnd.txt",
	"simulated_annealing.txt",
]


print(instance)

for i in range(len(files)):

	file_name = files[i]

	fp = open("res_copy/"+file_name, 'r')

	line = fp.readline().strip().replace(",", "").split()
	while line:
		if line[0] == instance:
			infeas = ""
			if len(line) >= 4:
				if line[3] == "infeasible":
					infeas = "$\\times$"
			if can_be_infeas:
				print("{} & {} & {} & {} \\\\ \\hline".format(
						names[i],
						line[1], 
						line[2], 
						infeas
					)
				)
			else:
				print("{} & {} & {} \\\\ \\hline".format(
						names[i],
						line[1], 
						line[2]
					)
				)
		line = fp.readline().strip().replace(",", "").split()

	fp.close()