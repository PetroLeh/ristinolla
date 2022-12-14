
import util.config as config
from util.ai import Minimax

c = config.CHARACTERS

def start(board):

    ai_vs_ai = config.AI_VS_AI

    player_one = 1
    player_two = -1

    turn = player_one
    ai_O = Minimax(player_two)
    if ai_vs_ai: 
        ai_X = Minimax(player_one)
        ai_X.set_logger_to(False)
        ai_O.set_logger_to(False)

    while True:
        
        show(board)

        if turn == player_one:
            if ai_vs_ai:
                print(f'Pelaaja {c[turn]} miettii...')
                move = ai_X.select_move(board)
            else:
                move = input(f'Pelaaja {c[turn]}, anna koordinaatit (rivi, sarake): ')
                try:
                    row, col = map(int, move.strip('()').split(','))
                    move = (row, col)
                except:
                    move = None
        else:
            print(f'Pelaaja {c[turn]} miettii...')
            move = ai_O.select_move(board)

        if board.set_cell(move, turn):
            if board.is_winning(move, turn):
                show(board)
                show_winner(turn)
                break
            if board.is_full():
                show(board)
                print('Tasapeli!')
                break
            turn *= -1
        else:
            print(f'{move} ei onnistu') if move else print('ei onnistu')

def show(board):
    print()
    grid = board.grid()
    for row in grid:
        s = ' '.join(map(lambda n: c[n], row))
        print(s)
    print()

def show_winner(player):
    print(f'Pelaaja {c[player]} voitti')