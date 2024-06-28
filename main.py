class Grafo:
    def __init__(self):
        self.vertices = {}

    def agregar_vertice(self, vertice):
        if vertice not in self.vertices:
            self.vertices[vertice] = {}

    def agregar_arista(self, origen, destino, peso):
        if origen in self.vertices and destino in self.vertices:
            self.vertices[origen][destino] = peso
            self.vertices[destino][origen] = peso  # El grafo es no dirigido

# Inicialización del grafo
grafo = Grafo()

# Lista de aeropuertos
aeropuertos = ["CCS", "AUA", "BON", "CUR", "SXM", "SDQ", "SBH", "POS", "BGI", "FDF", "PTP"]

# Agregar vertices
for aeropuerto in aeropuertos:
    grafo.agregar_vertice(aeropuerto)

# Agregar aristas con sus tarifas
vuelos = [
    ("CCS", "AUA", 40), ("CCS", "CUR", 35), ("CCS", "BON", 60), ("CCS", "SXM", 300),
    ("AUA", "CUR", 15), ("AUA", "BON", 15), ("CUR", "BON", 15), ("CCS", "SDQ", 180),
    ("SDQ", "SXM", 50), ("SXM", "SBH", 45), ("CCS", "POS", 150), ("CCS", "BGI", 180),
    ("POS", "BGI", 35), ("POS", "SXM", 90), ("BGI", "SXM", 70), ("POS", "PTP", 80),
    ("POS", "FDF", 75), ("PTP", "SXM", 100), ("PTP", "SBH", 80), ("CUR", "SXM", 80),
    ("AUA", "SXM", 85)
]

for vuelo in vuelos:
    grafo.agregar_arista(vuelo[0], vuelo[1], vuelo[2])

def obtener_datos_usuario():
    origen = input("Ingrese el código del aeropuerto de origen: ").upper()
    destino = input("Ingrese el código del aeropuerto de destino: ").upper()
    visa = input("¿Tiene visa? (si/no): ").lower() == 'si'
    return origen, destino, visa

import heapq

def dijkstra(grafo, inicio, destino, visa, requerimientos_visa):
    # Inicialización
    distancias = {vertice: float('infinity') for vertice in grafo.vertices}
    distancias[inicio] = 0
    pq = [(0, inicio)]
    predecesores = {vertice: None for vertice in grafo.vertices}
    
    while pq:
        (distancia_actual, vertice_actual) = heapq.heappop(pq)
        
        if distancia_actual > distancias[vertice_actual]:
            continue
        
        for vecino, peso in grafo.vertices[vertice_actual].items():
            if not visa and requerimientos_visa[vecino]:
                continue
            
            distancia = distancia_actual + peso
            
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                predecesores[vecino] = vertice_actual
                heapq.heappush(pq, (distancia, vecino))
    
    # Reconstrucción de la ruta
    ruta = []
    paso = destino
    if distancias[paso] == float('infinity'):
        return None, float('infinity')  # No hay ruta disponible
    while paso:
        ruta.append(paso)
        paso = predecesores[paso]
    ruta.reverse()
    
    return ruta, distancias[destino]

# Requerimientos de visa para cada destino
requerimientos_visa = {
    "CCS": False, "AUA": True, "BON": True, "CUR": True, "SXM": True,
    "SDQ": True, "SBH": False, "POS": False, "BGI": False, "FDF": False, "PTP": False
}

from collections import deque

def bfs(grafo, inicio, destino, visa, requerimientos_visa):
    visitados = set()
    cola = deque([(inicio, [inicio])])
    
    while cola:
        (vertice_actual, camino) = cola.popleft()
        
        if vertice_actual in visitados:
            continue
        
        visitados.add(vertice_actual)
        
        for vecino in grafo.vertices[vertice_actual]:
            if not visa and requerimientos_visa[vecino]:
                continue
            
            if vecino == destino:
                return camino + [vecino]
            
            cola.append((vecino, camino + [vecino]))
    
    return None  # No se encontró una ruta

def main():
    origen, destino, visa = obtener_datos_usuario()

    if origen not in grafo.vertices or destino not in grafo.vertices:
        print("Aeropuerto de origen o destino no válido.")
        return

    opcion = input("¿Desea la ruta más barata o la de menos escalas? (barata/escalas): ").lower()

    if opcion == 'barata':
        ruta, costo = dijkstra(grafo, origen, destino, visa, requerimientos_visa)
        if ruta:
            print(f"Ruta más barata: {' -> '.join(ruta)} con un costo de ${costo}")
        else:
            print("No se encontró una ruta disponible sin visa.")
    else:
        ruta = bfs(grafo, origen, destino, visa, requerimientos_visa)
        if ruta:
            print(f"Ruta con menos escalas: {' -> '.join(ruta)}")
        else:
            print("No se encontró una ruta disponible sin visa.")

if __name__ == "__main__":
    main()
