import unittest

from util.board import Board

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.size = 10
        self.winning_length = 3
        self.board = Board(self.size, self.winning_length)

    def test_board_has_correct_size(self):        
        self.assertEqual(self.size, self.board.size())
        
    def test_winning_length(self):
        self.assertEqual(self.winning_length, self.board.winning_length())
    
    def test_empty_board_is_filled_with_zeros(self):
        for row in self.board.grid():
            row_str = "".join(map(str, row))
            
            self.assertEqual(row_str, "0" * self.size)
    
    def test_setting_a_value_to_empty_cell_works(self):
        player = 1
        
        self.assertFalse(self.board.set_cell(None, player))
        self.assertFalse(self.board.set_cell((0, 0), None))
        
        self.assertEqual(self.board.get_cell((0, 0)), 0)
        self.board.set_cell((0, 0), player)
        self.assertEqual(self.board.get_cell((0, 0)), player)

    def test_value_of_non_empty_cell_cannot_be_changed(self):
        player_one = 1
        player_two = -1

        self.board.set_cell((0, 0), player_one)
        self.board.set_cell((0, 0), player_two)

        self.assertEqual(self.board.get_cell((0, 0)), player_one)
    
    def test_is_on_board(self):
        size = self.board.size()

        self.assertTrue(self.board.is_on_board((0, 0)))
        self.assertTrue(self.board.is_on_board((size - 1, size - 1)))

        self.assertFalse(self.board.is_on_board((size, size)))
    
    def test_empty_cell_check(self):
        player = 1
        self.assertTrue(self.board.is_empty((0, 0)))
        self.assertFalse(self.board.is_empty((-1, 0)))

        self.board.set_cell((0, 0), player)
        self.assertFalse(self.board.is_empty((0, 0)))
        
        
    def test_get_cell_out_of_board_is_none(self):
        self.assertIsNone(self.board.get_cell((-1, -1)))
        self.assertIsNone(self.board.get_cell((0, self.board.size())))
    
    def test_set_cell_empty(self):
        player = 1
        
        self.board.set_cell((0, 0), player)
        self.assertFalse(self.board.is_empty((0, 0)))

        self.board.set_empty((0, 0))
        self.assertTrue(self.board.is_empty((0, 0)))
        
        self.board.set_empty((0, 0))
        self.assertTrue(self.board.is_empty((0, 0)))

    def test_clear_board(self):
        player = 1
        size = self.board.size()

        for i in range(size):
            self.board.set_cell((i, i), player)
            self.board.set_cell((i, size - i), player)
        
        self.board.clear()
        for row in self.board.grid():
            row_str = "".join(map(str, row))
            
            self.assertEqual(row_str, "0" * self.size)
    
    def test_full_board_check(self):
        player = 1
        size = self.board.size()

        self.assertFalse(self.board.is_full())

        for row in range(size):
            for col in range(size):
                self.board.set_cell((row, col), player)
        
        self.assertTrue(self.board.is_full())

    def test_move_is_not_a_winning_move(self):
        player_one = 1
        player_two = -1
        length = self.winning_length - 1
        
        self.assertFalse(self.board.is_winning(None, player_one))

        for i in range(length):
            move = (0, i)
            self.assertFalse(self.board.is_winning(move, player_one))
            self.board.set_cell(move, player_one)
        
        move = (0, length)
        self.assertFalse(self.board.is_winning(move, player_two))
        
    
    def test_move_is_a_winning_move(self):
        player = 1
        length = self.winning_length - 1

        for i in range(length):
            move = (0, i)
            self.board.set_cell(move, player)
        
        move = (0, length)
        self.assertTrue(self.board.is_winning(move, player))

        self.board.clear()

        for i in range(length - 1):
            move = (0, i)
            self.board.set_cell(move, player)
        self.board.set_cell((0, length), player)

        move = (0, length - 1)
        self.assertTrue(self.board.is_winning(move, player))

    def test_heat_map_returns_something_reasonable(self):
        player = 1
        h_map = self.board.heat_map()
        self.assertEqual(h_map[0][0], 0)
        
        self.board.set_cell((1, 1), player)
        h_map = self.board.heat_map()
        a = h_map[0][0]
        self.assertGreater(a, 0)

        self.board.set_cell((1, 0), player)
        h_map = self.board.heat_map()
        self.assertGreater(h_map[0][0], a)
