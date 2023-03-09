# how to run
# python3 main.py 30 30 0.1

import sys
from game import Game

def main():
    size = (15, 15)
    prob = 0.1
    # Call Game to launge minesweeper
    g = Game(size, prob)
    g.run()

if __name__ == '__main__':
    main()