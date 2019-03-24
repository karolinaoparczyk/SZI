import pygame
import sys
import random
import time
from pygame.locals import *

from models.area import Area
from models.garbage_collector import GarbageCollector
from models.house import House


pygame.font.init()
myfont = pygame.font.SysFont(None, 130)

def display_text(text):
    label = myfont.render(text, True, (255, 255, 255), (255, 0, 0))
    textrect = label.get_rect()
    textrect.centerx = DISPLAYSURF.get_rect().centerx
    textrect.centery = DISPLAYSURF.get_rect().centery
    DISPLAYSURF.blit(label, textrect)
    pygame.display.update()
    time.sleep(1)

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

WINDOW_SIZE = (900, 900)
DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Inteligentna śmieciarka')
background_image = pygame.image.load("images/road_big.jpg")

all_sprites_list = pygame.sprite.Group()

grasses = []
roads = []
houses = []
for i in range(0, 900, 30):
    for j in range(0, 900, 30):
        if i == 0 and j == 0:
            pass
        elif i % 8 == 0 or j % 8 == 0:
            roads.append(Area('road', i, j))
        else:
            a = random.randrange(0, 900, 30)
            b = random.randrange(0, 900, 30)
            c = random.randrange(0, 900, 30)
            d = random.randrange(0, 900, 30)
            e = random.randrange(0, 900, 30)
            if j % 60 != 0 and (j == a or j == b or j == c or j == d or j == e):  # nie budujemy domu w środku kwadratu
                houses.append(House(100, i, j))
            else:
                grasses.append(Area('grass', i, j))

all_sprites_list.add(grasses)
all_sprites_list.add(roads)
all_sprites_list.add(houses)
garbage_dump = Area('garbage_dump', 0, 0)
all_sprites_list.add(garbage_dump)
garbage_collector = GarbageCollector(250, WINDOW_SIZE, grasses, houses, garbage_dump,  0, 0)
all_sprites_list.add(garbage_collector)

while True:
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
            if garbage_taken > 0:
                display_text("Zabrano: {}".format(garbage_taken))

    all_sprites_list.update()
    DISPLAYSURF.blit(background_image, (0, 0))
    all_sprites_list.draw(DISPLAYSURF)

    pygame.display.flip()

    fpsClock.tick(FPS)

