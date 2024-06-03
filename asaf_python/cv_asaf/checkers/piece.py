from .constants import GREEN, SQUARE_SIZE, BLACK, RED, CROWN
import pygame

class Piece:
    PADDING = 15  # Controls the size of the pieces

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        # Set direction based on color
        if self.color == RED:
            self.direction = -1
        else:
            self.direction = 1
        self.x = 0
        self.y = 0
        self.calc_pos()  # Calculate initial position

    def calc_pos(self):
        # Calculate the x and y position of the piece
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        # Make the piece a king
        self.king = True

    def draw(self, win):
        # Draw the piece on the window
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREEN, (self.x, self.y), radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        # Move the piece to a new row and column
        self.row = row
        self.col = col
        self.calc_pos()  # Recalculate the position

    def __repr__(self):
        # Representation of the piece for debugging purposes
        return str(self.color)
