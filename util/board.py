class Board:

    def __init__(self, size: int, winning_length: int):
        row = [0 for i in range(size)]
        self.__grid = [row[:] for i in range(size)]
        self.__winning_length = winning_length
        self.__move_table = self.init_move_table(size)
        self.__moves_made = []
        self.winning_line = {}


    def init_move_table(self, size):
        """ luo taulukon, josta jokaiselle siirrolle saa
        haettua lukuarvon """

        table = []
        for row in range(size):
            table_row = []
            for col in range(size * 2):
                table_row.append(row * 2 * size + col)
            table.append(table_row)
        return table

    def get_key(self, moves=None):
        if not moves:
            moves = self.__moves_made
        return ''.join(map(str, moves))

    def get_move_key(self, move, player):
        """ palauttaa siirron lukuarvon taulukosta """

        row, col = move

        # jos pelaaja on -1 offset on 0 eli haetaan arvo taulukon vasemmalta
         # puolelta, jos pelaaja on 1 haetaan arvo taulukon oikealta puolelta
        offset = (player + 1) // 2

        return self.__move_table[row][col + (offset * len(self.__grid))]

    def grid(self):
        """ Palauttaa pelitilanteen taulukkona """

        return self.__grid

    def middle(self):
        """ Palauttaa keskimmäisen ruudun merkin """

        return self.__grid[self.size() // 2][self.size() // 2]

    def get_cell(self, cell: tuple):
        """ Palauttaa argumenttina saadun ruudun merkin """

        row, col = cell
        if self.is_on_board(cell):
            return self.__grid[row][col]
        return 0

    def set_cell(self, cell: tuple, player):
        """ Merkitsee ruutuun pelaajan merkin

        palauttaa True jos merkintä on sallittu, muuten palautta False """

        if not cell:
            return False
        row, col = cell
        if self.is_on_board(cell) and self.__grid[row][col] == 0:
            self.__grid[row][col] = player
            self.__moves_made.append(self.get_move_key(cell, player))
            self.__moves_made.sort()
            return True
        return False

    def is_empty(self, cell: tuple):
        """ Tarkistaa onko argumenttina saatu ruutu tyhjä """

        if not self.is_on_board(cell):
            return False
        row, col = cell
        return self.__grid[row][col] == 0

    def set_empty(self, cell: tuple):
        """ Merkitsee argumenttina saadun ruudun tyhjäksi """

        row, col = cell
        if self.is_on_board(cell):
            if self.is_empty(cell):
                return
            self.__moves_made.remove(self.get_move_key(cell, self.__grid[row][col]))
            self.__grid[row][col] = 0

    def clear(self):
        """ Tyhjentää pelilaudan """

        row = [0 for i in range(self.size())]
        self.__grid = [row[:] for i in range(self.size())]

    def is_on_board(self, cell: tuple):
        """ Tarkistaa onko argumenttina saatu ruutu pelialueella """

        row, col = cell
        return row >= 0 and row < self.size() and col >= 0 and col < self.size()

    def is_winning(self, move: tuple, player):
        """ Tarkistaa muodostaako argumenttina saatu siirto voittavan suoran pelialueelle """

        if not move:
            return False

    # apumetodeja voittosuoran tarkistamiseen

        # haetaan suoran alkupiste tietyssä suunnassa
        def get_starting_point(move, direction, player):
            row, col = move
            row_dir, col_dir = direction
            new_row, new_col = (row + row_dir, col + col_dir)
            if self.is_on_board((new_row, new_col)) and self.__grid[new_row][new_col] == player:
                return get_starting_point((new_row, new_col), direction, player)
            return (row, col)

        # käännetään suunta
        def invert(direction: tuple):
            return (direction[0] * -1, direction[1] * -1)

        # lasketaan suoran pituus tiettyyn suuntaan
        def line_length(start: tuple, direction: tuple, player):
            row, col = start
            row_dir, col_dir = direction
            new_row, new_col = (row + row_dir, col + col_dir)
            if self.is_on_board((new_row, new_col)) and (self.__grid[new_row][new_col] == player or (new_row, new_col) == move):
                return 1 + line_length((new_row, new_col), direction, player)
            return 1

    # käydään läpi annetun siirron koordinaateista joka suuntaan kulkevien samaa merkkiä sisältävien
    # suorien pituudet ja tarkistetaan onko pituus vähintään voittoon tarvittava
        directions = [(1, 0), (0, 1), (1, -1), (1, 1)]
        for direction in directions:
            start = get_starting_point(move, direction, player)
            inv_direction = invert(direction)
            if line_length(start, inv_direction, player) >= self.__winning_length:
                self.winning_line['start'] = start
                self.winning_line['direction'] = inv_direction
                return True
        return False

    def size(self):
        return len(self.__grid)

    def is_full(self):
        for row in self.__grid:
            if 0 in row:
                return False
        return True

    def heat_map(self, player=None):
        """ Palauttaa taulukon, jonka solujen arvoina on pelilaudalla kyseisessä
        koordinaatissa olevan ruudun 'kuumuus'. Jos argumenttina ei ole annettu
        pelaajaa, kuumuus määräytyy sen mukaan, kuinka moneen naapuriruutuun on
        pelattu kumman tahansa pelaajan merkki. Jos argumenttina on annettu
        pelaaja, kuumuus määräytyy sen mukaan mikä on pisin kyseisen ruudun
        vierestä lähtevä pelaajan merkkejä sisältävä suora """

        row = [0 for i in range(self.size())]
        heat_map = [row[:] for i in range(self.size())]
        if player:
            for row in range(self.size()):
                for col in range(self.size()):
                    cell = (row, col)
                    if self.is_empty(cell):
                        heat_map[row][col] = self.heat2(cell, player)
                    else:
                        heat_map[row][col] = 0
            return heat_map

        for row in range(self.size()):
            for col in range(self.size()):
                cell = (row, col)
                if self.is_empty(cell):
                    heat_map[row][col] = self.heat(cell)
                else:
                    heat_map[row][col] = 0
        return heat_map

    def heat(self, cell: tuple):
        """ Palauttaa argumenttina saadun ruudun vieressä (kaikkiin suuntiin)
        olevien merkkien määrän """

        heat = 0
        surrounding_cells = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        row, col = cell
        for d_cell in surrounding_cells:
            delta_row, delta_col = d_cell
            new_row = row + delta_row
            new_col = col + delta_col
            if self.is_on_board((new_row, new_col)) and not self.is_empty((new_row, new_col)):
                heat += 1
        return heat

    def heat2(self, cell: tuple, player):
        """ Palauttaa argumenttina saadun ruudun vierestä lähtevien tietyn
        pelaajan merkkejä sisältävien suorien suurimman pituuden """

    # apumetodeja suoran pituuden laskemiseen

        # palautetaan seuraavan ruudun koordinaatit
        def get_delta_cell(cell, direction):
            row, col = cell
            delta_row, delta_col = direction
            new_row = row + delta_row
            new_col = col + delta_col
            return (new_row, new_col)

        # lasketaan suorassa olevat merkit
        def count_symbols(cell, direction, player, symbols_counted):
            d_cell = get_delta_cell(cell, direction)

            # jos seuraavassa ruudussa on pelaajan merkki, lisätään 1 ja jatketaan
            # laskemista eteenpäin
            if self.is_on_board(d_cell) and self.get_cell(d_cell) == player:
                return 1 + count_symbols(d_cell, direction, player, symbols_counted + 1)

            # jos seuraavassa ruudussa ei ole pelaajan merkkiä, mutta ei myöskään vastustajan,
            # lisätään vielä puoli ekstrapistettä mahdollisuudesta pelata tähän ruutuun
            if self.is_on_board(d_cell) and self.get_cell(d_cell) == 0 and symbols_counted:
                return .5
            return 0

    # lasketaan eri suuntiin lähtevien suorien pituudet
        length = 0
        directions = [(1, 1), (1, -1), (0, 1), (1, 0),
                      (-1, -1), (-1, 1), (0, -1), (-1, 0)]
        for direction in directions:
            invert_direction = (direction[0] * -1, direction[1] * -1)
            delta_cell = get_delta_cell(cell, direction)
            invert_d_cell = get_delta_cell(cell, invert_direction)

            # tarkastetaan onko ruutu kahden samansuuntaisen suoran välissä
            if self.is_on_board(delta_cell) and self.get_cell(delta_cell) == player and self.is_on_board(invert_d_cell) and self.get_cell(invert_d_cell) == player:
                # jos on, lasketaan molempien suorien pituus mukaan
                length = max(length, count_symbols(cell, direction, player, 0) + count_symbols(cell, invert_direction, player, 0))
            else:
                # jos ei, lasketaan yhteen suuntaan lähtevän suoran pituus
                length = max(length, count_symbols(cell, direction, player, 0))
        return length

    def winning_length(self):
        return self.__winning_length

    def is_on_border(self, cell):
        """ Tarkastaa onko annettu ruutu pelialueen reunalla """

        row, col = cell
        return row == 0 or col == 0 or row == self.size() - 1 or col == self.size() - 1
