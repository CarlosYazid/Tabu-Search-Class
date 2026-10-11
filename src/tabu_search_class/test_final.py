def test_data_is_consistent(data: dict):
    n = len(data["names"])
    assert n == 11 and data["depot"] == 0 and data["demand"][data["depot"]] == 0
    assert sum(data["demand"]) == 38_000
    assert data["num_vehicles"] == 15 and data["capacity"] == 6_000
    assert max(data["demand"]) <= data["capacity"]

def test_external_answer_quality_vs_tabu_search(
    data: dict, external_answer, reference: dict, tolerance: float
):
    ext = evaluate_routes(data, external_answer)
    _assert_feasible(data, ext)
    gap = (ext.total_time - reference.total_time) / reference.total_time
    print(
        f"\nReferencia Tabu Search: {reference.total_time} min | "
        f"{reference.total_distance:.1f} km | costo {reference.total_cost:.2f}"
        f"\nRespuesta externa:      {ext.total_time} min | "
        f"{ext.total_distance:.1f} km | costo {ext.total_cost:.2f}"
        f"\nBrecha en tiempo: {gap:+.2%} (tolerancia {tolerance:.0%})"
    )
    assert gap <= tolerance, (
        f"La respuesta externa ({ext.total_time} min) supera en {gap:.2%} "
        f"a Tabu Search ({reference.total_time} min); tolerancia {tolerance:.0%}"
    )

# --------------------------------------------------------------------------- #
# Validación de factibilidad
# --------------------------------------------------------------------------- #
def _assert_feasible(data: dict, routes: list[list[int]]) -> None:
    n = len(data["names"])
    assert 1 <= len(routes) <= data["num_vehicles"], (
        f"Se usan {len(routes)} vehículos; el máximo es {data['num_vehicles']}"
    )

    visited: list[int] = []
    for k, route in enumerate(routes):
        assert len(route) >= 3, f"Ruta {k} vacía o degenerada: {route}"
        assert route[0] == data["depot"] and route[-1] == data["depot"], (
            f"Ruta {k} debe iniciar y terminar en el depósito: {route}"
        )
        assert all(0 <= node < n for node in route), f"Ruta {k} con nodos inválidos: {route}"
        stops = route[1:-1]
        assert data["depot"] not in stops, f"Ruta {k} pasa por el depósito: {route}"
        load = sum(data["demand"][node] for node in stops)
        assert load <= data["capacity"], (
            f"Ruta {k} excede la capacidad: {load} > {data['capacity']}"
        )
        visited.extend(stops)

    customers = [i for i in range(n) if i != data["depot"]]
    assert sorted(visited) == customers, (
        f"Cada centro debe visitarse exactamente una vez. "
        f"Faltan: {sorted(set(customers) - set(visited))}; "
        f"repetidos: {sorted({x for x in visited if visited.count(x) > 1})}"
    )
