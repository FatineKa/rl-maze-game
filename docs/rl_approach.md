# Reinforcement learning approach

The agent learns to reach the goal tile from the spawn by trial and error,
guided only by the reward signal. No path is ever given to it.

## The problem

- **State:** which cell the agent is on (one integer).
- **Actions:** move up, down, left, or right one tile.
- **Reward:** a small penalty each step, a larger penalty for bumping a wall,
  and a big payoff for reaching the goal. Optional distance shaping adds a tiny
  bonus for moving closer. All weights are in `config.yaml`.
- **Episode end:** terminates on reaching the goal; truncates at `max_steps`.

Because reward is mostly negative until the goal is found, the agent is pushed
to find the *shortest* reliable route, not just *a* route.

## Algorithms

Three policies share one interface, so they're interchangeable from the training
loop's point of view.

### Random (baseline)
Picks uniformly at random, learns nothing. It exists to answer "is the task
actually being learned, or would chance do as well?" On this maze it solves only
a small fraction of episodes.

### SARSA (on-policy)
Tabular temporal-difference control like Dyna-Q, but it bootstraps from the
action it *actually takes next* rather than the best action — so it learns the
value of the exploratory policy it follows (on-policy). Without planning it's
less sample-efficient here (it needs ~1000 episodes to a clean greedy solve vs
Dyna-Q's ~120), but it's the canonical on-policy counterpart. See
`docs/on_policy_vs_off_policy.pdf` for the full math.

### Dyna-Q (default)
Tabular Q-learning plus planning. Every real step does a Q-update **and** a
handful of simulated updates replayed from a learned model of the environment.
Since the maze is deterministic the model is exact, so planning propagates
reward back along a path far faster than Q-learning alone. This is the right
tool for small, discrete worlds like the current 20x15 grid.

Key knobs (`config.yaml` -> `rl.dyna_q`): `alpha` (learning rate),
`planning_steps` (simulated updates per real step), and the shared `gamma`.

### DQN
A small MLP that maps a one-hot state to a Q-value per action, with experience
replay and a target network. Overkill for one fixed maze, but it's the path to
larger or procedurally generated worlds where a table no longer fits.

Key knobs (`config.yaml` -> `rl.dqn`): `learning_rate`, `batch_size`,
`replay_capacity`, `target_update_freq`, `hidden_sizes`.

## Exploration

All learning policies are epsilon-greedy. Epsilon starts high (mostly random),
and decays geometrically toward a floor after each episode, so the agent
explores early and exploits what it has learned later. The schedule lives in the
`Agent`, not the policies.

## Running it

    python -m src.rl.train                 # train with config defaults (Dyna-Q)
    python -m src.rl.train --agent random  # baseline for comparison
    python -m src.rl.train --episodes 300 --plot
    python -m src.rl.evaluate models/dyna_q_final   # evaluate a checkpoint
    python -m src.rl.watch --agent dyna_q           # watch the trained agent solve it
