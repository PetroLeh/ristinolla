import pygame
from util.ai import Minimax

cell_size = 30
wall = 2
width = 0
height = 0

player_one = 1
player_two = -1

player_one_color = (100,100,200)
player_two_color = (200,100,100)

ai = Minimax(player_two)

def start(board):
        
    pygame.init()

    global width
    global height

    width = board.size() * (cell_size + wall) + 2 * wall
    height = width

    scene = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Ristinolla')

    show(board, scene)

    cell = None
    move = None
    turn = player_one
    game_over = False

    while True:        

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and turn == player_one:
                move = get_cell_from_coordinates(event.pos, board)
            if game_over and event.type == pygame.KEYDOWN:
                turn = player_one
                board.clear()
                game_over = False
                move = None
                show(board, scene)

            if event.type == pygame.QUIT:
                exit()

        if turn == player_two:
            move = ai.select_move(board)
        
        if move and not game_over:
            if board.set_cell(move, turn):
                show(board, scene)
                if board.is_winning(move, turn):
                    show_winner(turn, board, scene)
                    game_over = True
                turn *= -1
                move = None
            
def show(board, scene):
    grid = board.grid()
    scene.fill((100, 100, 100))
    
    y = wall
    for row in grid:
        x = wall
        for cell in row:            
            pygame.draw.rect(scene, (200,200,200), (x, y, cell_size, cell_size))
            if cell == player_one:
                pygame.draw.line(scene, player_one_color, (x + wall, y + wall), (x + cell_size - 2 * wall, y + cell_size - 2 * wall), 2 * wall )
                pygame.draw.line(scene, player_one_color, (x + cell_size - 2 * wall, y + wall), (x + wall, y + cell_size - 2 * wall), 2 * wall )

            if cell == player_two:
                middle_x = int(x + cell_size / wall)
                middle_y = int(y + cell_size / wall)
                pygame.draw.circle(scene, player_two_color, (middle_x, middle_y), int(cell_size / 2 - wall))
                pygame.draw.circle(scene, (200,200,200), (middle_x, middle_y), int(cell_size / 2 - 3 * wall))

            x += cell_size + wall
        y += cell_size + wall
    
    pygame.display.flip()

def get_cell_from_coordinates(pos: tuple, board):
    x, y = pos
    if x > board.size() * (cell_size + wall): return None
    
    col = int(x / (cell_size + wall))
    row = int(y / (cell_size + wall))

    return (row, col)

def show_winner(player, board, scene):

    if player == player_one:
        winner_color = player_one_color
    else:
        winner_color = player_two_color

    middle = int(width / 2)
    big_font = pygame.font.SysFont('Arial', 48)
    small_font = pygame.font.SysFont('Arial', 22)
    winner = big_font.render('Voittaja on', True, winner_color)
    new_game = small_font.render('aloita uusi peli painamalla jotain näppäintä', False, winner_color)

    box_size = 440
    pygame.draw.rect(scene, (100,100,100), (middle - int(box_size / 2), middle - int(box_size / 2), box_size, box_size))
    pygame.draw.rect(scene, (200,200,200), (middle - int(box_size / 2) + wall, middle - int(box_size / 2) + wall, box_size - 2 * wall, box_size - 2 * wall))
    scene.blit(winner, (middle - 120, middle - 120))

    scene.blit(new_game, (middle - 200, middle + 120))
    
    cs = cell_size * 2
    if player == player_one:
        x = y = int(middle - cs / 2)

        pygame.draw.line(scene, player_one_color, (x, y), (x + cs, y + cs), 4 * wall )
        pygame.draw.line(scene, player_one_color, (x + cs, y), (x, y + cs), 4 * wall )

    else:
        pygame.draw.circle(scene, player_two_color, (middle, middle), int(cs))
        pygame.draw.circle(scene, (200,200,200), (middle, middle), int(cs - 5 * wall))
    
    pygame.display.flip()
