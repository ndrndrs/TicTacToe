from random import randint


def check_indx(val):
    if type(val) not in (tuple, list) or len(val) != 2:
        raise IndexError('incorrect index')
    r, c = val
    if 2 < r < 0 or 2 < c < 0:
        raise IndexError('incorrect index')


class Cell:

    def __bool__(self):
        return self.value == 0

    def __init__(self, value=0):
        self.value = value

    def __repr__(self):
        return str(self.value)


class TicTacToe:
    FREE_CELL = 0  # FREE CELL
    HUMAN_X = 1  # X
    COMPUTER_O = 2  # 0

    def __init__(self):
        self.win = 0
        self.size = 3
        self.pole = tuple(tuple(Cell(0) for _ in range(self.size)) for _ in range(self.size))

    def clear_pole(self):

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
            row, col = map(int, input('Enter coordinates: ').split())
            if not (0 <= row < self.size) or not (0 <= col < self.size):
                continue
            if self[row, col] == self.FREE_CELL:
                self[row, col] = self.HUMAN_X
                break

    def computer_go(self):
        if not self:
            return
        while True:
            row, col = randint(0, 2), randint(0, 2)
            if self[row, col] == self.FREE_CELL:
                self[row, col] = self.HUMAN_X
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



