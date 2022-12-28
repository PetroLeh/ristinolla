import math
import time

from util import config

class Minimax:

    def __init__(self, player):
        self.maximizer = player
        self.minimizer = -player
        self.h_map_max = None
        self.h_map_min = None
        self.counter = 0
        self.board_size = 0
        self.__logger = True

    def select_move(self, board):
        """ Valitsee parhaan siirron tietyssä pelitilanteessa. Jos peliruudukko on tyhjä, valitaan
        satunnainen ruutu peliruudukon keskialueelta. Muussa tapauksessa valitaan ruutu jo
        pelattujen ruutujen viereisistä ruuduista. """

        self.counter = 0
        self.board_size = board.size()

        # haetaan pelaajien tekstisymbolit tulostusta varten
        p_symbol = config.CHARACTERS[self.maximizer]
        print(f'vuorossa: {p_symbol}')

        # haetaan lista peliruuduista, joiden viereen on pelattu
        moves = self.heat_map_as_list(board.heat_map())
        if not moves and not board.is_full():
            move = (board.size() // 2, board.size() // 2)
            print(f'({p_symbol}) ensimmäinen siirto: {move}')
            return move

        # tutkitaan kummankin pelaajan suoranpätkien pituuksia ja haetaan pisimpiä
        self.h_map_min = board.heat_map(self.minimizer)
        self.h_map_max = board.heat_map(self.maximizer)
        mh_max = self.find_max_heat(self.h_map_max)
        mh_min = self.find_max_heat(self.h_map_min)

        # jos joku siirto voittaa suoraan, palautetaan se
        for move in moves:
            if board.is_winning(move, self.maximizer):
                print(f'({p_symbol}) voittava siirto: {move}')
                return move

        # jos vastustaja voittaisi suoraan jollain siirrolla, estetään se
        for move in moves:
            if board.is_winning(move, self.minimizer):
                print(f'({p_symbol}) välittömän häviön estävä siirto: {move}')
                return move

        # järjestetään siirtojen lista siten, että kärjessä on ne ruudut, joissa
        # on pisimpien suorien päät
        if mh_min > mh_max:
            moves.sort(key=lambda move: self.h_map_min[move[0]][move[1]])
        elif mh_min < mh_max:
            moves.sort(key=lambda move: self.h_map_max[move[0]][move[1]])
        else:
            moves.sort(key=lambda move: self.h_map_min[move[0]][move[1]]
                                      + self.h_map_max[move[0]][move[1]])

        best_move = moves[-1]

        for depth in range(3, 12):
            best = -math.inf
            alpha = -math.inf
            beta = math.inf
            evaluated_boards = {}

            start = time.process_time()
            print(f'syvyys: {depth}')

            for move in moves[::-1]:

                # lisätään uuden siirron vierusruudut listaan
                next_moves = self.add_adjacent_cells(move, moves)

                board.set_cell(move, self.maximizer)
                score = self.minmax(depth, board, next_moves, self.minimizer, alpha, beta, evaluated_boards)
                board.set_empty(move)
                if self.__logger:
                    print(f'({p_symbol}) siirto: {move} pisteet: {score}')
                if score > best:
                    best = score
                    best_move = move

            moves.remove(best_move)
            moves.append(best_move)

            end = time.process_time()
            elapsed = end - start
            print(f'laskennan kesto: {elapsed:.3f}')
            if elapsed > 2:
                break

        print()
        print(f'({p_symbol}): {best_move} syvyys: {depth} minmax-kutsuja: {self.counter} ', end ="")
        print(f'kesto: {(elapsed):.3f}s kesto/kutsu: ~{(elapsed*1000/max(1, self.counter)):.3f}ms')
        return best_move

    def minmax(self, depth, board, moves, turn, alpha, beta, evaluated_boards):

        # laskurimuuttuja ei liity algoritmin toimintaan, vaan on ainoastaan lokeja varten.
        self.counter += 1

        board_key = board.get_key()
        if board_key in evaluated_boards:
            if evaluated_boards[board_key][0] == depth:
                return evaluated_boards[board_key][1]

        if depth <= 0 or board.is_full():
            return 0

        if turn == self.maximizer:
            score = -math.inf
            for move in moves[::-1]:
                if not board.is_empty(move):
                    continue
                if board.is_winning(move, self.maximizer):
                    score = math.inf
                else:
                    board.set_cell(move, self.maximizer)
                    next_moves = self.add_adjacent_cells(move, moves)
                    score = max(score, self.minmax(depth - 1, board, next_moves, self.minimizer, alpha, beta, evaluated_boards))
                    board.set_empty(move)
                if score >= beta:
                    break
                alpha = max(alpha, score)
        else:
            score = math.inf
            for move in moves[::-1]:
                if not board.is_empty(move):
                    continue                
                if board.is_winning(move, self.minimizer):
                    score = -math.inf
                else:
                    board.set_cell(move, self.minimizer)
                    next_moves = self.add_adjacent_cells(move, moves)
                    score = min(score, self.minmax(depth - 1, board, next_moves, self.maximizer, alpha, beta, evaluated_boards))
                    board.set_empty(move)
                if score <= alpha:
                    break
                beta = min(beta, score)

        evaluated_boards[board_key] = (depth, score)
        return score

    def add_adjacent_cells(self, move, moves):
        moves_copy = moves.copy()
        moves_copy.remove(move)

        m_row, m_col = move

        rows = range(max(0, m_row - 1), min(self.board_size, m_row + 1))
        cols = range(max(0, m_col - 1), min(self.board_size, m_col + 1))

        for row in rows:
            for col in cols:
                if row == m_row and col == m_col:
                    continue
                moves_copy.append((row, col))
        return moves_copy

    def find_max_heat(self, heat_map):
        max_heat = 0
        for row in heat_map:
            max_heat = max(max_heat, max(row))
        return max_heat

    def heat_map_as_list(self, heat_map):
        res = []
        size = len(heat_map)
        for row in range(size):
            for col in range(size):
                if heat_map[row][col] > 0:
                    res.append((row, col))
        return res

    def set_logger_to(self, value: bool):
        self.__logger = value