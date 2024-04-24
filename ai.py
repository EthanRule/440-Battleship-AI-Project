import os
import numpy as np
import matplotlib.pyplot as plt
from utils import *

class AI:
    def __init__(self, env, samples, priority=5):
        """
        Initialize AI object.

        Args:
            env: Environment object representing the game environment.
            samples (int): Number of simulations to run.
            priority (int): Priority to give simulations that intersect hits.
        """
        self.env = env
        self.move_sim = samples
        self.priority = priority

    def eval_model(self, evals):
        """
        Evaluate the model by running it multiple times and averaging the scores.

        Args:
            evals (int): Number of evaluations to perform.
        """
        scores = [self.run(i) for i in range(evals)]
        avg_score = np.mean(scores)
        print(f"Average Score: {avg_score}")

    def monte_carlo(self, state, out_path=''):
        """
        Perform Monte Carlo simulation to predict ship positions.

        Args:
            state: Current state of the board.
            out_path (str): Path to save the output heatmap image.

        Returns:
            np.array: Probabilities of a ship being at each position.
        """
        simulations = []

        for _ in range(self.move_sim):
            self.env.simulate_board.update(state)
            brd, intersect = self.env.simulate_board.simulate_ship()

            if intersect:
                for _ in range(self.priority * intersect):
                    simulations.append(brd)
            simulations.append(brd)

        simulations = np.array(simulations)
        percentages = np.mean(simulations, axis=0)

        if out_path:
            fig, axs = plt.subplots(1, 2, figsize=(8, 8))
            axs[0].imshow(percentages, cmap='hot', interpolation='nearest')
            axs[1].imshow(state.get_board() * 5, cmap='bwr', interpolation=None)
            plt.savefig(out_path)
            plt.close(fig)

        return percentages

    def run(self, r_count):
        """
        Run a game of battleships for testing purposes.

        Args:
            r_count (int): Run count for saving files.

        Returns:
            int: Score achieved in the game.
        """
        save_path = f'save_file_{r_count}'
        os.makedirs(save_path, exist_ok=True)

        s = self.env.reset()
        done = False
        count = 0

        while not done:
            count += 1
            img_path = os.path.join(save_path, f'{count}.png')
            s, done = self.env.step(self.monte_carlo(s, img_path))

        score = np.count_nonzero(s.get_board() == 0)
        print(f"SCORE: {score}")
        return score

    def move(self):
        """
        Make a move using the Monte Carlo simulation algorithm.

        Returns:
            tuple: Result of the move.
        """
        return self.env.step(self.monte_carlo(self.env.attack_board, ''))
