import unittest

from util.ai import Minimax
from util.board import Board

class TestMinimax(unittest.TestCase):
        
    def setup_board_for_test(self, winning_length: int, board_state: list):
        board = Board(len(board_state), winning_length)
        for row in range(len(board_state)):
            for col in range(len(board_state)):
                cell = board_state[row][col]
                if cell:
                    board.set_cell((row, col), board_state[row][col])
        return board
    
    def test_board_is_set_up_correctly(self):
        empty = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        
        full = [
            [1, 1, -1],
            [-1, 1, 1],
            [1, -1, -1]
        ]
        
        empty_board = self.setup_board_for_test(3, empty)
        full_board = self.setup_board_for_test(3, full)
        
        for row in range(empty_board.size()):
            for col in range(empty_board.size()):
                cell = (row, col)
                self.assertTrue(empty_board.is_empty(cell))
                
        self.assertTrue(full_board.is_full())
    
    def test_finds_win_in_3x3(self):
        # 3x3 ruudukko. Aloittaja pelannut keskelle -> jos vastustaja ei pelaa kulmaan, aloittaja voittaa
        X = 1
        O = -1
        
        board_state = [
            [0, O, 0],
            [0, X, 0],
            [0, 0, 0]
        ]
        
        board = self.setup_board_for_test(3, board_state)
        
        ai_one = Minimax(X)
        ai_two = Minimax(O)
        
        turn = X
        winner = None
        
        while True:
            if turn == X:
                move = ai_one.select_move(board)
            else:
                move = ai_two.select_move(board)
            if board.is_winning(move, turn):
                winner = turn
                break
            board.set_cell(move, turn)
            if board.is_full():
                break
            turn *= -1
        
        self.assertEqual(winner, X)
        
    def test_finds_win_in_6x6_first(self):
        # 6x6 ruudukko ja voittoon vaaditaan kolmen suora -> aloittaja voittaa aina
        
        X = 1
        O = -1
        
        board_state = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        
        board = self.setup_board_for_test(3, board_state)
        
        ai_one = Minimax(X)
        ai_two = Minimax(O)
        
        turn = X
        winner = None
        
        while True:
            if turn == X:
                move = ai_one.select_move(board)
            else:
                move = ai_two.select_move(board)
            if board.is_winning(move, turn):
                winner = turn
                break
            board.set_cell(move, turn)
            if board.is_full():
                break
            turn *= -1
        
        self.assertEqual(winner, X)

    def test_finds_win_in_6x6_second(self):
        # pelitilanne seuraava:
        
        # ..OO..
        # OXXX..
        # ....XO
        # ....XO
        # ......
        # ......
        
        # X:n vuoro ja varma voitto seuraavilla siirroilla:

        # ..OO..    ..OO..  ..OO..  ..OOO.
        # OXXXX.    OXXXXO  OXXXXO  OXXXXO
        # ....XO    ....XO  ....XO  ....XO
        # ....XO    ....XO  ....XO  ....XO
        # ......    ......  ....X.  ....X.
        # ......    ......  ......  ....X.
        
        
        X = 1
        O = -1

        board_state = [
            [0, 0, O, O, 0, 0],
            [O, X, X, X, 0, 0],
            [0, 0, 0, 0, X, O],
            [0, 0, 0, 0, X, O],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        
        board = self.setup_board_for_test(3, board_state)
        
        ai_one = Minimax(X)
        ai_two = Minimax(O)
        
        turn = X
        winner = None
        
        while True:
            if turn == X:
                move = ai_one.select_move(board)
            else:
                move = ai_two.select_move(board)
            if board.is_winning(move, turn):
                winner = turn
                break
            board.set_cell(move, turn)
            if board.is_full():
                break
            turn *= -1
        
        self.assertEqual(winner, X)
