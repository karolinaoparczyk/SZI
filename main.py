import pygame
import sys
from pygame.locals import *

from models.area import Area
from models.garbage_collector import GarbageCollector

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

WINDOW_SIZE = (900, 900)
DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Inteligentna śmieciarka')
WHITE = (255, 255, 255)
WIDTH = 30
HEIGHT = 30
MARGIN = 5
background_image = pygame.image.load("images/road_big.jpg")

board = []

for i in range(30):
    board.append([])

all_sprites_list = pygame.sprite.Group()

grasses = []
roads = []
for i in range(0, 900, 30):
    for j in range(0, 900, 30):
        if i == 0 and j == 0:
            pass
        elif i % 8 == 0 or j % 8 == 0:
            roads.append(Area('road', i, j))
        else:
            grasses.append(Area('grass', i, j))


# board[i].append(grasses)
all_sprites_list.add(grasses)
all_sprites_list.add(roads)
garbage_collector = GarbageCollector(1000, WINDOW_SIZE, grasses, 0, 0)
all_sprites_list.add(garbage_collector)

# DISPLAYSURF.blit(grass.image, (0, 0))

while True:  # the main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                garbage_collector.move_right()
            elif event.key == K_LEFT:
                garbage_collector.move_left()
            elif event.key == K_DOWN:
                garbage_collector.move_down()
            elif event.key == K_UP:
                garbage_collector.move_up()
    all_sprites_list.update()
    DISPLAYSURF.blit(background_image, (0, 0))
    all_sprites_list.draw(DISPLAYSURF)

    pygame.display.flip()

    fpsClock.tick(FPS)
