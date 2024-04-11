from colorama import Fore
import random
import time
from misc.printGrid import printGrid
from misc.clearConsole import clear_console
from misc.checkWin import checkWin
from misc.initMusic import initMusic


#Grid
playerGrid = []
computerGrid = []
blankComputerGrid = []
blankPlayerGrid = []
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

#Computer Coordinate Relationship Dictionary: the key is a coordinate set (row, column) and the value is a list of coordinate sets
computerRelDic = {}

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

def initializeRelDic(relDic, gridSize):
    rows, cols = None, None
    if gridSize == "s":
        rows, cols = 8, 8
    elif gridSize == "m":
        rows, cols = 10, 10
    elif gridSize == "l":
        rows, cols = 15, 15
    if rows != None and cols != None:
        for i in range(0, rows):
            for j in range(0, cols):
                coord = (i, j)
                print(coord)
                neighbors = []
                if i > 0:
                    neighbors.append((i-1, j))
                if i < rows-1:
                    neighbors.append((i+1, j))
                if j > 0:
                    neighbors.append((i, j-1))
                if j < cols-1:
                    neighbors.append((i, j+1))
                relDic[coord] = neighbors
    else:
        print("Invalid grid size")

def placeAllShips(skipPlacement):
    ships = [(playerCarrier, 5), (playerBattlship, 4), (playerCruiser, 3), (playerSubmarine, 3), (playerDestroyer, 2)]
    computerShips = [(computerCarrier, 5), (computerBattlship, 4), (computerCruiser, 3), (computerSubmarine, 3), (computerDestroyer, 2)]

    #Place player ships
    for ship, size in ships:
        placeShip(ship, size, playerGrid, isComputer=skipPlacement)
        if not skipPlacement:
            printGrid(playerGrid)

    #Place computer ships
    for ship, size in computerShips:
        placeShip(ship, size, computerGrid, isComputer=True)

def placeShip(ship, size, grid, isComputer):
    x, y = None, None
    notValidPlacement = True
    while notValidPlacement:
        if isComputer: #used to skip player ship placement
            x, y = random.randint(0, len(grid) - 1), random.randint(0, len(grid[0]) - 1) #https://docs.python.org/3/library/random.html
            direction = random.choice(["h", "v"])
        else: #normal player ship placement
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

def playGame(autoplay):
    while True:
        clear_console()
        print("Computer")
        printGrid(blankComputerGrid)
        print("Player")
        printGrid(playerGrid)
        if autoplay:
            time.sleep(0.1) #delay for autoplay this will probably need to be removed
            x, y = random.randint(0, len(computerGrid) - 1), random.randint(0, len(computerGrid[0]) - 1)
            if isinstance(computerGrid[x][y], int) and computerGrid[x][y] > 0:
                print("Hit!")
                computerGrid[x][y] = "X"
                blankComputerGrid[x][y] = "X"
            else:
                print("Miss!")
            if checkWin(blankComputerGrid):
                clear_console()
                print("Computer")
                printGrid(blankComputerGrid)
                print("Player")
                printGrid(playerGrid)
                print("Hit!")
                print("You win!")
                break
        else:
            print("Enter coordinates to attack")
            coordinates = input().split()
            if len(coordinates) != 2 or not all(i.isdigit() for i in coordinates):
                print("\033[91mInvalid input.\033[0m Please enter two valid integers separated by a space.")
                print("Press enter to continue")
                input()
                continue
            x, y = map(int, coordinates)
            if x < 0 or x >= len(computerGrid) or y < 0 or y >= len(computerGrid[0]):
                print("\033[91mInvalid input.\033[0m Please enter coordinates within the grid.")
                print("Press enter to continue")
                input()
                continue
            if isinstance(computerGrid[x][y], int) and computerGrid[x][y] > 0:
                print("Hit!")
                computerGrid[x][y] = "X"
                blankComputerGrid[x][y] = "X"
            else:
                print("Miss!")
            if checkWin(blankComputerGrid):
                print("You win!")
                break
        #computer's turn # IMPLEMENT COMPUTER AI HERE ## IMPLEMENT COMPUTER AI HERE ## IMPLEMENT COMPUTER AI HERE ## IMPLEMENT COMPUTER AI HERE #
        x, y = random.randint(0, len(playerGrid) - 1), random.randint(0, len(playerGrid[0]) - 1)
        if isinstance(playerGrid[x][y], int) and playerGrid[x][y] > 0:
            print("Computer hit!")
            playerGrid[x][y] = "X"
            blankPlayerGrid[x][y] = "X"
        else:
            print("Computer miss!")
        # IMPLEMENT COMPUTER AI HERE ## IMPLEMENT COMPUTER AI HERE ## IMPLEMENT COMPUTER AI HERE ## IMPLEMENT COMPUTER AI HERE ## IMPLEMENT COMPUTER AI HERE #
        if checkWin(blankPlayerGrid):
            clear_console()
            print("Computer")
            printGrid(blankComputerGrid)
            print("Player")
            printGrid(playerGrid)
            print("Computer hit!")
            print("Computer wins!")
            break
        if autoplay:
            continue
        else:
            print("Press enter to continue")
            input()

def resetGame():
    #Grid
    global playerGrid, computerGrid, blankComputerGrid, blankPlayerGrid, gridSize
    playerGrid = []
    computerGrid = []
    blankComputerGrid = []
    blankPlayerGrid = []
    gridSize = None
    
    #Ships
    global playerCarrier, playerBattlship, playerCruiser, playerSubmarine, playerDestroyer
    global computerCarrier, computerBattlship, computerCruiser, computerSubmarine, computerDestroyer
    playerCarrier = []     # 5 holes
    playerBattlship = []   # 4 holes
    playerCruiser = []     # 3 holes
    playerSubmarine = []   # 3 holes
    playerDestroyer = []   # 2 holes
    computerCarrier = []   # 5 holes
    computerBattlship = [] # 4 holes
    computerCruiser = []   # 3 holes
    computerSubmarine = [] # 3 holes
    computerDestroyer = [] # 2 holes
    

def main():
    clear_console()
    initMusic()
    global gridSize
    gameLoop = None

    print("Welcome to Battleship!")
    while gameLoop != "q":
        while gridSize != "s" and gridSize != "m" and gridSize != "l":
            print("Select a grid size: small, medium, or large")
            print("Enter s for small, m for medium, or l for large")
            gridSize = input()

        initializeGrid(playerGrid, gridSize)
        initializeGrid(computerGrid, gridSize)
        initializeGrid(blankComputerGrid, gridSize)
        initializeGrid(blankPlayerGrid, gridSize)
        initializeRelDic(computerRelDic, gridSize)
        placeAllShips(skipPlacement=True)               #toggle this on and off to skip player ship placement
        playGame(autoplay=True)                         #toggle this on and off to autoplay the game (player does not need to input coordinates)
        resetGame()
        print("Press q to quit or any other key to play again")
        gameLoop = input()

if __name__ == "__main__":
    main()