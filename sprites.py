import pygame
import os


# getting images (?)
def load_images():
    image_names = [
        "empty",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "block",
        "flagged",
        "mine",
        "minesweep",
    ]
    imgs = {}
    imgs["nums"] = []

    one = pygame.image.load("sprites/one.png")
    two = pygame.image.load("sprites/two.png")
    three = pygame.image.load("sprites/three.png")
    four = pygame.image.load("sprites/four.png")
    five = pygame.image.load("sprites/five.png")
    six = pygame.image.load("sprites/six.png")
    seven = pygame.image.load("sprites/seven.png")
    eight = pygame.image.load("sprites/eight.png")
    empty = pygame.image.load("sprites/empty.png")
    block = pygame.image.load("sprites/block.png")
    flagged = pygame.image.load("sprites/flagged.png")
    mine = pygame.image.load("sprites/mine.png")
    # icon = pygame.image.load('sprites/minesweep.png')
    for i, im in enumerate(image_names):
        if i <= 8:  # handle 0-8 cases
            imgs["nums"].append(format(pygame.image.load(f"sprites/{im}.png")))
        else:
            imgs[im] = format(pygame.image.load(f"sprites/{im}.png"))

    return imgs


def format(image):
    return pygame.transform.scale(image, (40, 40))
