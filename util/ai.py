from random import randint
import math

class Minimax:

    def __init__(self, player):
        self.maximizer = player
        self.minimizer= -player
        self.max_depth = 6

    def select_move(self, board):   

        moves = self.heat_map_as_list(board.heat_map())
        if not moves and not board.is_full():
            return self.select_random(board)

        best = -math.inf
        a = -math.inf
        b = math.inf
        best_move = None
        depth = self.max_depth
        move_set = {}

        for move in moves:
            
            score = self.minmax(depth, board, move, self.maximizer, a, b, move_set)
            print(f'siirto: {move} pisteet: {score}')
            if score > best:
                best = score
                best_move = move
        
        print(f'valittu siirto: {best_move}')
        return best_move
  

    def minmax(self, depth, board, move, turn, a, b, move_set):
        
        board.set_cell(move, turn)
        if board.is_winning(move, turn):
            board.set_empty(move)
            return 1 if turn == self.maximizer else -1
        
        if board.is_full() or depth == 0:
            board.set_empty(move)
            return 0

        best = -math.inf if turn == self.maximizer else math.inf
        moves = self.heat_map_as_list(board.heat_map())
        if turn == self.maximizer:
            for next_move in moves:
                best = max(best, self.minmax(depth - 1, board, next_move, self.minimizer, a, b, move_set))
                if best <= a:
                    print(f'a: {a} best: {best}')
                    break
        else:
            for next_move in moves:
                best = min(best, self.minmax(depth - 1, board, next_move, self.maximizer, a, b, move_set))
                if best >= b: 
                    print(f'b: {b} best: {best}')
                    break

        board.set_empty(move)
        return best

    def evaluate(self, board):
        h_map_maximizer = board.heat_map2(self.maximizer)
        h_map_minimizer = board.heat_map2(self.minimizer)
        m_heat_maximizer = self.max_heat(h_map_maximizer)
        m_heat_minimizer = self.max_heat(h_map_minimizer)

        if m_heat_maximizer > m_heat_minimizer: return 1
        if m_heat_minimizer > m_heat_maximizer: return -1
        return 0


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

