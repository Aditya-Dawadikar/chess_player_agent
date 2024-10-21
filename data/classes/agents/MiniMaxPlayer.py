# /* MinimaxPlayer.py

from data.classes.Board import Board
from data.classes.agents.ChessAgent import ChessAgent
from data.classes.Simulation import SimulationBoard, SimulationSquare
from data.classes.Square import Square
import random

class MinimaxPlayer(ChessAgent):
    @staticmethod
    def translate_simulation_square_to_square(sim_square: SimulationSquare, board: Board) -> Square:
        position = sim_square.pos
        return board.get_square_from_pos(position)

    def choose_action(self, board: Board, verbose: bool = True):
        best_move = None
        best_value = float('-inf')

        sim_board = SimulationBoard()
        sim_board.copy_from_board(board)
        possible_move = self.get_all_possible_moves(sim_board, self.color)

        random.shuffle(possible_move)

        for move in possible_move:
            sim_board.handle_move(move['curr_pos'], move['next_pos'])
            move_value = self.minimax(sim_board, 
                                      depth=3, 
                                      alpha=float('-inf'), 
                                      beta=float('inf'), 
                                      maximizing_player=False)
            if move_value > best_value:
                best_value = move_value
                best_move = (move['start'], move['end'])
        
        # Convert the best move's SimulationSquare to Square before returning
        if best_move:
            start_square = self.translate_simulation_square_to_square(best_move[0], board)
            end_square = self.translate_simulation_square_to_square(best_move[1], board)
            return (start_square, end_square)

        return False

    def print_possible_moves(self, possible_moves):
        print("\n*********************************")
        print("============== MOVES ==============\n")
        for move in possible_moves:
                print("-----------------------------")
                print("curr_pos: ", move["curr_pos"])
                print("curr_piece", move["curr_piece_color"], move["curr_piece_notation"])
                print("next_pos: ", move["next_pos"])
                print("next_piece: ", move["next_piece_color"], move["next_piece_notation"])
                print("can_capture: ", move["can_capture"])
                print("points: ", move["points"])
        print()
    
    def evaluate_board(self, board: Board):
        point_map = {
            "P": 1,
            "N": 3,
            "B": 3,
            "R": 5,
            "Q": 9,
            "K": 0  # King should not be considered for evaluation
        }

        score = 0
        for square in board.squares:
            if square.occupying_piece:
                piece = square.occupying_piece
                piece_value = point_map.get(piece.notation.upper(), 0)
                score += piece_value if piece.color == self.color else -piece_value

        return score

    def get_all_possible_moves(self, board: SimulationBoard, color: str):
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
            "K": "INF"
        }
        
        possible_moves = []

        for square in board.squares:
            if square.occupying_piece is not None:
                if square.occupying_piece.notation != ' ':
                    if square.occupying_piece.color == color:
                        for target in square.occupying_piece.get_valid_moves(board):
                            can_capture = False
                            points = point_map[" "]

                            if not isinstance(target,SimulationSquare):
                                target_square = board.get_square(target)
                            else:
                                target_square = target

                            if target_square.occupying_piece != None:
                                if target_square.occupying_piece.color != self.color:
                                    can_capture = True
                                    points = point_map[target_square.occupying_piece.notation]

                            possible_moves.append({
                                "start":square,
                                "curr_pos": square.pos,
                                "curr_piece_color": color_code[square.occupying_piece.color] if square.occupying_piece else None,
                                "curr_piece_notation": square.occupying_piece.notation if square.occupying_piece else None,
                                "end": target_square,
                                "next_pos": target_square.pos,
                                "next_piece_color": color_code[target_square.occupying_piece.color] if target_square.occupying_piece else None,
                                "next_piece_notation": target_square.occupying_piece.notation if target_square.occupying_piece else None,
                                "can_capture":can_capture,
                                "points": points
                            })
        # print(possible_moves)
        return possible_moves

    def get_opponent_color(self):
        return "black" if self.color == "white" else "white"
    
    def minimax(self, board: SimulationBoard, depth: int, alpha: int, beta: int, maximizing_player: bool) -> int:
        if depth == 0:
            return self.evaluate_board(board)

        # Determine the color for the current maximizing or minimizing player
        color = self.color if maximizing_player else self.get_opponent_color()

        # Get all possible moves for the current player
        possible_moves = self.get_all_possible_moves(board, color)
        random.shuffle(possible_moves)

        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                board_copy = SimulationBoard()
                board_copy.copy_from_board(board)
                board_copy.handle_move(move['curr_pos'], move['next_pos'])
                eval = self.minimax(board_copy, depth - 1, alpha, beta, False)  # Recurse with minimizing player
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                board_copy = SimulationBoard()
                board_copy.copy_from_board(board)
                board_copy.handle_move(move['curr_pos'], move['next_pos'])
                eval = self.minimax(board_copy, depth - 1, alpha, beta, True)  # Recurse with maximizing player
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval
