import json
import os

class GameStorage:
    def __init__(self, filename='saves/game_data.json'):
        self.filename = filename

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {}

    def save(self, data):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)