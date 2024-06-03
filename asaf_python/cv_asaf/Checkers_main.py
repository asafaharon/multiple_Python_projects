import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, CROWN,RED
from checkers.board import Board
from checkers.game import Game
pygame.font.init()

FPS = 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Asaf Checkers Project ')


# Function called between the player's decision by mouse click
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)


#The main gameplay
    while run:
        clock.tick(FPS)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                #אם המשחק הוא נגד המחשב אז להוסיף תנאי שהפיצר של אור כחול הוא רק לאדום
                game.select(row,col)

        game.update()

    pygame.quit()


main()
