import random
import global_vars
import piece
import pygame


def convert_shape_format(shape):
    """
    Take an instanse of shape and return the positions of the shape

    :param shape: instance of class Piece
    :return: a list of positions ex: [(3, 2), (4, 2), (5, 2), (6, 2)]
    """
    start_positions = shape.shape[shape.rotation % len(shape.shape)]
    positions = []
    for pos in start_positions:
        positions.append((shape.x + pos[0], shape.y + pos[1]))
    return positions

def valid_space(shape, grid):
    """
    Check if we are moving to a valid space on the grid

    :param shape: instance of class Piece
    :param grid: list o lists with colors in their position
    :return: True or False
    """
    # accepted_pos only valid positions
    accepted_pos = [[(j, i) for j in range(global_vars.GRID_WIDTH) if grid[i][j] == (0,0,0)] for i in range(global_vars.GRID_HEIGTH)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    """
    Check if the game is over if the shape locked is over the grid

    :param positions: dictionary with position and color ex: {(x, y): (255, 0, 0)}
    :return: True or False
    """
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape(shapes_numbers):
    """
    Get the shape using the 7-bag system

    :param shapes_number: list with the numbers of the shapes availables
    :return: instance of class Piece
    """
    chosen_shape_number = random.choice(shapes_numbers)
    shapes_numbers.remove(chosen_shape_number)
    if len(shapes_numbers) == 0:
        shapes_numbers = [0, 1, 2, 3, 4, 5, 6]
    return piece.Piece(0, 0, global_vars.SHAPES[chosen_shape_number]), shapes_numbers

def clear_rows(grid, locked):
    """
    Clear row if every position if locked in a row

    :param grid: list o lists with colors in their position
    :param locked: dictionary with position and color ex: {(x, y): (255, 0, 0)}
    :return: number of rows cleared
    """
    inc = 0
    rows_ind = []
    # for position 19 to 0 check every row and if there is color
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            rows_ind.append(ind)
            # uodate locked_positions
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        # sort list form [(0,1), (0,0)] to [(0,0), (0,1)]
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            # move down the positions that are over the deleted row
            if y < rows_ind[0]:
                count = 0
                for deleted_row in rows_ind:
                    if y < deleted_row:
                        count += 1
                new_key = (x, y + count)
                # give color to new key
                locked[new_key] = locked.pop(key)
    return inc

def keyboard(current_piece, grid, hold, hold_piece, first_hold, retention_count):
    """
    Allows the user to use the keyboard

    :param current_piece: instance of class Piece
    :param grid: list o lists with colors in their position
    :param hold: True or False if there is a hold piece
    :param hold_piece: instance of class Piece
    :param first_hold: True or False if is the first piece holded in the game
    :param retention_count: count if there has been a retention while the piece is falling 
    :return: current_piece.x, current_piece.y, current_piece.rotation, run, hard_drop, position_hard_drop, soft_drop, hold, hold_piece, first_hold, aux_piece, retention_count
    """
    run = True
    soft_drop = 0
    hard_drop = False
    position_hard_drop = 0
    aux_piece = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                current_piece.x -= 1
                if not (valid_space(current_piece, grid)):
                    current_piece.x += 1

            if event.key == pygame.K_RIGHT:
                current_piece.x += 1
                if not (valid_space(current_piece, grid)):
                    current_piece.x -= 1

            if event.key == pygame.K_DOWN:
                current_piece.y += 1
                soft_drop += 1
                if not (valid_space(current_piece, grid)):
                    current_piece.y -= 1
                    soft_drop -= 1

            if event.key == pygame.K_UP:
                current_piece.rotation += 1
                if not (valid_space(current_piece, grid)):
                    current_piece.rotation -= 1

            if event.key == pygame.K_z or event.key == pygame.K_LCTRL:
                current_piece.rotation -= 1
                if not (valid_space(current_piece, grid)):
                    current_piece.rotation += 1

            if event.key == pygame.K_SPACE and current_piece.y > -1:
                hard_drop = True
                position_hard_drop = current_piece.y
                while valid_space(current_piece, grid):
                    current_piece.y += 1
                current_piece.y -= 1

            if event.key == pygame.K_c or (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                if retention_count == 0:
                    if hold_piece == False:
                        first_hold = True
                        hold_piece  = piece.Piece(0, 0, current_piece.shape)
                    else:
                        first_hold = False
                        aux_piece  = piece.Piece(0, 0, hold_piece.shape)
                        hold_piece  = piece.Piece(0, 0, current_piece.shape)
                    hold = True
                    retention_count += 1

 
    return current_piece.x, current_piece.y, current_piece.rotation, run, hard_drop, position_hard_drop, soft_drop, hold, hold_piece, first_hold, aux_piece, retention_count
