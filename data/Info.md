# Acerca de los datos

Este conjunto de datos proporciona toda la información necesaria para formular y resolver un problema de rutas de vehículos con capacidad limitada (CVRP) para la distribución de vacunas y suministros médicos desde un depósito central (MSO) a diez centros de salud en Trípoli, Libia. Incluye una matriz de tiempo completa de 11×11, una matriz de distancia de 11×11, los valores de demanda para cada centro y los parámetros de la flota utilizados para modelar rutas de distribución óptimas con Google OR-Tools.

El objetivo del conjunto de datos es apoyar la investigación en logística de salud pública, optimización de rutas, heurísticas de enrutamiento de vehículos y evaluaciones comparativas del CVRP en el mundo real. El conjunto de datos está diseñado para experimentos reproducibles que involucran la minimización del tiempo total, el análisis de costos y la distribución con restricciones de capacidad.

Este conjunto de datos se utilizó para calcular rutas optimizadas mediante OR-Tools con los algoritmos PATH_CHEAPEST_ARC y GUIDED_LOCAL_SEARCH, lo que generó rutas de entrega viables que satisfacen toda la demanda al tiempo que minimizan el tiempo. Es adecuado para estudiantes, investigadores y profesionales en ciencias del transporte, investigación operativa y logística humanitaria.

El conjunto de datos incluye:

- Tabla de ubicaciones y demanda: 11 nodos (depósito de la MSO + 10 centros de salud). Demanda total: 38 000 unidades. La demanda por centro se utiliza para garantizar que la capacidad sea ≤ 6 000 unidades por vehículo

- Matriz de tiempos (minutos): matriz simétrica de tiempos de viaje de 11×11. Se utiliza directamente como costo de arco en OR-Tools (objetivo del solucionador = minimizar el tiempo total)


- Matriz de distancias (kilómetros): matriz de distancias de 11×11. Se utiliza para la generación de informes y el cálculo de costos operativos. No se utiliza como objetivo de optimización

- Parámetros de la flota: 15 vehículos. Capacidad: 6,000 unidades cada uno. Índice de depósito: 0. Costo por km: 0.8. Costo por minuto: 0.3

Este conjunto de datos es adecuado para: comparativas de CVRP y VRP; modelación de distribución en salud pública; tutoriales y demostraciones de VRP en OR-Tools; comparación de algoritmos de optimización de rutas; modelación de transporte sin SIG; estudios de optimización de costos
