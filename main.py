import pygame
import global_vars
import piece
import draw_grid
import game

pygame.font.init()
pygame.init()


def main(screen, max_score):
    """
    Run one game

    :param screen: screen where the game is dispayed
    :param max_score: max score since the game was opened
    :return: run and max score
    """
    locked_positions = {}
    grid = draw_grid.create_grid(locked_positions)

    change_piece = False
    run = True

    shapes_numbers =  [0, 1, 2, 3, 4, 5, 6]
    current_piece, shapes_numbers = game.get_shape(shapes_numbers)
    next_piece_1, shapes_numbers = game.get_shape(shapes_numbers)
    next_piece_2, shapes_numbers = game.get_shape(shapes_numbers)
    next_piece_3, shapes_numbers = game.get_shape(shapes_numbers)

    hold = False
    hold_piece = False
    first_hold = True
    retention_count = 0

    level = 1
    score = 0
    rows_clear = 0
    rows_clear_cum = 0
    combo_count = -1

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = (0.8-((level-1)*0.007))**(level-1)

    while run:
        # update grid
        grid = draw_grid.create_grid(locked_positions)

        # time since the last clock.tick()
        fall_time += clock.get_rawtime()
        clock.tick()

        # shape moved 1 position down
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(game.valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        current_piece.x, current_piece.y, current_piece.rotation, run , hard_drop, position_hard_drop, soft_drop, hold, hold_piece, first_hold, aux_piece, retention_count = game.keyboard(current_piece, grid, hold, hold_piece, first_hold, retention_count)
        
        if hard_drop:
            score += 2 * (current_piece.y - position_hard_drop)
        score += soft_drop

        if hold:
            if first_hold:
                current_piece = next_piece_1
                next_piece_1 = next_piece_2
                next_piece_2 = next_piece_3
                next_piece_3, shapes_numbers = game.get_shape(shapes_numbers)
                hold = False
            else:
                current_piece = aux_piece
                hold = False

        shape_pos = game.convert_shape_format(current_piece)

        # shadow parameters
        shadow = piece.Piece(current_piece.x, current_piece.y, current_piece.shape)
        shadow.rotation = current_piece.rotation
        while game.valid_space(shadow, grid):
            shadow.y += 1
        shadow.y -= 1
        shadow_pos = game.convert_shape_format(shadow)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            x_s, y_s = shadow_pos[i]
            # draw while piece is falling
            if y > -1:
                # draw shadow
                grid[y_s][x_s] = (100, 100, 100, 0.9)
                # draw shape
                grid[y][x] = current_piece.color

        # if change_piece = True add piece to locked positions
        if change_piece:
            retention_count = 0
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color

            current_piece = next_piece_1
            next_piece_1 = next_piece_2
            next_piece_2 = next_piece_3
            next_piece_3, shapes_numbers = game.get_shape(shapes_numbers)
            change_piece = False
            rows_clear = game.clear_rows(grid, locked_positions)
            rows_clear_cum += rows_clear

            # to level up
            if rows_clear_cum >= level * 10:
                level += 1

            # combo count
            if rows_clear > 0 :
                combo_count += 1
            elif rows_clear == 0:
                combo_count = -1

            # score for perfect clear
            if len(locked_positions) == 0:
                if rows_clear == 1:
                    score += 800*level
                elif rows_clear == 2:
                    score += 1200*level
                elif rows_clear == 3:
                    score += 1800*level
                elif rows_clear >= 4:
                    score += 2000*level

            # score for cleared rows
            elif len(locked_positions) > 0:
                if rows_clear == 1:
                    score += 100 * level
                elif rows_clear == 2:
                    score += 300 * level
                elif rows_clear == 3:
                    score += 500 * level
                elif rows_clear >= 4:
                    score += 800 * level

            # score for combo
            if combo_count > 0:
                score += 50* combo_count * level

        draw_grid.draw_window(screen, grid, score, max_score, level)
        draw_grid.draw_next_shape(next_piece_1, next_piece_2, next_piece_3, screen)
        draw_grid.draw_hold_shape(hold_piece, screen)
        pygame.display.update()

        if game.check_lost(locked_positions):
            draw_grid.draw_text_middle(screen, "Game Over", 80, (255, 255, 255))
            pygame.display.update()
            pygame.mixer.music.stop()
            max_score = max(max_score, score)
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False, max_score
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return True, max_score

    return False, max_score

def main_menu(screen):
    """
    Run the game

    :param screen: screen where the game is dispayed
    """
    max_score = 0
    run = True
    while run:
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1)
        run, max_score = main(screen, max_score)
            

screen = pygame.display.set_mode((global_vars.S_WIDTH, global_vars.S_HEIGHT))
pygame.display.set_caption('Tetris')
main_menu(screen)
