import sys

import pygame
import random
from pygame.locals import *

from helpers import get_map, display_text, create_grid, color_grid

pygame.font.init()
myfont = pygame.font.SysFont(None, 25)

pygame.init()

FPS = 59
fpsClock = pygame.time.Clock()

WINDOW_SIZE = (900, 900)
DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Inteligentna śmieciarka')
background_image = pygame.image.load("images/road_big.jpg")

grid = create_grid(get_map(random.randrange(1, 5)))
all_sprites_list, garbage_collector, houses = color_grid(grid)

garbage_amount = 0

while True:
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
        elif event.type == KEYUP:
            garbage_taken = 0
            if event.key == K_RIGHT:
                garbage_taken = garbage_collector.move_right()
            elif event.key == K_LEFT:
                garbage_taken = garbage_collector.move_left()
            elif event.key == K_DOWN:
                garbage_taken = garbage_collector.move_down()
            elif event.key == K_UP:
                garbage_taken = garbage_collector.move_up()

            if garbage_collector.garbage_amount == 0:
                garbage_amount = 0
            else:
                garbage_amount += garbage_taken

    all_sprites_list.update()
    DISPLAYSURF.blit(background_image, (0, 0))
    all_sprites_list.draw(DISPLAYSURF)

    pygame.display.flip()

    fpsClock.tick(FPS)
