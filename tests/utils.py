from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# --------------------------------------------------------------------------- #
# Utilidades
# --------------------------------------------------------------------------- #

def evaluate_routes(data: dict, routes: list[list[int]]) -> tuple:
    """Calcula tiempo, distancia y costo de un conjunto de rutas (arcos dirigidos)."""
    total_time, total_dist = 0, 0.0
    for route in routes:
        for a, b in zip(route, route[1:]):
            total_time += data["time"][a][b]
            total_dist += data["distance"][a][b]
    cost = data["cost_per_km"] * total_dist + data["cost_per_min"] * total_time
    return routes, total_time, total_dist, cost

def solve_with_tabu_search(data: dict, params: dict) -> tuple:
    """Resuelve el CVRP con OR-Tools; la búsqueda local es Tabu Search."""

    n = len(data["names"])
    manager = pywrapcp.RoutingIndexManager(n, data["num_vehicles"], data["depot"])
    routing = pywrapcp.RoutingModel(manager)

    def time_cb(i: int, j: int) -> int:
        return data["time"][manager.IndexToNode(i)][manager.IndexToNode(j)]

    transit = routing.RegisterTransitCallback(time_cb)
    routing.SetArcCostEvaluatorOfAllVehicles(transit)

    def demand_cb(i: int) -> int:
        return data["demand"][manager.IndexToNode(i)]

    demand = routing.RegisterUnaryTransitCallback(demand_cb)
    routing.AddDimensionWithVehicleCapacity(
        demand, 0, [data["capacity"]] * data["num_vehicles"], True, "Capacity"
    )

    search = pywrapcp.DefaultRoutingSearchParameters()
    search.first_solution_strategy = params["first_solution_strategy"]
    search.local_search_metaheuristic = params["local_search_metaheuristic"]
    search.time_limit.FromSeconds(params["time_limit_seconds"])

    assignment = routing.SolveWithParameters(search)
    assert assignment is not None, "OR-Tools no encontró ninguna solución factible"

    routes: list[list[int]] = []
    for v in range(data["num_vehicles"]):
        idx, route = routing.Start(v), []
        while not routing.IsEnd(idx):
            route.append(manager.IndexToNode(idx))
            idx = assignment.Value(routing.NextVar(idx))
        route.append(manager.IndexToNode(idx))
        if len(route) > 2:  # vehículo realmente usado
            routes.append(route)
    return evaluate_routes(data, routes)
