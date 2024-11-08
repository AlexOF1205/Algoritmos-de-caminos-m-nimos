import osmnx as ox
import matplotlib.pyplot as plt
import time

# CREAR MAPA
lugar = "Xalapa, Veracruz"
Grafico = ox.load_graphml("C:/Users/adof1/xalapa.graphml")
Grafico_utm = ox.project_graph(Grafico)


# VER VECINOS, DISTANCIA
def vecino(nodo1):
    resultados = []
    for nodo2 in Grafico.neighbors(nodo1):
        arista = Grafico.get_edge_data(nodo1, nodo2)
        distancia = arista[0].get("length", float('inf'))
        resultados.append((nodo2, distancia))
    return resultados


# ALGORITMO DIJKSTRA
def dijkstra_visual(nodo_inicio, nodo_fin):
    # Inicialización
    lista_por_explorar = [(0, nodo_inicio)]
    costos = {nodo_inicio: 0}
    padres = {nodo_inicio: None}
    explorados = []

    fig, ax = ox.plot_graph(Grafico_utm, show=False, close=False)  # Preparar el mapa

    while lista_por_explorar:
        lista_por_explorar.sort()
        costo_actual, nodo_actual = lista_por_explorar.pop(0)
        explorados.append(nodo_actual)
        x, y = Grafico_utm.nodes[nodo_actual]['x'], Grafico_utm.nodes[nodo_actual]['y']
        ax.plot(x, y, 'o', color='orange', markersize=5, alpha=0.7)

        if nodo_actual == nodo_fin:
            break

        for nodo_vecino, distancia in vecino(nodo_actual):
            nuevo_costo = costos[nodo_actual] + distancia

            if nodo_vecino not in costos or nuevo_costo < costos[nodo_vecino]:
                costos[nodo_vecino] = nuevo_costo
                lista_por_explorar.append((nuevo_costo, nodo_vecino))
                padres[nodo_vecino] = nodo_actual

    # RECONSTRUCCIÓN FINAL
    camino = []
    nodo = nodo_fin
    while nodo is not None:
        camino.append(nodo)
        nodo = padres.get(nodo)
    camino.reverse()

    # CAMINO AZUL
    camino_x = [Grafico_utm.nodes[nodo]['x'] for nodo in camino]
    camino_y = [Grafico_utm.nodes[nodo]['y'] for nodo in camino]
    ax.plot(camino_x, camino_y, linewidth=2, color='blue', alpha=0.7, label='Camino final')

    x_inicio, y_inicio = Grafico_utm.nodes[nodo_inicio]['x'], Grafico_utm.nodes[nodo_inicio]['y']
    x_fin, y_fin = Grafico_utm.nodes[nodo_fin]['x'], Grafico_utm.nodes[nodo_fin]['y']

    ax.plot(x_inicio, y_inicio, 'go', markersize=5, label='Nodo Inicial')
    ax.plot(x_fin, y_fin, 'ro', markersize=5, label='Nodo Final')

    plt.legend()
    plt.show()
    return camino

def distancia_camino(camino):
    distancia_total = 0
    for i in range(len(camino) - 1):
        nodo1 = camino[i]
        nodo2 = camino[i + 1]
        arista = Grafico.get_edge_data(nodo1, nodo2)
        distancia_total += arista[0].get("length", float('inf'))
    return distancia_total

# INICIO
start_time = time.time()
nodo_inicio = 2703586603
nodo_fin = 8321745919
camino_encontrado = dijkstra_visual(nodo_inicio, nodo_fin)
print("Camino encontrado: ", camino_encontrado)
distancia_total = distancia_camino(camino_encontrado)
print("Distancia total del camino:", distancia_total)
end_time = time.time()
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
