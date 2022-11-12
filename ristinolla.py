from board import Board
from util.ai import Minimax
import ui.text_ui as ui

board = Board(5, 3)

player_one = 1
player_two = -1

turn = player_one
ai = Minimax(player_two)

while True:
    ui.show(board)

    if turn == player_one:
        move = input('Pelaaja X, anna koordinaatit (rivi, sarake): ')
        row, col = map(int, move.strip('()').split(','))
        move = (row, col)
    else:
        move = ai.select_move(board)

    if board.set_cell(move, turn):
        if board.is_winning(move, turn):
            ui.show(board)
            ui.show_winner(turn)
            break
        turn *= -1
    else:
        print(f'{move} ei onnistu')

