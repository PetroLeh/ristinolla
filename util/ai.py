from random import randint
import math
import time

class Minimax:

    def __init__(self, player):
        self.maximizer = player
        self.minimizer = -player
        self.max_depth = 6
        self.printer = False
        self.counter = 0

    def select_move(self, board):   
        return self.select_random(board)
        moves = self.heat_map_as_list(board.heat_map())
        if not moves and not board.is_full():
            return self.select_random(board)

        best = -math.inf
        a = -math.inf
        b = math.inf
        best_move = None
        depth = self.max_depth
        evaluated_boards = {}
        self.counter = 0
        start = time.process_time()
        h_map_max = board.heat_map2(self.maximizer)
        h_map_min = board.heat_map2(self.minimizer)

        for move in moves:
            if board.is_winning(move, self.maximizer):
                print(f'voittava siirto: {move}')
                return move
        for move in moves:
            if board.is_winning(move, self.minimizer):
                print(f'välittömän häviön estävä siirto: {move}')
                return move

        for move in moves:

            row, col = move
            h = h_map_min[row][col]

            board.set_cell(move, self.maximizer)
            score = self.minmax(depth, board, moves, move, self.minimizer, a, b, evaluated_boards, False)
            board.set_empty(move)

            score += h
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
            score = self.evaluate(board)
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


    def evaluate(self, board):
        score = 0

        h_map_max = board.heat_map2(self.maximizer)
        h_map_min = board.heat_map2(self.minimizer)
        mh_max = self.max_heat(h_map_max)
        mh_min = self.max_heat(h_map_min)

        if mh_min == board.winning_length() // 2 + 1: score -= 3

        if board.middle() == self.maximizer: score += 1
        if board.middle() == self.minimizer: score -= 1
        if mh_max > mh_min: score += 2
        if mh_max < mh_min: score -= 2

        if self.total_heat(h_map_max) > self.total_heat(h_map_min): score += 1
        if self.total_heat(h_map_max) < self.total_heat(h_map_min): score += 1
        
        return score

    def max_heat(self, heat_map):
        m = 0
        for row in heat_map:
            m = max(m, max(row))
        return m

    def total_heat(self, heat_map):
        s = 0
        for row in heat_map:
            s += sum(row)
        return s

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