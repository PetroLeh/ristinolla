c = {0: ".",
     1: "X",
    -1: "O"
    }

def show(board):
    print()
    for row in board.grid():
        for col in row:
            print(c[col], end="")
        print()

def show_winner(player):
    print(f'Pelaaja {c[player]} voitti')