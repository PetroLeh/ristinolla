class Board:
    
    def __init__(self, size: int, winning_length: int):
        row = [0 for i in range(size)]
        self.__grid = [row[:] for i in range(size)]
        self.__heat_map = [row[:] for i in range(size)]
        self.__heat_map2 = [row[:] for i in range(size)]
        self.__winning_length = winning_length

    def grid(self):
        return self.__grid
    
    def get_cell(self, cell: tuple):
        row, col = cell
        return self.__grid[row][col]

    def set_cell(self, cell: tuple, player):
        if not cell: return False
        row, col = cell
        if self.is_on_board(cell) and self.__grid[row][col] == 0:
            self.__grid[row][col] = player
            return True
        return False
   
    def is_empty(self, cell: tuple):
        if not self.is_on_board(cell): return False
        row, col = cell        
        return self.__grid[row][col] == 0
    
    def set_empty(self, cell: tuple):
        row, col = cell
        self.__grid[row][col] = 0
    
    def clear(self):
        row = [0 for i in range(self.size())]
        self.__grid = [row[:] for i in range(self.size())]

    def is_on_board(self, cell: tuple):
        row, col = cell
        return row >= 0 and row < self.size() and col >= 0 and col < self.size()

    def is_winning(self, move: tuple, player):
        if move == None: return False

        def get_starting_point(move, direction, player):
            row, col = move
            row_dir, col_dir = direction
            new_row, new_col = (row + row_dir, col + col_dir)
            if self.is_on_board((new_row, new_col)) and self.__grid[new_row][new_col] == player:
                return get_starting_point((new_row, new_col), direction, player)
            else:
                return (row, col)

        def invert(direction: tuple):
            return (direction[0] * -1, direction[1] * -1)

        def line_length(start: tuple, direction: tuple, player):
            row, col = start
            row_dir, col_dir = direction   
            new_row, new_col = (row + row_dir, col + col_dir)
            if self.is_on_board((new_row, new_col)) and (self.__grid[new_row][new_col] == player or (new_row, new_col) == move):
                return 1 + line_length((new_row, new_col), direction, player)
            else:
                return 1              

        directions = [(1, 0), (0, 1), (1, -1), (1, 1)]
        for direction in directions:
            start = get_starting_point(move, direction, player)
            inv_direction = invert(direction)
            if line_length(start, inv_direction, player) >= self.__winning_length:                
                return True
        return False

    def size(self):
        return len(self.__grid)

    def is_full(self):
        for row in self.__grid:
            if 0 in row:
                return False
        return True
    
    def heat_map(self):
        for row in range(self.size()):
            for col in range(self.size()):
                cell = (row, col)
                if self.is_empty(cell): self.__heat_map[row][col] = self.heat(cell)
                else: self.__heat_map[row][col] = 0
        return self.__heat_map
    
    def heat_map2(self, player=None):
        for row in range(self.size()):
            for col in range(self.size()):
                cell = (row, col)
                if self.is_empty(cell): self.__heat_map[row][col] = self.heat2(cell, player)
                else: self.__heat_map[row][col] = 0
        return self.__heat_map
    
    def heat(self, cell: tuple):
        h = 0
        surrounding_cells = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        row, col = cell
        for c in surrounding_cells:
            delta_row, delta_col = c
            new_row = row + delta_row
            new_col = col + delta_col
            if self.is_on_board((new_row, new_col)) and not self.is_empty((new_row, new_col)):
                h += 1
        return h

    def heat2(self, cell: tuple, player):
        def get_delta_cell(c, d):
            row, col = c
            delta_row, delta_col = d
            new_row = row + delta_row
            new_col = col + delta_col
            return (new_row, new_col)

        def start_of_line(c, d):
            d_cell = get_delta_cell(c, d)
            if self.is_on_board(d_cell):
                return self.get_cell(d_cell)

        def count_symbols(c, d, player):
            d_cell = get_delta_cell(c, d)
            if self.is_on_board(d_cell) and self.get_cell(d_cell) == player:
                return 2 + count_symbols(d_cell, d, player)
            return 0
    
        h = 0
        directions = [(1, 1), (1, -1), (0, 1), (1, 0),
                      (-1, -1), (-1, 1), (0, -1), (-1, 0)]
        for d in directions:
            if player:
                h = max(h, count_symbols(cell, d, player))
            else:
                player = start_of_line(cell, d)
                if player:
                    h = max(h, count_symbols(cell, d, player))
        return min(h, 8)

    def is_full_after(self, move):
        self.set_cell(move, 3)
        if self.is_full():
            self.set_empty(move)
            return True
        self.set_empty(move)
        return False
        