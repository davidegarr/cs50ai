from tictactoe import initial_state, player, actions, result, winner, terminal, utility

def main():
    X = "X"
    O = "O"
    EMPTY = None

    board = [[O, X, O],
            [O, X, X],
            [EMPTY, O, X]]


    if player(board) == X:
        v, action = max_value(board)
    else:
        v, action = min_value(board)


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


main()