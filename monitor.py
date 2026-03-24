import time
import collections
from minimax_api import MiniMaxAPI, parse_model_data

class UsageMonitor:
    def __init__(self, api_key: str, model_name: str = "MiniMax-M*"):
        self.api = MiniMaxAPI(api_key)
        self.model_name = model_name
        self.history = collections.deque(maxlen=60) # Store (timestamp, usage_count) for the last 60 seconds
        self.current_data = None
        self.error_message = None

    def update(self):
        """
        Performs one update cycle.
        Returns True if successful, False otherwise.
        """
        raw_data = self.api.fetch_data()
        if not raw_data or "error" in raw_data:
            self.error_message = raw_data.get("error", "Unknown error") if raw_data else "No data"
            return False
        
        model_data = parse_model_data(raw_data, self.model_name)
        if not model_data:
            # Fallback: maybe the model name changed or is different in the list
            if "model_remains" in raw_data and raw_data["model_remains"]:
                model_data = raw_data["model_remains"][0]
                self.model_name = model_data["model_name"]
            else:
                self.error_message = f"Model {self.model_name} not found"
                return False

        self.current_data = model_data
        self.error_message = None
        
        usage = model_data.get("current_interval_usage_count", 0)
        self.history.append((time.time(), usage))
        return True

    def get_rpm(self) -> int:
        if len(self.history) < 2:
            return 0
        
        # Calculate diff between newest and oldest in the 60s window
        # Note: if the window is less than 60s, it's a partial RPM
        start_time, start_usage = self.history[0]
        end_time, end_usage = self.history[-1]
        
        time_diff = end_time - start_time
        if time_diff <= 0:
            return 0
            
        usage_diff = max(0, end_usage - start_usage)
        
        # Normalize to 60 seconds
        rpm = (usage_diff / time_diff) * 60
        return int(rpm)

    def get_usage_str(self) -> str:
        if not self.current_data:
            return "N/A"
        used = self.current_data.get("current_interval_usage_count", 0)
        total = self.current_data.get("current_interval_total_count", 0)
        return f"{used} / {total}"

    def get_interval_str(self) -> str:
        if not self.current_data:
            return "N/A"
        start_ms = self.current_data.get("start_time", 0)
        end_ms = self.current_data.get("end_time", 0)
        
        import datetime
        start_dt = datetime.datetime.fromtimestamp(start_ms / 1000)
        end_dt = datetime.datetime.fromtimestamp(end_ms / 1000)
        
        return f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
