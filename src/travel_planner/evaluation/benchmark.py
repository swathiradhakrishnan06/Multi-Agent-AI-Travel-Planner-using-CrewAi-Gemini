# src/travel_planner/evaluation/benchmark.py
from travel_planner.tools.flight_search import FlightSearch
from travel_planner.tools.stopover_evaluator import StopoverEvaluator

flt = FlightSearch()
stop = StopoverEvaluator()

direct = flt.run("MEL", "BLR", "2025-08-01")
all_routes = flt.run("MEL", "BLR", "2025-08-01")  # assume multi_stop flag if implemented
top2 = stop.run(all_routes, ["food","culture"])
print("Direct:", direct)
print("Top2:", top2)
