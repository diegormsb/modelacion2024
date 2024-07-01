from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from app import *

class RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)
        
        origen = query.get('origen', [''])[0]
        destino = query.get('destino', [''])[0]
        visa = query.get('visa', [''])[0] == 'true'
        preferencia = query.get('preferencia', [''])[0]

        # Verificación de aeropuertos
        if origen not in grafo.vertices or destino not in grafo.vertices:
            self._set_response()
            self.wfile.write(json.dumps({'error': 'Aeropuerto de origen o destino no válido.'}).encode('utf-8'))
            return

        if preferencia == 'barata':
            ruta, costo = dijkstra(grafo, origen, destino, visa, requerimientos_visa)
            if ruta:
                result = f"Ruta más barata: {' -> '.join(ruta)} con un costo de ${costo}"
            else:
                result = "No se encontró una ruta disponible sin visa."
        else:
            ruta = bfs(grafo, origen, destino, visa, requerimientos_visa)
            if ruta:
                result = f"Ruta con menos escalas: {' -> '.join(ruta)}"
            else:
                result = "No se encontró una ruta disponible sin visa."
        
        self._set_response()
        self.wfile.write(json.dumps({'result': result}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()
