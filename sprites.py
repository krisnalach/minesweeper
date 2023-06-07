import pygame
import os


def load_images():
    """
    Load in images as pygame images
    Args:
        None
    Returns:
        A dictionary containing all images
    """
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
    # icon = pygame.image.load('sprites/minesweep.png')
    for i, im in enumerate(image_names):
        if i <= 8:  # handle 0-8 cases
            imgs["nums"].append(format(pygame.image.load(f"sprites/{im}.png")))
        else:
            imgs[im] = format(pygame.image.load(f"sprites/{im}.png"))

    return imgs


def format(image):
    """
    Helper function to resize images
    Args:
        image - the image to resize
    Returns:
        The resized image
    """
    return pygame.transform.scale(image, (120, 120))
