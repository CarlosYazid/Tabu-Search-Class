
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