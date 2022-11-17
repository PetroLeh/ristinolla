from random import randint

class Minimax:

    def __init__(self, player):
        self.__player = player
        self.__opponent = -player

    def select_move(self, board):
        #move = self.select_random(board)
        #best, move = self.minmax(None, board, True)
        #best, move = self.minmax_v2(3, board, None, self.__player)
        move = self.minmax_v3(board, None, self.__player)
        return move

    def minmax_v3(self, board, move, turn):
        h_map = board.heat_map()
        hots = self.hot_cells(h_map)
        if hots:
            hottest = hots[0]
            for row in range(len(h_map)):
                for col in range(len(h_map)):
                    hottest_row, hottest_col = hottest
                    if h_map[row][col] > h_map[hottest_row][hottest_col]: hottest = (row, col)
            return hottest
        else:
            return self.select_random(board)


    def minmax_v2(self, depth, board, move, turn):
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
    
        for cell in self.hot_cells(board.heat_map()):

            board.set_cell(cell, turn)
            score, m = self.minmax_v2(depth - 1, board, cell, turn * -1)
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
    
    def hot_cells(self, heat_map):
        res = []
        for row in range(len(heat_map)):
            for col in range(len(heat_map)):
                if heat_map[row][col] > 0: res.append((row, col))
        return res

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

