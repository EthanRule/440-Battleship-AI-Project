import os
import numpy as np
import matplotlib.pyplot as plt
from utils import *

class AI:
    def __init__(self, env, samples, ai_type, priority=5):
        """
        Initialize AI object.

        Args:
            env: Environment object representing the game environment.
            samples (int): Number of simulations to run.
            priority (int): Priority to give simulations that intersect hits.
        """
        self.env = env
        self.move_sim = samples
        self.ai_type = ai_type
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
    
    def hunt_target(self, attack_board, ships):
        """
        Implement the Hunt/Target algorithm for Battleship.

        Args:
            attack_board (AttackBoard): The attack board.
            ships (list): List of ship lengths.
            _ (str): Placeholder for consistency with monte_carlo method.

        Returns:
            np.ndarray: Array of probabilities for each square on the board.
        """
        probs = np.zeros((attack_board.size, attack_board.size))

        # If there are hits that have not been part of a destroyed ship, target them
        for x, y in attack_board.hits:
            if attack_board.get_board()[x, y] != attack_board.inv_square_states['destroyed']:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= x + dx < attack_board.size and 0 <= y + dy < attack_board.size:
                        probs[x + dx, y + dy] += 1

        # Hunt for ships. Checks diagonally for ships
        if np.sum(probs) == 0:
            for ship in ships:
                for x in range(attack_board.size):
                    for y in range(attack_board.size):
                        if x + ship <= attack_board.size:
                            if all(attack_board.get_board()[x + dx, y] == attack_board.inv_square_states['unknown'] for dx in range(ship)):
                                for dx in range(ship):
                                    probs[x + dx, y] += 1
                        if y + ship <= attack_board.size:
                            if all(attack_board.get_board()[x, y + dy] == attack_board.inv_square_states['unknown'] for dy in range(ship)):
                                for dy in range(ship):
                                    probs[x, y + dy] += 1
        return probs

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
    
    def move(self, ships):
        """
        Make a move using the Monte Carlo simulation algorithm.

        Returns:
            tuple: Result of the move.
        """
        if self.ai_type == 'monte_carlo':
            return self.env.step(self.monte_carlo(self.env.attack_board, ''))
        elif self.ai_type == 'hunt_target':
            return self.env.step(self.hunt_target(self.env.attack_board, ships))
        else:
            raise ValueError(f"Invalid AI type: {self.ai_type}")
