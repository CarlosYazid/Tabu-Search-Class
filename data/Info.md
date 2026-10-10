# About data

This dataset provides all required inputs to formulate and solve a Capacitated Vehicle Routing Problem (CVRP) for vaccine and medical-supply distribution from a central depot (MSO) to ten health centers in Tripoli, Libya. It includes a complete 11×11 time matrix, 11×11 distance matrix, demand values for each facility, and fleet parameters used to model optimal distribution routes with Google OR-Tools.

The objective of the dataset is to support research in public-health logistics, route optimization, vehicle routing heuristics, and real-world CVRP benchmarking. The dataset is designed for reproducible experiments involving total-time minimization, cost analysis, and capacity-constrained distribution.

This dataset was used to compute optimized routes using OR-Tools with PATH_CHEAPEST_ARC and GUIDED_LOCAL_SEARCH, producing feasible delivery routes that satisfy all demand while minimizing time. It is suitable for students, researchers, and practitioners in transportation science, operations research, and humanitarian logistics.

The dataset includes:

- Location & Demand Table 11 nodes (MSO depot + 10 health centers) Total demand: 38,000 units Per-center demand used to enforce capacity ≤ 6,000 units per vehicle

- Time Matrix (minutes) 11×11 symmetric travel time matrix Used directly as OR-Tools arc cost (solver objective = minimize total time)

- Distance Matrix (kilometers) 11×11 distance matrix Used for reporting and operating cost calculations Not used as the optimization objective

- Fleet Parameters 15 vehicles Capacity: 6,000 units each Depot index: 0 Cost per km: 0.8 Cost per minute: 0.3

This dataset is suitable for: CVRP and VRP benchmarking Public-health distribution modeling OR-Tools VRP tutorials and demonstrations Route optimization algorithm comparison GIS-free transportation modeling Cost optimization studies