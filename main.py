from game_env_interface import Game
from ai import AI
from utils import letter_to_coords
import argparse
import numpy as np
import random

# Dictionary to map game outcomes to winners
winner = {(True, False): 'Computer',
          (False, True): 'Player'}

def init_game(size, ships, samples, autoplay):
    """
    Initialize and run a game of Battleship.

    Args:
        size (int): Size of the game board.
        ships (list): List of ship lengths.
        samples (int): Number of Monte Carlo samples for AI moves.
    """
    # Initialize AI and player game environments
    ai_env = Game(size, ships)
    computer = AI(ai_env, samples)
    player_env = Game(size, ships)

    # Game loop until a player wins
    while True:
        c_state, c_outcome, c_done = computer.move()
        p_state, p_outcome, p_done = player_turn(player_env, autoplay)

        # Display game state after each turn
        c_state.print_board(f"=Your Board (Computer Target Ships)= [Last Outcome: {c_outcome}]")
        p_state.print_board(f"=Your Target Ships= [Last Outcome: {p_outcome}]")

        if c_done or p_done:
            break

    print("=" * 10 + "GAME OVER" + "=" * 10)
    print(f"The winner is: {winner[(c_done, p_done)]}")

def player_turn(player_env, autoplay):
    """
    Perform player's turn.

    Args:
        player_env (Game): Player's game environment.

    Returns:
        tuple: Tuple containing player's game state, outcome, and game completion status.
    """
    p_move = np.zeros(shape=[player_env.size, player_env.size])
    x, y = get_player_input(player_env, autoplay)
    p_move[x, y] = 1
    return player_env.step(p_move)

def get_player_input(player_env, autoplay):
    """
    Get player's input for making a move.

    Args:
        player_env (Game): Player's game environment.

    Returns:
        tuple: Tuple containing player's selected coordinates.
    """
    while True:
        if autoplay:
            ltr = chr(random.randint(0, player_env.size - 1) + ord('A'))
            nbr = str(random.randint(1, player_env.size))
        else:
            ltr, nbr = input("Enter letter: ").upper(), input("Enter number: ")
        try:
            if (len(ltr) > 1 or len(nbr)) > len(str(player_env.size)):
                raise ValueError("Input length should be 1.")
            x, y = letter_to_coords(ltr, nbr)
            if player_env.attack_board.get_board()[x, y] == 0:
                return x, y
            else:
                if not autoplay:
                    print("This position has already been targeted. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid letter and number.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_size', type=int, help='The size of the board, default: 10', default=10)
    parser.add_argument('--ship_sizes', help='Array of ship sizes to randomly place, default: "5,4,3,3,2"', default='5,4,3,3,2')
    parser.add_argument('--monte_carlo_samples', type=int, help='The number of samples to get the algorithm to do, default: 10000', default=10000)
    parser.add_argument('--autoplay', help='Whether to autoplay the game or not, default: False', action='store_true')
    args = parser.parse_args()

    try:
        print("Welcome to Battleship!")
        print("Chosen args: ", args.board_size, [int(x) for x in args.ship_sizes.split(',')], args.monte_carlo_samples)
        init_game(args.board_size, [int(x) for x in args.ship_sizes.split(',')], args.monte_carlo_samples, args.autoplay)
    except:
        print("Incorrect Args!")
        exit(1)