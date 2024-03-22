#Run with py -3 battleship.py
waterGrid = []
gridSize = None


def initializeGrid(waterGrid, gridSize):
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
            waterGrid.append(col)
    else:
        print("Invalid grid size")

def printGrid(grid):
    for row in grid:
        print(row)

def main():
    global gridSize
    while gridSize != "s" and gridSize != "m" and gridSize != "l":
        print("Welcome to Battleship!")
        print("Select a grid size: small, medium, or large")
        print("Enter s for small, m for medium, or l for large")
        gridSize = input()

    initializeGrid(waterGrid, gridSize)
    printGrid(waterGrid)

if __name__ == "__main__":
    main()
