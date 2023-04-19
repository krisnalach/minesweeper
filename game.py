import pygame
import numpy as np
import random


class Minesweeper:
    """
    Minesweeper class representing an entire game of minesweeper
    Board Representation:
    0 <= n <= 8 if a square is clicked and has n neighbors
    -1 if a square is neither clicked or flagged
    -2 if a square is flagged
    -3 if a square is a mine and unclicked or unflagged
    -4 if a square is a mine and flagged
    Args:
        n - the size of the board (n x n)
        mine_cnt - the number of mines
    """

    def __init__(self, n, mine_cnt):
        self.board = [[-1 for i in range(n)] for j in range(n)]
        self.n = n
        self.mines = mine_cnt
        self.first_clck = (0, 0)

    def place_mines(self, first_click):
        """
        Place mines, making sure to not place any near the first click
        Args:
            first_click - tuple of indeces representing where the first "click" occured
        Returns:
            Nothing
        """
        mines_to_place = []
        x, y = first_click
        illegal_spots = self.get_neighbors(
            x, y, 2, False
        )  # ensuring that you can't insta-lose
        # generating mines
        while len(mines_to_place) < self.mines:
            mine = (random.randrange(self.n), random.randrange(self.n))
            if mine not in set(illegal_spots + mines_to_place):
                mines_to_place.append(mine)
        # placing mines
        for m in mines_to_place:
            i, j = m
            self.board[i][j] = -3

    def reveal(self, x, y):
        """
        Reveal adjacent squares according to minesweeper rules
        Args:
            x - the x index of the square clicked
            y - the y index of the square clicked
        Returns:
            Nothing
        """
        # base case, we never auto-reveal non -1 squares
        if self.board[x][y] != -1:
            return

        # updating revealed square to show neighboring mines
        mines = self.get_neighbors(x, y, 1, True)
        self.board[x][y] = len(mines)

        # second base case, stop revealing when we've shown information
        if len(mines) != 0:
            return

        # only want to consider neighbors that aren't mines
        for neighbor in set(self.get_neighbors(x, y, 1, False)) - set(mines):
            i, j = neighbor
            # reveal rule: only reveal an adjacent tile if it's unrevealed
            if self.board[i][j] == -1:
                self.reveal(i, j)

    def get_neighbors(self, x, y, d, find_mine):
        """
        Given x and y indeces, return a list of tuples representing all the neighbors at depth d
        Args:
            x - the x index
            y - the y index
            d - the depth in which to find neighbors (d=1 finds 8, d=2 finds 2, etc)
            find_mine - True of False if we should only look for neighbors that are mines
        Returns:
            A list of tuples, with each tuple representing a neighbor
        """
        neighbors = []
        for i in range(max(0, x - d), min(x + d + 1, self.n)):
            for j in range(max(0, y - d), min(y + d + 1, self.n)):
                if not (i == x and j == y):  # not considering itself a neighbor
                    if not find_mine:
                        neighbors.append((i, j))
                    else:
                        if self.board[i][j] == -3:
                            neighbors.append((i, j))
        return neighbors

    def click(self, x, y):
        """
        'Click' on a square at position (x, y)
        Handles resulting logic
        Args:
            x - the x index of the square
            y - the y index of the square
        Returns:
            Nothing
        """
        if self.board[x][y] == -1:
            self.reveal(x, y)
        elif self.board[x][y] == -3:
            # TODO: Figure out how to handle game over logic
            self.game_over()

    def flag(self, x, y):
        """
        Flag a square at position (x, y)
        Args:
            x - the x index of the square
            y - the y index of the square
        Returns:
            Nothing
        """
        self.board[x][y] += -1

    def generate_actions(self):
        """
        Generate a list of possible actions to give to an agent
        Args:
            None
        Returns
            A list of tuples of the form:
            (action, (x, y), cost) where:
                action - the action to take on a tile (click, flag)
                x - the x index of the tile
                y - the y index of the title
                cost - the associated cost of performing the action
        """

    def draw_board(self, BOARD_WIDTH, BOARD_HEIGHT):
        """
        Function to draw out the board using Pygame
        Args:
            BOARD_WIDTH - width of the board in terms of square count
            BOARD_HEIGHT - height of the board in terms of square count
        Returns:
            None
        """
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                # this allows us to use the same indexing for the board
                if self.board[x][y] in range(0, 9):
                elif self.board[x][y] == -1:
                elif self.board[x][y] == -2:
                elif self.board[x][y] == -3:
                elif self.board[x][y] == -4:
    def print_board(self):
        """
        Function to print out the board
        Args:
            None
        Returns:
            Nothing
        """
        print(np.matrix(self.board))


class MineMaster:
    """
    Class representing a Minesweeper AI trained using Deep Q-Networks
    """

    def __init__(self, keys):
        q_table = {}
        for key in keys:
            q_table[key] = 0


def run_game():
    """
    Main game running loop
    Args:
        None
    Returns:
        Nothing
    """
    # initializing
    pygame.init()
    clock = pygame.time.Clock()
    WIN_WIDTH = 1024
    WIN_HEIGHT = 764
    PLAY_WIDTH = 600
    PLAY_HEIGHT = 600
    SQUARE_SIZE = 40
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("")

    # Define the board sizes in terms of counts of squares
    BOARD_WIDTH = int(WIN_WIDTH / SQUARE_SIZE)
    BOARD_HEIGHT = int(WIN_WIDTH / SQUARE_SIZE)


def main():
    run_game()


if __name__ == "__main__":
    main()
