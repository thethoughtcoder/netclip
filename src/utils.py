import yaml
import os
import json
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    config_path = get_config_path()
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def create_message(type: str, content: bytes) -> bytes:
    message = {
        'type': type,
        'content': content.hex() if isinstance(content, bytes) else content
    }
    return json.dumps(message).encode()

def parse_message(message: bytes) -> Dict[str, Any]:
    decoded = json.loads(message.decode())
    if isinstance(decoded['content'], str):
        try:
            decoded['content'] = bytes.fromhex(decoded['content'])
        except ValueError:
            pass
    return decoded 

def save_config(config: Dict[str, Any]):
    config_path = get_config_path()
    with open(config_path, 'w') as f:
        yaml.dump(config, f)

def get_config_path() -> str:
    config_path = os.getenv('CLIPBOARD_SHARE_CONFIG')
    if config_path:
        return config_path
        
    home_config = os.path.join(os.path.expanduser('~'), '.config', 'clipboard-share', 'config.yml')
    if os.path.exists(home_config):
        return home_config
        
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yml')

