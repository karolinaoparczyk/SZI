import pygame
import sys
import random
from pygame.locals import *

from models.area import Area
from models.garbage_collector import GarbageCollector
from models.house import House


pygame.font.init()
myfont = pygame.font.SysFont(None, 25)


def display_text(text):
    label = myfont.render(text, True, (255, 0, 0))
    DISPLAYSURF.blit(label, (750, 0))


pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

WINDOW_SIZE = (900, 900)
DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Inteligentna śmieciarka')
background_image = pygame.image.load("images/road_big.jpg")

all_sprites_list = pygame.sprite.Group()

white_boxes = []
grasses = []
roads = []
houses = []
for i in range(0, 930, 30):
    for j in range(0, 930, 30):
        if i == 0 and j == 0:
            pass
        elif j == 0:
            white_boxes.append(Area(None, i, j))
        elif i % 8 == 0 or j % 8 == 0:
            roads.append(Area('road', i, j+30))
        else:
            a = random.randrange(0, 900, 30)
            b = random.randrange(0, 900, 30)
            c = random.randrange(0, 900, 30)
            d = random.randrange(0, 900, 30)
            e = random.randrange(0, 900, 30)
            if j % 60 != 0 and (j == a or j == b or j == c or j == d or j == e):  # nie budujemy domu w środku kwadratu
                houses.append(House(100, i, j+30))
            else:
                grasses.append(Area('grass', i, j+30))

all_sprites_list.add(white_boxes)
all_sprites_list.add(grasses)
all_sprites_list.add(roads)
all_sprites_list.add(houses)
garbage_dump = Area('garbage_dump', 0, 0)
all_sprites_list.add(garbage_dump)
garbage_collector = GarbageCollector(250, WINDOW_SIZE, grasses, houses, garbage_dump, white_boxes,  0, 30)
all_sprites_list.add(garbage_collector)

garbage_amount = 0

while True:
    display_text("Ilość śmieci: {}".format(garbage_amount))
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

