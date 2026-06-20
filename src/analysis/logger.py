"""
MetricsLogger: records one row of numbers per training episode.

This is different from print() logging — it collects structured data (reward,
steps taken, whether the agent solved the maze, exploration rate) and can write
it to a CSV file that plots.py can turn into charts.
"""

import csv
from pathlib import Path


FIELDNAMES = ["episode", "reward", "steps", "success", "epsilon"]


class MetricsLogger:
    """Collects per-episode metrics in memory, then writes them to a CSV file."""

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
        """Average reward over the last `window` episodes."""
        if not self.rows:
            return 0.0
        recent = self.rows[-window:]
        return sum(r["reward"] for r in recent) / len(recent)

    def recent_success_rate(self, window=100):
        """Fraction of episodes solved over the last `window` episodes."""
        if not self.rows:
            return 0.0
        recent = self.rows[-window:]
        return sum(r["success"] for r in recent) / len(recent)

    def to_csv(self, path):
        """Write all collected rows to a CSV file. Returns the path."""
        out_path = Path(path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(self.rows)
        return out_path
