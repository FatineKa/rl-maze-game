"""
Logs structured training metrics to CSV.
"""

import csv
from pathlib import Path

FIELDNAMES = ["episode", "reward", "steps", "success", "epsilon"]


class MetricsLogger:
    """
    Collects per-episode metrics and saves them to a CSV file.
    """

    def __init__(self):
        self.rows = []

    def log_episode(self, episode, reward, steps, success, epsilon):
        self.rows.append({
            "episode": episode,
            "reward": round(reward, 4),
            "steps": steps,
            "success": int(bool(success)),
            "epsilon": round(epsilon, 4),
        })

    def recent_mean_reward(self, window=100):
        """Average reward calculated over a moving window of recent episodes."""
        if not self.rows:
            return 0.0
        recent = self.rows[-window:]
        return sum(r["reward"] for r in recent) / len(recent)

    def recent_success_rate(self, window=100):
        """Success rate calculated over a moving window of recent episodes."""
        if not self.rows:
            return 0.0
        recent = self.rows[-window:]
        return sum(r["success"] for r in recent) / len(recent)

    def to_csv(self, path):
        """Writes the collected metrics to a CSV file and returns the file path."""
        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(self.rows)
        return out_path
