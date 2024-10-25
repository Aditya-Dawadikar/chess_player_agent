"""
    Script for Performance Evaluation
"""

import os
import json
import matplotlib.pyplot as plt
import numpy as np
import random

def visualize_performance_grid(matches, grid_size=(3, 3)):
    """
    Visualizes performance across multiple matches using a grid of subplots.

    Args:
    matches (list): A list of match data, where each match contains 'p1_time_log' and 'p2_time_log'.
    grid_size (tuple): The dimensions of the grid (rows, columns).
    """

    num_matches = len(matches)
    rows, cols = grid_size

    # Adjust the grid size to fit the number of matches
    fig, axes = plt.subplots(rows, cols, figsize=(12, 8))
    axes = axes.flatten()  # Flatten to easily iterate

    # Loop through each match and plot the performance data
    for i, match in enumerate(matches):
        if i >= rows * cols:
            break  # Stop if we exceed the grid size

        y1 = match.get("p1_time_log", [])
        y2 = match.get("p2_time_log", [])

        # Ensure both logs have the same length by padding the shorter one with zeros
        if len(y1) > len(y2):
            y2.extend([0] * (len(y1) - len(y2)))
        elif len(y2) > len(y1):
            y1.extend([0] * (len(y2) - len(y1)))

        x = np.arange(len(y1))

        # Plot both time logs for the match
        axes[i].plot(x, y1, 'o--', label='White Player', color='blue')
        axes[i].plot(x, y2, 'o--', label='Black Player', color='green')

        # Add title and adjust labels
        axes[i].set_title(f'Match {i + 1}')
        axes[i].set_xlabel('Move')
        axes[i].set_ylabel('Time (milli seconds)')
        axes[i].legend()

    # Adjust layout for better display
    plt.tight_layout()
    plt.show()

def evaluate_performance(directory:str=""):
    all_matches = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                data = json.load(file)
                for match in data:
                    if match["p1_move_count"] > 20:
                        all_matches.append(match)
    
    sample = random.sample(all_matches, 9)

    visualize_performance_grid(sample)


evaluate_performance(directory="./data/results/minimax_vs_minimax/")
