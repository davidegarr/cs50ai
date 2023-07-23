"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    x_count = board[0].count(X) + board[1].count(X) + board[2].count(X)
    o_count = board[0].count(O) + board[1].count(O) + board[2].count(O)

    if x_count > o_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.append((i,j))

    return possible_actions


def result(board, action):
    copied_board = copy.deepcopy(board)

    if board[action[0]][action[1]] == EMPTY:
        copied_board[action[0]][action[1]] = player(board)
    else:
        raise ValueError("Tile already filled.")

    return copied_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #checks if there are any "horizontal" wins
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]

    #checks if there are any "vertical" wins
    for col in range(3):
        if board[0][col] == board [1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]

    #checks if there are any "diagonal" wins
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True

    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if player(board) == X:
        _, action = max_value(board)
    else:
        _, action = min_value(board)


    return action

def max_value(board):
    move = None
    v = float("-inf")
    if terminal(board):
        return utility(board), move

    for action in actions(board):
        new_v, _ = min_value(result(board, action))
        if new_v > v:
            v = new_v
            move = action

    return v, move

def min_value(board):
    move = None
    v = float("inf")
    if terminal(board):
        return utility(board), move

    for action in actions(board):
        new_v, _ = max_value(result(board, action))
        if new_v < v:
            v = new_v
            move = action

    return v, move