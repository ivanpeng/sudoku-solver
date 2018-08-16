

def assign_answer_to_board(sudoku, x, y):
    (answer,) = sudoku.cell_possibilities[x*9+y].possibilities
    sudoku.board[x][y] = answer


def get_row(sudoku, i):
    # We need a tuple of value and its associated possibilities
    # I.e. we need a way to map the ith row to the values in cell_possibilities, which is a 1d array 0-81
    return [(sudoku.board[i][j], sudoku.cell_possibilities[i * 9 + j]) for j in range(0, len(sudoku.board))]


def get_col(sudoku, i):
    return [(sudoku.board[j][i], sudoku.cell_possibilities[i + j * 9]) for j in range(0, len(sudoku.board))]


def get_box(sudoku, i):
    # [sudoku.board[int(i / 3) * 3 + int(j / 3)][i % 3 * 3 + j % 3] for j in range(0, len(sudoku.board))]
    return [(sudoku.board[int(i / 3) * 3 + int(j / 3)][i % 3 * 3 + j % 3],
             sudoku.cell_possibilities[(int(i / 3) * 3 + int(j / 3)) * 9 + (i % 3 * 3 + j % 3)])
            for j in range(0, len(sudoku.board))]


def _remove_generic(arr):
    s = set()
    for element in arr:
        n, possibility = element
        if n != 0:
            s.add(n)
    for element in arr:
        n, possibility = element
        if n == 0:
            possibility.possibilities -= s


def remove_possibilities(sudoku, x, y):
    row = get_row(sudoku, x)
    col = get_col(sudoku, y)
    box = get_box(sudoku, int(x / 3) * 3 + int(y / 3))
    # For each one, remove all cell_possibilities that have values
    _remove_generic(row)
    _remove_generic(col)
    _remove_generic(box)


class FullHouse:
    def solve(self, sudoku):
        # This is the simplest algorithm: if there is only one possibility for a cell, it's that! Just scan all
        # cells, and fill all cells with only one possibility Remove all boxes afterwards Recall that
        # sudoku.possibilities is a 1x81 array, so all we have to do is have the correct x and y to remove indexes
        for i in range(0, len(sudoku.board)):
            for j in range(0, len(sudoku.board[i])):
                remove_possibilities(sudoku, i, j)
                if sudoku.board[i][j] == 0 and len(sudoku.cell_possibilities[i*9+j].possibilities) == 1:
                    # This is the condition that we want
                    # Set board to that, and then empty cell possibilities
                    assign_answer_to_board(sudoku, i, j)
        return sudoku


class NakedSingle:
    def solve(self, sudoku):
        # Eliminate set items via
        return sudoku


class HiddenSingle:
    def solve(self, sudoku):
        return sudoku


'''
Okay, let's see here. We have taken a functional approach, but we need to have the remove_possibilities function work.
We have a mapping function that goes from box to row. Do we have the inverse? Yes
What do we need now?


'''
