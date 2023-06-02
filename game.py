import pygame
import numpy as np
import random
import sys
import time
from sprites import load_images


class Minesweeper:
    """
    Minesweeper class representing an entire game of minesweeper
    Board Representation:
    0 <= n <= 8 if a square is clicked and has n neighbors
    -1 if a square is neither clicked or flagged
    -2 if a square is flagged
    -3 if a square is a mine and unclicked or unflagged
    -4 if a square is a mine and flagged
    -5 if a square is a mine and clicked
    Args:
        n - the size of the board (n x n)
        mine_cnt - the number of mines
    """

    def __init__(self, n, mine_cnt):
        self.board = [[-1 for i in range(n)] for j in range(n)]
        self.n = n
        self.mines = mine_cnt
        self.flag_cnt = 0
        self.first_click = True

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
        illegal_spots.append((x, y))  # get_neighbors doesn't consider itself
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
                        if self.board[i][j] in {-3, -4, -5}:
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
        elif self.board[x][y] == -3:  # game over
            self.lose()

    def flag(self, x, y):
        """
        Flag a square at position (x, y)
        Args:
            x - the x index of the square
            y - the y index of the square
        Returns:
            Nothing
        """
        sq = self.board[x][y]
        if sq == -1:
            self.board[x][y] = -2
            self.flag_cnt += 1
        elif sq == -3:
            self.board[x][y] = -4
            self.flag_cnt += 1

    def unflag(self, x, y):
        """
        Unflag a square at position (x, y)
        Args:
            x - the x index of the square
            y - the y index of the square
        Returns:
            Nothing
        """
        sq = self.board[x][y]
        if sq == -2:
            self.board[x][y] = -1
            self.flag_cnt -= 1
        if sq == -4:
            self.board[x][y] = -3
            self.flag_cnt -= 1

    def game_end(self):
        """
        Iterate over the board to see if the game has ended
        Args:
            None
        Returns:
            Strings corresponding to a victory or a loss
        """
        remaining = []
        for x in range(self.n):
            for y in range(self.n):
                if self.board[x][y] == -5:  # lose condition
                    return self.lose()
                if self.board[x][y] in {-1, -2}:
                    remaining.append(self.board[x][y])
        if len(remaining) == 0:  # win condition
            return self.win()
        # game isn't over, return accordingly
        return "continue"

    def win(self):
        """
        End the game on a win and prompt the
        restart screen
        Args:
            None
        Returns:
            The string: "You won!"
        """
        return "You won!"

    def lose(self):
        """
        End the game on a loss by revealing all mines
        and prompting the restart screen
        Args:
            None
        Returns:
            The string: "You lost!"
        """
        for x in range(self.n):
            for y in range(self.n):
                if self.board[x][y] == -3:
                    self.board[x][y] = -5
        return "You lost!"

    def restart_game(self):
        """
        Restart the game by resetting all variables to
        their initial state
        Args:
            None
        Returns:
            Nothing
        """
        self.board = [[-1 for i in range(self.n)] for j in range(self.n)]
        self.first_click = True
        self.flag_cnt = 0

    def generate_actions(self):
        """
        Generate a list of possible actions to give to an agent
        Args:
            None
        Returns
            A list of tuples of the form (x, y),
            where x is the x coordinate of the square and y is the
            y coordinate of the square
        """
        actions = []
        for i in range(self.n):
            for j in range(self.n):
                actions.append((i, j))
        return actions

    def play(self, action):
        """
        Main function the AI uses to update the game environment
        given an action (a.k.a. play the game)
        Args:
            action - the action the agent took (the x, y square it picked)
        Returns:
            a tuple containing the reward it recieved for its action
            and whether or not the game is over and the score
        """
        x, y = action
        reward = 0
        game_over = False
        score = 0

        if self.board[x][y] == -1:  # safe square
            self.reveal(x, y)
            reward += 10
        elif self.board[x][y] == -3:  # game over
            self.lose()
            game_over = True
            reward -= 10
        elif self.board[x][y] in {0, 1, 2, 3, 4, 5, 6, 7, 8}:
            reward -= 1  # punish "nothing" moves

        # calculate score (number of cleared squares)
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] in {0, 1, 2, 3, 4, 5, 6, 7, 8}:
                    score += 1

        return reward, game_over, score

    def draw_board(self, board_width, board_height, images, window):
        """
        Function to draw out the board using Pygame
        Args:
            board_width - width of the board in terms of square count
            board_height - height of the board in terms of square count
            images - dictionary of images to use for the game squares
            window - the surface to draw on
        Returns:
            None
        """
        for x in range(board_width):
            for y in range(board_height):
                # this allows us to use the same indexing for the board
                sq = self.board[x][y]
                if sq in range(0, 9):
                    window.blit(images["nums"][sq], (x * 40, y * 40))
                elif sq == -1 or sq == -3:
                    window.blit(images["block"], (x * 40, y * 40))
                elif sq == -2 or sq == -4:
                    window.blit(images["flagged"], (x * 40, y * 40))
                elif sq == -5:
                    window.blit(images["mine"], (x * 40, y * 40))

    def print_board(self):
        """
        Function to print out the board
        Args:
            None
        Returns:
            Nothing
        """
        print(np.matrix(self.board))
