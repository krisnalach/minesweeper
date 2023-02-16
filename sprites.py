import pygame
import os

#getting images (?) 
def load_images():
    image_names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "empty", "block", "flagged", "mine", "minesweep"]
    var_names = 

    one = pygame.image.load('sprites/one.png')
    two = pygame.image.load('sprites/two.png')
    three = pygame.image.load('sprites/three.png')
    four = pygame.image.load('sprites/four.png')
    five = pygame.image.load('sprites/five.png')
    six = pygame.image.load('sprites/six.png')
    seven = pygame.image.load('sprites/seven.png')
    eight = pygame.image.load('sprites/eight.png')
    empty = pygame.image.load('sprites/empty.png')
    block = pygame.image.load('sprites/block.png')
    flagged = pygame.image.load('sprites/flagged.png')
    mine = pygame.image.load('sprites/mine.png')
    icon = pygame.image.load('sprites/minesweep.png')


def format(image):
    return pygame.transform.scale(image, (40,40))

#reformatting so it fits in game screen
def format_all()
one = format(one)
two = format(two)
three = format(three)
four = format(four)
five = format(five)
six = format(six)
seven = format(seven)
eight = format(eight)
empty = format(empty)
block = format(block)
flagged = format(flagged)
mine = format(mine)
icon = format(icon)

nums = [one, two, three, four, five, six, seven, eight] 