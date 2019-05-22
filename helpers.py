import re
import random
import pygame
import sys

from models.area import Area
from models.garbage_collector import *
from models.house import House

sys.setrecursionlimit(1000)


def display_text(myfont, DISPLAYSURF, text, width, height):
    label = myfont.render(text, True, (255, 0, 0))
    DISPLAYSURF.blit(label, (width, height))


def get_map(number):
    with open(f'maps/MAPA{number}.csv') as map:
        columns = []
        for line in map:
            columns.append(line.split(";"))
        return columns


def create_grid(map):
    pattern_grass = re.compile("G")
    pattern_road = re.compile("R")
    pattern_garbage_dump = re.compile("GD")
    pattern_house = re.compile("H")
    grid = []
    for (idx_c, column) in enumerate(map):
        grid.append([])
        for (idx_r, row) in enumerate(column):
            if idx_r == 0:
                grid[idx_c].append(Area(None, (idx_c, 0)))
            position = (idx_c, idx_r + 1)
            if pattern_garbage_dump.search(row):
                grid[idx_c].append(Area('garbage_dump', position))
            elif pattern_grass.search(row):
                grid[idx_c].append(Area('grass', position))
            elif pattern_road.search(row):
                grid[idx_c].append(Area('road', position))
            elif pattern_house.search(row):
                grid[idx_c].append(House(random.randint(1, 200), position))
    return grid


def color_grid(grid):
    all_sprites_list = pygame.sprite.Group()
    grasses = []
    roads = []
    houses = []
    white_boxes = []
    garbage_dump = None
    garbage_collector_position = None
    for (idx_c, column) in enumerate(grid):
        white_boxes.append(grid[idx_c])
        for (idx_r, row) in enumerate(column):
            if row.type == 'garbage_dump':
                garbage_dump = grid[idx_c][idx_r]
                garbage_collector_position = (idx_c, idx_r)
            elif row.type == 'grass':
                grasses.append(grid[idx_c][idx_r])
            elif row.type == 'road':
                roads.append(grid[idx_c][idx_r])
            elif row.type == 'house':
                houses.append(grid[idx_c][idx_r])
    all_sprites_list.add(white_boxes)
    all_sprites_list.add(grasses)
    all_sprites_list.add(roads)
    all_sprites_list.add(houses)
    all_sprites_list.add(garbage_dump)
    garbage_collector = GarbageCollector(45000, grid, garbage_collector_position)
    all_sprites_list.add(garbage_collector)
    return all_sprites_list, garbage_collector, houses


#
#
# back_path = []
# visited_roads = []
#
#
# def dfs_move(grid, position):
#     solution = []
#     check = 0
#     if grid[position[0] - 1][position[1]].type == 'road' and grid[position[0] - 1][position[1]] not in visited_roads:
#         solution.append("L")
#         back_path.append("R")
#         visited_roads.append(grid[position[0] - 1][position[1]])
#         check = 1
#     if grid[position[0]][position[1] - 1].type == 'road' and grid[position[0]][position[1] - 1] not in visited_roads and check == 0:
#         solution.append("U")
#         back_path.append("D")
#         visited_roads.append(grid[position[0]][position[1] - 1])
#         check = 1
#     if grid[position[0] + 1][position[1]].type == 'road' and grid[position[0] + 1][position[1]] not in visited_roads and check == 0:
#         solution.append("R")
#         back_path.append("L")
#         visited_roads.append(grid[position[0] + 1][position[1]])
#         check = 1
#     if grid[position[0]][position[1] + 1].type == 'road' and grid[position[0]][position[1] + 1] not in visited_roads and check == 0:
#         solution.append("D")
#         back_path.append("U")
#         visited_roads.append(grid[position[0]][position[1] + 1])
#         check = 1
#
#     if check == 0 and back_path != []:
#         solution.append(back_path.pop())
#
#     if grid[position[0] - 1][position[1]].type == 'house' and grid[position[0] - 1][position[1]].garbage_amount != 0:
#         solution.append("LH")
#     if grid[position[0]][position[1] - 1].type == 'house' and grid[position[0]][position[1] - 1].garbage_amount != 0:
#         solution.append("UH")
#     if grid[position[0] + 1][position[1]].type == 'house' and grid[position[0] + 1][position[1]].garbage_amount != 0:
#         solution.append("RH")
#     if grid[position[0]][position[1] + 1].type == 'house' and grid[position[0]][position[1] + 1].garbage_amount != 0:
#         solution.append("DH")
#
#     return solution
#

# do_another_dfs = []
#
#
# def dfs_move(grid, position, solution, count, visited_roads, back_path):
#
#     temp = []
#     active = True
#     if count > 0:
#         solution.append([solution[count - 1]])
#         visited_roads.append([visited_roads[count - 1]])
#         back_path.append([back_path[count - 1]])
#     else:
#         solution.append([])
#         visited_roads.append([])
#         back_path.append([])
#     while active:
#         check = 0
#         if grid[position[0] - 1][position[1]].type == 'road' and grid[position[0] - 1][position[1]] not in visited_roads[count]:
#             solution[count].append("L")
#             back_path[count].append("R")
#             visited_roads[count].append(grid[position[0] - 1][position[1]])
#             check = 1
#         if grid[position[0]][position[1] - 1].type == 'road' and grid[position[0]][position[1] - 1] not in visited_roads[count]:
#             if check > 0:
#                 do_another_dfs.append([position, solution, count + 1, visited_roads, back_path])
#             else:
#                 solution[count].append("U")
#                 back_path[count].append("D")
#                 visited_roads[count].append(grid[position[0]][position[1] - 1])
#                 check = 2
#         if grid[position[0] + 1][position[1]].type == 'road' and grid[position[0] + 1][position[1]] not in visited_roads[count]:
#             if check > 0:
#                 temp = solution[count]
#                 do_another_dfs.append([position, solution, count + 1, visited_roads, back_path])
#             else:
#                 solution[count].append("R")
#                 back_path[count].append("L")
#                 visited_roads[count].append(grid[position[0] + 1][position[1]])
#                 check = 3
#         if grid[position[0]][position[1] + 1].type == 'road' and grid[position[0]][position[1] + 1] not in visited_roads[count]:
#             if check > 0:
#                 do_another_dfs.append([position, solution, count + 1, visited_roads, back_path])
#             else:
#                 solution[count].append("D")
#                 back_path[count].append("U")
#                 visited_roads[count].append(grid[position[0]][position[1] + 1])
#                 check = 4
#         print(temp)
#
#         back_move = ""
#         if check == 0 and back_path[count] != []:
#             back_move = back_path[count].pop()
#             solution[count].append(back_move)
#         elif check == 0 and back_path[count] == []:
#             active = False
#
#         if check == 1 or back_move == "L":
#             position = [position[0] - 1, position[1]]
#         if check == 2 or back_move == "U":
#             position = [position[0], position[1] - 1]
#         if check == 3 or back_move == "R":
#             position = [position[0] + 1, position[1]]
#         if check == 4 or back_move == "D":
#             position = [position[0], position[1] + 1]
#
#         find_houses(grid, position, solution[count])
#
#     if do_another_dfs:
#         temp = do_another_dfs.pop()
#         # for i in range(5):
#         #     print(temp[i])
#         dfs_move(grid, temp[0], temp[1], temp[2], temp[3], temp[4])
#     return solution
#
#
# def find_houses(grid, position, solution):
#
#     if grid[position[0] - 1][position[1]].type == 'house' and grid[position[0] - 1][position[1]].garbage_amount != 0:
#         solution.append("LH")
#     if grid[position[0]][position[1] - 1].type == 'house' and grid[position[0]][position[1] - 1].garbage_amount != 0:
#         solution.append("UH")
#     if grid[position[0] + 1][position[1]].type == 'house' and grid[position[0] + 1][position[1]].garbage_amount != 0:
#         solution.append("RH")
#     if grid[position[0]][position[1] + 1].type == 'house' and grid[position[0]][position[1] + 1].garbage_amount != 0:
#         solution.append("DH")
#
#
# def dfs_check(grid, position, solution):
#     path = [find_houses(grid, position, solution)]
#
#     if path:
#         moves = back_path[::-1]
#         for move in moves[1:]:
#             if move == "L":
#                 path.append("R")
#             elif move == "U":
#                 path.append("D")
#             elif move == "R":
#                 path.append("L")
#             elif move == "D":
#                 path.append("U")
#         for move in back_path[:-1]:
#             path.append(move)
#     return path
#

# def dfs_move(grid, position, solution, last_move, count):
#
#     if grid[position[0] - 1][position[1]].type == 'road' and [position[0] - 1, position[1]] != last_move:
#         last_move = position
#         if find_houses(grid, position, solution):
#             solution.append(find_houses(grid, position, solution))
#         solution.append("L")
#         back_path.append("R")
#         position = [position[0] - 1, position[1]]
#         dfs_move(grid, position, solution, last_move, count)
#     if grid[position[0]][position[1] - 1].type == 'road' and [position[0], position[1] - 1] != last_move:
#         last_move = position
#         if find_houses(grid, position, solution):
#             solution.append(find_houses(grid, position, solution))
#         solution.append("U")
#         back_path.append("D")
#         position = [position[0], position[1] - 1]
#         dfs_move(grid, position, solution, last_move, count)
#     if grid[position[0] + 1][position[1]].type == 'road' and [position[0] + 1, position[1]] != last_move:
#         last_move = position
#         if find_houses(grid, position, solution):
#             solution.append(find_houses(grid, position, solution))
#         solution.append("R")
#         back_path.append("L")
#         position = [position[0] + 1, position[1]]
#         dfs_move(grid, position, solution, last_move, count)
#     if grid[position[0]][position[1] + 1].type == 'road' and [position[0], position[1] + 1] != last_move:
#         last_move = position
#         if find_houses(grid, position, solution):
#             solution.append(find_houses(grid, position, solution))
#         solution.append("D")
#         back_path.append("U")
#         position = [position[0], position[1] + 1]
#         dfs_move(grid, position, solution, last_move, count)
#
#     return solution


# Sprawdż pola wokół siebie (nie bierz pod uwagę tego z którego przyszedłeś)
# "sytuacja na końcu ślepiej uliczki, opcjonalnie można to zrobić"
# jeżeli skryżowanie to je zapisz do listy
# jeżeli nie to wykonaj możliwą akcję(zebranie śmieci, ruch drogą)
# jeżeli nie starczy ci miejsca, wróć na GD, po GD wróć do miejsca gdzie byłeś i zbierz śmieci z domu
# while true:
#     jeżeli doszedłeś do końca to wróć do ostatniego skrzyżowania i wybierz 2 opcję
#     jeżeli wróciłeś do punktu początkowego to zmień na false

solutions = []


def find_houses(grid):
    count = 0
    for i in range(30):
        for j in range(30):
            if grid[i][j].type == 'house':
                count += 1
    return count


def dfs_move(grid, position, last_move, visited_houses, counter, solution, count):
    positions = [[position[0] - 1, position[1]], [position[0], position[1] - 1], [position[0] + 1, position[1]],
                 [position[0], position[1] + 1]]
    house_move = ['LH', 'UH', 'RH', 'DH']
    move = ['L', 'U', 'R', 'D']

    if len(solution) > 1000:
        return 0
    if count == 0:
        solutions.append(solution[:])
        solution.clear()
        return 0

    for j in range(len(positions)):
        if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] not in visited_houses:
            count -= 1
            solution.append(house_move[j])
            visited_houses.append(positions[j])
            dfs_move(grid, position, last_move, visited_houses[:], counter, solution[:], count)

    for i in range(len(positions)):
        if grid[positions[i][0]][positions[i][1]].type == 'road' and positions[i] != last_move:
            last_move = position
            solution.append(move[i])
            dfs_move(grid, positions[i], last_move, visited_houses[:], counter, solution[:], count)

    for z in range(len(positions)):
        if grid[positions[z][0]][positions[z][1]].type == 'garbage_dump':
            solutions.append(solution[:])
            return 0

    return 0


def check_solutions(count):
    house_move = ['LH', 'UH', 'RH', 'DH']
    temp = len(solutions) - 1
    while temp >= 0:
        counter = 0
        for j in solutions[temp]:
            if j in house_move:
                counter += 1
        if counter != count:
            solutions.pop(temp)
        temp -= 1

# DFS
# rekurencją
# węzłem drzewa konkrenta sytuacja na planszy
# gałęziamy (możliwościami) jest to wszystko, co może zrobic agent
# zasada: nie powtarzamy ostatniej operacji
# jak może coś odwiedzić (zebrać śmieci), to niech to zrobi
# ucinanie ścieżki, jeśli robi zbyt dużo operacji (zapętlenie)

# przyjmuje ciąd dotyczhczasowych operacji
# dfs_find(GRID, CURRENT_OPERATIONS)
# 1. sprawdź czy koniec (czy zadanie zostało wykonane/czy wszystkie punkty zostały wykonane)
# a) TAK
#   ..globalna SOLUTIONS = []..
#   SOLUTIONS.append(current_operations)
# b) NIE
#   Sprawdź możliwości
#   ..operacje na gridie.. funkcja dodatkowa - przyjmuje grida i operację, zwraca zmienionego grida
#   .. zwiększamy liste operacji..
#   dfs_find(zmieniony grid, zwiekszona lista operacji)


# vowpal_wabbit
# getting started/dependencies/building/installing/tutorial
# ledna linia = jedna komórka danych:
# 0 lub 1 (wymieniać/nie wymieniaćdachu) cena: 123 metraż: 123 rok(string)
# (numer kroku/decyzja) 3 (stan planszy: lista komórek w bezpośrednim otoczeniu agenta oraz lista komórek w otoczeniu
# agenta w drugim rzędzie) cellleft:1 cellright:1 cellup:0
# po instalacji uruchomienie: vw
# zapis: house.model
# mogą być dwie osoby


# svm skleam maszyny wektorów nośnych (support vector machines)
# scikit-larn.org
# decision trees
# logistic regresion
