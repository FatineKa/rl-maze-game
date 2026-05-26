# RL Maze Game

A 2D dungeon explorer where you wander shadowed corridors alongside a learning
shade — an AI that doesn't follow a script, but figures the maze out as it goes.

Built with Pygame, Gymnasium, and PyTorch.

## The premise

RL Maze Game is half game, half experiment. The player walks through a procedurally
arranged dungeon: walls, doors, rooms, the occasional pocket of loot. Somewhere
in there, an agent walks too. It doesn't know the maze any better than you do.
It learns.

Underneath, it's a reinforcement learning policy — swappable between Dyna-Q
for small worlds, DQN for larger ones, and actor-critic methods when training
time permits. The agent can also be trained headlessly without the game window.

## Setup

Requires Python 3.11 and Miniconda.

    conda create -n rl-maze-game python=3.11
    conda activate rl-maze-game
    pip install -r requirements.txt

## Running

    conda activate rl-maze-game
    python src/main.py

## Project layout

    src/game/             core game logic, no rendering
    src/rendering/        all Pygame drawing
    src/env/              Gymnasium wrapper around the game
    src/rl/               agents, policies, training, evaluation
    src/analysis/         logging and plots
    src/utils/            config, asset loading

Design notes and architecture decisions live in `docs/`.

## Status

Early. The skeleton stands; the corridors are still being drawn.