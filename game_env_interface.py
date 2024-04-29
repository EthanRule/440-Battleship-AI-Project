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
        # Initialize game parameters
        self.size = size
        self.ships = ships
        
        # Initialize game boards
        self.defense_board = DefenseBoard(self.size, self.ships)  # Initialize defense board
        self.attack_board = AttackBoard(self.defense_board)  # Initialize attack board
        self.simulate_board = SimulationBoard(self.attack_board)  # Initialize simulation board
        
        # Print initial state of the attack board
        self.attack_board.print_board("-----Initial State-----")

        # Counter to track the number of moves made by the agent
        self.count = 0  

    def reset(self):
        """
        Reset the game environment.

        Returns:
            AttackBoard: The initial state of the attack board.
        """
        # Reinitialize the game environment
        self.__init__(self.size, self.ships)  
        
        # Return the initial state of the attack board
        return self.attack_board  

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
        # Find the square with highest probability
        x, y = np.unravel_index(probs.argmax(), probs.shape)  

        # Keep choosing squares until a legal hit is found
        while not self.attack_board.legal_hit(x, y):
            probs[x, y] = 0  # Set the probability of this square to 0
            x, y = np.unravel_index(probs.argmax(), probs.shape)  # Find the square with next highest probability

        # Send a hit to the defense board and get outcome and game status
        outcome, done = self.attack_board.send_hit(x, y)  

        # Return the updated attack board, outcome, and game status
        return self.attack_board, outcome, done  
