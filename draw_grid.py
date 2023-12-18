import global_vars
import pygame

def create_grid(locked_positions={}):
    """
    create_grid creates black spaces with grid metrics and replace the colors that come in locked_positions

    :param locked_positions: dictionary with position and color ex: {(x, y): (255, 0, 0)}
    :return: a list o lists with colors in their position
    """
    grid = [[(0,0,0) for x in range (global_vars.GRID_WIDTH)] for y in range(global_vars.GRID_HEIGTH)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                color = locked_positions[(x, y)]
                grid[y][x] = color
    return grid

def draw_grid_lines(surface, grid):
    """
    Draw all grid lines

    :param surface: screen where the game is dispayed
    :param grid: list o lists with colors in their position
    """
    sx = global_vars.TOP_LEFT_X
    sy = global_vars.TOP_LEFT_Y

    for y in range(len(grid)):
        # horizontal lines
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + y*global_vars.BLOCK_SIZE), (sx + global_vars.PLAY_WIDTH, sy + y*global_vars.BLOCK_SIZE))
        for x in range(len(grid[y])):
            # vertical lines
            pygame.draw.line(surface, (128, 128, 128), (sx + x*global_vars.BLOCK_SIZE, sy), (sx + x*global_vars.BLOCK_SIZE, sy + global_vars.PLAY_HEIGHT))

def draw_text_middle(surface, text, size, color):  
    """
    draw a text in the middle of the screen

    :param surface: screen where the game is dispayed
    :param text: text to be displayed
    :param size: size of the text    
    :param color: color of the text 
    """
    font = pygame.font.SysFont('arial', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (global_vars.TOP_LEFT_X + global_vars.PLAY_WIDTH /2 - (label.get_width()/2), global_vars.TOP_LEFT_Y + global_vars.PLAY_HEIGHT/2 - label.get_height()/2))

def draw_next_shape(next_piece_1, next_piece_2, next_piece_3, surface):
    """
    Draw the next shapes on the right side of the screen

    :param next_piece_1: instance of class Piece
    :param next_piece_2: instance of class Piece
    :param next_piece_3: instance of class Piece
    :param surface: screen where the game is dispayed
    """
    font = pygame.font.SysFont('arial', 30)
    label = font.render('NEXT SHAPES', 1, (255, 255, 255))

    sx = global_vars.TOP_LEFT_X + global_vars.PLAY_WIDTH + 50
    sy = global_vars.TOP_LEFT_Y + global_vars.PLAY_HEIGHT/2 - 100

    surface.blit(label, (sx - 15, sy - 140))

    # draw next shape 1
    positions = next_piece_1.shape[next_piece_1.rotation % len(next_piece_1.shape)]
    for pos in positions:
            pygame.draw.rect(surface, next_piece_1.color, (sx - 90 + pos[0]*global_vars.BLOCK_SIZE, sy - 0 + pos[1]*global_vars.BLOCK_SIZE, global_vars.BLOCK_SIZE, global_vars.BLOCK_SIZE), 0)

    # draw next shape 2
    positions = next_piece_2.shape[next_piece_2.rotation % len(next_piece_2.shape)]
    for pos in positions:
            pygame.draw.rect(surface, next_piece_2.color, (sx - 90 + pos[0]*global_vars.BLOCK_SIZE, sy + 150 + pos[1]*global_vars.BLOCK_SIZE, global_vars.BLOCK_SIZE, global_vars.BLOCK_SIZE), 0)

    # draw next shape 3
    positions = next_piece_3.shape[next_piece_3.rotation % len(next_piece_3.shape)]
    for pos in positions:
            pygame.draw.rect(surface, next_piece_3.color, (sx - 90 + pos[0]*global_vars.BLOCK_SIZE, sy + 300 + pos[1]*global_vars.BLOCK_SIZE, global_vars.BLOCK_SIZE, global_vars.BLOCK_SIZE), 0)

def draw_hold_shape(hold_piece, surface):
    """
    Draw the hold shape on the left side of the screen

    :param hold_piece: instance of class Piece
    :param surface: screen where the game is dispayed
    """
    font = pygame.font.SysFont('arial', 30)
    label = font.render('HOLD', 1, (255, 255, 255))

    sx = global_vars.TOP_LEFT_X + global_vars.PLAY_WIDTH + 50
    sy = global_vars.TOP_LEFT_Y + global_vars.PLAY_HEIGHT/2 - 100

    surface.blit(label, (sx - 500, sy - 140))

    if hold_piece != False:
        positions = hold_piece.shape[hold_piece.rotation % len(hold_piece.shape)]
        for pos in positions:
            pygame.draw.rect(surface, hold_piece.color, (sx - 610 + pos[0]*global_vars.BLOCK_SIZE, sy - 40 + pos[1]*global_vars.BLOCK_SIZE, global_vars.BLOCK_SIZE, global_vars.BLOCK_SIZE), 0)

def draw_window(surface, grid, score=0, max_score=0, level=1):
    """
    Draw tittle, level, score, max_score, shapes, border and lines

    :param surface: screen where the game is dispayed
    :param grid: list o lists with colors in their position
    :param score: actual score
    :param max_score: max score since the game was opened
    :param level: actual level
    """

    surface.fill((0, 0, 0))

    # game tittle
    pygame.font.init()
    font = pygame.font.SysFont('arial', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(label, (global_vars.TOP_LEFT_X + global_vars.PLAY_WIDTH/2 - label.get_width()/2, 30))

    sx = global_vars.TOP_LEFT_X + global_vars.PLAY_WIDTH + 20
    sy = global_vars.TOP_LEFT_Y + global_vars.PLAY_HEIGHT/2 - 50    

    # Level
    font = pygame.font.SysFont('arial', 30)
    label = font.render('LEVEL', 1, (255, 255, 255))
    surface.blit(label, (sx - 520, sy + 30))
    label = font.render(str(level), 1, (255, 255, 255))
    surface.blit(label, (sx - 520, sy + 70))

    # score
    label = font.render('SCORE', 1, (255, 255, 255))
    surface.blit(label, (sx - 520, sy + 110))
    label = font.render(str(score), 1, (255, 255, 255))
    surface.blit(label, (sx - 520, sy + 150))

    # MAX score
    label = font.render('MAX SCORE', 1, (255, 255, 255))
    surface.blit(label, (sx - 520, sy + 190))
    label = font.render(str(max_score), 1, (255, 255, 255))
    surface.blit(label, (sx - 520, sy + 230))

    draw_shapes(surface, grid)
    
    # grid border
    pygame.draw.rect(surface, (255, 0, 0), (global_vars.TOP_LEFT_X, global_vars.TOP_LEFT_Y, global_vars.PLAY_WIDTH, global_vars.PLAY_HEIGHT), 4)

    # grid lines
    draw_grid_lines(surface, grid)

def draw_shapes(surface, grid):
    """
    Draw color of each position on the grid

    :param surface: screen where the game is dispayed
    :param grid: list o lists with colors in their position
    """
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            # surface, color, position
            pygame.draw.rect(surface, grid[y][x], (global_vars.TOP_LEFT_X + x*global_vars.BLOCK_SIZE, global_vars.TOP_LEFT_Y + y*global_vars.BLOCK_SIZE, global_vars.BLOCK_SIZE, global_vars.BLOCK_SIZE))
