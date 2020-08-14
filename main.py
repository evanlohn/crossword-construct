import tkinter as tk
import argparse
from board import Board
from game import Game
import pickle

def load_board(pth):
    with open(pth, 'rb') as f:
        board = pickle.load(f)
    return board

def main():
    parser = argparse.ArgumentParser(description='Process chess configuration')
    parser.add_argument('size', type=int, default=5, help='the size of your square crossword puzzle')
    parser.add_argument('--load', type=str, default='', help='arg to specify if you want to load a puzzle')
    args = parser.parse_args()

    if args.load:
        board = load_board(args.load)
    else:
        board = Board(args.size)

    g = Game(board)
    g.display_board()


if __name__ == '__main__':
    main()
