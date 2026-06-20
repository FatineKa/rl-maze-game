"""
Plots training performance metrics from CSV data.
"""

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Run headless without window display
import matplotlib.pyplot as plt


def _read_metrics(csv_path):
    """Parses CSV metrics into lists."""
    episodes, rewards, steps, success = [], [], [], []
    with open(csv_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            episodes.append(int(row["episode"]))
            rewards.append(float(row["reward"]))
            steps.append(int(row["steps"]))
            success.append(int(row["success"]))
    return episodes, rewards, steps, success


def _moving_average(values, window):
    """Computes a trailing moving average."""
    out = []
    running = 0.0
    for i, v in enumerate(values):
        running += v
        if i >= window:
            running -= values[i - window]
        out.append(running / min(i + 1, window))
    return out


def plot_training(csv_path, out_dir="results", window=50):
    """
    Generates and saves performance charts (reward, success rate, path steps).
    """
    episodes, rewards, steps, success = _read_metrics(csv_path)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    saved = []

    # Reward chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(episodes, rewards, color="lightsteelblue", linewidth=0.8, label="reward")
    ax.plot(episodes, _moving_average(rewards, window), color="navy",
            linewidth=1.5, label=f"{window}-ep average")
    ax.set_xlabel("episode")
    ax.set_ylabel("total reward")
    ax.set_title("Episode reward")
    ax.legend()
    saved.append(_save(fig, out / "reward.png"))

    # Success rate chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(episodes, _moving_average(success, window), color="seagreen", linewidth=1.5)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel("episode")
    ax.set_ylabel(f"success rate ({window}-ep window)")
    ax.set_title("Success rate")
    saved.append(_save(fig, out / "success_rate.png"))

    # Steps chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(episodes, steps, color="indianred", linewidth=0.8, label="steps")
    ax.plot(episodes, _moving_average(steps, window), color="darkred",
            linewidth=1.5, label=f"{window}-ep average")
    ax.set_xlabel("episode")
    ax.set_ylabel("steps to finish")
    ax.set_title("Steps per episode")
    ax.legend()
    saved.append(_save(fig, out / "steps.png"))

    return saved


def _save(fig, path):
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def main():
    parser = argparse.ArgumentParser(description="Plot training metrics from a CSV file.")
    parser.add_argument("csv", help="path to the metrics CSV (e.g. results/dyna_q_metrics.csv)")
    parser.add_argument("--out", default="results", help="output directory for PNG files")
    parser.add_argument("--window", type=int, default=50, help="moving-average window size")
    args = parser.parse_args()

    saved = plot_training(args.csv, args.out, args.window)
    for path in saved:
        print(f"Saved plot: {path}")


if __name__ == "__main__":
    main()
