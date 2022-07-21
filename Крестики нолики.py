from random import randint


class Cell:
    # Класс отвечает за пустую клетку
    def __init__(self):
        self.value = 0

    def __bool__(self):
        # Если клетка пустая True
        return True if self.value == 0 else False


class TicTacToe:
    FREE_CELL = 0  # Пустая клетка
    HUMAN_X = 1  # Клетка игрока
    COMPUTER_O = 2  # Клетка компьютера

    def __init__(self):
        # Создание игрового поля
        self.pole = tuple(tuple(Cell() for _ in range(3)) for _ in range(3))  # Каждая клетка обьект класс Cell
        self.game_over = True

    @property
    def is_human_win(self):
        # Обьект свойство показывает победу игрока
        return self._is_human_win

    @is_human_win.setter
    def is_human_win(self, ob):
        # Обьект свойство меняет значение победы игрока
        self._is_human_win = ob

    @property
    def is_computer_win(self):
        # Обьект свойство показывает победу компьютера
        return self._is_computer_win

    @is_computer_win.setter
    def is_computer_win(self, ob):
        # Обьект свойство меняет значение победы компьютера
        self._is_computer_win = ob

    @property
    def is_draw(self):
        # Обьект свойство показывает ничию
        return self._is_draw

    @is_draw.setter
    def is_draw(self, ob):
        # Обьект свойство меняет значение ничии
        self._is_draw = ob

    def __getitem__(self, item):
        # Возврашает значение клетки по указанному индексу
        a, b = item
        if not 0 <= a < 3 or not 0 <= b < 3:
            raise IndexError('некорректно указанные индексы')
        return self.pole[a][b].value

    def __setitem__(self, key, value):
        # Устанавливает значение клетки по указанному индексу
        a, b = key
        if not 0 <= a < 3 or not 0 <= b < 3:
            raise IndexError('некорректно указанные индексы')
        self.pole[a][b].value = value
        free = self.free_cell()  # Проверка на свободные клетки
        human = self.win_game(self.HUMAN_X)  # Проверка победы игрока
        computer = self.win_game(self.COMPUTER_O)  # Победа победы компьютера
        if not human and not computer:
            # Если нет победителя или ничии игра продолжается
            if not free:
                self.is_draw = True
                self.game_over = False
            return
        self.game_over = False
        if human:  # Если победил игрок
            self.is_human_win = True
            return
        if computer:  # Если победил компьютер
            self.is_computer_win = True
            return

    def init(self):
        # Создание игры
        for i in range(3):
            for n in range(3):
                self.__setitem__([i, n], 0)
        self.is_draw = False
        self.is_computer_win = False
        self.is_human_win = False

    def show(self):
        # Вывод на экран игрового поля
        for i in range(3):
            for n in range(3):
                print(self.__getitem__([i, n]), end=' ')
            print()

    def human_go(self):
        # Ход игрока
        key = tuple(map(int, input('Ваш ход- ').split()))
        self.__setitem__(key, self.HUMAN_X)

    def computer_go(self):
        # Ход компьютера
        while True:
            a = randint(0, 2)
            b = randint(0, 2)
            if self.pole[a][b]:
                self.__setitem__([a, b], self.COMPUTER_O)
                return

    def win_game(self, p):
        # Проверка на победу
        for i in self.pole:
            a = all(map(lambda n: n.value == p, i))  # Каждую строку
            if a:
                break
        c = list(zip(*[i for i in self.pole]))
        for i in c:
            b = all(map(lambda n: n.value == p, i))  # Каждый столбец
            if b:
                break
        v = all([self.__getitem__([i, i]) == p for i in range(3)])  # По диагонали
        q = all([self.__getitem__([0, 2]) == p, self.__getitem__([1, 1]) == p, self.__getitem__([2, 0]) == p])
        return any((a, b, v, q))

    def free_cell(self):
        # Проверка пустых клеток
        for i in range(3):
            for n in range(3):
                if bool(self.pole[i][n]):
                    return True
        return False

    def __bool__(self):
        # Возврашает закончена игра или нет
        return self.game_over


game = TicTacToe()  # Создание игры
game.init()  # Создание игрового поля
step_game = 0
while game:  # Цикл не закончится пока нет победителя или ничия
    game.show()

    if step_game % 2 == 0:
        game.human_go()  # Ход игрока
    else:
        game.computer_go()  # Ход компьютера

    step_game += 1

game.show()

if game.is_human_win:  # Если победил игрок
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:  # Если победил компьютер
    print("Все получится, со временем")
else:  # Если ничия
    print("Ничья.")
