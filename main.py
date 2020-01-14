import pygame
import random
import os
from sprites import *
import time

#initialize pygame
pygame.display.init()   
pygame.font.init()


#setting variables to values
clock = pygame.time.Clock()
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (160,160,160)
PLAY_WIDTH = 600
PLAY_HEIGHT = 600
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) /2
TOP_LEFT_Y = (SCREEN_HEIGHT - PLAY_HEIGHT) /2
PLAY_SCREEN = (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT)
SQSZ = PLAY_WIDTH / 15
MINESTOTAL = 40
flag_count = MINESTOTAL
PLAY_W_LEFT = SCREEN_WIDTH - PLAY_WIDTH
PLAY_W_RIGHT = SCREEN_WIDTH - PLAY_WIDTH + PLAY_WIDTH
PLAY_H_TOP = SCREEN_HEIGHT - PLAY_HEIGHT
PLAY_H_BOT = SCREEN_HEIGHT - PLAY_HEIGHT + PLAY_HEIGHT
bigfont = pygame.font.SysFont('symbola', 80)
smallfont = pygame.font.SysFont('symbola', 45)


#main class for each individual square
class squares():
    def __init__(self, type, status, image, prox, x, y):
        self.type = type
        self.status = status
        self.image = image
        self.prox = prox
        self.x = x
        self.y = y
    def get_type(self, type):
        return type
    
#makes screen and the border around play area
def draw_play(win):
    win.fill(WHITE)
    pygame.draw.rect(win, BLACK, (TOP_LEFT_X-15, TOP_LEFT_Y-15, PLAY_WIDTH+30, PLAY_HEIGHT+30))

#makes a 15x15 grid of square objects
def make_squares(win):
    topx = TOP_LEFT_X
    topy = TOP_LEFT_Y
    w, h = 15,15
    grid = [['[]' for x in range(w)] for y in range(h)] 
    for i in range(w):
        for j in range(h):
            grid[i][j] = squares('safe', 'none', block, 0, topx+i*SQSZ, topy+j*SQSZ)
    return grid

#makes 40 bombs from any square in the grid
def make_bombs(grid, box):
    mineCount = 0
    xy = [] 
    while mineCount < MINESTOTAL: 
        x = random.randint(0,14)
        y = random.randint(0,14)
        xy.append([x,y]) 
        if xy.count([x,y]) > 1: 
            xy.remove([x,y]) 
        else: 
            grid[x][y].type = 'mine' 
            mineCount += 1

#draws the squares on the grid
def draw_squares(win, grid):
    for i in range(15):
        for j in range(15):
            win.blit(block, (grid[i][j].x, grid[i][j].y))

#check if the block passed through is a mine or not
def mine_check(grid, x, y):
    return grid[x][y].type == 'mine'

#checks if a safe block is near a mine or not and gives it a corresponding number
def proximity(win, grid):
    count = 0
    for i in range(15):
        for j in range(15):
            if grid[i][j].type == 'safe':
                count = 0
                if i != 0: 
                    if mine_check(grid, i-1, j):
                        count += 1
                    if j != 0: 
                        if mine_check(grid, i-1, j-1):
                            count += 1
                    if j != 14: 
                        if mine_check(grid, i-1, j+1):
                            count += 1
                if i != 14: 
                    if mine_check(grid, i+1, j):
                        count += 1
                    if j != 0: 
                        if mine_check(grid, i+1, j-1):
                            count += 1
                    if j != 14: 
                        if mine_check(grid, i+1, j+1):
                            count += 1
                if j != 0: 
                    if mine_check(grid, i, j-1):
                        count += 1
                if j != 14: 
                    if mine_check(grid, i, j+1):
                        count += 1
            grid[i][j].prox = count

#check whether safe blocks are near each other and clears them when pressed
#unfortunately is not as good as I would like      
def clear_adjacent(win, grid):
    for i in range(15):
        for j in range(15):
            if grid[i][j].type == 'safe' and grid[i][j].status == 'clicked':
                if i != 0:
                    if grid[i-1][j].type == 'safe' and grid[i-1][j].prox == 0:
                        grid[i-1][j].status = 'clicked'
                        if i > 1 and 14 > j > 0:
                            grid[i-2][j].status = 'clicked'
                            grid[i-2][j+1].status = 'clicked'
                            grid[i-2][j-1].status = 'clicked' 
                if i != 14: 
                    if grid[i+1][j].type == 'safe' and grid[i+1][j].prox == 0:
                        grid[i+1][j].status = 'clicked'
                        if i < 13 and 14 > j > 0:
                            grid[i+2][j].status = 'clicked'  
                            grid[i+2][j+1].status = 'clicked'
                            grid[i+2][j-1].status = 'clicked'                  
                if j != 0: 
                    if grid[i][j-1].type == 'safe' and grid[i][j-1].prox == 0:
                        grid[i][j-1].status = 'clicked'
                        if j > 1 and 14 > i > 0:
                            grid[i][j-2].status = 'clicked'
                            grid[i+1][j-2].status = 'clicked'
                            grid[i-1][j-2].status = 'clicked'
                if j != 14: 
                    if grid[i][j+1].type == 'safe' and grid[i][j+1].prox == 0:
                        grid[i][j+1].status = 'clicked'
                        if j < 13 and 14 > i > 0:
                            grid[i][j+2].status = 'clicked'
                            grid[i+1][j+2].status = 'clicked'
                            grid[i-1][j+2].status = 'clicked'

#gives flag status and image to box passed through
def flag(box):
    if box.status == 'none':
        box.status = 'flagged'
        box.image = flagged

#returns block back to default status
def unflag(box):
    if box.status == 'flagged':
        box.status = 'none'
        box.image = block

#clicks a box, whether mine or not, revealing it
def clicked(win, box, boxes, grid):
    if box.status == 'none' and box.type == 'safe':
        box.status = 'clicked'
        if box.prox == 0:
            box.image = empty
        elif box.prox > 0 and box.prox <= 8:
            for x in range(8):
                if box.prox == x:
                    box.image = nums[x-1]
    if box.status == 'none' and box.type == 'mine':
        box.image = mine
        box.status = 'clicked'
    return(grid)  
    
#checks if all mines have been flagged, if so, player wins
def win_con(boxes):
    count = 0
    for box in boxes:
        if box.type == 'mine':
            if box.status == 'flagged':
                count += 1
    if count == MINESTOTAL:
        return True
    else:
        return False

#check if player has lost
def lose_con(boxes):
    for box in boxes:
            if box.status == 'clicked':
                if box.type == 'mine':
                    return True
                          
def update_flag(win):
    flags = 'Flags: %d' % (flag_count)
    pygame.draw.rect(win, WHITE, (TOP_LEFT_X+PLAY_WIDTH-95, TOP_LEFT_Y-45, 30,30))
    draw_text(win, flags, 28, BLACK, TOP_LEFT_X+PLAY_WIDTH-95, TOP_LEFT_Y-45)

#shows win screen
def you_win(win):
    draw_end(win, 'You Won!', 30, BLACK)
    #button(win, 'Retry', 30, BLACK, main(win))

#runs through all boxes and updates their image according to their status
def update_sq(win, boxes):
    for box in boxes:
        if box.status == 'clicked' and box.type == 'safe':
            if box.prox == 0:
                box.image = empty
            elif box.prox > 0 and box.prox <=8:
                for x in range(8):
                    if box.prox == x:
                        box.image = nums[x-1] 
    for box in boxes:       
        win.blit(box.image, (box.x, box.y))
    pygame.display.update()

#show mine count at top screen
def show_info(win):
    bombs = 'Mines: %d' % (MINESTOTAL)
    pygame.draw.rect(win, WHITE, (TOP_LEFT_X, TOP_LEFT_Y-45, 30,30))
    draw_text(win, bombs, 28, BLACK,  TOP_LEFT_X, TOP_LEFT_Y-45)
    flags = 'Flags: %d' % (flag_count)
    pygame.draw.rect(win, WHITE, (TOP_LEFT_X+PLAY_WIDTH-95, TOP_LEFT_Y-45, 30,30))
    draw_text(win, flags, 28, BLACK, TOP_LEFT_X+PLAY_WIDTH-95, TOP_LEFT_Y-45)
    
#basic method to draw text
def draw_text(surface, text, size, color, x, y):
    font = pygame.font.SysFont('symbola', size, bold=False)
    label = font.render(text, 1, color)
    surface.blit(label, (x,y))

#method to draw text at bottom screen with bordering box for style
def draw_end(surface, text, size, color):
    font = pygame.font.SysFont('symbola', size, bold=True)
    label = font.render(text, 1, color)
    pygame.draw.rect(surface, BLACK, (TOP_LEFT_X +PLAY_WIDTH /2 - (label.get_width()/2) - 15, TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2 - 15 + 350, label.get_width()+30, label.get_height()+30))
    pygame.draw.rect(surface, WHITE, (TOP_LEFT_X +PLAY_WIDTH /2 - (label.get_width()/2) - 10, TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2 - 10 + 350, label.get_width()+20, label.get_height()+20))
    surface.blit(label,(TOP_LEFT_X +PLAY_WIDTH /2 - (label.get_width()/2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2 + 350))

#method to draw text in center of screen
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('symbola', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label,(TOP_LEFT_X +PLAY_WIDTH /2 - (label.get_width()/2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))

#method to show reset button and reset game if clicked
def play_again(win, words):

    text = bigfont.render(words, 13, (0, 0, 0))
    textx = SCREEN_WIDTH / 2 - text.get_width() / 2
    texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
    textx_size = text.get_width()
    texty_size = text.get_height()

    pygame.draw.rect(display, BLACK, ((textx - 10, texty - 10),
                                               (textx_size + 20, texty_size +
                                                20)))

    pygame.draw.rect(display, WHITE, ((textx - 5, texty - 5),
                                               (textx_size + 10, texty_size +
                                                10)))

    display.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2,
                       SCREEN_HEIGHT / 2 - text.get_height() / 2))

    clock = pygame.time.Clock()
    pygame.display.flip()
    in_main_menu = True
    while in_main_menu:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_main_menu = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if x >= textx - 5 and x <= textx + textx_size + 5:
                    if y >= texty - 5 and y <= texty + texty_size + 5:
                        in_main_menu = False
                        main(win)
                        break


#main game method
def main(win):

    #runs all methods to start a game and to reset a game
    draw_play(win)
    grid = make_squares(win)
    draw_squares(win, grid)
    boxes = []
    pygame.display.update()
    flag_count = MINESTOTAL

    #puts all square objects in 'grid' into a string called boxes
    #having all objects in a list rather than a 2D array helps iterate through it better
    for i in range(15):
        for j in range(15):
            box = grid[i][j]
            boxes.append(box)
    
    #more methods for game start and restart
    make_bombs(grid, box)
    proximity(win, grid)
    show_info(win)

    #main game loop
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                #get mouse pos and if clicked
                click = pygame.mouse.get_pressed()
                x, y = pygame.mouse.get_pos()
                
                #readjusting mouse because for some reason it was off centered
                x = x-SQSZ
                y = y-SQSZ 
            
                #if right mouse button is clicked, put it in list and pass flag method through all objects in list
                flagged_sq = [box for box in boxes if click[2] and x<box.x<x+SQSZ and y<box.y<y+SQSZ]
                for count, box in enumerate(flagged_sq):
                    flag(box)
                    flag_count = flag_count - count

                
            
                #if left mouse button is clicked, put it in list and pass clicked method through all objects in list
                clicked_sq = [box for box in boxes if click[0] and x<box.x<x+SQSZ and y<box.y<y+SQSZ]
                for box in clicked_sq:
                    clicked(win, box, boxes, grid)

                #if middle mouse button is clicked, put it in list and pass unflag method through all objects in list
                unflagged_sq = [box for box in boxes if click[1] and x<box.x<x+SQSZ and y<box.y<y+SQSZ]
                for box in unflagged_sq:
                    unflag(box)      

        #constantly updates status of boxes near clicked boxes
        clear_adjacent(win, grid)


        #constantly checks if player won/lost and updates game
        if win_con(boxes):
            play_again(win, 'You Won! Play Again?')
        update_sq(win, boxes)

        if lose_con(boxes):
            play_again(win, 'You Lost! Try Again?')
            for box in boxes:
                if box.type == 'mine':
                    box.image == 'mine'
        update_sq(win, boxes)

        clock.tick(60)
        pygame.display.update()
        
def main_menu(win):
    running = True
    while running:
        win.fill(BLACK)
        draw_text_middle(win, 'PRESS ANY KEY TO BEGIN', 60, WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                main(win)
            

#initializing screen and applying caption
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Minesweeper')
pygame.display.set_icon(icon)
#runs game
main_menu(display)


#TODO
#show all mines upon loss
#make it so you can't just flag every box to win

