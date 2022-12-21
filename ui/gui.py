import pygame
from util.ai import Minimax as Minimax
import util.config as config

width = 0
height = 0

player_one = 1
player_two = -1

player_one_color = config.player_one_color
player_two_color = config.player_two_color
cell_size = config.CELL_SIZE
wall = config.WALL_THICKNESS
hm = False

def start(board):
    """ Käynnistää graafisen käyttöliittymän """

    pygame.init()

    global width
    global height
    global hm

    hm = config.HEAT_MAP

    height = board.size() * (cell_size + wall) + 2 * wall
    width = int(height * 1.5) if hm else height

    scene = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Ristinolla - vuorossa X')

    show(board, scene)
    game_loop(board, scene)


def game_loop(board, scene):
    """ pelisilmukka """

    cell = None
    marked_cell = None
    move = None
    turn = player_two
    game_over = False
    ai_vs_ai = config.AI_VS_AI

    ai_O = Minimax(player_two)
    if ai_vs_ai: ai_X = Minimax(player_one)

    blop = pygame.mixer.Sound('util/sounds/blop.wav')

    while True:        
        if not game_over:
        
            if turn == player_two:
                move = ai_O.select_move(board)
            elif ai_vs_ai:
                move = ai_X.select_move(board)

            for event in pygame.event.get():                

                if event.type == pygame.QUIT:
                    exit()                    

                if turn == player_one:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        marked_cell = get_cell_from_coordinates(event.pos, board)
                        if board.is_empty(marked_cell): mark_cell(marked_cell, player_one_color, scene)
                        else: marked_cell = None

                    if event.type == pygame.MOUSEBUTTONUP and marked_cell:
                        current_cell = get_cell_from_coordinates(event.pos, board)
                        move = marked_cell if marked_cell == current_cell else remove_mark(marked_cell, scene)

            if move:
                pygame.mixer.Sound.play(blop)
                if board.set_cell(move, turn):
                    show(board, scene)
                    if board.is_winning(move, turn):
                        show_winner(turn, move, board, scene)
                        game_over = True
                    elif board.is_full():
                        pygame.display.set_caption('Ristinolla - tasapeli')
                        game_over = True
                        turn = player_one                        
                    else:
                        turn *= -1
                        if turn == player_one: pygame.display.set_caption('Ristinolla - vuorossa X')
                        else: pygame.display.set_caption('Ristinolla - vuorossa O')
                    move = None

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                    game_over = False
                    move = None
                    turn = player_one
                    board.clear()
                    pygame.display.set_caption('Ristinolla - vuorossa X')

                    show(board, scene)

def show(board, scene):
    """ Piirtää peliruudukon """

    grid = board.grid()
    scene.fill((100, 100, 100))    

    y = wall
    for row in grid:
        x = wall
        for cell in row:            
            pygame.draw.rect(scene, (200,200,200), (x, y, cell_size, cell_size))
            if cell == player_one:
                draw_player_one(x, y, scene)
            if cell == player_two:
                draw_player_two(x, y, scene)
            x += cell_size + wall
        y += cell_size + wall
        
    if hm: show_heat_maps(board, scene)
    pygame.display.flip()

def get_cell_from_coordinates(pos: tuple, board):
    """ Laskee hiiren osoittimen koordinaateista
    mikä peliruudukon ruutu sillä kohtaa on ja palauttaa sen """

    x, y = pos     
    col = int(x / (cell_size + wall))
    row = int(y / (cell_size + wall))

    return (row, col)

def show_winner(player, move, board, scene):
    if player == player_one:
        winner_color = player_one_color
        w = 'X'
    else:
        winner_color = player_two_color
        w = 'O'
    
    pygame.display.set_caption(f'Voittaja on {w}')

    middle = int(height / 2)

    font = pygame.font.SysFont('Arial', 22)
    winner = font.render(f'Voittaja on {w}', True, winner_color, (200,200,200))
    new_game = font.render('aloita uusi peli painamalla jotain näppäintä', True, winner_color, (200,200,200))

    line_start_y, line_start_x = board.winning_line['start']
    line_direction_y, line_direction_x = board.winning_line['direction']
    line_length = board.winning_length()

    line_start_x *= (cell_size + wall)
    line_start_x += (wall + cell_size // 2)
    line_start_y *= (cell_size + wall)
    line_start_y += (wall + cell_size // 2)

    line_end_x = line_start_x + (line_direction_x * (cell_size + wall) * (line_length - 1))
    line_end_y = line_start_y + (line_direction_y * (cell_size + wall) * (line_length - 1))

    pygame.draw.line(scene, winner_color, (line_start_x, line_start_y), (line_end_x, line_end_y), wall*3)

    scene.blit(winner, (middle - 80, 20))
    scene.blit(new_game, (middle - 200, 60))
    pygame.display.flip()

def mark_cell(cell, color, scene):
    """ Merkitsee klikatun ruudun valituksi """

    y, x = cell
    x *= (cell_size + wall)
    y *= (cell_size + wall)
    x += (wall * 2)
    y += (wall * 2)
    pygame.draw.rect(scene, color, (x, y, cell_size - wall * 2, cell_size - wall * 2))
    pygame.display.flip()
    
def remove_mark(cell, scene):
    mark_cell(cell, (200, 200, 200), scene)

def show_heat_maps(board, scene):
    show_heat_map_1(board, scene)
    show_heat_map_2(board, scene)

def show_heat_map_1(board, scene):
    """ Piirtää pelaajan X heatmapin """

    heat_map = board.heat_map(player_one)

    scale = 2
    y = wall
    for row in heat_map:
        x = 2 * wall + board.size() * (cell_size + wall)
        for cell in row:
            r = min(255, 95 + 20 * cell)
            pygame.draw.rect(scene, (r, 95, 110), (x, y, cell_size / scale, cell_size / scale))

            x += ((cell_size + wall) / scale)
        y += ((cell_size + wall) / scale)

def show_heat_map_2(board, scene):
    """ Piirtää pelaajan O heatmapin """

    heat_map = board.heat_map(player_two)

    scale = 2
    y = int((2 * wall + board.size() * (cell_size + wall)) / 2)
    for row in heat_map:
        x = 2 * wall + board.size() * (cell_size + wall)
        for cell in row:
            r = min(255, 95 + 20 * cell)
            pygame.draw.rect(scene, (r, 110, 95), (x, y, cell_size / scale, cell_size / scale))

            x += ((cell_size + wall) / scale)
        y += ((cell_size + wall) / scale)

def draw_player_one(x: int , y: int, scene):
    pygame.draw.line(scene, player_one_color, (x + wall, y + wall), (x + cell_size - 2 * wall, y + cell_size - 2 * wall), 2 * wall )
    pygame.draw.line(scene, player_one_color, (x + cell_size - 2 * wall, y + wall), (x + wall, y + cell_size - 2 * wall), 2 * wall )

def draw_player_two(x:int, y:int, scene):
    middle_x = int(x + cell_size / 2)
    middle_y = int(y + cell_size / 2)
    pygame.draw.circle(scene, player_two_color, (middle_x, middle_y), int(cell_size / 2 - wall))
    pygame.draw.circle(scene, (200,200,200), (middle_x, middle_y), int(cell_size / 2 - 3 * wall))