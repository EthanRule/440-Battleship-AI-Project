from game_env_interface import Game
from ai import AI
from utils import letter_to_coords
import argparse
import numpy as np
import random
import time
from csp import BattleshipCSP  # Import the BattleshipCSP class

# Dictionary to map game outcomes to winners
winner = {(True, False): 'Computer',
          (False, True): 'Player'}

def init_game(size, ships, samples, autoplay, ai_type):
    """
    Initialize and run a game of Battleship.

    Args:
        size (int): Size of the game board.
        ships (list): List of ship lengths.
        samples (int): Number of Monte Carlo samples for AI moves.
    """
    # Initialize AI and player game environments
    ai_env = Game(size, ships)
    if ai_type == 'csp':  # If using CSP for ship configuration
        csp = BattleshipCSP(size, ships)
        solutions = csp.solve()
        if solutions:
            ai_env.defense_board.board = solutions[0]  # Use the first solution as ship configuration
        else:
            print("No valid ship configurations found using CSP.")
            exit(1)
    else:  # Use other types of AI
        computer = AI(ai_env, samples, ai_type)

    player_env = Game(size, ships)

    # Initialize match statistics
    c_turn_times = []
    p_turn_times = []
    c_hits = 0
    p_hits = 0
    c_turns = 0
    p_turns = 0

    # Game loop until a player wins
    while True:
        start_time = time.time()
        if ai_type == 'csp':
            c_state, c_outcome, c_done = computer_move(ai_env)  # Use predefined function for CSP-based AI move
        else:
            c_state, c_outcome, c_done = computer.move(ships)
        c_turn_times.append(time.time() - start_time)
        c_turns += 1
        if c_outcome == 'hit':
            c_hits += 1
        
        start_time = time.time()
        p_state, p_outcome, p_done = player_turn(player_env, autoplay)
        p_turn_times.append(time.time() - start_time)
        p_turns += 1
        if p_outcome == 'hit':
            p_hits += 1

        # Display game state after each turn
        c_state.print_board(f"=Your Board (Computer Target Ships)= [Last Outcome: {c_outcome}]")
        p_state.print_board(f"=Your Target Ships= [Last Outcome: {p_outcome}]")

        if c_done or p_done:
            break
    print("=" * 10 + "GAME OVER" + "=" * 10)
    print(f"The winner is: {winner[(c_done, p_done)]}")

    print_stats(c_turn_times, p_turn_times, c_hits, p_hits, c_turns, p_turns)
    return max(c_turns, p_turns)

def computer_move(ai_env):
    """Computer's move using the CSP-based ship configuration."""
    p_move = np.zeros(shape=[ai_env.size, ai_env.size])
    x, y = ai_env.attack_board.get_best_move()  # Define your logic to get the best move
    p_move[x, y] = 1
    return ai_env.step(p_move)

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

def print_stats(c_turn_times, p_turn_times, c_hits, p_hits, c_turns, p_turns):
    # Print statistics
    print("\n", "=" * 10 + "STATISTICS" + "=" * 10)
    print("Computer average turn time: ", "{:.6f}".format(sum(c_turn_times) / len(c_turn_times)))
    print("Player average turn time: ", "{:.6f}".format(sum(p_turn_times) / len(p_turn_times)))
    print("Computer total turn time: ", "{:.6f}".format(sum(c_turn_times)))
    print("Player total turn time: ", "{:.6f}".format(sum(p_turn_times)))
    print("Computer hit ratio: ", f"{c_hits} / {c_turns}")
    print("Player hit ratio: ", f"{p_hits} / {p_turns}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--board_size', type=int, help='The size of the board, default: 10', default=10)
    parser.add_argument('--ship_sizes', help='Array of ship sizes to randomly place, default: "5,4,3,3,2"', default='5,4,3,3,2')
    parser.add_argument('--monte_carlo_samples', type=int, help='The number of samples to get the algorithm to do, default: 10000', default=10000)
    parser.add_argument('--autoplay', help='Whether to autoplay the game or not, default: False', action='store_true')
    parser.add_argument('--ai_type', help='The type of AI to use, default: "monte_carlo"', default='monte_carlo')
    parser.add_argument('--num_games', type=int, help='The number of games to play, default: 1', default=1)
    args = parser.parse_args()

    try:
        total_turns = 0
        for _ in range(args.num_games):
            print("Welcome to Battleship!")
            print("Chosen args: ", args.board_size, [int(x) for x in args.ship_sizes.split(',')], args.monte_carlo_samples)
            if args.ai_type == 'monte_carlo':
                total_turns += init_game(args.board_size, [int(x) for x in args.ship_sizes.split(',')], args.monte_carlo_samples, args.autoplay, args.ai_type)
            elif args.ai_type == 'hunt_target':
                total_turns += init_game(args.board_size, [int(x) for x in args.ship_sizes.split(',')], args.monte_carlo_samples, args.autoplay, args.ai_type)
            elif args.ai_type == 'csp':  # Handle CSP-based AI
                total_turns += init_game(args.board_size, [int(x) for x in args.ship_sizes.split(',')], args.monte_carlo_samples, args.autoplay, args.ai_type)
            else:
                print("Invalid AI type!")
                exit(1)
        print(f"Average number of turns for AI to win over {args.num_games} games: {total_turns / args.num_games}")
    except:
        print("Incorrect Args!")
        exit(1)
