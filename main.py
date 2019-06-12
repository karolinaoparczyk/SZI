import sys
from random import randrange
import numpy as np
import os

import pygame
from pygame.locals import *
from sklearn.model_selection import train_test_split

from helpers import create_dataset, train_linear_regression, get_linear_regression_decision_test

from helpers import get_map, display_text, create_grid, color_grid, dfs_move, find_houses, solutions, \
    get_data_tree_from_file, train_decision_tree, decision_tree_move, get_tree_decision_test, bfs_move


#decision tree
choices_train, choices_test, possibilities_train, possibilities_test = get_data_tree_from_file()
clf = train_decision_tree(choices_train, possibilities_train)
# get_tree_decision_test(clf, possibilities_test, choices_test)

#linear regression
X = np.asarray(possibilities_train)
y = choices_train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
regr = train_linear_regression(X_train, y_train)
decision = get_linear_regression_decision_test(regr, X_test, y_test)

pygame.font.init()
myfont = pygame.font.SysFont(None, 25)
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

FPS = 59
fpsClock = pygame.time.Clock()

WINDOW_SIZE = (900, 900)
DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Inteligentna śmieciarka')
background_image = pygame.image.load("images/road_big.jpg")
temp = randrange(1, 75)
print(temp)
grid = create_grid(get_map(temp))
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
        count = find_houses(grid)
        # START of DFS
        # visited_houses = []
        # counter = 0
        # solution = ['test']
        # temp = 'start'
        # dfs_move(grid, position, visited_houses, counter, solution, count, temp)
        #
        # solution = solutions
        # find = 30000
        # for i in range(len(solution)):
        #     if len(solution[i]) < find:
        #         find = len(solution[i])
        #         index = i
        #
        # solution = solution[index]
        # create_dataset(grid, solution, position)
        # END of DFS
        # solution = decision_tree_move(grid, position, clf, regr, count)
        solution = bfs_move(grid, position, count)
        print(solution)
        while solution:
            display_text(myfont, DISPLAYSURF,
                         f"Ilość śmieci w śmieciarce: {garbage_amount}/{garbage_collector.container_capacity}", 600,
                         0)

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

    fpsClock.tick(FPS)
    break
