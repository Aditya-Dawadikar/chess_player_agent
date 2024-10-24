# /* RandomAgent.py

import random

from data.classes.Square import Square
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
            "K": 20
        }

class RandomPlayer(ChessAgent):
    def choose_action(self, board: Board):
        possible_moves: list[tuple[Square, Square]] = []
        for square in board.squares:
            if square.occupying_piece != None \
               and square.occupying_piece.color == self.color:
                for target in square.occupying_piece.get_valid_moves(board):
                    points = 0
                    if target.occupying_piece != None:
                                if target.occupying_piece.color != self.color:
                                    points = point_map[target.occupying_piece.notation]

                    possible_moves.append((square, target, points))
        if len(possible_moves) < 1:
            return False
        return random.choice(possible_moves)
