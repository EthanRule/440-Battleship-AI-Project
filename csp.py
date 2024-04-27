import numpy as np

class BattleshipCSP:
    def __init__(self, size, ship_lengths):
        self.size = size
        self.ship_lengths = ship_lengths
        self.board = np.zeros((size, size), dtype=int)  # Initialize empty board
        self.solutions = []

    def solve(self):
        self.backtrack(0)
        return self.solutions

    def backtrack(self, ship_index):
        if ship_index == len(self.ship_lengths):
            # All ships have been placed, add current solution to solutions list
            self.solutions.append(np.copy(self.board))
            return True

        for x in range(self.size):
            for y in range(self.size):
                for orientation in ['horizontal', 'vertical']:
                    if self.can_place_ship(ship_index, x, y, orientation):
                        self.place_ship(ship_index, x, y, orientation)
                        if self.backtrack(ship_index + 1):
                            return True
                        self.remove_ship(ship_index, x, y, orientation)
        return False

    def can_place_ship(self, ship_index, x, y, orientation):
        length = self.ship_lengths[ship_index]
        if orientation == 'horizontal':
            if y + length > self.size:
                return False
            for j in range(y, y + length):
                if self.board[x, j] != 0:
                    return False
        elif orientation == 'vertical':
            if x + length > self.size:
                return False
            for i in range(x, x + length):
                if self.board[i, y] != 0:
                    return False
        return True

    def place_ship(self, ship_index, x, y, orientation):
        length = self.ship_lengths[ship_index]
        if orientation == 'horizontal':
            for j in range(y, y + length):
                self.board[x, j] = ship_index + 1  # Assign ship index (starting from 1) to board cells
        elif orientation == 'vertical':
            for i in range(x, x + length):
                self.board[i, y] = ship_index + 1

    def remove_ship(self, ship_index, x, y, orientation):
        length = self.ship_lengths[ship_index]
        if orientation == 'horizontal':
            for j in range(y, y + length):
                self.board[x, j] = 0
        elif orientation == 'vertical':
            for i in range(x, x + length):
                self.board[i, y] = 0
