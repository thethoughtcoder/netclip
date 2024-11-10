import socket
import threading
import logging
from typing import Dict, Set
from encryption import Encryption
from utils import load_config, create_message, parse_message, save_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClipboardServer:
    def __init__(self):
        self.config = load_config()
        self.encryption = Encryption(self.config['security']['encryption_key'].encode())
        
        # If we generated a new key, save it to config
        if self.config['security']['encryption_key'] == 'generate_random_key_here':
            self.config['security']['encryption_key'] = self.encryption.get_key().decode()
            # Save updated config to file
            save_config(self.config)
        
        self.clients: Dict[socket.socket, str] = {}
        self.pending_approvals: Set[socket.socket] = set()
        self.clipboard_content = b''
        
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.config['server']['host'], self.config['server']['port']))
        server.listen(self.config['server']['max_clients'])
        
        logger.info(f"Server started on {self.config['server']['host']}:{self.config['server']['port']}")
        
        while True:
            client, address = server.accept()
            if self._is_allowed(address[0]):
                threading.Thread(target=self._handle_client, args=(client, address)).start()
            else:
                client.close()
                logger.warning(f"Rejected connection from {address[0]}")

    def _is_allowed(self, ip: str) -> bool:
        allowed_ips = self.config['server']['allowed_ips']
        return not allowed_ips or ip in allowed_ips

    def _handle_client(self, client: socket.socket, address: tuple):
        if self.config['server']['require_approval']:
            self.pending_approvals.add(client)
            logger.info(f"Waiting for approval: {address[0]}")
            # In a real implementation, you'd notify admin and wait for approval
            self.pending_approvals.remove(client)
            
        self.clients[client] = address[0]
        logger.info(f"New connection from {address[0]}")
        
        try:
            while True:
                message = client.recv(self.config['server']['max_content_size'])
                if not message:
                    break
                    
                decoded = parse_message(message)
                if decoded['type'] == 'clipboard':
                    decrypted = self.encryption.decrypt(decoded['content'])
                    self.clipboard_content = decrypted
                    self._broadcast(client, decrypted)
                    
        except Exception as e:
            logger.error(f"Error handling client {address[0]}: {e}")
        finally:
            client.close()
            del self.clients[client]
            logger.info(f"Client disconnected: {address[0]}")

    def _broadcast(self, sender: socket.socket, content: bytes):
        encrypted = self.encryption.encrypt(content)
        message = create_message('clipboard', encrypted)
        
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message)
                except:
                    pass

if __name__ == '__main__':
    server = ClipboardServer()
    server.start() 