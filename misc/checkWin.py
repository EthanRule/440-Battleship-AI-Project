def checkWin(grid):
    hits = 0
    for row in grid:
        for col in row:
            if col == "X":
                hits += 1
    if hits == 17:
        return True
    else:
        return False