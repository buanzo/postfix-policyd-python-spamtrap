#!/usr/bin/env python3
import socket
import logging
from blocklist_backend import BlocklistBackend
from config import backend_type, redis_config, sqlite_config

backend = BlocklistBackend(backend_type, redis_config if backend_type == "redis" else sqlite_config)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

def handle_request(data):
    request_data = dict(line.split('=', 1) for line in data.strip().split('\n') if line)
    logging.debug(f"Received data: {request_data}")

    if backend.is_sender_blocked(request_data.get('sender', '')):
        return "action=REJECT\n\n"
    return "action=DUNNO\n\n"

def start_server(port=10667):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', port))
        s.listen()
        logging.info(f"Policy server listening on port {port}")
        while True:
            conn, addr = s.accept()
            with conn:
                logging.debug(f"Connection from {addr}")
                data = conn.recv(4096)
                if not data:
                    break
                response = handle_request(data.decode())
                conn.sendall(response.encode())

if __name__ == '__main__':
    start_server()
