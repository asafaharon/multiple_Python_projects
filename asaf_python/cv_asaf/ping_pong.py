import pygame
import tkinter as tk

def get_speed():
    ball_speed = float(selected_speed.get())
    root.destroy()
    start_game(ball_speed)

def start_game(ball_speed):
    # Initialize pygame
    pygame.init()

    # Set up window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Ping Pong")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74)
    score = 0

    # General settings
    paddle_height = 120
    paddle_width = 15
    ball_size = 15
    ball_dx = ball_speed
    ball_dy = -ball_speed

    # Initial positions of paddles and ball
    paddle_left_y = (600 - paddle_height) // 2
    paddle_right_y = (600 - paddle_height) // 2
    ball_x, ball_y = 400 - ball_size // 2, 300 - ball_size // 2

    restart_key_pressed = False
    running = True
    game_over = False
    while running:
        screen.fill((0, 0, 0))  # Black
        game_text = font.render('Score ' + str(int(score)), True, (255, 255, 255))
        screen.blit(game_text, (300, 350))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # Paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and paddle_left_y > 0:
                paddle_left_y -= 7
            if keys[pygame.K_s] and paddle_left_y < 480:
                paddle_left_y += 7
            if keys[pygame.K_UP] and paddle_right_y > 0:
                paddle_right_y -= 7
            if keys[pygame.K_DOWN] and paddle_right_y < 480:
                paddle_right_y += 7

            # Ball movement
            ball_x += ball_dx
            ball_y += ball_dy

            # Collision with walls
            if ball_y <= 0 or ball_y >= 585:
                ball_dy *= -1

            # Collision with paddles or miss
            if ball_x <= paddle_width:
                if paddle_left_y <= ball_y <= paddle_left_y + paddle_height:
                    ball_dx *= -1
                    score += 1
                    ball_dx += ball_dx * 0.1  # Increase speed by 10%
                    ball_dy += ball_dy * 0.1 if ball_dy > 0 else -ball_dy * 0.1
                else:
                    game_over = True
            if ball_x >= 785 - paddle_width:
                if paddle_right_y <= ball_y <= paddle_right_y + paddle_height:
                    ball_dx *= -1
                    score += 1
                    ball_speed *= 1.1  # Increase initial speed by 10%
                    ball_dx += ball_dx * 0.1  # Increase ball speed by 10%
                    ball_dy += ball_dy * 0.1 if ball_dy > 0 else -ball_dy * 0.1
                else:
                    game_over = True

            # Draw paddles and ball
            pygame.draw.rect(screen, (255, 255, 255), (15, paddle_left_y, paddle_width, paddle_height))
            pygame.draw.rect(screen, (255, 255, 255), (770, paddle_right_y, paddle_width, paddle_height))
            pygame.draw.ellipse(screen, (255, 255, 255), (ball_x, ball_y, ball_size, ball_size))

        else:
            # Display game over message
            screen.fill((0, 0, 0))  # Black
            game_over_text = font.render('Game Over, your score was ' + str(score), True, (255, 255, 255))
            screen.blit(game_over_text, (50, 250))

        pygame.display.flip()
        clock.tick(60)

        if game_over:
            # Display game over message with smaller font
            screen.fill((0, 0, 0))  # Black
            game_over_text = font.render('Game Over, your score was ' + str(score), True, (255, 255, 255))
            screen.blit(game_over_text, (50, 250))

            if not restart_key_pressed:
                restart_text = font.render('Press R to restart', True, (0, 0, 255))
                screen.blit(restart_text, (50, 350))
                pygame.display.flip()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r] and not restart_key_pressed:
                game_over = False
                restart_key_pressed = True
                score = 0
                ball_x, ball_y = 400 - ball_size // 2, 300 - ball_size // 2
            elif not keys[pygame.K_r]:
                restart_key_pressed = False

            pygame.display.flip()
            clock.tick(60)
    pygame.quit()

# Create input window using tkinter
root = tk.Tk()
selected_speed = tk.StringVar()
selected_speed.set("3")
tk.Label(root, text="Select ball speed: ").pack()
tk.Radiobutton(root, text="Slow", variable=selected_speed, value="1").pack()
tk.Radiobutton(root, text="Normal", variable=selected_speed, value="3").pack()
tk.Radiobutton(root, text="Fast", variable=selected_speed, value="5").pack()
tk.Button(root, text="Start Game", command=get_speed).pack()
root.mainloop()
