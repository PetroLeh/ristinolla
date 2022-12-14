import sys

from util.board import Board
import ui.text_ui as tui
import ui.gui as gui
import util.config as config

def main():
    args = sys.argv[1:]
    ui = gui
    board_size = config.board_size
    winning_length = config.winning_length

    if args:
        for arg in args:
            if arg in ['-t', '--text']: ui = tui
            if arg in ['-hm', '--heat_map']: config.heat_map = True
            if arg == '-ai': config.ai_vs_ai = True
            if ':' in arg:
                try:
                    s, wl = map(int, arg.split(':'))
                    if s >= 3 and s <= 25: board_size = s
                    if wl >= 3 and wl <= 6: winning_length = wl
                except:
                    pass

            # seuraavaa ominaisuutta ei ole vielä toteutettu
            if arg == '--test_run':
                config.ai_vs_ai = True
                config.is_test_run = True

    if winning_length > board_size: winning_length = board_size
    board = Board(board_size, winning_length)
    ui.start(board)

if __name__ == '__main__':
    main()
