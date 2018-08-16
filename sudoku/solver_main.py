import copy
import argparse

from sudoku.models import Sudoku

from sudoku.algorithms import HiddenSingle, FullHouse


class SolverRunner:
    # A runner for algorithms. It takes a list of algorithm class references, instantiates them and executes it
    # against the board. The runner will run the algorithm list left to right and determine the delta. If the delta is
    # 0, it will move down the algorithm list and see if a delta is found. If so, we reset to the beginning of the list.
    # This is because the algorithms on the right are progressively more expensive.

    def __init__(self, sudoku, *args):
        # args is a sequence of algorithms object references to iterate the board over
        self.sudoku = sudoku
        self.algorithms = args

    @staticmethod
    def determine_delta(prev_board, next_board):
        for i in range(0, len(prev_board)):
            for j in range(0, len(prev_board)):
                if prev_board[i][j] != next_board[i][j]:
                    return True
        return False

    @staticmethod
    def is_solved(board):
        # Two ways to determine if it's correct: sum of board is 324 (36*9), or no 0s. Unknown which is faster
        for i in range(0, len(board)):
            for j in range(0, len(board)):
                if board[i][j] == 0:
                    return False
        return True

    def run_solver(self):
        N = 50
        iterations = 0
        algorithm_idx = 0
        solved = self.is_solved(self.sudoku.board)
        while not solved and iterations < N and algorithm_idx < len(algorithms):
            algorithm = algorithms[algorithm_idx]()  # The brackets are crucial to instantiation
            new_state = algorithm.solve(copy.deepcopy(self.sudoku))
            has_delta = self.determine_delta(self.sudoku.board, new_state.board)
            if not has_delta:
                algorithm_idx += 1
            else:
                algorithm_idx = 0
                self.sudoku = new_state
                solved = self.is_solved(self.sudoku.board)
            iterations += 1
        if not solved:
            return False
        else:
            return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A sudoku solver command-line interface")
    parser.add_argument("board", type=str, help="A string representation of the board")

    board_str = "5.3.......89..75.242..316..7..81....8.14.59.6....63..8..437..516.81..49.......2.7"
    sudoku = Sudoku(board_str)
    print(sudoku)
    algorithms = [FullHouse, HiddenSingle]
    solver = SolverRunner(sudoku, algorithms)
    res = solver.run_solver()
    print(res)
    print(solver.sudoku)
