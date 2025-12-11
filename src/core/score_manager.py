import json
import os

SCORE_FILE = "high_score.json"

class ScoreManager:
    def __init__(self):
        self.high_score = self.load_high_score()

    def load_high_score(self):
        if not os.path.exists(SCORE_FILE):
            return 0
        try:
            with open(SCORE_FILE, "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except:
            return 0

    def save_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            try:
                with open(SCORE_FILE, "w") as f:
                    json.dump({"high_score": self.high_score}, f)
            except Exception as e:
                print(f"Error saving high score: {e}")
            return True
        return False

    def get_high_score(self):
        return self.high_score
