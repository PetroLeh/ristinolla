from board import Board
import ui.text_ui as tui
import ui.gui as gui

def main():
    ui = gui
    board = Board(25, 5)
    ui.start(board)
    
if __name__ == '__main__':
    main()