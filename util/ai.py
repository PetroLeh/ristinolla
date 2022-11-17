from random import randint

class Minimax:

    def __init__(self, player):
        self.__player = player
        self.__opponent = -player

    def select_move(self, board):
        move = self.select_random(board)
        #best, move = self.minmax(None, board, True)

        #best, move = self.minmax_v2(2, board, self.__player, None)
        return move

    def minmax_v2(self, depth, board, turn, move):
        if turn == self.__player:
            best = -1000
            if board.is_winning(move, self.__player):
                return (1000, move)
        else:
            best = 1000
            if board.is_winning(move, self.__opponent):
                return (-1000, move)
        
        if board.is_full() or depth == 0:
            return (0, move)
        
        size = board.size()
        for row in range(size):
            for col in range(size):
                cell = (row, col)
                if board.is_empty(cell):
                    board.set_cell(cell, turn)
                    score, m = self.minmax_v2(depth - 1, board, turn*-1, cell)
                    board.set_empty(cell)
                    if turn == self.__player:
                        if score > best:
                            best = score
                            move = m
                    else:
                        if score < best:
                            best = score
                            move = m
        return (best, move)

    def minmax(self, move, board, maximizing):
        
        if maximizing:
            best_score = -1000
            turn = self.__player
        else:
            best_score = 1000
            turn = self.__opponent
        
        if maximizing and board.is_winning(move, self.__player):
            return (1000, move)
        elif not maximizing and board.is_winning(move, self.__opponent):
            return (-1000, move)
        elif board.is_full():
            return (0, move)

        for row in range(board.size()):
            for col in range(board.size()):
                move = (row, col)
                if board.is_empty(move):
                    board.set_cell(move, turn)
                    score, m = self.minmax(move, board, not maximizing)
                    board.set_empty(move)
                    if maximizing and score >= best_score:
                        return (score, m)
                    if not maximizing and score <= best_score:
                        return (score, m)


    def select_random(self, board):
        row = randint(0, board.size() - 1)
        col = randint(0, board.size() - 1)

        return (row, col)

