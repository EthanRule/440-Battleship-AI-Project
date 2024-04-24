import numpy as np
from utils import place_random_ship

# The icons/keys used to represent board display
chars = {'unknown': '■',
         'hit': 'X',
         'miss': '□',
         'sea': '■',
         'destroyed': '*'}

class Board:
    def __init__(self, size):
        """
        Initialize the game board.

        Args:
            size (int): Size of the board.
        """
        self.size = size
        self.board = np.zeros((size, size), dtype=np.int8)

    def get_board(self, copy=False):
        """
        Get the game board.

        Args:
            copy (bool): Whether to return a copy of the board or not.

        Returns:
            np.ndarray: The game board.
        """
        if copy:
            return self.board.copy()
        else:
            return self.board

    def print_board(self, text):
        """
        Print the game board to the console.

        Args:
            text (str): Text to display before the board.
        """
        print(text)
        print("   ", end='')
        for i in range(self.size):
            print(i + 1, end=' ')
        print('')
        for i, row in enumerate(self.board):
            print(chr(i + 65), end='  ')
            for square in row:
                print(chars[self.square_states[square]], end=' ')
            print('')

class DefenseBoard(Board):
    def __init__(self, size, ships_array):
        """
        Initialize the defense board.

        Args:
            size (int): Size of the board.
            ships_array (list): List of ship lengths.
        """
        super().__init__(size)
        self.attack_board = None
        self.square_states = {0: 'sea',
                              1: 'ship'}
        self.inv_square_states = {v: k for k, v in self.square_states.items()}
        self.ships = []
        self.available_ships = ships_array
        self.init_from_array()

    def init_from_array(self):
        """Place ships on the board randomly."""
        for ship_length in self.available_ships:
            place_random_ship(self, ship_length, [self.inv_square_states['ship']])

class AttackBoard(Board):
    def __init__(self, defense_board):
        """
        Initialize the attack board.

        Args:
            defense_board (DefenseBoard): The defense board.
        """
        super().__init__(defense_board.size)
        self.defense_board = defense_board
        self.squares_left = np.sum(self.defense_board.get_board())
        self.ship_counts = self.defense_board.available_ships.copy()
        self.hits = []
        self.square_states = {0: 'unknown',
                              1: 'hit',
                              2: 'destroyed',
                              3: 'miss'}
        self.inv_square_states = {v: k for k, v in self.square_states.items()}

    def send_hit(self, x, y):
        """
        Send a hit to the defense board.

        Args:
            x (int): X-coordinate of the hit.
            y (int): Y-coordinate of the hit.

        Returns:
            tuple: Outcome of the hit and whether the game is over.
        """
        assert self.legal_hit(x, y), "Invalid attack square"
        if self.defense_board.get_board()[x, y] == self.defense_board.inv_square_states['ship']:
            self.get_board()[x, y] = self.inv_square_states['hit']
            self.hits.append((x, y))
            self.squares_left -= 1
            for i, ship in enumerate(self.defense_board.ships):
                if (x, y) in ship:
                    self.ship_counts[i] -= 1
                if self.ship_counts[i] == 0:
                    for crds in ship:
                        self.get_board()[crds[0], crds[1]] = self.inv_square_states['destroyed']
            return 'hit', self.squares_left == 0
        self.get_board()[x, y] = self.inv_square_states['miss']
        return 'miss', False

    def legal_hit(self, x, y):
        """
        Check if the hit is legal.

        Args:
            x (int): X-coordinate of the hit.
            y (int): Y-coordinate of the hit.

        Returns:
            bool: True if the hit is legal, False otherwise.
        """
        return (0 <= x < self.size and 0 <= y < self.size and
                self.get_board()[x, y] == self.inv_square_states['unknown'])

class SimulationBoard(Board):
    def __init__(self, attack_board):
        """
        Initialize the simulation board.

        Args:
            attack_board (AttackBoard): The attack board.
        """
        super().__init__(attack_board.size)
        self.attack_board = attack_board
        self.board = self.attack_board.get_board(copy=True)
        self.square_states = {0: 'unknown',
                              1: 'hit',
                              2: 'destroyed',
                              3: 'miss',
                              4: 'ship'}
        self.inv_square_states = {v: k for k, v in self.square_states.items()}
        self.ships = []

    def simulate_ship(self):
        """Simulate the placement of a ship."""
        index = np.random.choice(np.nonzero(self.attack_board.ship_counts)[0])
        length = self.attack_board.defense_board.available_ships[index]
        place_random_ship(self, length, [self.inv_square_states['miss'], self.inv_square_states['destroyed']])
        intersect = sum(1 for coord in self.ships[0] if coord in self.attack_board.hits)
        if intersect == len(self.ships[0]):
            intersect = 0
        sim_board = self.get_board(copy=True)
        sim_board[sim_board != self.inv_square_states['ship']] = 0
        return sim_board, intersect

    def update(self, attack_board):
        """
        Update the simulation board.

        Args:
            attack_board (AttackBoard): The updated attack board.
        """
        self.__init__(attack_board)
