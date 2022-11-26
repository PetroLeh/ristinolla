from random import randint
import math
import time

class Minimax:

    def __init__(self, player, max_depth):
        self.maximizer = player
        self.minimizer = -player
        self.h_map_max = None
        self.h_map_min = None
        self.mh_maximizer = 0
        self.mh_minimizer = 0
        self.max_depth = max_depth
        self.counter = 0

    def select_move(self, board):

        start = time.process_time()

        moves = self.heat_map_as_list(board.heat_map())
        if not moves and not board.is_full():
            return self.select_random(board)

        self.counter = 0

        self.h_map_max = board.heat_map2(self.maximizer)
        self.h_map_min = board.heat_map2(self.minimizer)
        self.mh_maximizer = self.find_max_heat(self.h_map_max)
        self.mh_minimizer = self.find_max_heat(self.h_map_min)

        for move in moves:
            if board.is_winning(move, self.maximizer):
                print(f'voittava siirto: {move}')
                return move
        for move in moves:
            if board.is_winning(move, self.minimizer):
                print(f'välittömän häviön estävä siirto: {move}')
                return move

        best = -math.inf
        a = -math.inf
        b = math.inf
        best_move = None
        depth = self.max_depth
        evaluated_boards = {}
        
        for move in moves:
            row, col = move
            h = self.h_map_min[row][col]

            board.set_cell(move, self.maximizer)
            score = self.minmax(depth, board, moves, move, self.minimizer, a, b, evaluated_boards, False)
            board.set_empty(move)

            score += h
            if board.is_on_border(move): score -= 1
            a = max(a, score)

            print(f'siirto: {move} pisteet: {score} h-arvo: {h}')
            if score > best:
                best = score
                best_move = move
        
        end = time.process_time()
        elapsed = end - start
        print(f'valittu siirto: {best_move} minmax-kutsuja: {self.counter} kesto: {(elapsed):.3f} s (kesto / kutsu: ~{(elapsed*1000/self.counter):.3f} ms)')
        return best_move

    def minmax(self, depth, board, moves, move, turn, a, b, evaluated_boards, terminal):

        self.counter += 1
        if board.is_full() or depth == 0 or terminal:
            score = self.evaluate(board, move)
            return score

        best = -math.inf if turn == self.maximizer else math.inf

        for i, move in enumerate(moves):
            if not board.is_empty(move): continue

            terminal = i == len(moves) - 1
            if turn == self.maximizer:
                if board.is_winning(move, self.maximizer):
                    return 100 - depth
                board.set_cell(move, self.maximizer)
                score = self.minmax(depth - 1, board, moves, move, self.minimizer, a, b, evaluated_boards, terminal)
                best = max(best, score)
                a = max(a, score)
            else:                
                if board.is_winning(move, self.minimizer):
                    return -100 + depth
                board.set_cell(move, self.minimizer)
                score = self.minmax(depth - 1, board, moves, move, self.maximizer, a, b, evaluated_boards, terminal)
                best = min(best, score)
                b = min(b, score)
            board.set_empty(move)
        
            if b <= a: break
        return best

    def evaluate(self, board, move):
        score = 0
        if board.middle() == self.maximizer: score += 1
        if board.middle() == self.minimizer: score -= 1        
        return score

    def find_max_heat(self, heat_map):
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

    def show(self, board):
        c = {
            0: '.',
            1: 'X',
           -1: '0'
        }
        for row in board.grid():
            s = " ".join(map(lambda n: c[n], row))
            print(s)
        print()