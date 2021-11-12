from random import randint
from random import choice
from settings import CELL


class BoardException(Exception):
    pass


class BoardCheckCoordinateException(BoardException):
    def __str__(self):
        return 'Введите корректные данные'


class BoardAllreadyShotException(BoardException):
    def __str__(self):
        return 'Вы уже сюда стреляли'


class Ship:
    def __init__(self, id_name='comp', size=6, visible_ship=True):
        self.size = size if 6 <= size <= 9 else 6
        self.table = [[CELL] * self.size for _ in range(self.size)]
        self.id_name = 'comp' if id_name not in ('comp', 'user') else id_name
        self.error = False
        self.visible_ship = visible_ship  # True-скрыть позиции компьютера  False-показать позиции компьютера
        self.level = {6: [3, 2, 2, 1, 1, 1, 1],
                      7: [3, 2, 2, 2, 1, 1, 1, 1],
                      8: [3, 3, 2, 2, 2, 1, 1, 1, 1],
                      9: [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]}
        self.ships = self.level[self.size]
        # self.ships = [3, 2, 2, 1, 1, 1, 1]
        self.free_dot = [(i, j) for i in range(self.size) for j in range(self.size)]  # список свободных точек на поле
        self.cache = []
        self.near_dots = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    def ship_location(self):
        for ship_len in self.ships:
            flag = False
            count = 0
            while not flag:
                horiz_vert = randint(0, 1)  # 0-horizontal, 1-vertical
                while 1:
                    row, column = choice(self.free_dot)
                    if horiz_vert and (row + ship_len) <= (self.size - 1):
                        break
                    elif horiz_vert == 0 and (column + ship_len) <= (self.size - 1):
                        break
                flag = self.check(row, column, horiz_vert, ship_len)
                if flag:  # vertical location
                    for i in range(ship_len):
                        if horiz_vert == 1:
                            self.table[row + i][column] = '■'
                            self.free_dot.remove((row + i, column))
                        elif horiz_vert == 0:
                            self.table[row][column + i] = '■'
                            self.free_dot.remove((row, column + i))
                count += 1
                if count > 100:
                    self.error = True
                    break

    def print_table(self):
        # flag = False # True-скрыть позиции компьютера  False-показать позиции компьютера
        if self.id_name == 'comp':
            name = 'Поле компьютера'
        else:
            name = 'Поле игрока'
        print(name)
        print('  |', ' | '.join([str(i) for i in range(1, self.size + 1)]), '|')
        for i in range(self.size):
            print(i + 1, '| ', end='')
            if self.visible_ship and self.id_name == 'comp':
                print(*[CELL if el == '■' else el for el in self.table[i]], sep=' | ', end='')
            else:
                print(*self.table[i], sep=' | ', end='')
            print(' |')

    def check(self, row, column, horiz_vert=1, ship=1):
        # horiz_vert: 1 - vert, 0 - horiz
        if horiz_vert == 0:
            ship = 1
        for el in range(row - 1, row + ship + 1):
            # if 0 <= el <= 5:
            if 0 <= el <= (self.size - 1):
                if horiz_vert:
                    if '■' in self.table[el][0 if column == 0 else column - 1: self.size if column == (self.size - 1) else column + 2]:
                        return False
                else:
                    if '■' in self.table[el][0 if column == 0 else column - 1: self.size if column == (self.size - 2) else column + 3]:
                        return False
        return True

    def set_attack(self, coordinate: str):
        if len(coordinate) == 2 and coordinate.isdigit() \
                and 1 <= int(coordinate[:1]) <= self.size and 1 <= int(coordinate[1:]) <= self.size:
            row = int(coordinate[:1]) - 1
            column = int(coordinate[1:]) - 1
            if self.table[row][column] == CELL:
                self.table[row][column] = 'T'
                self.free_dot.remove((row, column))
                return 'Промах'
            elif self.table[row][column] == '■':
                self.table[row][column] = 'X'
                return 'Вы попали'
            elif self.table[row][column] in ('T', 'X'):
                return 'Вы уже сюда стреляли'
        else:
            return 'error'

    def check_end_game(self):
        for row in self.table:
            if '■' in row:
                return False  # continue game
        return True  # stop game

    def add_dot_to_cache(self, row, column):
        for x, y in self.near_dots:
            self.cache.append((row + x, column + y))

    def get_dot_cache(self):
        return self.cache.pop(0)


class Game:
    def __init__(self, size, visible_ship=True):
        self.size = size
        self.visible_ship = visible_ship
        self.comp = Ship(visible_ship=self.visible_ship, size=self.size)
        self.user = Ship(id_name='user', size=self.size)

    def locate(self):
        self.comp.ship_location()
        self.user.ship_location()
        while self.comp.error or self.user.error:
            self.comp = Ship()
            self.comp.ship_location()
            self.user = Ship('user')
            self.user.ship_location()

    def loop(self):
        game_over = False
        while not game_over:
            while not game_over:  # user step
                try:
                    self.comp.print_table()
                    self.user.print_table()
                    coordinate = input('Ваш ход. Выберите номер строки и колонки без пробела:')
                    answer = self.comp.set_attack(coordinate)
                    if answer == 'Промах':
                        print(answer)
                        break
                    elif answer == 'Вы попали':
                        print(answer)
                        game_over = self.comp.check_end_game()
                        if game_over:
                            print('Вы выиграли')
                            break
                    elif answer == 'Вы уже сюда стреляли':
                        raise BoardAllreadyShotException()
                    elif answer == 'error':
                        raise BoardCheckCoordinateException()
                except BoardException as e:
                    print(e)

            while not game_over:  # comp step
                if len(self.comp.cache) == 0:
                    row, column = choice(self.comp.free_dot)
                else:
                    row, column = self.comp.get_dot_cache()
                answer = self.user.set_attack(f'{row}{column}')
                if answer == 'Промах':
                    print(f'Координаты {row, column}. {answer}')
                    break
                elif answer == 'Вы попали':
                    print(f'Координаты {row, column}. Компьютер попал.')
                    game_over = self.user.check_end_game()
                    if len(self.comp.cache) == 0:
                        self.comp.add_dot_to_cache(row, column)  # init cache
                        print(self.comp.cache)
                    if game_over:
                        print('Компьютер выиграл')
                        break
                    self.comp.print_table()
                    self.user.print_table()

    def greeting(self):
        print('*' * 25)
        print('****** Морской бой ******')
        print('*' * 25)

    def start(self):
        self.greeting()
        self.locate()
        self.loop()


g = Game(size=9)
g.start()
