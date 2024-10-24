"""
    Script for Performance Evaluation
"""

import pygame
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from data.classes.Board import Board
from data.classes.agents.ChessAgent import ChessAgent
from data.classes.agents.MiniMaxPlayer import MinimaxPlayer

color_code = {
            "black": "b",
            "white": "w"
        }

point_map = {
            " ": 0,
            "P": 1,
            "N": 3,
            "B": 3,
            "R": 5,
            "Q": 9,
            "K": "20"
        }

def chess_match(white_player: ChessAgent, black_player: ChessAgent):
    assert(white_player.color == 'white')
    assert(black_player.color == 'black')
    pygame.init()
    WINDOW_SIZE = (600, 600)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    board = Board(screen, WINDOW_SIZE[0], WINDOW_SIZE[1])
    agents: list[ChessAgent] = [white_player, black_player]
    i: int = 0
    moves_count: int = 0

    # Run the main game loop
    running = True

    # Outcome
    winner = None
    is_draw = False
    p1_move_count, p2_move_count = 0,0
    p1_capture_count, p2_capture_count = 0,0
    p1_points, p2_points = 0,0
    game_end_status: str = ""

    white_player_time_log = []
    black_player_time_log = []

    while running:
        print(f"Current Turn: {board.turn}")  # Debug: Show current turn
        time_start = time.time()
        chosen_action = agents[i].choose_action(board)
        time_end = time.time()

        # time_delta in seconds
        time_delta = time_end-time_start
        print("time_elapsed: ",time_delta)

        if board.turn == 'white':
            white_player_time_log.append(time_delta)
        else:
            black_player_time_log.append(time_delta)

        if chosen_action is False:
            print('Players draw!')
            running = False
            game_end_status = "NO_VALID_MOVES"
        elif moves_count > 100:
            print('Players draw!')
            running = False
            game_end_status = "MORE_THAN_100_MOVES"
        else:
            print("Chosen action:", chosen_action[0].pos, chosen_action[1].pos)  # Debug: Show chosen action
            
            # Check if the move is valid before applying it
            if board.handle_move(chosen_action[0], chosen_action[1]):

                if board.turn == 'white':
                    if chosen_action[2] > 0:
                        # captured a piece
                        p1_capture_count +=1
                        p1_points += chosen_action[2]

                    p1_move_count += 1
                else:
                    if chosen_action[2] > 0:
                        # captured a piece
                        p2_capture_count += 1
                        p2_points += chosen_action[2]
                    p2_move_count += 1

                moves_count += 1
                i = (i + 1) % len(agents)  # Switch turns only on valid move
                # Check for checkmate after a valid move
                if board.is_in_checkmate(board.turn):
                    if board.turn == 'white':
                        winner = "B"
                        print('Black wins!')
                    else:
                        winner = "W"
                        print('White wins!')

                    # End Game
                    running = False
                    game_end_status = "CHECK_MATE"
            else:
                if p1_points > p2_points:
                    winner = "W"
                elif p1_points < p2_points:
                    winner = "B"
                else:
                    winner = None
                    is_draw = True

                # End Game
                running = False
                game_end_status = "INVALID_MOVE_BUG"

                print("Invalid move!")  # Notify about invalid moves
                break
        board.draw()

    pygame.time.wait(3000)
    pygame.quit()

    outcome = {
        "winner": winner,
        "is_draw": is_draw,
        "p1_points": p1_points,
        "p2_points": p2_points,
        "p1_capture_count": p1_capture_count,
        "p2_capture_count": p2_capture_count,
        "p1_move_count": p1_move_count,
        "p2_move_count": p2_move_count,
        "game_end_status": game_end_status,
        "p1_time_log": white_player_time_log,
        "p2_time_log": black_player_time_log
        # TODO: We can add move sequence to the outcome for both players
    }
    return outcome

def visualize_performance(y1, y2):
    """
    Plots both the original and smooth curves for the given x, y1, and y2 values.

    Args:
    x (list): X-axis values.
    y1 (list): Y-axis values for the first line.
    y2 (list): Y-axis values for the second line.
    """

    x = [i for i in range(max(len(y1), len(y2)))]

    # Create smooth curves for both lines
    x_new = np.linspace(min(x), max(x), 300)  # Generate more x values for a smoother curve

    # Apply smoothing using cubic splines
    spl_y1 = make_interp_spline(x, y1, k=3)
    smooth_y1 = spl_y1(x_new)

    spl_y2 = make_interp_spline(x, y2, k=3)
    smooth_y2 = spl_y2(x_new)

    # Plot the original lines
    plt.plot(x, y1, 'o--', label='Line 1 (original)', color='blue')
    plt.plot(x, y2, 'o--', label='Line 2 (original)', color='green')

    # Plot the smoothed curves
    plt.plot(x_new, smooth_y1, label='Line 1 (smoothed)', color='blue', alpha=0.6)
    plt.plot(x_new, smooth_y2, label='Line 2 (smoothed)', color='green', alpha=0.6)

    # Add labels and legend
    plt.xlabel('Move')
    plt.ylabel('Time')
    plt.title('Original and Smoothed Line Chart')
    plt.legend()

    # Show the plot
    plt.show()

def evaluate_performance():
    outcome = chess_match(MinimaxPlayer('white'), MinimaxPlayer('black'))
    print(outcome)

    p1_avg_decision_time = sum(outcome["p1_time_log"])/len(outcome["p1_time_log"])
    p2_avg_decision_time = sum(outcome["p2_time_log"])/len(outcome["p2_time_log"])

    print("Avg P1 decision time: ", p1_avg_decision_time)
    print("Avg P2 decision time: ", p2_avg_decision_time)

    visualize_performance(outcome["p1_time_log"], outcome["p2_time_log"])

evaluate_performance()