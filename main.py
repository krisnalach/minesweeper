import pygame
import random
from sprites import *

pygame.display.init()
pygame.font.init()

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
SQUARE_SIZE = PLAY_WIDTH / 15

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
    
def draw_play(win):
    pygame.draw.rect(win, GRAY, PLAY_SCREEN)

def make_squares(win):
    X = TOP_LEFT_X
    Y = TOP_LEFT_Y
    grid = []
    boxes = []
    j = 1
    for i in range(15):
        for j in range(15):
            square = pygame.draw.rect(win, BLACK, (X+i*SQUARE_SIZE, Y+j*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            grid.append(square)
    for square in grid:
        sqrz = squares('safe', 'none', block, 0,  square.x, square.y)
        boxes.append(sqrz) 
    for count, box in enumerate(boxes):
        check = random.randint(0,3)
        if check == 1:
            box.type = 'bomb'
            box.image = mine
        if count == 40:
            break
    return boxes

def draw_squares(win):
    for box in make_squares(win):
        win.blit(block, (box.x, box.y))

def proximity(win, boxes):
    count = 0
    for box in boxes:
        if box.type == 'safe':    #prob scrap this, find better solution to set numbers
            if boxes.index(box) < 224:
                if boxes[boxes.index(box)+1].type == 'bomb':
                    count += 1
            if boxes[boxes.index(box)-1].type == 'bomb':
                count += 1
            if boxes.index(box) < 209:
                if boxes[boxes.index(box)+15].type == 'bomb':
                    count += 1
            if boxes[boxes.index(box)-15].type == 'bomb':
                count += 1
            if boxes[boxes.index(box)-14].type == 'bomb':
                count += 1
            if boxes[boxes.index(box)-16].type == 'bomb':
                count += 1
            if boxes.index(box) < 208:
                if boxes[boxes.index(box)+16].type == 'bomb':
                    count += 1
            if boxes.index(box) < 210:
                if boxes[boxes.index(box)+14].type == 'bomb':
                    count += 1
    box.prox = count     

def flag(win, box):
    if box.status == 'none':
        box.status = 'flagged'
        box.image = flagged
    update_sq(win, box, box.image)    

def unflag(win, box):
    if box.status == 'flagged':
        box.status = 'none'
        box.image = block
    update_sq(win, box, box.image)

def clicked(win, box):
    if box.status == 'none' and box.type == 'safe':
        box.status = 'clicked'
        if box.prox == 0:
            box.image = empty
        else:
            for x in range(8):
                if box.prox == x:
                    box.image = nums[x+1]
    if box.status == 'none' and box.type == 'bomb':
        box.status = 'clicked'
        box.image = mine    
    update_sq(win, box, box.image)

def update_sq(win, box, image):
    win.blit(box.image, (box.x, box.y))
    pygame.display.update()


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('sansserif', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (0, SCREEN_HEIGHT/2))

def main(win):
    draw_play(win)
    boxes = make_squares(win)
    draw_squares(win)
    proximity(win, boxes)
    pygame.display.update()
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pressed()
                x, y = pygame.mouse.get_pos()

                x = x-SQUARE_SIZE
                y = y-SQUARE_SIZE

                flagged_sq = [box for box in boxes if click[2] and x<box.x<x+SQUARE_SIZE and y<box.y<y+SQUARE_SIZE]
                for box in flagged_sq:
                    flag(win, box)

                clicked_sq = [box for box in boxes if click[0] and x<box.x<x+SQUARE_SIZE and y<box.y<y+SQUARE_SIZE]
                for box in clicked_sq:
                    clicked(win, box)
            
                unflagged_sq = [box for box in boxes if click[1] and x<box.x<x+SQUARE_SIZE and y<box.y<y+SQUARE_SIZE]
                for box in unflagged_sq:
                    unflag(win, box)
        
        pygame.display.update()
          
#def main_menu(win):
    #running = True
    #while running:
        #win.fill(BLACK)
        #draw_text_middle(win, 'Enter any to key to begin', 60, WHITE)
        #pygame.display.update()
        #for event in pygame.event.get():
            #if event.type == pygame.QUIT:
                #running = False
            #if event.type == pygame.KEYDOWN:
                #main(win)
            

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Minesweeper')

main(display)