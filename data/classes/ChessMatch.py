import pygame
import time
from data.classes.Board import Board
from data.classes.agents.ChessAgent import ChessAgent

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

    while running:
        print(f"Current Turn: {board.turn}")  # Debug: Show current turn
        chosen_action = agents[i].choose_action(board)


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
        "game_end_status": game_end_status
        # TODO: We can add move sequence to the outcome for both players
    }
    return outcome
