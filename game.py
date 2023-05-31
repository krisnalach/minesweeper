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
        elif self.board[x][y] == -3:
            # TODO: Figure out how to handle game over logic
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
            A list of tuples of the form:
            (action, (x, y), cost) where:
                action - the action to take on a tile (click, flag)
                x - the x index of the tile
                y - the y index of the title
                cost - the associated cost of performing the action
        """

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
    win_width = 600
    win_height = 650
    play_width = 600
    play_height = 600
    square_size = 40
    bar_height = 50
    mine_cnt = 10
    squares = 15
    window = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("")

    # Define the board sizes in terms of counts of squares
    board_width = int(play_width / square_size)
    board_height = int(play_height / square_size)

    # intialize font
    font_name = pygame.font.get_default_font()
    font_size = 24
    font = pygame.font.Font(font_name, font_size)

    # initally draw whole board
    images = load_images()
    game = Minesweeper(squares, mine_cnt)
    game.draw_board(board_width, board_height, images, window)

    # add bottom bar ui and add on the mines left counter
    bar_ui = pygame.Surface((win_width, bar_height))
    mine_text = font.render(f"Mines: {str(mine_cnt)}", True, (0, 0, 0))
    bar_ui.fill((255, 255, 255))
    bar_ui.blit(mine_text, (0, bar_height / 2))
    window.blit(bar_ui, (0, win_height - bar_height))

    # initializing restart UI features
    restart_ui_width = play_width
    restart_ui_height = 200
    restart_ui_surface = pygame.Surface((restart_ui_width, restart_ui_height))
    restart_ui_surface.fill((255, 255, 255))

    pygame.display.update()

    # main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # getting mouse information
                left, middle, right = pygame.mouse.get_pressed()
                x, y = event.pos

                over = game.game_end()
                if over == "continue":
                    if y <= board_height * square_size:  # prevent out of bounds errors
                        x = int(x / square_size)
                        y = int(y / square_size)

                        if game.first_click:
                            game.first_click = False
                            game.place_mines((x, y))
                            print((x, y))

                        if left:
                            game.click(x, y)  # handle clear action
                        elif right:
                            if game.board[x][y] in {-2, -4}:  # handle unflag action
                                game.unflag(x, y)
                            else:
                                game.flag(x, y)  # handle flag action

                    # updating mine counter
                    mine_cnt = game.mines - game.flag_cnt
                    mine_text = font.render(f"Mines: {str(mine_cnt)}", True, (0, 0, 0))

                    # re-render board + ui
                    game.draw_board(board_width, board_height, images, window)
                    bar_ui.fill((255, 255, 255))
                    bar_ui.blit(mine_text, (0, bar_height / 2))
                    window.blit(bar_ui, (0, win_height - bar_height))

                over = game.game_end()

                # check if game over
                if over != "continue":
                    # render "you win" or "you lose" message
                    game_result_text = font.render(over, True, (0, 0, 0))
                    result_text_pos = (
                        restart_ui_width // 2 - game_result_text.get_width() // 2,
                        25,
                    )
                    # render restart button text
                    restart_button_text = font.render("Restart", True, (0, 0, 0))
                    restart_button_pos = (
                        restart_ui_width // 4 - restart_button_text.get_width() // 2,
                        125,
                    )
                    # render exit button text
                    exit_button_text = font.render("Exit", True, (0, 0, 0))
                    exit_button_pos = (
                        3 * restart_ui_width // 4 - exit_button_text.get_width() // 2,
                        125,
                    )

                    # add onto restart ui
                    restart_ui_surface.blit(game_result_text, result_text_pos)
                    restart_ui_surface.blit(restart_button_text, restart_button_pos)
                    restart_ui_surface.blit(exit_button_text, exit_button_pos)

                    # create appropriate buttons
                    restart_button_rect = pygame.Rect(restart_button_pos, (100, 50))
                    exit_button_rect = pygame.Rect(exit_button_pos, (100, 50))

                    # calculate the centered position for restart button
                    restart_button_text_rect = restart_button_text.get_rect()
                    restart_button_rect.center = (
                        restart_button_pos[0] + restart_button_text_rect.width // 2,
                        restart_button_pos[1] + restart_button_text_rect.height // 2,
                    )

                    # calculate the centered position for exit button
                    exit_button_text_rect = exit_button_text.get_rect()
                    exit_button_rect.center = (
                        exit_button_pos[0] + exit_button_text_rect.width // 2,
                        exit_button_pos[1] + exit_button_text_rect.height // 2,
                    )

                    # draw buttons
                    pygame.draw.rect(
                        restart_ui_surface, (0, 0, 0), restart_button_rect, 2
                    )
                    pygame.draw.rect(restart_ui_surface, (0, 0, 0), exit_button_rect, 2)
                    window.blit(restart_ui_surface, (0, win_height / 4))

                    # adjustive relative positioning
                    adjusted_pos = (
                        event.pos[0] - 0,
                        event.pos[1] - win_height / 4,
                    )

                    print(adjusted_pos)
                    print(restart_button_rect)
                    # handle restart and exit
                    if restart_button_rect.collidepoint(adjusted_pos):
                        # restart the game
                        game.restart_game()
                        game.draw_board(board_width, board_height, images, window)

                    if exit_button_rect.collidepoint(adjusted_pos):
                        # quit the game
                        pygame.quit()
                        sys.exit()

                pygame.display.update()


def main():
    run_game()


if __name__ == "__main__":
    main()
