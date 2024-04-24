# Battleships AI

## Introduction

This version of Battleships pits you against an AI opponent powered by Monte Carlo Simulation. Originally designed with the intention of developing a neural reinforcement learning agent, the project has yet to achieve this goal. Ideas and contributions are welcome from anyone interested in advancing this endeavor!

## Monte Carlo Simulation

### Description

The Monte Carlo Simulation operates as follows:

1. Input the current board state.
2. Create a copy of the board state.
3. Simulate a specific number of samples (defined by `--monte_carlo_samples`), each representing a random placement of a remaining ship type.
4. Stack all simulations and tally the total number of ships in each square (with emphasis on ships overlapping existing hits).
5. Calculate the mean frequency for each square, resulting in a heatmap.
6. Select the highest value corresponding to a legal move in the heatmap.
7. Repeat steps 1-6.

### Heatmap

Two heatmap GIFs, available in heatmap_gifs.

## Prerequisites

### Packages

The project utilizes only the standard library of Python 3.6, with the exception of the required `numpy` package.

### Instructions

The `main.py` file accepts the following arguments:

- `--board_size`: Size of the board (default: `10`).
- `--ship_sizes`: Array of ship sizes to randomly place (default: `5,4,3,3,2`).
- `--monte_carlo_samples`: Number of samples for the algorithm to perform (default: `10000`).

For slower computers, reduce the number of samples, though generally, 10,000 should yield good results in reasonable time. Ensure there are no spaces between integers in `ship_sizes`. Extreme board sizes may exhibit unexpected behavior; the recommended range is 5-10, with adjustments to other parameters for sizes beyond this range.

Upon execution, the game initializes two boards with randomly placed ships—one for the player and one for the computer. Square types are represented as follows:

- Sea: ■
- Hit: X
- Miss: □
- Destroyed: *

The player starts and specifies moves by providing a letter followed by a number to designate the target square.

## License

This project is licensed under the MIT license; see LICENSE.md for more details.