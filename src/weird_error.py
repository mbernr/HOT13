giulio@giulio-PC:~/Documents/repo/HOT13/src$ python3 experiment_giulio.py 
ga and then plugging the 10 best in vnd, then returning best of the resulting
Traceback (most recent call last):
  File "experiment_giulio.py", line 36, in <module>
    vnd(hof[i], [TourReversal(),  DriverOneExchange(), OneBlockMove()], max_iterations = 100,  max_time=10, using_delta_eval=True)	
  File "/home/giulio/Documents/repo/HOT13/src/search.py", line 46, in vnd
    if ns[i].move(sol, step_function=step_function, using_delta_eval=using_delta_eval):
  File "/home/giulio/Documents/repo/HOT13/src/neighbourhood_structures.py", line 45, in move
    self.apply(sol, best["pos1"], best["pos2"])
  File "/home/giulio/Documents/repo/HOT13/src/neighbourhood_structures.py", line 16, in apply
    sol.calc_objective()
  File "/home/giulio/Documents/repo/HOT13/src/hot_solution.py", line 53, in calc_objective
    self.calc_driver_distances()
  File "/home/giulio/Documents/repo/HOT13/src/hot_solution.py", line 67, in calc_driver_distances
    self.driver_distances[driver] += dist
TypeError: list indices must be integers or slices, not numpy.float64
Error in sys.excepthook:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 63, in apport_excepthook
    from apport.fileutils import likely_packaged, get_recent_crashes
  File "/usr/lib/python3/dist-packages/apport/__init__.py", line 5, in <module>
    from apport.report import Report
  File "/usr/lib/python3/dist-packages/apport/report.py", line 30, in <module>
    import apport.fileutils
  File "/usr/lib/python3/dist-packages/apport/fileutils.py", line 23, in <module>
    from apport.packaging_impl import impl as packaging
  File "/usr/lib/python3/dist-packages/apport/packaging_impl.py", line 24, in <module>
    import apt
  File "/usr/lib/python3/dist-packages/apt/__init__.py", line 23, in <module>
    import apt_pkg
ModuleNotFoundError: No module named 'apt_pkg'

Original exception was:
Traceback (most recent call last):
  File "experiment_giulio.py", line 36, in <module>
    vnd(hof[i], [TourReversal(),  DriverOneExchange(), OneBlockMove()], max_iterations = 100,  max_time=10, using_delta_eval=True)	
  File "/home/giulio/Documents/repo/HOT13/src/search.py", line 46, in vnd
    if ns[i].move(sol, step_function=step_function, using_delta_eval=using_delta_eval):
  File "/home/giulio/Documents/repo/HOT13/src/neighbourhood_structures.py", line 45, in move
    self.apply(sol, best["pos1"], best["pos2"])
  File "/home/giulio/Documents/repo/HOT13/src/neighbourhood_structures.py", line 16, in apply
    sol.calc_objective()
  File "/home/giulio/Documents/repo/HOT13/src/hot_solution.py", line 53, in calc_objective
    self.calc_driver_distances()
  File "/home/giulio/Documents/repo/HOT13/src/hot_solution.py", line 67, in calc_driver_distances
    self.driver_distances[driver] += dist
TypeError: list indices must be integers or slices, not numpy.float64
