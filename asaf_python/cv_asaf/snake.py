import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Constants
BLUE, RED, GREEN, GREY, YELLOW, GOLD, PURPLE = (0, 0, 255), (255, 0, 0), (0, 255, 0), (107, 107, 107), (255, 255, 0), (
212, 175, 55), (204, 65, 239)
LIST_COLOR = [BLUE, YELLOW, GOLD, RED, PURPLE]
ROWS, WIDTH = 20, 800

# Initialize pygame
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)
screen = pygame.display.set_mode([WIDTH, WIDTH])
pygame.display.set_caption('Asaf Snake Project')
width = WIDTH

# Difficulty levels configuration
difficulty_levels = {
    'easy': 150,
    'medium': 70,
    'hard': 20
}

# Initialize default difficulty choice
difficulty_choice = "medium"

class Cube:
    """Class representing a cube in the game."""

    rows = ROWS
    w = width

    def __init__(self, start, dirnx=1, dirny=0, color=random.choice(LIST_COLOR)):
        """Initialize cube object."""
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
        self.color = color

    def move(self, dirnx, dirny):
        """Move the cube."""
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        """Draw the cube on the screen."""
        dis = self.w // self.rows
        i, j = self.pos

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle1 = (i * dis + centre - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, random.choice(LIST_COLOR), circle_middle1, radius)
            pygame.draw.circle(surface, random.choice(LIST_COLOR), circle_middle2, radius)

class Snake:
    """Class representing the snake in the game."""

    body = []
    turns = {}

    def __init__(self, color, pos):
        """Initialize snake object."""
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        """Move the snake."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx, self.dirny = -1, 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx, self.dirny = 1, 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx, self.dirny = 0, -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx, self.dirny = 0, 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        """Reset the snake."""
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        """Add a cube to the snake."""
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx, self.body[-1].dirny = dx, dy

    def draw(self, surface):
        """Draw the snake on the screen."""
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def draw_grid(w, rows, surface):
    """Draw the grid lines on the screen."""
    size_btwn = w // rows
    x, y = 0, 0
    for l in range(rows + 1):
        pygame.draw.line(surface, random.choice(LIST_COLOR), (x, 0), (x, w))
        pygame.draw.line(surface, random.choice(LIST_COLOR), (0, y), (w, y))
        x += size_btwn
        y += size_btwn

def redraw_window(surface):
    """Redraw the window with updated elements."""
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    draw_grid(width, ROWS, surface)
    pygame.display.update()

def random_snack(rows, item):
    """Generate random position for a snack."""
    positions = item.body
    while True:
        x, y = random.randrange(rows), random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return x, y

def draw_misc():
    """Draw miscellaneous elements like score."""
    score_text = font.render(f'Score: {len(s.body)}', True, 'white')
    text_rect = score_text.get_rect(top=10, right=WIDTH - 10)
    screen.blit(score_text, text_rect.topleft)

def message_box(subject, content):
    """Display a message box."""
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def calculate_delay(score):
    """Calculate the delay based on the current score."""
    base_delay = 150
    decrease_factor = 2
    new_delay = max(20, base_delay - (score * decrease_factor))
    return new_delay

def change_difficulty(choice):
    """Change the difficulty level."""
    global difficulty_choice
    difficulty_choice = choice
    messagebox.showinfo("Difficulty", f"Difficulty chosen: {choice}")
def main():

    # Initialize Pygame
    pygame.init()

    """Main function to run the game."""
    global width, s, snack, delay_time, difficulty_choice


    win = pygame.display.set_mode((width, width))
    s = Snake(random.choice(LIST_COLOR), (10, 10))
    snack = Cube(random_snack(ROWS, s), color=random.choice(LIST_COLOR))
    flag = True
    clock = pygame.time.Clock()

    while flag:

        current_score = len(s.body)
        delay_time = calculate_delay(current_score)
        pygame.time.delay(delay_time)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(ROWS, s), color=random.choice(LIST_COLOR))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                message_box('Score', str(len(s.body)))
                message_box('You Lost!', 'Play again...')
                s.reset((10, 10))
                break

        redraw_window(win)
        draw_misc()
        pygame.display.flip()

        # Check for user input to change difficulty
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # Press 'e' for easy
                    change_difficulty('easy')
                elif event.key == pygame.K_m:  # Press 'm' for medium
                    change_difficulty('medium')
                elif event.key == pygame.K_h:  # Press 'h' for hard
                    change_difficulty('hard')

if __name__ == "__main__":
    main()

