"""
    Script to generate Visualizations
"""
import os
import json
import numpy as np
import matplotlib.pyplot as plt

def aggregate_data(directory: str):
    """
        Aggregates the results from individual simulation
        outcome JSON files.
    """
    all_results = []
    aggregate = {}

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                data = json.load(file)  # Use json.load instead of json.loads
                # print(data)
                all_results.extend(data)

    p1_win_count = 0
    p1_lose_count = 0
    p2_win_count = 0
    p2_lose_count = 0
    draw_count = 0
    p1_captures_per_match = []
    p2_captures_per_match = []
    p1_points_per_match = []
    p2_points_per_match = []
    avg_captures_per_turn_p1 = []
    avg_captures_per_turn_p2 = []
    avg_points_per_turn_p1 = []
    avg_points_per_turn_p2 = []
    p1_points = 0
    p2_points = 0
    p1_capture_count = 0
    p2_capture_count = 0

    total_matches = len(all_results)

    for outcome in all_results:
        if outcome["winner"] == 'W':
            p1_win_count += 1
            p2_lose_count += 1
            p1_points += outcome["p1_points"]
            p1_capture_count += outcome["p1_capture_count"]
            p1_points_per_match.append(outcome["p1_points"])
            p1_captures_per_match.append(outcome["p1_capture_count"])
            avg_captures_per_turn_p1.append(outcome["p1_capture_count"]/outcome["p1_move_count"])
            avg_points_per_turn_p1.append(outcome["p1_points"]/outcome["p1_move_count"])
        elif outcome["winner"] == 'B':
            p2_win_count += 1
            p1_lose_count += 1
            p2_points += outcome["p2_points"]
            p2_capture_count += outcome["p2_capture_count"]
            p2_points_per_match.append(outcome["p2_points"])
            p2_captures_per_match.append(outcome["p2_capture_count"])
            avg_captures_per_turn_p2.append(outcome["p2_capture_count"]/outcome["p2_move_count"])
            avg_points_per_turn_p2.append(outcome["p2_points"]/outcome["p2_move_count"])
        elif outcome["winner"] is None or outcome["is_draw"] is True:
            draw_count += 1

    aggregate["p1_win_count"] = p1_win_count
    aggregate["p1_lose_count"] = p1_lose_count
    aggregate["p2_win_count"] = p2_win_count
    aggregate["p2_lose_count"] = p2_lose_count
    aggregate["p1_captures_per_match"] = p1_captures_per_match
    aggregate["p1_points_per_match"] = p1_points_per_match
    aggregate["p2_captures_per_match"] = p2_captures_per_match
    aggregate["p2_points_per_match"] = p2_points_per_match
    aggregate["draw_count"] = draw_count
    aggregate["avg_captures_per_turn_p1"] = avg_captures_per_turn_p1
    aggregate["avg_captures_per_turn_p2"] = avg_captures_per_turn_p2
    aggregate["avg_points_per_turn_p1"] = avg_points_per_turn_p1
    aggregate["avg_points_per_turn_p2"] = avg_points_per_turn_p2
    aggregate["p1_points"] = p1_points
    aggregate["p2_points"] = p2_points
    aggregate["p1_capture_count"] = p1_capture_count
    aggregate["p2_capture_count"] = p2_capture_count
    aggregate["total_matches"] = total_matches
    aggregate["avg_points_per_match_p1"] = p1_points/total_matches
    aggregate["avg_points_per_match_p2"] = p2_points/total_matches
    aggregate["avg_captures_per_match_p1"] = p1_capture_count/total_matches
    aggregate["avg_captures_per_match_p2"] = p2_capture_count/total_matches

    for key,value in aggregate.items():
        print(key,value)

    return aggregate

def visualize_data(aggregate:dict):
    """
        Generates charts from aggreate results
    """
    p1_win_count = aggregate["p1_win_count"]
    p1_lose_count = aggregate["p1_lose_count"]
    p2_win_count = aggregate["p2_win_count"]
    p2_lose_count = aggregate["p2_lose_count"]
    draw_count = aggregate["draw_count"]
    p1_points_per_match = aggregate["p1_points_per_match"]
    p1_captures_per_match = aggregate["p1_captures_per_match"]
    p2_points_per_match = aggregate["p2_points_per_match"]
    p2_captures_per_match = aggregate["p2_captures_per_match"]
    avg_captures_per_turn_p1=aggregate["avg_captures_per_turn_p1"]
    avg_captures_per_turn_p2=aggregate["avg_captures_per_turn_p2"]
    avg_points_per_turn_p1=aggregate["avg_points_per_turn_p1"]
    avg_points_per_turn_p2=aggregate["avg_points_per_turn_p2"]
    p1_points=aggregate["p1_points"]
    p2_points=aggregate["p2_points"]
    p1_capture_count=aggregate["p1_capture_count"]
    p2_capture_count=aggregate["p2_capture_count"]
    total_matches=aggregate["total_matches"]
    avg_points_per_match_p1= aggregate["avg_points_per_match_p1"]
    avg_points_per_match_p2= aggregate["avg_points_per_match_p2"]
    avg_captures_per_match_p1=aggregate["avg_captures_per_match_p1"]
    avg_captures_per_match_p2=aggregate["avg_captures_per_match_p2"]

    # Derived data
    matches_p1 = list(range(1, len(avg_captures_per_turn_p1) + 1))
    matches_p2 = list(range(1, len(avg_captures_per_turn_p2) + 1))

    # Create subplots
    fig, axs = plt.subplots(2,3, figsize=(12, 8))

    # Plot Win/lose/draw counts
    axs[0, 0].bar(['P1 Wins', 'P2 Wins', 'Draws'], 
                [p1_win_count, p2_win_count, draw_count],
                color=['blue', 'orange', 'green', 'red', 'purple'])
    axs[0, 0].set_title('Game Outcomes')
    axs[0, 0].set_ylabel('Count')

    # Plot p1 and p2 points per match
    axs[0, 1].plot(p1_points_per_match, label='P1 Points per Match', marker='o', color='blue')
    axs[0, 1].plot(p2_points_per_match, label='P2 Points per Match', marker='x', color='red')
    axs[0, 1].axhline(np.mean(p1_points_per_match), color='blue', linestyle='--', label='P1 Avg Points')
    axs[0, 1].axhline(np.mean(p2_points_per_match), color='red', linestyle='--', label='P2 Avg Points')
    axs[0, 1].set_title("Points per Match")
    axs[0, 1].legend()

    # Plot p1 and p2 captures per match
    axs[0, 2].plot(p1_captures_per_match, label='P1 Captures per Match', marker='o', color='green')
    axs[0, 2].plot(p2_captures_per_match, label='P2 Captures per Match', marker='x', color='orange')
    axs[0, 2].axhline(np.mean(p1_captures_per_match), color='green', linestyle='--', label='P1 Avg Captures')
    axs[0, 2].axhline(np.mean(p2_captures_per_match), color='orange', linestyle='--', label='P2 Avg Captures')
    axs[0, 2].set_title("Captures per Match")
    axs[0, 2].legend()

    # Plot Total Points per Player
    axs[1, 0].bar(['P1 Total Points', 'P2 Total Points'], [p1_points, p2_points], color=['green', 'red'])
    axs[1, 0].set_title('Total Points by Player')
    axs[1, 0].set_ylabel('Total Points')

    # Plot Captures per Match
    axs[1, 1].bar(['P1 Avg Captures/Match', 'P2 Avg Captures/Match'],
                [avg_captures_per_match_p1, avg_captures_per_match_p2], color=['blue', 'orange'])
    axs[1, 1].set_title('Avg Captures per Match')
    axs[1, 1].set_ylabel('Avg Captures')

    # Plot Points per Match
    axs[1, 2].bar(['P1 Avg Points/Match', 'P2 Avg Points/Match'],
                [avg_points_per_match_p1, avg_points_per_match_p2], color=['green', 'red'])
    axs[1, 2].set_title('Avg Points per Match')
    axs[1, 2].set_ylabel('Avg Points')

    # Adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()
