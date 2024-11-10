import socket
import threading
import pyperclip
import time
from encryption import Encryption
from utils import load_config, create_message, parse_message
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClipboardClient:
    def __init__(self, server_host: str):
        self.config = load_config()
        self.server_host = server_host
        self.server_port = self.config['server']['port']
        self.encryption = Encryption(self.config['security']['encryption_key'].encode())
        self.socket = None
        self.last_clipboard = ''
        self.connected = False
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            self.connected = True
            logger.info(f"Connected to server at {self.server_host}:{self.server_port}")
            
            # Start listening for clipboard updates from server
            threading.Thread(target=self._receive_updates, daemon=True).start()
            # Start monitoring local clipboard
            threading.Thread(target=self._monitor_clipboard, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            self.connected = False
            
    def _receive_updates(self):
        while self.connected:
            try:
                message = self.socket.recv(self.config['server']['max_content_size'])
                if not message:
                    break
                    
                decoded = parse_message(message)
                if decoded['type'] == 'clipboard':
                    decrypted = self.encryption.decrypt(decoded['content'])
                    self.last_clipboard = decrypted.decode()
                    pyperclip.copy(self.last_clipboard)
                    
            except Exception as e:
                logger.error(f"Error receiving updates: {e}")
                break
                
        self.connected = False
        logger.info("Disconnected from server")
        
    def _monitor_clipboard(self):
        while self.connected:
            try:
                current = pyperclip.paste()
                if current != self.last_clipboard:
                    self.last_clipboard = current
                    encrypted = self.encryption.encrypt(current.encode())
                    message = create_message('clipboard', encrypted)
                    self.socket.send(message)
            except Exception as e:
                logger.error(f"Error monitoring clipboard: {e}")
            time.sleep(0.1)  # Check clipboard every 100ms

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python client.py <server_ip>")
        sys.exit(1)
        
    client = ClipboardClient(sys.argv[1])
    client.connect()
    
    # Keep the main thread running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down client...") 