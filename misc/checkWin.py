def checkWin(grid):
    """
    Check if all ships on the grid have been hit.

    Args:
        grid (list of lists): The game grid representing the board.

    Returns:
        bool: True if all ships have been hit, False otherwise.
    """
    # Initialize hits count
    hits = 0
    
    # Iterate through each cell in the grid
    for row in grid:
        for col in row:
            # If cell contains "X" (hit), increment hits count
            if col == "X":
                hits += 1
    
    # If total hits equal to number of cells occupied by ships, return True
    if hits == 17:
        return True
    else:
        return False
