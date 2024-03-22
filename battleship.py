#Run with py -3 battleship.py
import random

#Grid
playerGrid = []
computerGrid = []
gridSize = None

#Ships
playerCarrier = []   # 5 holes
playerBattlship = [] # 4 holes
playerCruiser = []   # 3 holes
playerSubmarine = [] # 3 holes
playerDestroyer = [] # 2 holes

computerCarrier = []   # 5 holes
computerBattlship = [] # 4 holes
computerCruiser = []   # 3 holes
computerSubmarine = [] # 3 holes
computerDestroyer = [] # 2 holes

def initializeGrid(grid, gridSize):
    rows, cols = None, None
    if gridSize == "s":
        rows, cols = 8, 8
    elif gridSize == "m":
        rows, cols = 10, 10
    elif gridSize == "l":
        rows, cols = 15, 15
    if rows != None and cols != None:
        for i in range(rows):
            col = []
            for j in range(cols):
                col.append(0)
            grid.append(col)
    else:
        print("Invalid grid size")

def printGrid(grid):
    for row in grid:
        print(row)

def placeAllShips():
    #player ship placement
    placeShip(playerCarrier, 5, playerGrid, isComputer=False)
    printGrid(playerGrid)
    placeShip(playerBattlship, 4, playerGrid, isComputer=False)
    printGrid(playerGrid)
    placeShip(playerCruiser, 3, playerGrid, isComputer=False)
    printGrid(playerGrid)
    placeShip(playerSubmarine, 3, playerGrid, isComputer=False)
    printGrid(playerGrid)
    placeShip(playerDestroyer, 2, playerGrid, isComputer=False)
    printGrid(playerGrid)

    #computer ship placement
    placeShip(computerCarrier, 5, computerGrid, isComputer=True)
    placeShip(computerBattlship, 4, computerGrid, isComputer=True)
    placeShip(computerCruiser, 3, computerGrid, isComputer=True)
    placeShip(computerSubmarine, 3, computerGrid, isComputer=True)
    placeShip(computerDestroyer, 2, computerGrid, isComputer=True)

def placeShip(ship, size, grid, isComputer):
    x, y = None, None
    notValidPlacement = True
    while notValidPlacement:
        if isComputer:
            x, y = random.randint(0, len(grid) - 1), random.randint(0, len(grid[0]) - 1) #https://docs.python.org/3/library/random.html
            direction = random.choice(["h", "v"])
        else:
            print(f"Enter starting coordinates for your ship of size {size} (format: x y)")
            coordinates = input().split()
            if len(coordinates) != 2 or not all(i.isdigit() for i in coordinates):
                if isComputer:
                    continue
                print("\033[91mInvalid input.\033[0m Please enter two valid integers separated by a space.")
                continue
            x, y = map(int, coordinates)
            direction = None
            while direction != "h" and direction != "v":
                if isComputer:
                    continue
                print("Enter direction for your ship (h for horizontal, v for vertical)")
                direction = input()
        if direction == "h":
            if y + size > len(grid[0]):
                if isComputer:
                    continue
                print("\033[91mInvalid position.\033[0m Ship goes out of bounds") # https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
                continue
            if any(grid[x][y + i] > 0 for i in range(size)):
                if isComputer:
                    continue
                print("\033[91mInvalid position.\033[0m Ship overlaps with another ship")
                continue
            for i in range(size):
                grid[x][y + i] = size
                ship.append([x, y + i])
        elif direction == "v":
            if x + size > len(grid):
                if isComputer:
                    continue
                print("\033[91mInvalid position.\033[0m Ship goes out of bounds")
                continue
            if any(grid[x + i][y] > 0 for i in range(size)):
                if isComputer:
                    continue
                print("\033[91mInvalid position.\033[0m Ship overlaps with another ship")
                continue
            for i in range(size):
                grid[x + i][y] = size
                ship.append([x + i, y])
        notValidPlacement = False


def main():
    global gridSize
    while gridSize != "s" and gridSize != "m" and gridSize != "l":
        print("Welcome to Battleship!")
        print("Select a grid size: small, medium, or large")
        print("Enter s for small, m for medium, or l for large")
        gridSize = input()

    initializeGrid(playerGrid, gridSize)
    initializeGrid(computerGrid, gridSize)
    placeAllShips()
if __name__ == "__main__":
    main()
