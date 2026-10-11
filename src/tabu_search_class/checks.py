from .utils import evaluate_routes, solve_with_tabu_search

def test_vecindario(n, vecindario, aplicar):
    """Verifica que la función vecindario() devuelva los 9 movimientos esperados."""

    movs = vecindario(n)
    assert len(movs) == 9, f"Debe haber n - 1 = 9 movimientos y hay {len(movs)}"
    assert all(j == i + 1 and 0 <= i < 9 for i, j in movs) and len(set(movs)) == 9, "Deben ser las parejas (i, i + 1)"
    
    print("TODO 1 correcto: 9 vecinos por solución")

def test_es_tabu_y_actualizar_tabu(X_ejemplo, es_tabu, actualizar_lista_tabu, aplicar):
    """Verifica que la función es_tabu() y actualizar_lista_tabu() funcionen correctamente."""
    
    lista = {}
    actualizar_lista_tabu(X_ejemplo, (0, 1), lista, it=1, tenencia=5)   # el 1 deja la posición 0 y el 2 deja la 1
    y = aplicar(X_ejemplo, (0, 1))                                 # [2, 1, 3, 4, 5, ...]

    assert lista == {(1, 0): 6, (2, 1): 6}, f"La lista tabú quedó así: {lista}"
    assert es_tabu(y, (0, 1), lista, it=2), "Deshacer el movimiento debe ser tabú en la iteración 2"
    assert es_tabu(y, (0, 1), lista, it=6), "Sigue prohibido hasta la iteración it + tenencia = 6"
    assert not es_tabu(y, (0, 1), lista, it=7), "En la iteración 7 ya no es tabú"
    assert not es_tabu(y, (3, 4), lista, it=2), "Un movimiento que no devuelve nada a su lugar no es tabú"
    assert not es_tabu(y, (1, 2), lista, it=2), "Mover el 1 a la posición 2 (no prohibida) está permitido"
    
    print("TODO 2 y 3 correctos")

def test_external_answer_coherence(data: dict, external_answer):
    """Verifica que la respuesta externa cumpla con las restricciones del CVRP."""

    n = len(data["names"])
    
    ext_routes, _, _, _ = evaluate_routes(data, external_answer)

    assert 1 <= len(ext_routes) <= data["num_vehicles"], (
        f"Se usan {len(ext_routes)} vehículos; el máximo es {data['num_vehicles']}"
    )

    visited: list[int] = []
    
    for k, route in enumerate(ext_routes):

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

    print("TODO 4 correcto: la respuesta externa es factible y coherente con el CVRP")  

def test_external_answer_quality_vs_tabu_search(
    data: dict, external_answer, tolerance: float
    ):
    
    _, ext_total_time, ext_total_dist, ext_cost = evaluate_routes(data, external_answer)

    _, ref_total_time, ref_total_dist, ref_cost = solve_with_tabu_search(data)

    gap = (ext_total_time - ref_total_time) / ref_total_time
    
    print(
        f"\nReferencia Tabu Search: {ref_total_time} min | "
        f"{ref_total_dist:.1f} km | costo {ref_cost:.2f}"
        f"\nRespuesta externa:      {ext_total_time} min | "
        f"{ext_total_dist:.1f} km | costo {ext_cost:.2f}"
        f"\nBrecha en tiempo: {gap:+.2%} (tolerancia {tolerance:.0%})"
    )

    assert gap <= tolerance, (
        f"La respuesta externa ({ext_total_time} min) supera en {gap:.2%} "
        f"a Tabu Search ({ref_total_time} min); tolerancia {tolerance:.0%}"
    )

    print(f"La respuesta es competitiva {gap:+.2%} frente a Tabu Search")