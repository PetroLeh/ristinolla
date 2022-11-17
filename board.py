class Board:
    
    def __init__(self, size: int, winning_length: int):
        row = [0 for i in range(size)]
        self.__grid = [row[:] for i in range(size)]

        self.__winning_length = winning_length

    def grid(self):
        return self.__grid
    
    def get_cell(self, cell: tuple):
        row, col = cell
        return self.__grid[row][col]

    def set_cell(self, cell: tuple, player):
        print(f'* {cell}')
        if not cell: return False
        row, col = cell
        if self.is_on_board(cell) and self.__grid[row][col] == 0:
            self.__grid[row][col] = player
            return True
        return False
   
    def is_empty(self, cell: tuple):
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
            if self.is_on_board((new_row, new_col)) and self.__grid[new_row][new_col] == player:
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