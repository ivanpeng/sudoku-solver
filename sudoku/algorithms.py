

def assign_answer_to_board(sudoku, x, y, answer):
    sudoku.cell_possibilities[x*9+y].possibilities = {answer}
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


def get_sets_for_cell(sudoku, x, y):
    return get_box(sudoku, x), get_col(sudoku, y), get_box(sudoku, int(x / 3) * 3 + int(y / 3))


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
    if sudoku.board[x][y] == 0:
        row, col, box = get_sets_for_cell(sudoku, x, y)
        # For each one, remove all cell_possibilities that have values
        _remove_generic(row)
        _remove_generic(col)
        _remove_generic(box)


class FullHouse:
    """
    TODO: a cleaner way to get more comprehensive fill in one go is to remove all possibilities first, then loop through
    and fill the appropriate boxes. But the delta in algorithm solver picks it up either way. It may cause some
    unintended consequences though.
    """
    def solve(self, sudoku):
        # This is the simplest algorithm: if there is only one possibility for a cell, it's that! Just scan all
        # cells, and fill all cells with only one possibility Remove all boxes afterwards Recall that
        # sudoku.possibilities is a 1x81 array, so all we have to do is have the correct x and y to remove indexes
        for i in range(0, len(sudoku.board)):
            for j in range(0, len(sudoku.board[i])):
                remove_possibilities(sudoku, i, j)
        for i in range(0, len(sudoku.board)):
            for j in range(0, len(sudoku.board[i])):
                if sudoku.board[i][j] == 0 and len(sudoku.cell_possibilities[i*9+j].possibilities) == 1:
                    # This is the condition that we want
                    # Set board to that, and then empty cell possibilities
                    # Get first element of set, because apparently that's tough
                    (answer,) = sudoku.cell_possibilities[i*9+j].possibilities
                    assign_answer_to_board(sudoku, i, j, answer)
        return sudoku


class HiddenSingle:

    @staticmethod
    def _count_occurrence_in_set(array_of_sets, n):
        count = 0
        for s in array_of_sets:
            if n in s:
                count += 1
        return count

    def _count_all_occurrences_in_set(self, array_of_sets):
        for i in range(0, 9):
            c = self._count_occurrence_in_set(array_of_sets, i+1)
            if c == 1:
                return i+1
        return 0

    def solve(self, sudoku):
        # The algorithm to this is simple: instead of counting the possibilities, we can also count the occurrences of
        # possibilities. If the number of occurrences is only 1, then that cell is populated by that value.
        # Contrary to naked single, we *MUST* have the board in a clean state to do this. Else we have erroneous fills
        for i in range(0, len(sudoku.board)):
            for j in range(0, len(sudoku.board[i])):
                remove_possibilities(sudoku, i, j)
        # Need
        for i in range(0, len(sudoku.board)):
            for j in range(0, len(sudoku.board[i])):
                row, col, box = get_sets_for_cell(sudoku, i, j)
                if sudoku.board[i][j] == 0:
                    answer_row = self._count_all_occurrences_in_set(
                        [x[1].possibilities if len(x[1].possibilities) != 1 else {} for x in row])
                    if answer_row != 0:
                        assign_answer_to_board(sudoku, i, j, answer_row)
                        return sudoku
                    answer_col = self._count_all_occurrences_in_set(
                        [x[1].possibilities if len(x[1].possibilities) != 1 else {} for x in col])
                    if answer_col != 0:
                        assign_answer_to_board(sudoku, i, j, answer_col)
                        return sudoku
                    answer_box = self._count_all_occurrences_in_set(
                        [x[1].possibilities if len(x[1].possibilities) != 1 else {} for x in box])
                    if answer_box != 0:
                        assign_answer_to_board(sudoku, i, j, answer_box)
                        return sudoku
        return sudoku


class NakedDouble:
    def solve(self, sudoku):
        # The alogrithm here is that if there are two cells that only have these two numbers and these two numbers only,
        # then all other possibilities may be removed
        return sudoku

'''

TODO:
- generalize to NakedN
- hiddenN?
    - at least a good brainstorm exercise

'''
