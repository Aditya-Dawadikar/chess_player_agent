import json
import time
import pandas as pd
from data.classes.ChessMatch import chess_match
from data.classes.agents.MiniMaxPlayer import MinimaxPlayer
from data.classes.agents.RandomPlayer import RandomPlayer

def run_match():
    outcome = chess_match(MinimaxPlayer('white'), RandomPlayer('black'))
    return outcome

def run_simulation(iterations:int=5):
    outcomes = []
    player_1_wins = 0
    player_2_wins = 0
    draws = 0
    for i in range(iterations):
        print("==============================================")
        print(f"""              GAME #{i+1}                """)
        print("==============================================")
        sim_outcome = run_match()
        print("-------------------OUTCOME--------------------")
        print(sim_outcome)
        print("----------------------------------------------")
        print("\n\n")

        if sim_outcome["winner"] == 'W':
            player_1_wins += 1
        elif sim_outcome["winner"] == 'B':
            player_2_wins += 1
        else:
            draws += 1

        outcomes.append(sim_outcome)
    
    export_simulation_data(outcomes)


def export_simulation_data(outcome_list: list):
    timestamp = str(int(time.time()))
    file_name = f"""results_{timestamp}.json"""
    with open(file_name, 'w') as fout:
        json.dump(outcome_list , fout)
