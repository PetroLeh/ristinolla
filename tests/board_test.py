import unittest

import board

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.size = 10
        self.board = board.Board(self.size, 3)

    def test_board_has_correct_size(self):        
        self.assertEqual(self.size, self.board.size())
    
    def test_empty_board_is_filled_with_zeros(self):
        for row in self.board.grid():
            row_str = "".join(map(str, row))
            
            self.assertEqual(row_str, "0" * self.size)
    
    def test_setting_a_value_to_empty_cell_works(self):
        player = 1
        
        self.assertEqual(self.board.get_cell((0, 0)), 0)
        self.board.set_cell((0, 0), player)
        self.assertEqual(self.board.get_cell((0, 0)), player)

    def test_value_of_non_empty_cell_cannot_be_changed(self):
        player_one = 1
        player_two = -1

        self.board.set_cell((0, 0), player_one)
        self.board.set_cell((0, 0), player_two)

        self.assertEqual(self.board.get_cell((0, 0)), player_one)
