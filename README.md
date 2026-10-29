# Snake Reinforcement Learning

A Snake game environment and reinforcement learning agent developed in Python using Deep Q-Networks (DQN) and Double DQN.

## Overview

This project explores how a reinforcement learning agent can learn to play Snake through interaction with the environment and reward-based learning.

The environment includes multiple maps, obstacles, bonus and toxic fruits, and reward shaping to encourage more effective behavior.

## Features

- DQN and Double DQN agents
- Prioritized Experience Replay (PER)
- Target network for more stable learning
- Multiple maps with different obstacle layouts
- Bonus fruits with limited availability
- Toxic fruits with negative rewards
- Reward shaping based on Manhattan distance
- Dynamic step limit based on snake length
- CSV logging for training experiments

## Technologies

- Python
- TensorFlow / Keras
- NumPy
- Pandas
- Matplotlib

## Experiments and Logging

Training metrics are saved to CSV files, including collected fruits, steps, total reward, best score, snake length, and exploration rate (epsilon).

These logs can be used to compare training runs and analyze the agent's behavior.

## Running the Project

1. Clone the repository.
2. Install the required dependencies.
3. Run the training script.

See the project files for the exact configuration and execution instructions.

## Project Goals

The project was developed to explore reinforcement learning algorithms, environment design, reward engineering, and experimental evaluation.
