import sys
import time

import pygame
import random
from pygame.locals import *

from helpers import get_map, display_text, create_grid, color_grid, dfs_move, find_houses, solutions, check_solutions


pygame.font.init()
myfont = pygame.font.SysFont(None, 25)

pygame.init()

FPS = 59
fpsClock = pygame.time.Clock()

WINDOW_SIZE = (900, 900)
DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Inteligentna śmieciarka')
background_image = pygame.image.load("images/road_big.jpg")

grid = create_grid(get_map(5))
all_sprites_list, garbage_collector, houses = color_grid(grid)

garbage_amount = 0
x = 0

while x == 0:
    display_text(myfont, DISPLAYSURF,
                 f"Ilość śmieci w śmieciarce: {garbage_amount}/{garbage_collector.container_capacity}", 600, 0)

    for house in houses:
        display_text(myfont, DISPLAYSURF, f"{house.garbage_amount}",
                     house.rect.x,
                     house.rect.y + 10)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        position = garbage_collector.position
        visited_houses = []
        last_move = position
        counter = 0
        solution = []
        count = find_houses(grid)
        print(count)
        dfs_move(grid, position, last_move, visited_houses, counter, solution, count)
        check_solutions(count)
        solution = solutions
        print(solution)
        find = 30000
        for i in range(len(solution)):
            if len(solution[i]) < find:
                find = len(solution[i])
                index = i
        print(solution[index])
        solution = solution[index]
        while solution:
            # time.sleep(0.2)
            display_text(myfont, DISPLAYSURF,
                         f"Ilość śmieci w śmieciarce: {garbage_amount}/{garbage_collector.container_capacity}", 600, 0)

            for house in houses:
                display_text(myfont, DISPLAYSURF, f"{house.garbage_amount}",
                             house.rect.x,
                             house.rect.y + 10)

            pygame.display.update()
            move = solution.pop(0)
            garbage_taken = 0
            if move == "R":
                garbage_taken = garbage_collector.move_right()
                garbage_collector.position = [garbage_collector.position[0] + 1, garbage_collector.position[1]]
            elif move == "L":
                garbage_taken = garbage_collector.move_left()
                garbage_collector.position = [garbage_collector.position[0] - 1, garbage_collector.position[1]]
            elif move == "D":
                garbage_taken = garbage_collector.move_down()
                garbage_collector.position = [garbage_collector.position[0], garbage_collector.position[1] + 1]
            elif move == "U":
                garbage_taken = garbage_collector.move_up()
                garbage_collector.position = [garbage_collector.position[0], garbage_collector.position[1] - 1]
            elif move == "RH":
                garbage_taken = garbage_collector.move_right()
            elif move == "LH":
                garbage_taken = garbage_collector.move_left()
            elif move == "DH":
                garbage_taken = garbage_collector.move_down()
            elif move == "UH":
                garbage_taken = garbage_collector.move_up()

            if garbage_collector.garbage_amount == 0:
                garbage_amount = 0
            else:
                garbage_amount += garbage_taken
            all_sprites_list.update()
            DISPLAYSURF.blit(background_image, (0, 0))
            all_sprites_list.draw(DISPLAYSURF)
            pygame.display.flip()
        break
    # all_sprites_list.update()
    # DISPLAYSURF.blit(background_image, (0, 0))
    # all_sprites_list.draw(DISPLAYSURF)
    #
    # pygame.display.flip()

    fpsClock.tick(FPS)
    break
