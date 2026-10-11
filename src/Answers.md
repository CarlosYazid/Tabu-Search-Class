# Respuestas

### TODO 1: Vecindario

```python
def vecindario(n):
    """N(x): intercambiar dos centros CONSECUTIVOS del tour. Cada movimiento es la pareja (i, i + 1).
    Devuelve la lista con TODOS los movimientos posibles para un tour de n centros."""
    return [(i, i + 1) for i in range(n - 1)]
```

### TODO 2: Es tabu?

```python
def es_tabu(x, mov, lista_tabu, it):
    """¿El movimiento (i, j) está prohibido en la iteración `it`?
    Está prohibido si dejaría a algún centro en una posición que aún es tabú."""
    i, j = mov
    a, b = x[i], x[j]
    return lista_tabu.get((a, j), 0) >= it or lista_tabu.get((b, i), 0) >= it
```

### TODO 3: Actualizar tabu

```python
def actualizar_lista_tabu(x, mov, lista_tabu, it, tenencia):
    """Registra el movimiento (i, j) que se va a ejecutar sobre x (x es la solución ANTES de moverse).
    Prohíbe devolver cada centro intercambiado a la posición que acaba de dejar."""
    i, j = mov
    lista_tabu[(x[i], i)] = it + tenencia
    lista_tabu[(x[j], j)] = it + tenencia
```

### TODO 4: Busqueda tabu

```python
def busqueda_tabu(tenencia, iteraciones, sin_mejora, aspiracion, rng, mostrar=False):
    n = len(CLIENTES)
    x = solucion_aleatoria(rng)
    fx = costo(x)
    inicial = fx
    mejor_x, mejor_f = x[:], fx
    lista_tabu = {}
    historial = {"actual": [fx], "mejor": [fx], "empeora": [], "aspiracion": []}
    visitadas = {tuple(x)}
    evaluaciones = 0
    ultima_mejora = it = 0
    if mostrar:
        print(f"Solución inicial (aleatoria): costo = {fx} min\n")

    for it in range(1, iteraciones + 1):
        candidatos, mejor_fy = [], None
        for mov in vecindario(n):
            fy = costo(aplicar(x, mov))
            evaluaciones += 1
            tabu = es_tabu(x, mov, lista_tabu, it)
            if tabu and not (aspiracion and fy < mejor_f):
                continue
            if mejor_fy is None or fy < mejor_fy:
                candidatos, mejor_fy = [(mov, tabu)], fy
            elif fy == mejor_fy:
                candidatos.append((mov, tabu))
        if not candidatos:
            if mostrar:
                print(f"  iteración {it}: no hay movimientos permitidos, la búsqueda se bloquea "
                      f"(si pasa desde la iteración 1, revisa el TODO 4)")
            break

        mov, es_aspiracion = candidatos[rng.integers(len(candidatos))]
        i, j = mov
        a, b = x[i], x[j]
        fx_anterior = fx

        actualizar_lista_tabu(x, mov, lista_tabu, it, tenencia)
        x = aplicar(x, mov)
        fx = mejor_fy

        if fx < mejor_f:
            mejor_x, mejor_f = x[:], fx
            ultima_mejora = it

        visitadas.add(tuple(x))
        historial["actual"].append(fx)
        historial["mejor"].append(mejor_f)
        if fx > fx_anterior:
            historial["empeora"].append(it)
        if es_aspiracion:
            historial["aspiracion"].append(it)

        if mostrar:
            if it <= MOSTRAR_ITERACIONES:
                nota = ""
                if es_aspiracion:
                    nota = "  <- ASPIRACIÓN: era tabú, pero da un nuevo mejor"
                elif fx > fx_anterior:
                    nota = "  <- EMPEORA: ningún vecino permitido mejora, igual se acepta"
                elif ultima_mejora == it:
                    nota = "  <- nuevo mejor"
                activos = [f"{CORTOS[c]}@{p}" for (c, p), hasta in lista_tabu.items() if hasta > it]
                print(f"  iteración {it:3d}: {CORTOS[a]} (pos {i}) <-> {CORTOS[b]} (pos {j})"
                      f" | costo {fx_anterior:4d} -> {fx:4d}{nota}")
                print(f"                  lista tabú ({len(activos)}): {activos}")
            elif ultima_mejora == it:
                print(f"  iteración {it:3d}: nuevo mejor -> costo = {mejor_f}")
            if it == MOSTRAR_ITERACIONES:
                print("  ... (desde aquí solo se muestran los nuevos mejores)")

        if it - ultima_mejora >= sin_mejora:
            if mostrar:
                print(f"  {sin_mejora} iteraciones sin mejorar: se detiene en la iteración {it}")
            break

    historial["visitadas"] = len(visitadas)
    historial["evaluaciones"] = evaluaciones
    return mejor_x, mejor_f, inicial, it, historial
```