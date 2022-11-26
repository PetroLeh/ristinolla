import pygame
from util.ai import Minimax
import util.config as config

width = 0
height = 0

player_one = 1
player_two = -1

player_one_color = config.player_one_color
player_two_color = config.player_two_color
cell_size = config.cell_size
wall = config.wall_thickness
hm = False

def start(board):
    ai = Minimax(player_two, config.max_depth_in_minimax)
        
    pygame.init()

    global width
    global height
    global hm

    hm = config.heat_map
    height = board.size() * (cell_size + wall) + 2 * wall
    width = int(height * 1.5) if hm else height

    scene = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Ristinolla - vuorossa X')

    show(board, scene)

    cell = None
    marked_cell = None
    move = None
    turn = player_one
    game_over = False

    while True:        
        
        if not game_over:
        
            if turn == player_two:
                move = ai.select_move(board)

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
                if board.set_cell(move, turn):
                    show(board, scene)
                    if board.is_winning(move, turn):
                        show_winner(turn, board, scene)
                        game_over = True
                    if board.is_full():
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
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    game_over = False
                    move = None
                    turn = player_one
                    board.clear()

                    show(board, scene)
            
def show(board, scene):
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
    x, y = pos     
    col = int(x / (cell_size + wall))
    row = int(y / (cell_size + wall))

    return (row, col)

def show_winner(player, board, scene):

    if player == player_one:
        winner_color = player_one_color
        w = 'X'
    else:
        winner_color = player_two_color
        w = 'O'

    middle = int(height / 2)
    big_font = pygame.font.SysFont('Arial', 48)
    small_font = pygame.font.SysFont('Arial', 22)
    winner = big_font.render(f'Voittaja on {w}', True, winner_color, (200,200,200))
    new_game = small_font.render('aloita uusi peli painamalla jotain näppäintä', True, winner_color, (200,200,200))

    box_size = 440
    #pygame.draw.rect(scene, (100,100,100), (middle - int(box_size / 2), middle - int(box_size / 2), box_size, box_size))
    #pygame.draw.rect(scene, (200,200,200), (middle - int(box_size / 2) + wall, middle - int(box_size / 2) + wall, box_size - 2 * wall, box_size - 2 * wall))
    scene.blit(winner, (middle - 120, middle - 120))

    scene.blit(new_game, (middle - 200, middle + 120))
    
    cs = cell_size * 2
    # if player == player_one:
    #     x = y = int(middle - cs / 2)

    #     pygame.display.set_caption('Ristinolla - X voitti')
    #     pygame.draw.line(scene, player_one_color, (x, y), (x + cs, y + cs), 4 * wall )
    #     pygame.draw.line(scene, player_one_color, (x + cs, y), (x, y + cs), 4 * wall )

    # else:
    #     pygame.display.set_caption('Ristinolla - O voitti')
    #     pygame.draw.circle(scene, player_two_color, (middle, middle), int(cs))
    #     pygame.draw.circle(scene, (200,200,200), (middle, middle), int(cs - 5 * wall))
    
    pygame.display.flip()

def mark_cell(cell, color, scene):
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
    heat_map = board.heat_map2(player_one)

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
    heat_map = board.heat_map2(player_two)

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