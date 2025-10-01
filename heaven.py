from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import time
import os
from datetime import datetime

# Rutas señuelo
bait_paths = [
    "/admin",
    "/wp-login",
    "/phpmyadmin",
    "/backup"
]

#crear la carpeta si no existe
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configuración del logger
logging.basicConfig(
    filename=os.path.join(logs_dir, "heven.log"),
    level=logging.INFO,
    format='%(message)s'  # Solo el mensaje plano, sin info extra
)

# Payload molesto dw 10MB
def generate_payload(size_in_mb=10):
    # Crear un patrón base más simple y repetirlo
    base_pattern = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
    pattern_size = len(base_pattern)
    payload_size = size_in_mb * 1024 * 1024  # Bytes totales

    # Calcular cuántas veces repetir el patrón
    full_repeats = payload_size // pattern_size
    remainder = payload_size % pattern_size

    # Generar el payload
    payload = base_pattern * full_repeats + base_pattern[:remainder]
    return payload

class HoneypotHandler(BaseHTTPRequestHandler):
    def log_access(self, ip, path, user_agent):
        timestamp = datetime.utcnow().isoformat()
        log_line = f"{timestamp} | {ip} | {path} | {user_agent}"
        logging.info(log_line)

    def do_GET(self):
        client_ip = self.client_address[0]
        path = self.path
        user_agent = self.headers.get('User-Agent', '-')

        self.log_access(client_ip, path, user_agent)

        if path == "/robots.txt":
            self.send_response(200)
            self.end_headers()
            content = "User-agent: *\n" + "\n".join([f"Disallow: {p}" for p in bait_paths])
            self.wfile.write(content.encode())

        elif path in bait_paths:
            time.sleep(3)  # Delay molesto
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(10 * 1024 * 1024))
            self.end_headers()
            self.wfile.write(generate_payload(10).encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found\n")

def run_server(port=8080):
    print(f"[+] Honeypot web server listening on port {port}")
    server = HTTPServer(('', port), HoneypotHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_server()
