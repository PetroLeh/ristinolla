from random import randint

class Minimax:

    def __init__(self, player):
        self.__player = player
        self.__opponent = -player

    def select_move(self, board):
        return self.select_random(board)

        move, score = self.minmax(None, board, True)
        return move

    def minmax(self, move, board, maximizing):
        
        if maximizing:
            best_score = -1000
            turn = self.__player
        else:
            best_score = 1000
            turn = self.__opponent
        
        if maximizing and board.is_winning(move, self.__player):
            return (move, 1000)
        elif not maximizing and board.is_winning(move, self.__opponent):
            return (move, -1000)
        elif board.is_full():
            return (move, 0)

        for row in range(board.size()):
            for col in range(board.size()):
                if board.is_empty(row, col):
                    move = (row, col)
                    board.set_cell((row, col), turn)
                    move, score = self.minmax(move, board, not maximizing)
                    board.set_empty(row, col)
                    if maximizing and score >= best_score:
                        return (move, score)
                    if not maximizing and score <= best_score:
                        return (move, score)


    def select_random(self, board):
        row = randint(0, board.size() - 1)
        col = randint(0, board.size() - 1)

        return (row, col)

