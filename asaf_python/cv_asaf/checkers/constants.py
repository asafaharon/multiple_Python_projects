import pygame

# Help page for defining game data (board size, rows-columns, game slots, graphics colors)

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS


beige = (245, 245, 220)
GREEN = (69, 139, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Embedding the crown image into a variable and arranging it in the appropriate resolution
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (25, 15))
