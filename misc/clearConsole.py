import os

def clear_console():
    """
    Clear the console screen.

    This function uses the 'os.system' function to execute the system command 'cls'
    (Windows) or 'clear' (Linux/Mac) to clear the console screen.

    """
    os.system('cls')  # For Windows
    # os.system('clear')  # For Linux/Mac
