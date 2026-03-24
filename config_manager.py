import base64
import os

CONFIG_FILE = "config.b64"

def save_api_key(api_key: str):
    """
    Saves the API key to a base64 encoded file.
    """
    encoded = base64.b64encode(api_key.encode('utf-8')).decode('utf-8')
    with open(CONFIG_FILE, "w", encoding='utf-8') as f:
        f.write(encoded)

def load_api_key() -> str:
    """
    Loads the API key from a base64 encoded file.
    """
    if not os.path.exists(CONFIG_FILE):
        return ""
    try:
        with open(CONFIG_FILE, "r", encoding='utf-8') as f:
            encoded = f.read().strip()
            if not encoded:
                return ""
            return base64.b64decode(encoded).decode('utf-8')
    except Exception:
        return ""

def has_api_key() -> bool:
    return os.path.exists(CONFIG_FILE) and len(load_api_key()) > 0
