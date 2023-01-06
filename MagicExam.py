import random as rd


class Cell:

    def __bool__(self):
        return self.value == 0

    def __init__(self, value=0):
        self.value = value

    def __repr__(self):
        return str(self.value)


def check_indx(val):
    if type(val) not in (tuple, list) or len(val) != 2:
        raise IndexError('некорректно указанные индексы')
    r, c = val
    if 2 < r < 0 or 2 < c < 0:
        raise IndexError('некорректно указанные индексы')


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self.win = 0
        self.size = 3
        self.pole = tuple(tuple(Cell(0) for _ in range(self.size)) for _ in range(self.size))

    def init(self):

        for row in self.pole:
            for cell in row:
                cell.value = 0
        self.win = 0

    def show(self):
        print('-' * 5)
        for i in self.pole:
            print(*map(lambda x: '*' if x.value == 0 else x.value, i))
        print('-' * 5)

    def __getitem__(self, item):
        check_indx(item)
        r, c = item
        return self.pole[r][c].value

    def __setitem__(self, key, value):
        check_indx(key)
        r, c = key
        self.pole[r][c].value = value
        self.who_is_winner()

    def human_go(self):
        if not self:
            return
        while True:
            r, c = map(int, input('Введите координаты клетки: ').split())
            if not (0 <= r < self.size) or not (0 <= c < self.size):
                continue
            if self[r, c] == self.FREE_CELL:
                self[r, c] = self.HUMAN_X
                break

    def computer_go(self):
        if not self:
            return
        while True:
            r, c = rd.randint(0, 2), rd.randint(0, 2)
            if self[r, c] == self.FREE_CELL:
                self[r, c] = self.HUMAN_X
                break

    def who_is_winner(self):
        for row in self.pole:
            if all(cell.value == self.HUMAN_X for cell in row):
                self.win = 1
                return
            if all(cell.value == self.COMPUTER_O for cell in row):
                self.win = 2
                return
        for i in range(self.size):
            if all(cell.value == self.HUMAN_X for cell in (value[i] for value in self.pole)):
                self.win = 1
                return
            if all(cell.value == self.COMPUTER_O for cell in (value[i] for value in self.pole)):
                self.win = 2
                return
        if all(self.pole[i][i] == self.HUMAN_X for i in range(self.size)) or \
                all(self.pole[i][- 1 - i] == self.HUMAN_X for i in range(self.size)):
            self.win = 1
            return
        if all(self.pole[i][i] == self.COMPUTER_O for i in range(self.size)) or \
                all(self.pole[i][- 1 - i] == self.COMPUTER_O for i in range(self.size)):
            self.win = 2
            return
        if all(cell.value != self.FREE_CELL for row in self.pole for cell in row):
            self.win = 3

    def __bool__(self):
        return self.win == 0 and self.win not in (1, 2, 3)

    @property
    def is_human_win(self):
        return self.win == 1

    @property
    def is_computer_win(self):
        return self.win == 2

    @property
    def is_draw(self):
        return self.win == 3

# 2 вариант
from random import choice


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self._n = 3
        self.init()

    @property
    def is_human_win(self):
        return self.__is_human_win

    @property
    def is_computer_win(self):
        return self.__is_computer_win

    @property
    def is_draw(self):
        return self.__is_draw

    def init(self):
        self.__is_human_win, self.__is_computer_win, self.__is_draw = False, False, False
        self.pole = tuple(tuple(Cell() for j in range(self._n)) for i in range(self._n))
        self.total_lst = []

    def show(self):
        for i in range(self._n):
            for j in range(self._n):
                if self.pole[i][j].value == self.FREE_CELL: print(f'{i}_{j}', end=' ')
                if self.pole[i][j].value == self.HUMAN_X: print('_x_', end=' ')
                if self.pole[i][j].value == self.COMPUTER_O: print('_0_', end=' ')
            print()
            print()

    def human_go(self):
        key = tuple(map(int, input('Ваш ход- ').split()))
        self.__setitem__(key, self.HUMAN_X)

    def computer_go(self):
        key = choice(self.total_lst)
        self.__setitem__(key, self.COMPUTER_O)

    def __bool__(self):
        '''возвращает True, если игра не окончена (никто не победил и есть свободные клетки) и False - в противном случае'''
        return not any((self.is_human_win, self.is_computer_win, self.is_draw))

    def check_win(self):
        '''Проверка таблицы поля на выйгрыш или ничью'''
        self.total_lst = [(i, j) for j in range(self._n) for i in range(self._n) if
                          self.pole[i][j].value == self.FREE_CELL]
        humax = tuple(True if self.pole[i][i].value == self.HUMAN_X else False for i in range(self._n) if
                      self.pole[i][i].value != self.FREE_CELL)
        if len(humax) == 3:
            if self.check_vs(humax): return False

        humax = tuple(True if self.pole[i][self._n - 1 - i].value == self.HUMAN_X else False for i in range(self._n) if
                      self.pole[i][self._n - 1 - i].value != self.FREE_CELL)
        if len(humax) == 3:
            if self.check_vs(humax): return False
        for i in range(self._n):
            humax = tuple(True if value == self.HUMAN_X else False for value in self[i, :] if value != self.FREE_CELL)
            if len(humax) == 3:
                if self.check_vs(humax): return False
        for j in range(self._n):
            humax = tuple(True if value == self.HUMAN_X else False for value in self[:, j] if value != self.FREE_CELL)
            if len(humax) == 3:
                if self.check_vs(humax): return False
        if len(self.total_lst) == 0:
            self.__is_human_win, self.__is_computer_win, self.__is_draw = False, False, True
            return False
        return True

    def check_vs(self, humax):
        '''вспомогательная функция для check_win'''
        if all(humax):
            self.__is_human_win, self.__is_computer_win, self.__is_draw = True, False, False
            return True
        if sum(humax) == 0:
            self.__is_human_win, self.__is_computer_win, self.__is_draw = False, True, False
            return True
        return False

    def check_index(self, indx):
        if not isinstance(indx, (slice, tuple)) or not all(0 <= n <= 2 for n in indx if type(n) == int):
            raise IndexError('некорректно указанные индексы')

    def __getitem__(self, item):
        self.check_index(item)
        if type(item[1]) == slice:
            return tuple(n.value for n in self.pole[item[0]][item[1]])
        if type(item[0]) == slice:
            lst = [self.pole[i][item[1]] for i in range(3)][item[0]]
            return tuple(n.value for n in lst)
        return self.pole[item[0]][item[1]].value

    def __setitem__(self, key, value):
        self.check_index(key)
        cell = self.pole[key[0]][key[1]]
        if not cell:
            raise ValueError('клетка уже занята')
        if self:
            cell.value = value
            self.check_win()


class Cell:
    def __init__(self, value=0):
        self.value = value  # value - значение поля: 1 - крестик; 2 - нолик (по умолчанию 0).

    def __bool__(self):  # возвращает True, если клетка свободна (value = 0) и False - в противном случае.
        return not self.value
game = TicTacToe()
game.init()
step_game = 0
game[0, 0] = TicTacToe.HUMAN_X
game[1, 1] = TicTacToe.HUMAN_X
game[2, 2] = TicTacToe.HUMAN_X
print(game.is_human_win and game.is_computer_win and game.is_draw)
game.init()
game[0, 0] = TicTacToe.COMPUTER_O
game[1, 0] = TicTacToe.COMPUTER_O
game[2, 0] = TicTacToe.COMPUTER_O
print(game.is_human_win == False and game.is_computer_win and game.is_draw == False)
game.show()

