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
            if field is EMPTY:
                moves.append((row_index, field_index))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copy_board = copy.deepcopy(board)
    which_turn = player(board)
    copy_board[action[0]][action[1]] = which_turn
    return copy_board


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
    if winner(board) != None or len(actions(board)) <= 0:
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


def max_value(board, lowest_value):
    if terminal(board):
        return utility(board)
    highest_value = -math.inf
    for action in actions(board):
        current_value = min_value(result(board, action), highest_value)
        highest_value = max(highest_value, current_value)
    return highest_value


def min_value(board, highest_value):
    if terminal(board):
        return utility(board)
    lowest_value = math.inf
    for action in actions(board):
        current_value = max_value(result(board, action), lowest_value)
        lowest_value = min(lowest_value, current_value)
    return lowest_value


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    which_turn = player(board)
    possible_actions = actions(board)

    if which_turn is X:
        best_score = -1
        best_move = None
        for possible_action in possible_actions:
            if best_score == 1:
                return best_move
            new_board = result(board, possible_action)
            score = min_value(new_board, best_score)
            if score > best_score:
                best_score = score
                best_move = possible_action
        return best_move

    if which_turn is O:
        best_score = 1
        best_move = None
        for possible_action in possible_actions:
            if best_score == -1:
                return best_move
            new_board = result(board, possible_action)
            score = max_value(new_board, best_score)
            if score < best_score:
                best_score = score
                best_move = possible_action
        return best_move


minimax(initial_state())
