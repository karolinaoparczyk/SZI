import re
import random

import pygame

from models.area import Area
from models.garbage_collector import GarbageCollector
from models.house import House


def display_text(myfont, DISPLAYSURF, text, width, height):
    label = myfont.render(text, True, (255, 0, 0))
    DISPLAYSURF.blit(label, (width, height))


def get_map(number):
    with open(f'maps/MAPA{number}.csv') as map:
        columns = []
        for line in map:
            columns.append(line.split(";"))
        return columns


def render_models(map, WINDOW_SIZE):
    all_sprites_list = pygame.sprite.Group()
    grasses = []
    roads = []
    houses = []
    white_boxes = []
    garbage_dump = None
    garbage_collector_position = None
    pattern_grass = re.compile("G")
    pattern_road = re.compile("R")
    pattern_garbage_dump = re.compile("GD")
    pattern_house = re.compile("H")
    for (idx_c, column) in enumerate(map):
        white_boxes.append(Area(None, idx_c * 30, 0))
        for (idx_r, row) in enumerate(column):
            if pattern_garbage_dump.search(row):
                garbage_dump = Area('garbage_dump', idx_c * 30, idx_r * 30 + 30)
                garbage_collector_position = (idx_c * 30, idx_r * 30 + 30)
            elif pattern_grass.search(row):
                grasses.append(Area('grass', idx_c * 30, idx_r * 30 + 30))
            elif pattern_road.search(row):
                roads.append(Area('road', idx_c * 30, idx_r * 30 + 30))
            elif pattern_house.search(row):
                houses.append(House(random.randint(1, 200), idx_c * 30, idx_r * 30 + 30))
    all_sprites_list.add(white_boxes)
    all_sprites_list.add(grasses)
    all_sprites_list.add(roads)
    all_sprites_list.add(houses)
    all_sprites_list.add(garbage_dump)
    garbage_collector = GarbageCollector(450, WINDOW_SIZE, grasses, houses, garbage_dump, white_boxes,
                                         garbage_collector_position[0], garbage_collector_position[1])
    all_sprites_list.add(garbage_collector)
    return all_sprites_list, houses, garbage_collector


def auto_map(WINDOW_SIZE):
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
                roads.append(Area('road', i, j + 30))
            else:
                a = random.randrange(0, 900, 30)
                b = random.randrange(0, 900, 30)
                c = random.randrange(0, 900, 30)
                d = random.randrange(0, 900, 30)
                e = random.randrange(0, 900, 30)
                if j % 60 != 0 and (
                        j == a or j == b or j == c or j == d or j == e):  # nie budujemy domu w środku kwadratu
                    houses.append(House(100, i, j + 30))
                else:
                    grasses.append(Area('grass', i, j + 30))

    all_sprites_list.add(white_boxes)
    all_sprites_list.add(grasses)
    all_sprites_list.add(roads)
    all_sprites_list.add(houses)
    garbage_dump = Area('garbage_dump', 0, 0)
    all_sprites_list.add(garbage_dump)
    garbage_collector = GarbageCollector(250, WINDOW_SIZE, grasses, houses, garbage_dump, white_boxes, 0, 30)
    all_sprites_list.add(garbage_collector)
    return all_sprites_list, garbage_collector
