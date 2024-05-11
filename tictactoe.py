# Libraries
import math
import copy
import random

# Globals
X = "X"
O = "O"
EMPTY = None

# Initial State
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# Function to find player
def player(board):
    x_count = 0
    o_count = 0
    
    for row in board:
        for item in row:
            if item == X:
                x_count += 1
            if item == O:
                o_count += 1

    # Check for game over
    if x_count >= 5:
        return "Game Over"
    
    # If more X's than O's, it is X turn
    if x_count > o_count:
        return O
    else:
        return X 

# All possible actions
def actions(board):
    moves = []
    free_box = tuple()
    row_num = -1

    # Check each cell for empty space
    for row in board:
        row_num += 1
        for box in range(len(row)):
            if board[row_num][box] == EMPTY:
                free_box = (row_num, box)
                moves.append(free_box)
    return moves

# Result of current board and intended action
def result(board, action):
    if board[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid Action")
    else:
        turn = player(board)

        # Deepcopy to avoid changing original
        updated = copy.deepcopy(board)
        updated[action[0]][action[1]] = turn
    return updated

# Determine winner with terminal board
def winner(board):

    # Check rows for winner
    for row in board: 
        if X in row and O not in row and EMPTY not in row:
            return X
        elif O in row and X not in row and EMPTY not in row:
            return O
    
    # Check columns for winner
    for column in range(len(board)):
        column = [board[0][column],  
                  board[1][column], 
                  board[2][column]]
        if X in column and O not in column and EMPTY not in column:
            return X
        elif O in column and X not in column and EMPTY not in column:
            return O
        
    # Checks diagonals for winner
    diagonal1 = [board[0][0],  
                  board[1][1], 
                  board[2][2]]
    diagonal2 = [board[2][0],  
                  board[1][1], 
                  board[0][2]]
    if X in diagonal1 and O not in diagonal1 and EMPTY not in diagonal1:
        return X
    elif O in diagonal1 and X not in diagonal1 and EMPTY not in diagonal1:
        return O
    
    if X in diagonal2 and O not in diagonal2 and EMPTY not in diagonal2:
        return X
    elif O in diagonal2 and X not in diagonal2 and EMPTY not in diagonal2:
        return O  

# Check if board is terminal
def terminal(board):
    if winner(board) == X or winner(board) == O:
        return True
    
    for row in board: 
        for box in row:
            if box == EMPTY:
                return False
    return True

# Assign utility to a terminal board
def utility(board):
    won = winner(board)
    if won == 'X':
        return int(1)
    if won == "O":
        return int(-1)
    else:
        return int(0)

# Minimax algorithm implementation
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # If initial board terminal, no actions possible
    if terminal(board):
        return None
    
    # Check if AI is "X" or max player
    if player(board) == "X":
        _, action = max_value(board) 
        return action
    
    # Check if AI is "O" or min player
    else:
        _, action = min_value(board) 
        return action

def max_value(board):

    # Terminal board assigned a utility and returned
    # Recursive ending condition 
    if terminal(board):
        return utility(board), None
    
    # Variables to store best/max actions and utilities
    max_utility = float('-inf')
    max_action = None

    for action in actions(board):

        # Calls min_value for each child action
        eval, _ = min_value(result(board, action))

        # Once recursion complete and terminal state reached finds lowest utility
        if eval > max_utility:

            # Stored in variables
            max_utility = eval
            max_action = action

            # Alpha-beta pruning
            if max_utility == 1:
                return max_utility, max_action
    
    # Returns best action and utility
    return max_utility, max_action

def min_value(board):

    # Terminal board assigned a utility and returned
    # Recursive ending condition 
    if terminal(board):
        return utility(board), None
    
    # Variables to store best/min actions and utilities
    min_utility = float('inf')
    min_action = None
    for action in actions(board):

        # Calls max_value for each child action
        eval, _= (max_value(result(board, action)))

        # Once recursion complete and terminal state reached finds lowest utility
        if eval < min_utility:
            min_utility = eval 

            # Alpha-beta pruning
            min_action = action
            if eval == -1:
                return eval, action
    return min_utility, min_action