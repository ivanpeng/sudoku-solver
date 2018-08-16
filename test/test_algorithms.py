import unittest

from sudoku.models import Sudoku, CellPossibilities

from sudoku.algorithms import get_row, get_col, get_box, FullHouse, _remove_generic, remove_possibilities


class TestAlgorithms(unittest.TestCase):
    def test_get_row_is_correct(self):
        board_str = "86..2.......7...59.............6.8...4.........53....7..........2....6....75.9..."
        sudoku = Sudoku(board_str)
        row = get_row(sudoku, 0)
        self.assertListEqual([x[0] for x in row], [8, 6, 0, 0, 2, 0, 0, 0, 0])
        self.assertTrue(row[0][1] == CellPossibilities(0, 0, {8}))
        self.assertTrue(row[2][1] == CellPossibilities(0, 2, {1, 2, 3, 4, 5, 6, 7, 8, 9}))

    def test_get_col_is_correct(self):
        board_str = "86..2.......7...59.............6.8...4.........53....7..........2....6....75.9..."
        sudoku = Sudoku(board_str)
        col = get_col(sudoku, 0)
        self.assertListEqual([x[0] for x in col], [8, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertTrue(col[0][1] == CellPossibilities(0, 0, {8}))
        self.assertTrue(col[2][1] == CellPossibilities(2, 0, {1, 2, 3, 4, 5, 6, 7, 8, 9}))

    def test_get_box_is_correct(self):
        board_str = "86..2.......7...59.............6.8...4.........53....7..........2....6....75.9..."
        sudoku = Sudoku(board_str)
        x = 5
        y = 7
        z = int(x / 3) * 3 + int(y / 3)
        box = get_box(sudoku, z)
        self.assertListEqual([x[0] for x in box], [8, 0, 0, 0, 0, 0, 0, 0, 7])
        self.assertTrue(box[0][1] == CellPossibilities(3, 6, {8}))
        self.assertTrue(box[7][1] == CellPossibilities(5, 7, {1, 2, 3, 4, 5, 6, 7, 8, 9}))

    def test_get_box_is_correct_2(self):
        board_str = "86..2.......7...59.............6.8...4.........53....7..........2....6....75.9..."
        sudoku = Sudoku(board_str)
        box = get_box(sudoku, 5)
        self.assertListEqual([x[0] for x in box], [8, 0, 0, 0, 0, 0, 0, 0, 7])

    def test_remove_from_set_row_is_correct(self):
        board_str = "786435.92351926647429176538192354876637289415548761923874512369215693784963847251"
        sudoku = Sudoku(board_str)
        self.assertSetEqual({1, 2, 3, 4, 5, 6, 7, 8, 9}, sudoku.cell_possibilities[6].possibilities)
        row = get_row(sudoku, 0)
        _remove_generic(row)
        self.assertSetEqual({1}, sudoku.cell_possibilities[6].possibilities)

    def test_remove_from_set_col_is_correct(self):
        board_str = "786435..2351926647429176538192354876637289415548761923874512369215693784963847251"
        sudoku = Sudoku(board_str)
        row = get_row(sudoku, 0)
        col = get_col(sudoku, 6)
        _remove_generic(row)
        self.assertSetEqual({1, 9}, sudoku.cell_possibilities[6].possibilities)
        _remove_generic(col)
        self.assertSetEqual({1}, sudoku.cell_possibilities[6].possibilities)

    def test_remove_from_set_box_is_correct(self):
        board_str = "786435..2351926647429176538192354876637289415548761923874512369215693784963847251"
        sudoku = Sudoku(board_str)
        box = get_box(sudoku, 2)
        _remove_generic(box)
        self.assertSetEqual({1, 9}, sudoku.cell_possibilities[6].possibilities)

    def test_remove_possibilities_is_correct(self):
        board_str = "786435...351926647429176538192354...637289415548761923874512369215693784963847251"
        sudoku = Sudoku(board_str)
        remove_possibilities(sudoku, 0, 6)
        self.assertSetEqual({1}, sudoku.cell_possibilities[6].possibilities)
        remove_possibilities(sudoku, 3, 7)
        self.assertSetEqual({7}, sudoku.cell_possibilities[34].possibilities)
        remove_possibilities(sudoku, 0, 8)
        self.assertSetEqual({2}, sudoku.cell_possibilities[8].possibilities)


class TestFullHouseAlgorithm(unittest.TestCase):

    def test_full_house_solves_board(self):
        board_str = "786435...351926647429176538192354...637289415548761923874512369215693784963847251"
        sudoku = Sudoku(board_str)
        fh = FullHouse()
        res = fh.solve(sudoku)
        self.assertEqual(res.board[0][6], 1)
        self.assertEqual(res.board[0][7], 9)
        self.assertEqual(res.board[0][8], 2)
        self.assertEqual(res.board[3][6], 8)
        self.assertEqual(res.board[3][7], 7)
        self.assertEqual(res.board[3][8], 6)
