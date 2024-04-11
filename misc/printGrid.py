from colorama import Fore
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