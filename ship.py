from random import randint
from settings import FLAG, CELL


class Ship:
    def __init__(self, id_name='comp'):
        self.table = [[CELL] * 6 for _ in range(6)]
        self.id_name = 'comp' if id_name not in ('comp', 'user') else id_name
        self.error = False

    def ship_location(self):
        # размещаем один 3х палубный
        while 1:
            horiz_vert = randint(0, 1)  # 0-horizontal, 1-vertical
            if horiz_vert:  # vertical location
                row, column = randint(0, 3), randint(0, 5)
                for i in range(3):
                    self.table[row + i][column] = '■'
            else:  # horizontal location
                row, column = randint(0, 5), randint(0, 3)
                for i in range(3):
                    self.table[row][column + i] = '■'
            # print(f'row={row+1}, column={column+1}, horiz_vert={horiz_vert}')
            break

        # размещаем два 2х палубных
        count = 0
        while count < 2:
            horiz_vert = randint(0, 1)  # 0-horizontal, 1-vertical
            if horiz_vert:  # vertical location
                row, column = randint(0, 4), randint(0, 5)
                # print(f'row={row + 1}, column={column + 1}, horiz_vert={horiz_vert}')
                flag = self.check(row, column, horiz_vert, ship=2)
                if flag:  # set ship
                    self.table[row][column] = '■'
                    self.table[row + 1][column] = '■'
                    count += 1

            else:  # horizontal location
                row, column = randint(0, 5), randint(0, 4)
                # print(f'row={row + 1}, column={column + 1}, horiz_vert={horiz_vert}')
                flag = self.check(row, column, horiz_vert=0, ship=2)
                if flag:  # set ship
                    self.table[row][column] = '■'
                    self.table[row][column + 1] = '■'
                    # print(f'Set ship {row + 1} {column + 1} and {row + 1} {column + 1 + 1}')
                    count += 1

        # размещаем четыре 1 полубных
        count = 0
        for row in range(6):
            for column in range(6):
                if count == 4:
                    break
                flag = self.check(row, column)
                if flag and count < 4:
                    # print(f'row={row + 1}, column={column + 1}')
                    self.table[row][column] = '■'
                    count += 1
        if count < 4:
            self.error = True

    def get_err(self):
        return self.error

    def get_table(self):
        return self.table

    def print_table(self):
        # flag = False # True-скрыть позиции компьютера  False-показать позиции компьютера
        if self.id_name == 'comp':
            name = 'Поле компьютера'
        else:
            name = 'Поле игрока'
        print(name)
        print('  | 1 | 2 | 3 | 4 | 5 | 6 |')
        for i in range(6):
            print(i + 1, '| ', end='')
            # if flag and self.id_name == 'comp':
            if FLAG and self.id_name == 'comp':
                print(*[CELL if el == '■' else el for el in self.table[i]], sep=' | ', end='')
            else:
                print(*self.table[i], sep=' | ', end='')
            print(' |')

    def check(self, row, column, horiz_vert=1, ship=1):
        # horiz_vert: 1 - vert, 0 - horiz
        if horiz_vert == 0:
            ship = 1
        for el in range(row - 1, row + ship + 1):
            if 0 <= el <= 5:
                if horiz_vert:
                    if '■' in self.table[el][0 if column == 0 else column - 1: 6 if column == 5 else column + 2]:
                        return False
                else:
                    # print(el + 1, self.table[el][0 if column == 0 else column - 1: 6 if column == 4 else column + 3])
                    if '■' in self.table[el][0 if column == 0 else column - 1: 6 if column == 4 else column + 3]:
                        return False
        return True

    def set_attack(self, coordinate: str):
        if len(coordinate) == 2 and coordinate.isdigit() \
                and 1 <= int(coordinate[:1]) <= 6 and 1 <= int(coordinate[1:]) <= 6:
            row = int(coordinate[:1]) - 1
            column = int(coordinate[1:]) - 1
            # print(row, column)
            # print(self.table[row][column])
            if self.table[row][column] == CELL:
                self.table[row][column] = 'T'
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