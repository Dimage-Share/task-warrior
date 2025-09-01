import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from app import App

def loadConfig():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return None

if __name__ == "__main__":
    config = loadConfig()
    if config:
        app = App(config)
        app.run()