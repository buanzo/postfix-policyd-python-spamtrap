#!/usr/bin/env python3
import socket
import logging
import re
from blocklist_backend import BlocklistBackend
from config import backend_type, redis_config, sqlite_config, spamtrap_addresses, WHITELIST_DOMAINS, INCLUDE_SUBDOMAINS

backend = BlocklistBackend(backend_type, redis_config if backend_type == "redis" else sqlite_config)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

def extract_domain(email):
    return email.split('@')[-1].lower()

def is_sender_whitelisted(sender):
    sender_domain = extract_domain(sender)
    for domain in WHITELIST_DOMAINS:
        if INCLUDE_SUBDOMAINS:
            if sender_domain == domain or sender_domain.endswith('.' + domain):
                return True
        else:
            if sender_domain == domain:
                return True
    return False

def is_spamtrap(recipient):
    return recipient.lower() in spamtrap_addresses

def handle_request(data):
    request_data = dict(line.split('=', 1) for line in data.strip().split('\n') if line)
    logging.debug(f"Received data: {request_data}")

    if is_sender_whitelisted(request_data.get('sender', '')):
        logging.debug(f"Sender {request_data.get('sender', '')} is whitelisted.")
        return "action=DUNNO\n\n"
    
    if is_spamtrap(request_data.get('recipient', '')):
        if request_data.get('sender','') == '':
            # Wont spamtrap <>
            return "action=DUNNO\n\n"
        backend.add_blocked_sender(request_data.get('sender', ''))
        return "action=DISCARD\n\n"
    
    return "action=DUNNO\n\n"

def start_server(port=10666):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
