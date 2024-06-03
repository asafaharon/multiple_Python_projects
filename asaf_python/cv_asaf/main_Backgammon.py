import pygame
import random
import os
def initialize():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (150, 30)
    pygame.init()
    pygame.display.set_caption('Backgammon')


def play_game():
    size = (800, 800)
    screen = pygame.display.set_mode(size)

    # הגדר את הנתיב הבסיסי לתיקיית התמונות
    images_path = os.path.join("Backgammon", "Images")

    # טען את התמונות באמצעות הנתיב הבסיסי והשם של כל תמונה
    button_roll = pygame.image.load(os.path.join(images_path, "Button-Roll.png"))
    button_undo = pygame.image.load(os.path.join(images_path, "Button-Undo.png"))
    button_done = pygame.image.load(os.path.join(images_path, "Button-Done.png"))
    background = pygame.image.load(os.path.join(images_path, "Board.png"))
    # game data
    table = default_table()
    # Table has w or b for pieces from 0 to 23,
    # and the number of out pieces on 24(b) and 25(w)
    playing = True
    black_pips = 167
    white_pips = 167

    dices_thrown = False
    dice_values = [[0, False, False], [0, False, False], [0, False, False], [0, False, False]]
    dice_position = 0
    # dice_values pattern: [[Value, Not Used Yet, Available]]

    stage = ['roll', 'piece moved', 'all pieces', 'start roll', 'nothing']
    turn = ['white', 'black']
    current_turn = 0
    current_stage = 3

    undo_stack = []
    dice_undo_stack = []
    position_undo_stack = []

    # text
    pygame.font.init()
    pipfont = pygame.font.SysFont('Times New Roman', 50)
    turn_font = pygame.font.SysFont('Times New Roman', 15)

    while playing:
        # pygame.mouse.set_cursor(*pygame.cursors.diamond)
        mouse = pygame.mouse.get_pos()
        # click = pygame.mouse.get_pressed(3)


        # text
        blacksurface = pipfont.render(str(black_pips), True, (0, 0, 0))
        whitesurface = pipfont.render(str(white_pips), True, (0, 0, 0))
        who_turns = turn_font.render(turn[current_turn], True, (0, 0, 0))

        # blit
        screen.blit(background, (0, 0))
        screen.blit(blacksurface, (362, -7))
        screen.blit(whitesurface, (362, 752))
        screen.blit(who_turns, (40, 21))
        put_pieces(screen, table)
        if dices_thrown:
            put_dice(screen, dice_values, dice_position)

        if stage[current_stage] == 'roll' or stage[current_stage] == 'start roll':
            screen.blit(button_roll, (541, 353))
        if stage[current_stage] == 'piece moved':
            screen.blit(button_undo, (541, 353))
        if stage[current_stage] == 'all pieces':
            screen.blit(button_undo, (471, 353))
            screen.blit(button_done, (611, 353))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:

                pos_x = mouse[0]
                pos_y = mouse[1]
                # Roll
                if current_stage == 0 or current_stage == 3:
                    # Roll Button
                    if 368 <= pos_y <= 438 and 541 <= pos_x <= 640:
                        [dices1, dices2] = get_dice()
                        dice_undo_stack = []
                        position_undo_stack = []
                        if dices1 < dices2:
                            dices1, dices2 = dices2, dices1
                        dice_values[0][0] = dices1
                        dice_values[0][1] = True
                        dice_values[0][2] = check_available(table, dices1, turn[current_turn])
                        dice_values[1][0] = dices2
                        dice_values[1][1] = True
                        dice_values[1][2] = check_available(table, dices2, turn[current_turn])
                        if dices1 == dices2:
                            dice_values[2] = [0, False, False]
                            dice_values[3] = [0, False, False]
                            dice_values[2][0] = dice_values[3][0] = dices1

                            dice_values[2][1] = True
                            dice_values[2][2] = check_available(table, dices1, turn[current_turn])
                            dice_values[3][1] = True
                            dice_values[3][2] = check_available(table, dices1, turn[current_turn])
                        else:
                            dice_values[2] = [0, False, False]
                            dice_values[3] = [0, False, False]
                        dices_thrown = True
                        dice_position = 0
                        if dice_values[dice_position][2] is False:
                            dice_position = get_next_position(dice_values, dice_position)
                        clear_file()
                        current_stage = 4
                        if can_turn(dice_values) is False:
                            current_stage = 2

                if current_stage == 4 or current_stage == 1:
                    # Move pieces
                    click_on_piece = False
                    if 40 <= pos_x <= 760 and 40 <= pos_y <= 356:
                        click_on_piece = True
                    if 40 <= pos_x <= 760 and 450 <= pos_y <= 760:
                        click_on_piece = True
                    if 40 <= pos_x <= 380 and 356 <= pos_y <= 450:
                        dice_position = get_next_position(dice_values, dice_position)

                    if click_on_piece:
                        row = pos_x - 40
                        row = row // 56
                        if 450 <= pos_y <= 760:
                            row += 12
                        if 40 <= pos_y <= 356:
                            row = 11 - row
                        if row == 5:
                            row = -1
                        elif row < 5:
                            row += 1
                        if row == 18:
                            row = -1
                        elif row > 18:
                            row -= 1
                        if can_turn(dice_values):
                            undo_stack.append(full_copy(table))
                            dice_undo_stack.append(full_dice_copy(dice_values))
                            position_undo_stack.append(dice_position)
                            if row != -1:
                                usable = True
                                if dice_values[dice_position][1] is False or dice_values[dice_position][2] is False:
                                    usable = False
                                if usable and perform_move(table, turn[current_turn], row, dice_values[dice_position][0]):
                                    dice_values[dice_position][1] = False
                                    dice_position = get_next_position(dice_values, dice_position)
                                    for i in range(0, 4):
                                        if dice_values[i][0] != 0:
                                            dice_values[0][2] = check_available(table, dice_values[0][1], turn[current_turn])
                                    if can_turn(dice_values):
                                        current_stage = 1
                                    else:
                                        current_stage = 2
                                else:
                                    undo_stack.pop(-1)
                                    dice_undo_stack.pop(-1)
                                    position_undo_stack.pop(-1)
                            else:
                                # if perform_move(table, turn[current_turn], row, dices1):
                                usable = True
                                if dice_values[dice_position][1] is False or dice_values[dice_position][2] is False:
                                    usable = False
                                if usable and discard_out_piece(table, turn[current_turn], dice_values[dice_position][0]):
                                    dice_values[dice_position][1] = False
                                    dice_position = get_next_position(dice_values, dice_position)
                                    for i in range(0, 4):
                                        if dice_values[i][0] != 0:
                                            dice_values[0][2] = check_available(table, dice_values[0][1], turn[current_turn])
                                    if can_turn(dice_values):
                                        current_stage = 1
                                    else:
                                        current_stage = 2
                                else:
                                    undo_stack.pop(-1)
                                    dice_undo_stack.pop(-1)
                                    position_undo_stack.pop(-1)
                if current_stage == 1:
                    # Undo Button
                    if 368 <= pos_y <= 438 and 541 <= pos_x <= 640:
                        if len(undo_stack) > 0:
                            table = undo_stack.pop(-1)
                            dice_values = dice_undo_stack.pop(-1)
                            dice_position = position_undo_stack.pop(-1)
                            for i in range(0, 4):
                                if dice_values[i][0] != 0:
                                    dice_values[0][2] = check_available(table, dice_values[0][1], turn[current_turn])
                            if len(undo_stack) == 0:
                                current_stage = 4
                if current_stage == 2:
                    # Undo Shifted Left
                    if 368 <= pos_y <= 438 and 470 <= pos_x <= 570:
                        if len(undo_stack) > 0:
                            table = undo_stack.pop(-1)
                            dice_values = dice_undo_stack.pop(-1)
                            dice_position = position_undo_stack.pop(-1)
                            current_stage = 1
                            for i in range(0, 4):
                                if dice_values[i][0] != 0:
                                    dice_values[0][2] = check_available(table, dice_values[0][1], turn[current_turn])
                    if 368 <= pos_y <= 438 and 610 <= pos_x <= 710:
                        dices_thrown = False
                        if current_turn == 0:
                            current_turn = 1
                        elif current_turn == 1:
                            current_turn = 0
                        current_stage = 0
                        undo_stack = []
                        dice_undo_stack = []
                        position_undo_stack = []

        pygame.display.update()
def can_turn(dice_table):
    to_return = False
    for i in range(0, 4):
        if dice_table[i][0] != 0:
            if dice_table[i][2]:
                if dice_table[i][1]:
                    to_return = True
    return to_return
def get_next_position(dice_table, position):
    dice_values = dice_table
    dice_position = position
    dice_position += 1
    if dice_values[3][0] == 0 and dice_position == 2:
        dice_position = 0
    if dice_values[3][0] != 0 and dice_position == 4:
        dice_position = 0
    while dice_values[dice_position][1] is False or dice_values[dice_position][2] is False:
        dice_position += 1
        if dice_values[3][0] == 0 and dice_position == 2:
            dice_position = 0
        if dice_values[3][0] != 0 and dice_position == 4:
            dice_position = 0
        if dice_position == position:
            return position
    return dice_position
def full_copy(table):
    to_ret = []
    for i in range(0, 24):
        to_ret.append([])
        for j in table[i]:
            to_ret[i].append(j)
    to_ret.append(table[24])
    to_ret.append(table[25])
    return to_ret
def full_dice_copy(table):
    to_ret = [[0, False, False], [0, False, False], [0, False, False], [0, False, False]]
    for i in range(0, 4):
        to_ret[i][0] = table[i][0]
        to_ret[i][1] = table[i][1]
        to_ret[i][2] = table[i][2]
    return to_ret
def default_table():
    to_return = []
    for i in range(0, 24):
        to_return.append([])
    b = 'b'
    w = 'w'
    to_return[0] = [b, b]
    to_return[5] = [w, w, w, w, w]
    to_return[7] = [w, w, w]
    to_return[11] = [b, b, b, b, b]
    to_return[12] = [w, w, w, w, w]
    to_return[16] = [b, b, b]
    to_return[18] = [b, b, b, b, b]
    to_return[23] = [w, w]
    to_return.append(0)  # Number of out black-pieces
    to_return.append(0)  # Number of out white-pieces
    # game_sample(to_return)
    return to_return
def game_sample(table):
    to_return = table
    perform_move(to_return, 'black', 16, 1)
    perform_move(to_return, 'white', 23, 6)
    discard_out_piece(to_return, 'black', 4)
    perform_move(to_return, 'white', 23, 4)
    perform_move(to_return, 'black', 16, 1)
    perform_move(to_return, 'black', 18, 1)
    # return
    discard_out_piece(to_return, 'white', 4)
    discard_out_piece(to_return, 'white', 5)
    discard_out_piece(to_return, 'black', 4)
def check_available(table, dice, colour):
    if dice > 6:
        return False
    if colour == 'black':
        colour = 'b'
    if colour == 'white':
        colour = 'w'
    if colour == 'w':
        if table[25] > 0:
            if check_moves(table, colour)[24 - dice]:
                return True
            else:
                return False
    if colour == 'b':
        if table[24] > 0:
            if check_moves(table, colour)[dice - 1]:
                return True
            else:
                return False
    # Check for the rest
    available = False
    if colour == 'b':
        for i in range(0, 23 - dice):
            if check_moves(table, colour)[i + dice]:
                available = True
    if colour == 'w':
        for i in range(23, dice + 1, -1):
            if check_moves(table, colour)[i - dice]:
                available = True
    return available
def check_moves(table, colour):
    to_ret = []
    if colour == 'black':
        colour = 'b'
    elif colour == 'white':
        colour = 'w'
    for i in range(0, 24):
        to_ret.append(False)
    for i in range(0, 24):
        if len(table[i]) == 0:
            to_ret[i] = True
        if len(table[i]) == 1 and table[i][0] != colour:
            to_ret[i] = True
        if len(table[i]) > 0 and table[i][0] == colour:
            to_ret[i] = True
    return to_ret
def perform_move(table, colour, row, value):
    if row < -1 or row > 23:
        return False
    if colour == 'black':
        colour = 'b'
    elif colour == 'white':
        colour = 'w'
    if colour == 'b':
        new_position = row + value
    else:
        new_position = row - value
    if colour == 'w' and table[25] > 0 and row != -1:
        return False
    if colour == 'b' and table[24] > 0 and row != -1:
        return False
    performable = True
    if row == -1:
        new_position = value
    else:
        if row != -1:
            if len(table[row]) == 0 or table[row][0] != colour:
                return False
        else:
            if colour == 'b' and table[24] == 0:
                return False
            if colour == 'w' and table[25] == 0:
                return False
        if new_position > 23 or new_position < 0:
            return False
    if check_moves(table, colour)[new_position] is False:
        performable = False
    if performable:
        if row != -1:
            table[row].pop(-1)
        if len(table[new_position]) == 0:
            table[new_position] = [colour]
        else:
            if table[new_position][0] != colour:
                table[new_position] = [colour]
                if colour == 'w':
                    # If colour is white, it means that the other piece is black
                    table[24] += 1
                if colour == 'b':
                    table[25] += 1
            else:
                table[new_position].append(colour)
        return True
    else:
        return False
def discard_out_piece(table, colour, value):
    """
    Puts a piece back on the table after it was taken out
    """
    if colour == 'black':
        colour = 'b'
    elif colour == 'white':
        colour = 'w'

    if colour == 'b':
        if table[24] < 1:
            return False
        if check_moves(table, colour)[value - 1] is True:
            if perform_move(table, colour, -1, value - 1):
                table[24] -= 1
                return True
        else:
            return False
    if colour == 'w':
        if table[25] < 1:
            return False
        if check_moves(table, colour)[24 - value] is True:
            if perform_move(table, colour, -1, 24 - value):
                table[25] -= 1
                return True
        else:
            return False
def put_pieces(screen, table):
    white_piece = pygame.image.load(
        "Backgammon/Images/Piece-White.png")
    black_piece = pygame.image.load(
        "Backgammon/Images/Piece-Black.png")
    for i in range(0, 24):
        for j in range(0, len(table[i])):
            if table[i][j] == 'w':
                screen.blit(white_piece, get_piece_position(i, j))
            if table[i][j] == 'b':
                screen.blit(black_piece, get_piece_position(i, j))
    for i in range(0, table[24]):
        black_piece = pygame.transform.scale(black_piece, (50, 50))
        screen.blit(black_piece, get_piece_position(-1, i))  # -1 for black pieces
    for i in range(0, table[25]):
        white_piece = pygame.transform.scale(white_piece, (50, 50))
        screen.blit(white_piece, get_piece_position(-2, i))  # -2 for white pieces
def get_dice():

    f = open(
        "Backgammon/Dice.txt")
    value1 = 1
    value2 = 1
    line = str(f.readline())
    try:
        x = int(line[0])
        if 1 <= x <= 6:
            value1 = x
        x = int(line[2])
        if 1 <= x <= 6:
            value2 = x
    except (Exception,):
        value1 = random.randint(1, 6)
        value2 = random.randint(1, 6)

    f.close()
    return [value1, value2]
def put_dice(screen, dice_table, current_dice):

    # dice_first = rotated_image = pygame.transform.rotate(dice_2, 30)
    dice_1 = pygame.image.load(
        "Backgammon/Images/Dice-1.png")
    dice_2 = pygame.image.load(
        "Backgammon/Images/Dice-2.png")
    dice_3 = pygame.image.load(
        "Backgammon/Images/Dice-3.png")
    dice_4 = pygame.image.load(
        "Backgammon/Images/Dice-4.png")
    dice_5 = pygame.image.load(
        "Backgammon/Images/Dice-5.png")
    dice_6 = pygame.image.load(
        "Backgammon/Images/Dice-6.png")
    dice_s = pygame.image.load(
        "Backgammon/Images/Dice-Shadow.png")
    dices = [dice_s, dice_1, dice_2, dice_3, dice_4, dice_5, dice_6]
    dice_positions = [[148, 363], [227, 393], [78, 383], [297, 373]]
    all_used = False
    for i in range(0, 4):
        if dice_table[i][1] == True and dice_table[i][2] == True:
            all_used = True
    if all_used is False:
        current_dice = -1
    for i in range(3, -1, -1):
        if dice_table[i][0] != 0:
            dice_pic = dices[dice_table[i][0]]
            dice_s = pygame.image.load(
                "Backgammon/Images/Dice-Shadow.png")
            dice_pic.set_alpha(255)
            dice_s.set_alpha(255)
            if i == current_dice:
                dice_pic = pygame.transform.scale(dice_pic, (70, 70))
                dice_s = pygame.transform.scale(dice_s, (70, 70))
            if dice_table[i][1] == False or dice_table[i][2] == False:
                dice_pic.set_alpha(80)
                dice_s.set_alpha(80)
            screen.blit(dice_s, (dice_positions[i][0] + dice_table[i][0] + 5, dice_positions[i][1] + dice_table[i][0] + 5))
            screen.blit(dice_pic, (dice_positions[i][0] + dice_table[i][0], dice_positions[i][1] + dice_table[i][0]))
def get_piece_position(row, height):
    if row == -1:
        piece_x = 374
        piece_y = 28 + height * 43
        return piece_x, piece_y
    elif row == -2:
        piece_x = 374
        piece_y = 710 - height * 43
        return piece_x, piece_y
    else:
        x_positions = [700, 644, 588, 532, 476, 420, 320, 264, 208, 152, 96, 40, 40, 96, 152, 208, 264, 320, 420, 476, 532, 588, 644, 700]
        piece_x = x_positions[row]
        if row <= 11:
            piece_y = 40 + height * 52
        else:
            piece_y = 703 - height * 52
        return piece_x, piece_y
def clear_file():

    f = open(
        "../Dice.txt", "w")
    f.write("x x")
    f.close()
if __name__ == '__main__':
    initialize()
    play_game()
