from random import randint
import math
import time

from util import config

class Minimax:

    def __init__(self, player, max_depth):
        self.maximizer = player
        self.minimizer = -player
        self.h_map_max = None
        self.h_map_min = None
        self.max_depth = max_depth
        self.counter = 0
        self.logging = True

    def select_move(self, board):
        """ Valitsee parhaan siirron tietyssä pelitilanteessa. Jos peliruudukko on tyhjä, valitaan
        satunnainen ruutu peliruudukon keskialueelta. Muussa tapauksessa valitaan ruutu jo
        pelattujen ruutujen viereisistä ruuduista. """

        # haetaan pelaajien tekstisymbolit tulostusta varten
        p_symbol = config.CHARACTERS[self.maximizer]

        print()
        start = time.process_time()

        # haetaan lista peliruuduista, joiden viereen on pelattu
        moves = self.heat_map_as_list(board.heat_map())
        if not moves and not board.is_full():
            move = self.select_random(board)
            print(f'({p_symbol}) satunnainen siirto: {move}')
            return move

        self.counter = 0

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
        moves.sort(key=lambda move: self.h_map_max[move[0]][move[1]] + self.h_map_min[move[0]][move[1]], reverse=True)

        # jos vastustajalla on pidempää pätkää valitaan puolustava taktiikka, muutoin hyökkäävä
        choose_to_defence = mh_min > mh_max

        best = -math.inf
        alpha = -math.inf
        beta = math.inf

        for move in moves:
            row, col = move

            # jos on valittu puolustuslinja, painotetaan ruutuja, joissa on
            # vastustajan suorien päät...
            if choose_to_defence:
                heat = self.h_map_max[row][col] + self.h_map_min[row][col] * 3

            # ...muuten painotetaan omia suoria
            # jos saadaan muodostettua suora, joka on 4 mittainen tai avoin 3 palautetaan se
            else:
                if self.h_map_max[row][col] > 3:
                    print(f'({p_symbol}) hyökkäävä siirto: {move}')
                    return move
                heat = self.h_map_max[row][col] * 3 + self.h_map_min[row][col]

            # siirto ei ole vielä osoittautunut voittavaksi tai välttämättömäksi
            # puolustaa -> lasketaan sen arvo
            board.set_cell(move, self.maximizer)
            score = self.minmax(self.max_depth, board, moves, self.minimizer, alpha, beta, False)
            board.set_empty(move)

            # lisätään aiemmin laskettu puolustus/hyökkäys -arvo
            score += heat

            # vähennetään vielä piste, jos ruutu on aivan laudan reunalla
            if board.is_on_border(move):
                score -= 1

            alpha = max(alpha, score)

            if self.logging:
                print(f'({p_symbol}) siirto: {move} pisteet: {score} h-arvo: {heat}')
            if score > best:
                best = score
                best_move = move

        end = time.process_time()
        elapsed = end - start
        motivate = 'puolustava siirto' if choose_to_defence else 'hyökkäävä siirto'

        print()
        print(f'({p_symbol}) {motivate}: {best_move} minmax-kutsuja: {self.counter} ', end ="")
        print(f'kesto: {(elapsed):.3f}s kesto/kutsu: ~{(elapsed*1000/max(1, self.counter)):.3f}ms')
        return best_move

    def minmax(self, depth, board, moves, turn, alpha, beta, is_terminal):

        # laskurimuuttuja ei liity algoritmin toimintaa, vaan on ainoastaan lokeja varten.
        self.counter += 1

        if board.is_full() or depth <= 0 or is_terminal:
            return 0

        best = -math.inf if turn == self.maximizer else math.inf

        for i, move in enumerate(moves):
            if not board.is_empty(move):
                continue

            is_terminal = i == len(moves) - 1
            if turn == self.maximizer:
                row, col = move
                if self.h_map_max[row][col] > 3:
                    score = 10
                else:
                    board.set_cell(move, self.maximizer)
                    score = self.minmax(depth - 1, board, moves, self.minimizer, alpha, beta, is_terminal)
                best = max(best, score)
                alpha = max(alpha, score)
            else:
                row, col = move
                if self.h_map_min[row][col] > 3:
                    score = -10
                else:
                    board.set_cell(move, self.minimizer)
                    score = self.minmax(depth - 1, board, moves, self.maximizer, alpha, beta, is_terminal)
                best = min(best, score)
                beta = min(beta, score)
            board.set_empty(move)

            if beta <= alpha:
                break
        return best

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

    def select_random(self, board):
        min_val, max_val = self.get_bounds_for_random_move(board)
        row = randint(min_val, max_val)
        col = randint(min_val, max_val)
        return (row, col)

    def get_bounds_for_random_move(self, board):
        middle = board.size() // 2
        min_val = middle - middle // 2
        max_val = middle + middle // 2
        return (min_val, max_val)

    def set_logger_to(self, value: bool):
        self.logging = value
