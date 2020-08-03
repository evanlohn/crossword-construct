import tkinter as tk
import argparse
from board import Board
from game import Game

def main():
    parser = argparse.ArgumentParser(description='Process chess configuration')
    parser.add_argument('size', type=int, default=5, help='the size of your square crossword puzzle')
    args = parser.parse_args()

    board = Board(args.size)

    g = Game(board)
    g.display_board()




if __name__ == '__main__':
    main()
