from util.ai import Minimax

c = {0: ".",
     1: "X",
    -1: "O"
    }

def start(board):

    player_one = 1
    player_two = -1

    turn = player_one
    ai = Minimax(player_two)

    while True:
        show(board)

        if turn == player_one:
            move = input('Pelaaja X, anna koordinaatit (rivi, sarake): ')
            try:
                row, col = map(int, move.strip('()').split(','))
                move = (row, col)
            except:
                move = None
        else:
            move = ai.select_move(board)

        if board.set_cell(move, turn):
            if board.is_winning(move, turn):
                show(board)
                show_winner(turn)
                break
            turn *= -1
        else:
            print(f'{move} ei onnistu') if move else print('ei onnistu')

def show(board):
    print()
    grid = board.grid()
    for row in grid:
        for col in row:
            print(c[col], end="")
        print()

def show_winner(player):
    print(f'Pelaaja {c[player]} voitti')