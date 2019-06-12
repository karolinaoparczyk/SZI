import re
import random
import sys
import os
from sklearn import tree, linear_model
from sklearn.preprocessing import StandardScaler

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

# 0 - grass
# 1 - road
# 2 - house
# 3 - garbage dump
# possibilities[0] - left
# possibilities[1] - up
# possibilities[2] - right
# possibilities[3] - down


def get_data_tree_from_file():
    choices_train = []
    choices_test = []
    possibilities_train = []
    possibilities_test = []
    i = 5600
    with open(f'dataset.txt') as data:
        for line in data:
            if i > 0:
                choice = int(line[0])
                choices_train.append(choice)
                moves = list(map(int, line[2:-1].split(","))) #na końcu usuwamy znak nowej lini /n
                possibilities_train.append(moves)
                i -= 1
            else:
                choice = int(line[0])
                choices_test.append(choice)
                moves = list(map(int, line[2:-1].split(",")))  # na końcu usuwamy znak nowej lini /n
                possibilities_test.append(moves)
    return choices_train, choices_test, possibilities_train, possibilities_test


def train_decision_tree(choices_train, possibilities_train):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(possibilities_train, choices_train)
    return clf


# possible_choices = [ , , , ]
# possible_choices_list = [[ , , , ]]
# decision_list[0] = []


#to dataset from map
def get_tree_decision(clf, possible_choices):
    possible_choices_list = [possible_choices]
    decision_list = clf.predict(possible_choices_list)
    return decision_list[0]


#to dataset from dfs
def get_tree_decision_test(clf, possible_choices, expected_choices):
    decision_list = clf.predict(possible_choices)
    write_tree_output_to_file(expected_choices, decision_list, 'decision_tree_output')
    return decision_list[0]


def train_linear_regression(X_train, y_train):
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)
    return regr


# possible_choices_list [[ , , , ]]
# decision []
#to dataset from map
def get_logistic_regression_decision(regr, possible_choices):
    possible_choices_list = [possible_choices]
    decision = regr.predict(possible_choices_list)
    return decision


#to dataset from dfs
def get_linear_regression_decision_test(regr, possible_choices, expected_choices):
    decisions = regr.predict(possible_choices)
    write_tree_output_to_file(expected_choices, decisions, 'linear_regression_output')
    return decisions


def a_i_move(grid, position, clf, regr, count):
    solution = []
    visited_houses = []
    house_move = ['LH', 'UH', 'RH', 'DH']
    move = ['L', 'U', 'R', 'D']
    move_id = ['6', '7', '8', '9']
    last_position = position

    for i in range(1000):
        positions_for_move = [[position[0] - 1, position[1]], [position[0], position[1] - 1], [position[0] + 1, position[1]], [position[0], position[1] + 1]]

        positions = []
        e = -2
        for q in range(5):
            r = -2
            for w in range(5):
                if e == 0 and r == 0:
                    r += 1
                    continue
                positions.append([position[0] + e, position[1] + r])
                r += 1
            e += 1

        check_possible_moves = 0
        for w in range(len(positions_for_move)):
            if (grid[positions_for_move[w][0]][positions_for_move[w][1]].type == 'road' and positions_for_move[w] != last_position) or (grid[positions_for_move[w][0]][positions_for_move[w][1]].type == 'house' and positions_for_move[w] not in visited_houses):
                check_possible_moves += 1
        if check_possible_moves == 0:
            for w in range(len(positions_for_move)):
                if grid[positions_for_move[w][0]][positions_for_move[w][1]].type == 'road' and positions_for_move[w] == last_position:
                    last_position = position

        possible_moves = []
        for j in range(len(positions)):
            if grid[positions[j][0]][positions[j][1]].type == 'grass':
                possible_moves.append('0')
            if grid[positions[j][0]][positions[j][1]].type == 'road' and positions[j] != last_position:
                possible_moves.append('1')
            if grid[positions[j][0]][positions[j][1]].type == 'road' and positions[j] == last_position:
                possible_moves.append('5')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] not in visited_houses:
                possible_moves.append('2')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] in visited_houses:
                possible_moves.append('0')
            if grid[positions[j][0]][positions[j][1]].type == 'garbage_dump':
                possible_moves.append('3')

        ai_move = get_tree_decision(clf, possible_moves)
        check = 0
        while check == 0:
            for j in range(len(move)):
                if int(round(ai_move)) == int(move_id[j]):
                    if grid[positions_for_move[j][0]][positions_for_move[j][1]].type == 'house':
                        if positions_for_move[j] not in visited_houses:
                            count -= 1
                        solution.append(house_move[j])
                        last_position = position
                        visited_houses.append(positions_for_move[j])
                        check = 1
                    if grid[positions_for_move[j][0]][positions_for_move[j][1]].type == 'road':
                        last_position = position
                        solution.append(move[j])
                        position = positions_for_move[j]
                        check = 1
            ai_move = random.randint(6, 9)
        if count == 0:
            return solution
    return solution

def logistic_regression_move(grid, position, regr, count):
    solution = []
    visited_houses = []
    house_move = ['LH', 'UH', 'RH', 'DH']
    move = ['L', 'U', 'R', 'D']
    move_id = ['6', '7', '8', '9']
    last_position = position

    for i in range(1000):
        positions_for_move = [[position[0] - 1, position[1]], [position[0], position[1] - 1], [position[0] + 1, position[1]], [position[0], position[1] + 1]]

        positions = []
        e = -2
        for q in range(5):
            r = -2
            for w in range(5):
                if e == 0 and r == 0:
                    r += 1
                    continue
                positions.append([position[0] + e, position[1] + r])
                r += 1
            e += 1

        possible_moves = []
        for j in range(len(positions)):
            if grid[positions[j][0]][positions[j][1]].type == 'grass':
                possible_moves.append('0')
            if grid[positions[j][0]][positions[j][1]].type == 'road' and positions[j] != last_position:
                possible_moves.append('1')
            if grid[positions[j][0]][positions[j][1]].type == 'road' and positions[j] == last_position:
                possible_moves.append('5')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] not in visited_houses:
                possible_moves.append('2')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] in visited_houses:
                possible_moves.append('0')
            if grid[positions[j][0]][positions[j][1]].type == 'garbage_dump':
                possible_moves.append('3')

        for i in range(4):
            if grid[positions_for_move[i][0]][positions_for_move[i][1]].type == 'house' \
                    and positions_for_move[i] not in visited_houses:
                solution.append(house_move[i])
                visited_houses.append(positions_for_move[i])
                last_position = position
                count -= 1

        ai_move = get_logistic_regression_decision(regr, list(map(int, possible_moves)))
        check = 0
        while check == 0:
            for j in range(len(move)):
                if int(ai_move) == int(move_id[j]):
                    if grid[positions_for_move[j][0]][positions_for_move[j][1]].type == 'road':
                        last_position = position
                        solution.append(move[j])
                        position = positions_for_move[j]
                        check = 1
            ai_move = random.randint(6, 9)
        if count == 0:
            return solution
    return solution


def write_tree_output_to_file(expected_choices, decisions, filename):
    with open('{}.txt'.format(filename), 'w') as data:
        data.write('expected_choice, decision\n')
        for (choice_test, decision) in zip(expected_choices, decisions):
            data.write(str(choice_test) + ',' + str(decision) + '\n')


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


solutions = []


def find_houses(grid):
    count = 0
    for i in range(30):
        for j in range(30):
            if grid[i][j].type == 'house':
                count += 1
    return count


def dfs_move(grid, position, visited_houses, counter, solution, count, temp):
    positions = [[position[0] - 1, position[1]], [position[0], position[1] - 1], [position[0] + 1, position[1]],
                 [position[0], position[1] + 1]]
    house_move = ['LH', 'UH', 'RH', 'DH']
    move = ['L', 'U', 'R', 'D']
    last_move = ['R', 'D', 'L', 'U']

    counter += 1
    if counter > 130:
        if count != 0:
            solution.pop()
            return 0
        return 0
    if count == 0:
        solutions.append(solution[:])
        return 0

    if temp != 'start':
        solution.append(temp)

    for j in range(len(positions)):
        if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] not in visited_houses:
            count -= 1
            solution.append(house_move[j])
            visited_houses.append(positions[j])
            dfs_move(grid, position, visited_houses[:], counter, solution[:], count, temp)

    for i in range(len(positions)):
        if grid[positions[i][0]][positions[i][1]].type == 'road' and last_move[i] != solution[-1]:
            temp = move[i]
            dfs_move(grid, positions[i], visited_houses[:], counter, solution[:], count, temp)

    return 0


def bfs_move(grid, position, count):
    house_move = ['LH', 'UH', 'RH', 'DH']
    move = ['L', 'U', 'R', 'D']
    last_move = ['R', 'D', 'L', 'U']
    solution = [['test']]
    remaining_houses = [count]
    visited_houses = [[]]
    bfs_position = [position]
    counter = 1

    while True:
        for j in range(counter):
            temp_solutions = []
            positions = [[bfs_position[j][0] - 1, bfs_position[j][1]], [bfs_position[j][0], bfs_position[j][1] - 1], [bfs_position[j][0] + 1, bfs_position[j][1]], [bfs_position[j][0], bfs_position[j][1] + 1]]

            for i in range(len(positions)):
                if grid[positions[i][0]][positions[i][1]].type == 'house' and positions[i] not in visited_houses[j]:
                    visited_houses[j].append(positions[i])
                    solution[j].append(house_move[i])
                    remaining_houses[j] -= 1

            if remaining_houses[j] == 0:
                return solution[j]

            check = 0
            for i in range(len(positions)):
                if grid[positions[i][0]][positions[i][1]].type == 'road' and last_move[i] != solution[j][-1]:
                    check += 1
                    temp_solutions.append(move[i])

            for i in range(check - 1):
                remaining_houses.append(remaining_houses[j])
                solution.append(solution[j][:])
                bfs_position.append(bfs_position[j][:])
                visited_houses.append(visited_houses[j][:])

            for i in range(check):
                if i == 0:
                    solution[j].append(temp_solutions.pop(0))
                    for q in range(len(positions)):
                        if solution[j][-1] == move[q]:
                            bfs_position[j] = positions[q]
                else:
                    solution[counter].append(temp_solutions.pop(0))
                    for q in range(len(positions)):
                        if solution[counter][-1] == move[q]:
                            bfs_position[counter] = positions[q]
                    counter += 1


def create_dataset(grid, solution, position, dataset_by):
    f = open('dataset.txt', 'a')
    move = ['L', 'U', 'R', 'D']
    house_move = ['LH', 'UH', 'RH', 'DH']
    visited_houses = []
    last_position = position
    for i in solution:
        if i == 'test':
            continue

        positions_for_move = [[position[0] - 1, position[1]], [position[0], position[1] - 1], [position[0] + 1, position[1]], [position[0], position[1] + 1]]

        positions = []
        e = -2
        for q in range(5):
            r = -2
            for w in range(5):
                if e == 0 and r == 0:
                    r += 1
                    continue
                positions.append([position[0] + e, position[1] + r])
                r += 1
            e += 1

        temp = []
        if i == 'LH' or i == 'L':
            temp.append('6')
        if i == 'UH' or i == 'U':
            temp.append('7')
        if i == 'RH' or i == 'R':
            temp.append('8')
        if i == 'DH' or i == 'D':
            temp.append('9')
        for j in range(len(positions)):
            if grid[positions[j][0]][positions[j][1]].type == 'grass':
                temp.append('0')
            if grid[positions[j][0]][positions[j][1]].type == 'road' and positions[j] != last_position:
                temp.append('1')
            if grid[positions[j][0]][positions[j][1]].type == 'road' and positions[j] == last_position:
                temp.append('5')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] not in visited_houses:
                temp.append('2')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] in visited_houses:
                temp.append('4')
            if grid[positions[j][0]][positions[j][1]].type == 'garbage_dump':
                temp.append('3')
        temp = ', '.join(temp)
        f.write(f'{temp}\n')
        for j in range(len(move)):
            if move[j] == i:
                last_position = position
                position = positions_for_move[j]
            if house_move[j] == i:
                visited_houses.append(positions_for_move[j])
    f.close()


def create_dataset_for_rabbit(grid, solution, position):
    f = open('rabbit_dataset.txt', 'a')
    move = ['L', 'U', 'R', 'D']
    house_move = ['LH', 'UH', 'RH', 'DH']
    visited_houses = []
    last_position = position
    for i in solution:
        if i == 'test':
            continue

        positions_for_move = [[position[0] - 1, position[1]], [position[0], position[1] - 1],
                              [position[0] + 1, position[1]], [position[0], position[1] + 1]]

        positions = []
        e = -2
        for q in range(5):
            r = -2
            for w in range(5):
                if e == 0 and r == 0:
                    r += 1
                    continue
                positions.append([position[0] + e, position[1] + r])
                r += 1
            e += 1

        temp = []
        if i == 'LH' or i == 'L':
            temp.append('6')
        if i == 'UH' or i == 'U':
            temp.append('7')
        if i == 'RH' or i == 'R':
            temp.append('8')
        if i == 'DH' or i == 'D':
            temp.append('9')
        for j in range(len(positions)):
            if grid[positions[j][0]][positions[j][1]].type == 'grass':
                temp.append('0')
            if grid[positions[j][0]][positions[j][1]].type == 'road' and positions[j] != last_position:
                temp.append('20')
            if grid[positions[j][0]][positions[j][1]].type == 'road' and positions[j] == last_position:
                temp.append('2')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] not in visited_houses:
                temp.append('35')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] in visited_houses:
                temp.append('4')
            if grid[positions[j][0]][positions[j][1]].type == 'garbage_dump':
                temp.append('1')

        s = ""
        s = s + temp[0] + " | 1x1:." + temp[1] + " 1x2:." + temp[2]
        s = s + " 1x3:." + temp[3] + " 1x4:." + temp[4]
        s = s + " 1x5:." + temp[5]

        s = s + " 2x1:." + temp[6] + " 2x2:." + temp[7]
        s = s + " 2x3:." + temp[8] + " 2x4:." + temp[9]
        s = s + " 2x5:." + temp[10]

        s = s + " 3x1:." + temp[11] + " 3x2:." + temp[12]
        s = s + " 3x4:." + temp[13] + " 3x5:." + temp[14]

        s = s + " 4x1:." + temp[15] + " 4x2:." + temp[16]
        s = s + " 4x3:." + temp[17] + " 4x4:." + temp[18]
        s = s + " 4x5:." + temp[19]

        s = s + " 5x1:." + temp[20] + " 5x2:." + temp[21]
        s = s + " 5x3:." + temp[22] + " 5x4:." + temp[23]
        s = s + " 5x5:." + temp[24]

        f.write(f'{s}\n')

        for j in range(len(move)):
            if move[j] == i:
                last_position = position
                position = positions_for_move[j]
            if house_move[j] == i:
                visited_houses.append(positions_for_move[j])
    f.close()


def create_rabbit_model():
    os.system('vw {} -c --passes 25 -f {}'.format(os.path.join('.', 'rabbit_dataset.txt'), os.path.join('.', 'rabbit.model')))


def move_rabbit(grid, position, count):
    solution = []
    visited_houses = []
    house_move = ['LH', 'UH', 'RH', 'DH']
    move = ['L', 'U', 'R', 'D']
    move_id = ['6', '7', '8', '9']
    last_position = position

    for i in range(1000):
        positions_for_move = [[position[0] - 1, position[1]], [position[0], position[1] - 1],
                              [position[0] + 1, position[1]], [position[0], position[1] + 1]]

        positions = []
        e = -2
        for q in range(5):
            r = -2
            for w in range(5):
                if e == 0 and r == 0:
                    r += 1
                    continue
                positions.append([position[0] + e, position[1] + r])
                r += 1
            e += 1

        possible_moves = []
        for j in range(len(positions)):
            if grid[positions[j][0]][positions[j][1]].type == 'grass':
                possible_moves.append('0')
            if grid[positions[j][0]][positions[j][1]].type == 'road' and positions[j] != last_position:
                possible_moves.append('20')
            if grid[positions[j][0]][positions[j][1]].type == 'road' and positions[j] == last_position:
                possible_moves.append('2')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] not in visited_houses:
                possible_moves.append('35')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] in visited_houses:
                possible_moves.append('4')
            if grid[positions[j][0]][positions[j][1]].type == 'garbage_dump':
                possible_moves.append('1')

        s = ""
        s = s + " | 1x1:." + possible_moves[0][0] + " 1x2:." + possible_moves[1][0]
        s = s + " 1x3:." + possible_moves[2][0] + " 1x4:." + possible_moves[3][0]
        s = s + " 1x5:." + possible_moves[4][0]

        s = s + " 2x1:." + possible_moves[5][0] + " 2x2:." + possible_moves[6][0]
        s = s + " 2x3:." + possible_moves[7][0] + " 2x4:." + possible_moves[8][0]
        s = s + " 2x5:." + possible_moves[9][0]

        s = s + " 3x1:." + possible_moves[10][0] + " 3x2:." + possible_moves[11][0]
        s = s + " 3x4:." + possible_moves[12][0] + " 3x5:." + possible_moves[13][0]

        s = s + " 4x1:." + possible_moves[14][0] + " 4x2:." + possible_moves[15][0]
        s = s + " 4x3:." + possible_moves[16][0] + " 4x4:." + possible_moves[17][0]
        s = s + " 4x5:." + possible_moves[18][0]

        s = s + " 5x1:." + possible_moves[19][0] + " 5x2:." + possible_moves[20][0]
        s = s + " 5x3:." + possible_moves[21][0] + " 5x4:." + possible_moves[22][0]
        s = s + " 5x5:." + possible_moves[23][0]

        f = open('input.txt', 'w')
        f.write(f'{s}')
        f.close()

        os.system('vw -i {} -t {} -p {} --quiet'.format(os.path.join('.', 'rabbit.model'),
                                                        os.path.join('.', 'input.txt'), os.path.join('.', 'output.txt')))

        with open('output.txt', 'r') as myfile:
            rabbit_move = int(str(myfile.readline())[0])
            print(f"{rabbit_move}")

        # linear_regression_move = get_linear_regression_decision(regr, list(map(int, possible_moves)))
        for j in range(len(move)):
            if int(rabbit_move) == int(move_id[j]):
                if grid[positions_for_move[j][0]][positions_for_move[j][1]].type == 'house':
                    if positions_for_move[j] not in visited_houses:
                        count -= 1
                    solution.append(house_move[j])
                    visited_houses.append(positions_for_move[j])
                if grid[positions_for_move[j][0]][positions_for_move[j][1]].type == 'road':
                    last_position = position
                    solution.append(move[j])
                    position = positions_for_move[j]
        if count == 0:
            return solution
    return solution


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
