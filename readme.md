## Assignment Description
Your task is to write an agent inheriting from `ChessAgent` based on the methods discussed in class. You pay place your agent `.py` file in `data/classes/agents/`, where you will also find the `HumanPlayer` and `RandomPlayer` for reference. Like the previous assignment, you must collect data on the performance of your agent over at least 100 matches. It is suggested that you use the `chess_match` function as demonstrated in `main.py` and write your own script which uses your agent over those 100 matches.

## Setup Instructions
You can install the requirements (only pygame) by running `pip install -r requirements.txt`

Then you can run the program with `python main.py HumanPlayer RandomPlayer` to have a human play as white by selecting which pieces to move against an agent which chooses its moves randomly. You can choose both as `HumanPlayer` for both black and white players to be human-controlled

## Game Details
In general, the player can choose into which type of piece the pawn promotes. For simplicity, when a pawn reaches the end of the board in this version of the game, it automatically promotes to a queen piece. Another rule of chess is that if both players repeat the same move 3 times in a row, the game is a draw. To prevent games between `RandomPlayer`s taking forever, we instead declare a draw after 1000 total moves is neither player has won.

When one of the players wins by checkmating the opponent's King, the message "White/Black wins!" will be printed in the terminal and no more moves can be played

As a human player, you can click on any of your pieces and be shown in green to which squares that piece can move (which do not cause you to be in check). Click any square which is not highlighted to stop showing the valid moves for that piece.

## Credits
This assignment is adapted from the following tutorial for coding chess in python.

https://thepythoncode.com/article/make-a-chess-game-using-pygame-in-python

The images used for the chess pieces are taken from the wikimedia foundation.

https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent

## Solution
Following Assignment Solution implements Minimax Algorithm based chess agent.

### Running the Code:
Clone this repository

    https://github.com/Aditya-Dawadikar/chess_player_agent.git

Enter the folder

    cd chess_player_agent

Create a virtual environment

    pip install virtualenv
    virtualenv venv

Activate the environment
    
    source venv/bin/activate

Install the dependencies

    pip install -r requirements.txt

Run the code

    python3 main.py

Currently the Code is setup to run chess simulations for a Minimax Agent Vs Minimax Agent. But this can be turned into a Human Vs MiniMax Game by making the following changes in the SimulationRunner.py

    from data.classes.agents.HumanPlayer import HumanPlayer

    def run_match():
        outcome = chess_match(HumanPlayer('white'), MinimaxPlayer('black'))
        return outcome


## Minimax Agent Implementation

The utility function for the Minimax Agent is the Points assigned to the opponent chess pieces.

| Piece      | Capture Point |
|------------|---------------|
| Pawn (P)   | 1             |
| Rook (R)   | 3             |
| Bishop (B) | 3             |
| Knight (N) | 3             |
| Queen (Q)  | 9             |
| King (K)   | 20            |

All simulations are executed with a max depth of 3. The Agents may perform better if the depth is increased but the execution time increases exponentially.

### Architecture

Base implementation uses a **PyGame** board described as **Board.py**. Using the same board running simulation slows down the program. Additionally when the board is being evaluated, we do not need graphic representation of the moves, hence I implemented a lightweight board **SimulationBoard**. This is equivalent to the Board class, except there is no PyGame graphics code. All the moves are taken on a 2D matrix based representation of the game board, where each piece is denoted as a string.

## Performance Evaluation

### Minimax Vs Random Agent
In this simulation, the White Player was the Minimax Agent and Black Player was the Random Agent. Total of 100 matches were played.

![img](https://github.com/Aditya-Dawadikar/chess_player_agent/blob/master/data/results/Visualization/Minimax_vs_Random.png)

#### Analysis
It turns out that the Random Agent has higher win rate as compared to the Minimax Agent.

A possible explanations:
1. Minimax Agent assumes that the opponent always chooses the best possible move, but Random Agent trumps this strategy with random moves.
2. Minimax Agent's Check and Checkmate logic is flawed at the moment, the Minimax's King tends to save himself when under a check where as there is also a possibility that the threat piece can be captured by the King, or it can be blocked or captured by any other Minimax Piece. Thus we are not able to find the best possible move, when under a Check state.

### Minimax Vs Minimax Agent
In this simulation, both the White and Black Players are Minimax Agents. Total of 100 matches were played.

![img](https://github.com/Aditya-Dawadikar/chess_player_agent/blob/master/data/results/Visualization/Minimax_vs_Minimax.png)

#### Analysis
It is evident that both White and Black Players have similar capabilities hence the number of Draws are high. Although the White Player seems to have an upper hand in winning games because of having the first move advantage.

Limitations regarding the Check and CheckMate situations are present in both agents, hence the matches are fair.

## Algorithm Performance

There are about 100 simulations for Minimax vs Minimax Agent, we choose a random sample of 9 where the move_count is more than 20 for white players.

**Random Sample 1**
![img](https://github.com/Aditya-Dawadikar/chess_player_agent/blob/master/data/results/Visualization/performance_01.png)

**Random Sample 2**
![img](https://github.com/Aditya-Dawadikar/chess_player_agent/blob/master/data/results/Visualization/performance_02.png)

**Random Sample 3**
![img](https://github.com/Aditya-Dawadikar/chess_player_agent/blob/master/data/results/Visualization/performance_03.png)

The general trend shows that the time required to evaluate the moves is very low in the beginning, then this exponentially increases as the game progresses, then it shows a gradual decrease.

Explanation:

**1. Initial Low Evaluation Time**

Initially the number of movable pieces are the Pawns and the Knights. The Pawns can only move maximum of 2 places at once and the Knight can only move to the 3rd row. Having the depth=3, the pawns or other chess pieces are not directly interacting with each otherm hence less possibilities.

**2. Exponential Growth in Evaluation Time**

As more chess pieces are moved on the board, the number of possibilities increases, because of the possibility of captures and check mate conditions. As more pieces are opened as the game progresses, the time required to find all possible moves for each piece increases.

**3. Gradual decrease in Evaluation Time**

The time complexity gradually decreases as more and more pieces are captured as the game progresses.

## Limitations

### Bugs
1. Currently, the check and check mate conditions are flawed. Minimax's King tries to save himself and makes a move. Even though other pieces can block the attack or capture the threatening piece, these moves are not considered during check state.
2. Some times the Algorithm chooses invalid moves under check/check-mate conditions. This is because the logic fails to check if moving the King to a new location may lead to another check/check-mate situation.

Currently, when either of these bugs appear, the game ends and the player who has most captures, is declared the winner on terms of technicality.

### Performance
1. The Algorithm is slow and can be optimized by caching its results, in the sense that the algorithm reevaluates the possible moves for all chess pieces irrespective of the fact that most of them were not moved.

### Presentation
1. This project does not follow the naming standards for the rows and columns on the board.
2. No time Logging for the Human and Random Agent
3. No time display on chess board
4. No Player names displayed on the chess board
