from board import DefenseBoard, AttackBoard, SimulationBoard
import numpy as np

class Game:
    def __init__(self, size, ships):
        """
        Initialize the game environment.

        Args:
            size (int): Size of the game board (size * size).
            ships (list): List of ship lengths.
        """
        self.size = size
        self.ships = ships
        self.defense_board = DefenseBoard(self.size, self.ships)  # Initialize defense board
        self.attack_board = AttackBoard(self.defense_board)  # Initialize attack board
        self.simulate_board = SimulationBoard(self.attack_board)  # Initialize simulation board
        self.attack_board.print_board("=Initial State=")  # Print initial state of the attack board

        self.count = 0  # Counter to track the number of moves made by the agent

    def reset(self):
        """
        Reset the game environment.

        Returns:
            AttackBoard: The initial state of the attack board.
        """
        self.__init__(self.size, self.ships)  # Reinitialize the game environment
        return self.attack_board  # Return the initial state of the attack board

    def step(self, probs):
        """
        Take a step in the game environment.

        Args:
            probs (np.ndarray): Array of probabilities for each square on the board.

        Returns:
            AttackBoard: The updated state of the attack board.
            str: Outcome of the step (hit or miss).
            bool: Whether the game is finished or not.
        """
        x, y = np.unravel_index(probs.argmax(), probs.shape)  # Find the square with highest probability

        # Keep choosing squares until a legal hit is found
        while not self.attack_board.legal_hit(x, y):
            probs[x, y] = 0  # Set the probability of this square to 0
            x, y = np.unravel_index(probs.argmax(), probs.shape)  # Find the square with next highest probability

        outcome, done = self.attack_board.send_hit(x, y)  # Send a hit to the defense board

        return self.attack_board, outcome, done  # Return the updated attack board, outcome, and game status
