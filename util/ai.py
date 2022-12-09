from random import randint
import math
import time

class Minimax:

    def __init__(self, player, max_depth):
        self.maximizer = player
        self.minimizer = -player
        self.h_map_max = None
        self.h_map_min = None
        self.mh_max = 0
        self.mh_min = 0
        self.max_depth = max_depth
        self.counter = 0
        self.use_of_dict = 0

    def select_move(self, board):

        print()
        start = time.process_time()

        moves = self.heat_map_as_list(board.heat_map())
        if not moves and not board.is_full():
            move = self.select_random(board)
            print(f'satunnainen siirto: {move}')
            return move

        self.counter = 0

        self.h_map_min = board.heat_map(self.minimizer)
        self.h_map_max = board.heat_map(self.maximizer)

        self.mh_max = self.find_max_heat(self.h_map_max)
        self.mh_min = self.find_max_heat(self.h_map_min)

        for move in moves:
            if board.is_winning(move, self.maximizer):
                print(f'voittava siirto: {move}')
                return move
        for move in moves:
            if board.is_winning(move, self.minimizer):
                print(f'välittömän häviön estävä siirto: {move}')
                return move
        
        moves.sort(key=lambda move: self.h_map_max[move[0]][move[1]] + self.h_map_min[move[0]][move[1]], reverse=True)
        
        choose_to_defence = True if self.mh_min > self.mh_max else False

        best = -math.inf
        a = -math.inf
        b = math.inf
        best_move = None
        depth = self.max_depth
        evaluated_boards = {}
        
        for move in moves:
            row, col = move

            if choose_to_defence: h = self.h_map_max[row][col] + self.h_map_min[row][col] * 3
            else: h = self.h_map_max[row][col] * 3 + self.h_map_min[row][col]

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
        motivate = "puolustava siirto" if choose_to_defence else "hyökkäävä siirto"

        print()
        print(f'{motivate}: {best_move} minmax-kutsuja: {self.counter} kesto: {(elapsed):.3f} s (kesto / kutsu: ~{(elapsed*1000/self.counter):.3f} ms) hajautustaulun käyttö: {self.use_of_dict} kertaa')
        return best_move

    def minmax(self, depth, board, moves, move, turn, a, b, evaluated_boards, terminal):

        self.counter += 1
        if board.key() in evaluated_boards:
            self.use_of_dict += 1
            return evaluated_boards[board.key()]

        if board.is_full() or depth == 0 or terminal:
            score = self.evaluate(board, move, evaluated_boards)
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

    def evaluate(self, board, move, evaluated_boards):
        score = 0
        if board.middle() == self.maximizer: score += 1
        if board.middle() == self.minimizer: score -= 1
        evaluated_boards[board.key()] = score 
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

    def print_heatmap(self, h_map):
        for row in h_map:
            s = " ".join(map(str, row))
            print(s)