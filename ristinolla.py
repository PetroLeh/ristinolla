from board import Board
from util.ai import Minimax
import ui.text_ui as tui
import ui.gui as gui

def main():
    ui = tui
    board = Board(20, 5)
    ui.start(board)
    
main()