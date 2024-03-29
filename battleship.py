#Run with py -3 battleship.py
#Python Version 3.8.10 (3 May 2021) and above
#pip install pygame <-- for audio

from colorama import Fore #pip install colorama or py -3 -m pip install colorama
import random
import time
import os
import pygame #pip install pygame or py -3 -m pip install pygame
pygame.mixer.init()
pygame.mixer.music.load("Strategy Background Music  No Copyright Music  Free Music.mp3") # https://www.youtube.com/watch?v=BMGWF6U6d7c 
pygame.mixer.music.play(-1)  # loop indefinitely
pygame.mixer.music.set_volume(0.01)

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

computer_total_turns = 0
computer_total_hits = 0
computer_total_misses = 0
computer_tried_coordinates = set()

player_total_turns = 0
player_total_hits = 0
player_total_misses = 0
player_tried_coordinates = set()

log_messages = []

def clear_console():
    os.system('cls')

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
def placeAllShips(skipPlacement):
    #player ship placement
    if skipPlacement:
        placeShip(playerCarrier, 5, playerGrid, isComputer=True)
        placeShip(playerBattlship, 4, playerGrid, isComputer=True)
        placeShip(playerCruiser, 3, playerGrid, isComputer=True)
        placeShip(playerSubmarine, 3, playerGrid, isComputer=True)
        placeShip(playerDestroyer, 2, playerGrid, isComputer=True)
    else:
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
    
hits = []
def hunt_targetAlgorithm():
    global computer_tried_coordinates
    global log_messages
    if not hits:  # hunt
        while True:
            x, y = random.randint(0, len(blankPlayerGrid) - 1), random.randint(0, len(blankPlayerGrid[0]) - 1)
            if (x, y) not in computer_tried_coordinates and blankPlayerGrid[x][y] != "X" and blankPlayerGrid[x][y] != "O":
                computer_tried_coordinates.add((x, y))
                log_messages.append(f"Hunting: Selected coordinates ({x}, {y})")
                return x, y
    else:  # target
        x, y = hits[0]
        log_messages.append(f"Targeting: Starting from coordinates ({x}, {y})")
        if x - 1 >= 0 and (x - 1, y) not in computer_tried_coordinates and blankPlayerGrid[x - 1][y] != "X" and blankPlayerGrid[x - 1][y] != "O":
            computer_tried_coordinates.add((x - 1, y))
            return x - 1, y
        elif x + 1 < len(blankPlayerGrid) and (x + 1, y) not in computer_tried_coordinates and blankPlayerGrid[x + 1][y] != "X" and blankPlayerGrid[x + 1][y] != "O":
            computer_tried_coordinates.add((x + 1, y))
            return x + 1, y
        elif y - 1 >= 0 and (x, y - 1) not in computer_tried_coordinates and blankPlayerGrid[x][y - 1] != "X" and blankPlayerGrid[x][y - 1] != "O":
            computer_tried_coordinates.add((x, y - 1))
            return x, y - 1
        elif y + 1 < len(blankPlayerGrid[0]) and (x, y + 1) not in computer_tried_coordinates and blankPlayerGrid[x][y + 1] != "X" and blankPlayerGrid[x][y + 1] != "O":
            computer_tried_coordinates.add((x, y + 1))
            return x, y + 1
        else:
            hits.pop(0)
            if not hits:  # Switch back to hunting mode
                log_messages.append("Switching back to hunting mode")
                return hunt_targetAlgorithm()
        

def playGame(autoplay):
    global computer_total_turns, computer_total_hits, computer_total_misses, player_total_turns, player_total_hits, player_total_misses
    while True:
        clear_console()
        print("Computer")
        printGrid(blankComputerGrid)
        print("Player")
        printGrid(playerGrid)
        if autoplay:
            x, y = random.randint(0, len(computerGrid) - 1), random.randint(0, len(computerGrid[0]) - 1)
            if isinstance(computerGrid[x][y], int) and computerGrid[x][y] > 0:
                print("Hit!")
                computerGrid[x][y] = "X"
                blankComputerGrid[x][y] = "X"
                player_total_hits += 1
            else:
                print("Miss!")
                player_total_misses += 1
            player_total_turns += 1
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
                player_total_hits += 1
            else:
                print("Miss!")
                player_total_misses += 1
            player_total_turns += 1
            if checkWin(blankComputerGrid):
                print("You win!")
                break
        #computer's turn # IMPLEMENT COMPUTER AI HERE ## IMPLEMENT COMPUTER AI HERE ## IMPLEMENT COMPUTER AI HERE ## IMPLEMENT COMPUTER AI HERE #
        x, y = hunt_targetAlgorithm()
        print("X", x, "Y", y)
        if isinstance(playerGrid[x][y], int) and playerGrid[x][y] > 0:
            print("Computer hit!")
            playerGrid[x][y] = "X"
            blankPlayerGrid[x][y] = "X"
            hits.append((x, y))
            computer_total_hits += 1
        else:
            print("Computer miss!")
            blankPlayerGrid[x][y] = "0"
            computer_total_misses += 1
        computer_total_turns += 1
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

def printGrid(grid): #https://pypi.org/project/colorama/
    print ("  ", end="")
    for i in range(len(grid[0])):
        print(Fore.YELLOW + str(i), end=" ")
    print(Fore.RESET)
    for i, row in enumerate(grid):
        print(Fore.YELLOW + str(i), end="")
        print(Fore.RESET, end=" ")
        for col in row:
            if col == 0:
                print(Fore.BLUE + '~', end=" ")
            elif col == 2 or col == 3 or col == 4 or col == 5:
                print(Fore.GREEN + str(col), end=" ")
            elif col == "X":
                print(Fore.RED + col, end=" ")
        print(Fore.RESET)

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
    computerDestroyer = [] # 2 hole

def printStatistics():
    print("\n-- Computer Statistics --")
    print("Total turns:", computer_total_turns)
    print("Total hits:", computer_total_hits)
    print("Total misses:", computer_total_misses)
    print("\n-- Player Statistics --")
    print("Total turns:", player_total_turns)
    print("Total hits:", player_total_hits)
    print("Total misses:", player_total_misses)
    print("Press enter to continue")
    input()

    

def main():
    clear_console()
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
        placeAllShips(skipPlacement=True)               #toggle this on and off to skip player ship placement
        playGame(autoplay=True)                         #toggle this on and off to autoplay the game (player does not need to input coordinates)
        resetGame()
        printStatistics()
        print("\n -- LOG MESSAGES FROM AI --\n")
        for message in log_messages:
            print(message)
        print("Press q to quit or any other key to play again")
        gameLoop = input()
if __name__ == "__main__":
    main()


        









