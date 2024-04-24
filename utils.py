import numpy as np

def place_random_ship(board, length, no_intersect):
    """
    Place a random ship on the given board of the given length, ensuring it does not intersect with anything in no_intersect.

    Args:
        board (Board): The game board.
        length (int): The length of the ship to be placed.
        no_intersect (set): Set of coordinates where ships cannot intersect.

    Returns:
        list: List of coordinates representing the placed ship.
    """
    while True:
        # Choose whether to place ship vertically or horizontally
        vertical = np.random.choice([True, False])

        # Choose starting coordinates
        start_x = np.random.randint(0, board.size)
        start_y = np.random.randint(0, board.size)

        # Calculate ending coordinates based on ship length and direction
        if vertical:
            end_x = start_x
            end_y = start_y + length - 1
        else:
            end_x = start_x + length - 1
            end_y = start_y

        # Check if ship intersects with existing ships or goes out of bounds
        if is_valid_ship_placement(board, start_x, start_y, end_x, end_y, no_intersect):
            ship_coords = place_ship(board, start_x, start_y, end_x, end_y)
            board.ships.append(ship_coords)
            return ship_coords

def is_valid_ship_placement(board, start_x, start_y, end_x, end_y, no_intersect):
    """
    Check if placing a ship with given coordinates is valid.

    Args:
        board (Board): The game board.
        start_x (int): Starting x-coordinate of the ship.
        start_y (int): Starting y-coordinate of the ship.
        end_x (int): Ending x-coordinate of the ship.
        end_y (int): Ending y-coordinate of the ship.
        no_intersect (set): Set of coordinates where ships cannot intersect.

    Returns:
        bool: True if the ship placement is valid, False otherwise.
    """
    # Check if ship is within the board boundaries
    if not (0 <= start_x < board.size and 0 <= start_y < board.size and
            0 <= end_x < board.size and 0 <= end_y < board.size):
        return False

    # Check if ship intersects with existing ships
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            if (x, y) in no_intersect:
                return False

    return True

def place_ship(board, start_x, start_y, end_x, end_y):
    """
    Place a ship on the board with given coordinates.

    Args:
        board (Board): The game board.
        start_x (int): Starting x-coordinate of the ship.
        start_y (int): Starting y-coordinate of the ship.
        end_x (int): Ending x-coordinate of the ship.
        end_y (int): Ending y-coordinate of the ship.

    Returns:
        list: List of coordinates representing the placed ship.
    """
    ship_coords = []
    for x in range(start_x, end_x + 1):
        for y in range(start_y, end_y + 1):
            board.get_board()[x, y] = board.inv_square_states['ship']
            ship_coords.append((x, y))
    return ship_coords

def letter_to_coords(letter, number):
    """
    Convert a letter and a number into x and y coordinates.

    Args:
        letter (str): Letter representing the column on the board.
        number (str): Number representing the row on the board.

    Returns:
        tuple: Tuple containing x and y coordinates.
    """
    letter_coord = ord(letter) - 65
    number_coord = int(number) - 1
    return letter_coord, number_coord
