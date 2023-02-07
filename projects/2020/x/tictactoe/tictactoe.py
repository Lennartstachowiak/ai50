"""
Tic Tac Toe Player
"""

import math

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
    x_amount = 0
    o_amount = 0
    for row in board:
        for field in row:
            if field == X:
                x_amount += 1
            elif field == O:
                o_amount += 1
    if x_amount > o_amount:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = []
    for row_index, row in enumerate(board):
        for field_index, field in enumerate(row):
            if field != X and field != O:
                moves.append((row_index, field_index))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    which_turn = player(board)
    board[action[0]][action[1]] = which_turn
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winning_plays = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]
    player = X
    for play in winning_plays:
        skip = False
        for field in play:
            if board[field[0]][field[1]] != player:
                skip = True
                break
        if not skip:
            return player

    player = O
    for play in winning_plays:
        skip = False
        for field in play:
            if board[field[0]][field[1]] != player:
                skip = True
                break
        if not skip:
            return player

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None and len(actions(board)) <= 0:
        return True
    else:
        return False


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
    copy_board = board.copy()
    which_turn = player(copy_board)
    moves = actions(copy_board)
    print("moves", moves)
    if len(moves) > 0:
        for move in moves:
            new_board = result(copy_board, move)
            print(new_board)
            minimax(new_board)
    print("Done")


minimax(initial_state())
