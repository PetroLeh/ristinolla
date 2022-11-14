from board import Board
from util.ai import Minimax
import ui.text_ui as tui
import ui.gui as gui

def main():
    ui = gui
    board = Board(25, 5)
    ui.start(board)
    
main()