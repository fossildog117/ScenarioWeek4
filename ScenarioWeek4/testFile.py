
"""
Run this file to start the program
"""

import time
from ScenarioWeek4 import GreedyDynamicSchedule as gs

start_time = time.time()
gs.start()
# gs.GenerateCycle()
# gs.greedy()
print("--- %s seconds ---" % (time.time() - start_time))