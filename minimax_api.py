import requests
from typing import Dict, List, Optional
import time

class MiniMaxAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains"

    def get_remains(long_running: bool = False) -> Optional[Dict]:
        """
        Fetches the usage information from MiniMax API.
        """
        pass # To be implemented as instance method below

    def fetch_data(self) -> Optional[Dict]:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.get(self.base_url, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}", "detail": response.text}
        except Exception as e:
            return {"error": str(e)}

def parse_model_data(data: Dict, target_model: str = "MiniMax-M*") -> Optional[Dict]:
    if not data or "model_remains" not in data:
        return None
    
    for item in data["model_remains"]:
        if item.get("model_name") == target_model:
            return item
    return None
