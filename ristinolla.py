import sys

from util.board import Board
import ui.text_ui as tui
import ui.gui as gui
import util.config as config

def main():
    args = sys.argv[1:]
    ui = gui
    board_size = config.BOARD_SIZE
    winning_length = config.WINNING_LENGTH

    if args:
        for arg in args:
            if arg in ['-t', '--text']: ui = tui
            if arg in ['-hm', '--heat_map']: config.HEAT_MAP = True
            if arg == '-ai': config.AI_VS_AI = True
            if ':' in arg:
                try:
                    s, wl = map(int, arg.split(':'))
                    if s >= 3 and s <= 25: board_size = s
                    if wl >= 3 and wl <= 6: winning_length = wl
                except:
                    pass

            # seuraavaa ominaisuutta ei ole vielä toteutettu
            if arg == '--test_run':
                config.AI_VS_AI = True
                config.IS_TEST_RUN = True

    if winning_length > board_size: winning_length = board_size
    board = Board(board_size, winning_length)
    ui.start(board)

if __name__ == '__main__':
    main()
