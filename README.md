# RL Maze Game

A 2D dungeon explorer where you wander shadowed corridors alongside a learning
shade — an AI that doesn't follow a script, but figures the maze out as it goes.

Built with Pygame, Gymnasium, and PyTorch.

## The premise

RL Maze Game is half game, half experiment. The player walks through a procedurally
arranged dungeon: walls, doors, rooms, the occasional pocket of loot. Somewhere
in there, an agent walks too. It doesn't know the maze any better than you do.
It learns.

The agent can be companion, rival, or quiet bystander, depending on how the
session is configured. Underneath, it's a reinforcement learning policy —
swappable between Dyna-Q for the small worlds, DQN for the larger ones, and
actor-critic methods when training time permits.

The player has a face of their own. Outfits, hair, accessories — layered
sprites stitched together at runtime and saved per username, so the next time
you load the game, your traveler is dressed exactly as you left them.

## Why three things at once

The project is deliberately three layers that don't usually appear in one
codebase:

- A **game** that has to feel responsive and look intentional
- A **reinforcement learning** loop that can train headlessly on the same world
- A **system** with users, saved appearances, scores, and customization unlocks

Keeping these three honest about their own boundaries is most of the work.

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
    src/character_system/ layered appearance, catalog of items
    src/env/              Gymnasium wrapper around the game
    src/rl/               agents, training, evaluation
    src/ui/               Pygame screens (login, customize, gameplay)
    src/services/         business logic (users, scores, customization)
    src/data/             SQLite access layer
    src/utils/            logging, config, asset loading

Design notes and architecture decisions live in `docs/`.

## Status

Early. The skeleton stands; the corridors are still being drawn.