from flask import Flask, request, jsonify, render_template
from collections import deque

app = Flask(__name__)

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

requerimientos_visa = {
    "CCS": False, "AUA": True, "BON": True, "CUR": True, "SXM": True,
    "SDQ": True, "SBH": False, "POS": False, "BGI": False, "FDF": False, "PTP": False
}

def dijkstra(grafo, inicio, destino, visa, requerimientos_visa):
    # Inicializar las distancias de todos los nodos como infinitas, excepto el nodo de inicio que es 0
    distancias = {vertice: float('infinity') for vertice in grafo.vertices}
    distancias[inicio] = 0
    
    # Inicializar predecesores de todos los nodos como None
    predecesores = {vertice: None for vertice in grafo.vertices}
    
    # Conjunto para guardar los nodos que ya han sido visitados
    visitados = set()

    # Bucle principal hasta que todos los nodos hayan sido visitados
    while len(visitados) < len(grafo.vertices):
        vertice_actual = None
        distancia_minima = float('infinity')

        # Encontrar el nodo no visitado con la distancia más corta
        for vertice in distancias:
            if vertice not in visitados and distancias[vertice] < distancia_minima:
                vertice_actual = vertice
                distancia_minima = distancias[vertice]

        # Si no hay un nodo accesible no visitado, salir del bucle
        if vertice_actual is None:
            break

        # Marcar el nodo actual como visitado
        visitados.add(vertice_actual)

        # Explorar los vecinos del nodo actual
        for vecino, peso in grafo.vertices[vertice_actual].items():
            # Si el vecino requiere visa y el usuario no tiene visa, saltar este vecino
            if not visa and requerimientos_visa[vecino]:
                continue

            # Calcular la nueva distancia al vecino
            nueva_distancia = distancias[vertice_actual] + peso

            # Si la nueva distancia es menor, actualizar la distancia y el predecesor
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = vertice_actual

    # Reconstruir el camino desde el destino al origen
    ruta = []
    paso = destino
    if distancias[paso] == float('infinity'):
        # Si la distancia al destino es infinita, no hay camino disponible
        return None, float('infinity')
    while paso:
        ruta.append(paso)
        paso = predecesores[paso]
    ruta.reverse()  # Invertir la ruta para obtener la secuencia correcta

    # Devolver la ruta más corta y su costo total
    return ruta, distancias[destino]


def bfs(grafo, inicio, destino, visa, requerimientos_visa):
    # Conjunto para guardar los nodos que ya han sido visitados
    visitados = set()
    
    # Cola para gestionar los nodos a explorar, cada elemento es una tupla (nodo, camino hasta ese nodo)
    cola = deque([(inicio, [inicio])])

    # Bucle principal hasta que la cola esté vacía
    while cola:
        # Extraer el primer elemento de la cola
        (vertice_actual, camino) = cola.popleft()

        # Si el nodo actual ya ha sido visitado, continuar con el siguiente
        if vertice_actual in visitados:
            continue

        # Marcar el nodo actual como visitado
        visitados.add(vertice_actual)

        # Explorar los vecinos del nodo actual
        for vecino in grafo.vertices[vertice_actual]:
            # Si el vecino requiere visa y el usuario no tiene visa, saltar este vecino
            if not visa and requerimientos_visa[vecino]:
                continue

            # Si el vecino es el destino, devolver el camino actual más el vecino
            if vecino == destino:
                return camino + [vecino]

            # De lo contrario, añadir el vecino a la cola con el camino actualizado
            cola.append((vecino, camino + [vecino]))

    # Si no se encuentra el destino, devolver None
    return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ruta', methods=['GET'])
def obtener_ruta():
    origen = request.args.get('origen')
    destino = request.args.get('destino')
    visa = request.args.get('visa').lower() == 'true'
    preferencia = request.args.get('preferencia')

    if preferencia == 'barata':
        ruta, costo = dijkstra(grafo, origen, destino, visa, requerimientos_visa)
        if ruta:
            return jsonify({'result': f"Ruta más barata: {' -> '.join(ruta)} con un costo de ${costo}"})
        else:
            return jsonify({'error': 'No se encontró una ruta disponible sin visa.'})
    elif preferencia == 'escalas':
        ruta = bfs(grafo, origen, destino, visa, requerimientos_visa)
        if ruta:
            return jsonify({'result': f"Ruta con menos escalas: {' -> '.join(ruta)}"})
        else:
            return jsonify({'error': 'No se encontró una ruta disponible sin visa.'})
    else:
        return jsonify({'error': 'Preferencia de ruta no válida.'})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
