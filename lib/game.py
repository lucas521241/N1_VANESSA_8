import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.full((3, 3), ' ')
        self.current_winner = None

    def print_board(self):
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def make_move(self, square, letter):
        if self.board[square[0]][square[1]] == ' ':
            self.board[square[0]][square[1]] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind, col_ind = square
        row_win = all([s == letter for s in self.board[row_ind]])
        col_win = all([s == letter for s in self.board[:, col_ind]])
        diag1_win = all([self.board[i][i] == letter for i in range(3)])
        diag2_win = all([self.board[i][2-i] == letter for i in range(3)])
        return row_win or col_win or diag1_win or diag2_win
