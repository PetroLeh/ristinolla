import pygame

cell_size = 30

def start(board):
        
    pygame.init()

    height = board.size() * (cell_size + 2) + 4
    width = height + 200

    scene = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Ristinolla')

    scene.fill((100, 100, 100))
    pygame.display.flip()

    show(board, scene)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
def show(board, scene):
    grid = board.grid()
    
    y = 2
    for row in grid:
        x = 2
        for cell in row:            
            pygame.draw.rect(scene, (200,200,200), (x, y, cell_size, cell_size))
            x += cell_size + 2
        y += cell_size + 2
    
    pygame.display.flip()