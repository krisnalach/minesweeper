from game import Minesweeper
import pygame
from sprites import load_images
import sys


# Moved from game.py since game.py will be repurposed for an agent.
# Kept around so it can still be played by real people with a mouse


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
    square_size = 75
    bar_height = 50
    mine_cnt = 4
    squares = 8
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
    game.draw_board(board_width, board_height, images, window, 75)

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
                    game.draw_board(board_width, board_height, images, window, 75)
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
                        game.draw_board(board_width, board_height, images, window, 75)

                    if exit_button_rect.collidepoint(adjusted_pos):
                        # quit the game
                        pygame.quit()
                        sys.exit()

                pygame.display.update()


def main():
    run_game()


if __name__ == "__main__":
    main()
