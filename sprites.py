import pygame
import os

one = pygame.image.load(os.path.join('sprites/one.png'))
two = pygame.image.load(os.path.join('sprites/two.png'))
three = pygame.image.load(os.path.join('sprites/three.png'))
four = pygame.image.load(os.path.join('sprites/four.png'))
five = pygame.image.load(os.path.join('sprites/five.png'))
six = pygame.image.load(os.path.join('sprites/six.png'))
seven = pygame.image.load(os.path.join('sprites/seven.png'))
eight = pygame.image.load(os.path.join('sprites/eight.png'))
empty = pygame.image.load(os.path.join('sprites/empty.png'))
block = pygame.image.load(os.path.join('sprites/block.png'))
flagged = pygame.image.load(os.path.join('sprites/flagged.png'))
mine = pygame.image.load(os.path.join('sprites/mine.png'))

def format(image):
    return pygame.transform.scale(image, (40,40))

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

nums = [one, two, three, four, five, six, seven, eight] 