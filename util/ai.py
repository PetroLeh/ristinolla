from random import randint
import math

class Minimax:

    def __init__(self, player):
        self.maximizer = player
        self.minimizer= -player

    def select_move(self, board):
        #move = self.select_random(board)

        move, score = self.minmax(board, math.inf, -math.inf, self.maximizer, None)
        
        print(move)
        return move
  

    def minmax(self, board, a, b, turn, last_move):

        if last_move: 
            last_cell, last_player = last_move

            if board.is_winning(last_cell, last_player):
                score = 1000 if last_player == self.maximizer else -1000
                return (last_cell, score)
            if board.is_full():
                return (last_cell, self.evaluate(board, turn))

        moves = self.heat_map_as_list(board.heat_map())
        best_move = moves[0]

        best_score = -math.inf if turn == self.maximizer else math.inf

        for move in moves:
            board.set_cell(move, turn)
            last_move = (move, turn)
            m, score = self.minmax(board, a, b, turn * -1, last_move)
            board.set_empty(move)
            if turn == self.maximizer:
                if score > best_score:
                    best_score = score
                    best_move = m
                a = max(a, score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = m
                b = min(b, score)                
            if b <= a:
                break
        return (best_move, best_score)

    def evaluate(self, board, player):
        h_map_maximizer = board.heat_map2(self.maximizer)
        h_map_minimizer = board.heat_map2(self.minimizer)
        m_heat_maximizer = self.max_heat(h_map_maximizer)
        m_heat_minimizer = self.max_heat(h_map_minimizer)

        if player == self.maximizer:
            if m_heat_maximizer > m_heat_minimizer:
                return m_heat_maximizer
            return -m_heat_minimizer * 10
        
        if m_heat_minimizer > m_heat_maximizer:
            return -m_heat_minimizer
        return m_heat_maximizer * 10


    def max_heat(self, heat_map):
        m = 0
        for row in heat_map:
            m = max(m, max(row))
        return m

    def heat_map_as_list(self, heat_map):
        res = []
        for row in range(len(heat_map)):
            for col in range(len(heat_map)):
                if heat_map[row][col] > 0: res.append((row, col))
        return res

    def select_random(self, board):
        row = randint(0, board.size() - 1)
        col = randint(0, board.size() - 1)

        return (row, col)

