# There is a possibility we can replace board with a list of cells, but I'll leave it for now
from sudoku.exceptions import BoardInputException


class Sudoku:
    # Board is a 2d array, 9x9
    # cell_possibilities is a list of CellPossibility objects describing the options at point
    def __init__(self, board):
        if isinstance(board, str):
            self.board = self.convert_to_board(board)
        else:
            self.board = board
        self.cell_possibilities = self.determine_possibilities(self.board)

    @staticmethod
    def convert_to_board(board_str):
        # board is a string which we will convert to 2d array
        if len(board_str) != 81:
            print("Board length is not 81")
            raise BoardInputException
        processed_board_str = [int(x) for x in board_str.replace(".", "0")]
        board = [processed_board_str[i:i+9] for i in range(0, len(processed_board_str), 9)]
        return board

    @staticmethod
    def determine_possibilities(board):
        # Calculate the board value
        possibilities = []
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                p = {board[i][j]} if board[i][j] != 0 else {1, 2, 3, 4, 5, 6, 7, 8, 9}
                possibilities.append(CellPossibilities(i, j, p))
        return possibilities

    def __str__(self):
        output = "-" * 19 + "\n"
        for i in self.board:
            s = "|" + "|".join([str(x) for x in i]) + "|\n"
            output += s
        output += "-" * 19 + "\n"
        return output


class SudokuHistory:
    sudoku_orientations = []

    def __init__(self, initial):
        self.sudoku_orientations.append(initial)

    def add_state(self, state):
        self.sudoku_orientations.append(state)

    def __str__(self):
        output = ""
        for i in range(0, len(self.sudoku_orientations)):
            output += "Output at iteration %d:\n" % i
            output += str(self.sudoku_orientations[i]) + "\n"
        return output


class CellPossibilities:
    def __init__(self, x, y, possibilities):
        self.x = x
        self.y = y
        self.possibilities = possibilities

    def __str__(self):
        return "Possibilities for cell ({self.x}, {self.y}): {self.possibilities}".format(self=self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


if __name__ == '__main__':
    board_str = "86..2.......7...59.............6.8...4.........53....7..........2....6....75.9..."
    sudoku = Sudoku(board_str)
    print(sudoku)