import json
import os

CONFIG_FILE = "settings.json"
DEFAULT_CONFIG = {
    "resolution": [1000, 700],
    "volume": 0.5
}

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return DEFAULT_CONFIG.copy()
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                # Merge with default to ensure all keys exist
                config = DEFAULT_CONFIG.copy()
                config.update(data)
                return config
        except:
            return DEFAULT_CONFIG.copy()

    def save_config(self, key, value):
        self.config[key] = value
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key):
        return self.config.get(key, DEFAULT_CONFIG.get(key))
