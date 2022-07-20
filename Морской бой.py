from random import randint


class SeaBattle:
    # Класс для управления игрой
    def __init__(self):
        self.player = GamePole(10)  # Локальный атрибут для управления короблями игрока(обьект класса GamePole)
        self.computer = GamePole(10)  # Локальный атрибут для управления короблями компьютера(обьект класса GamePole)
        self.player.init()  # Расстановка кораблей игрока на игровом поле
        self.computer.init()  # Расстановка кораблей компьютера на игровом поле
        self.player_Win = False  # Локальный атрибут выйграл игрок по умолчанию False
        self.computer_Win = False  # Локальный атрибут выйграл Компьютер по умолчанию False
        self.Winer = False  # Локальный атрибут есть победитель по умолчанию False
        self.res = set()  # Множество в котором будут кординаты точек, которые компьютер будет игнорировать для стрельбы
        self.aimed_res = []  # Кординаты выстрела компьютера после попадания в корабль игрока
        self.gorizont = True  # Возможен ли карабль игрока по горизонтали от поподания
        self.gorizont_L = True  # Возможен ли карабль игрока по горизонтали слева от поподания
        self.gorizont_R = True  # Возможен ли карабль игрока по горизонтали справа от поподания
        self.vertical = True  # Возможен ли карабль игрока по вертикали от поподания
        self.vertical_Up = True  # Возможен ли карабль игрока по вертикали выше от поподания
        self.vertical_Down = True  # Возможен ли карабль игрока по вертикали ниже от поподания
        self.aimed = False  # Прицельная стрельба компьютера после попадания
        self.ship_4 = 0  # Счетчик палуб после попадания компьютера
        self.all_ship = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Список для определения компьютеру какой у игрока есть
        # максимальный корабль

    def win_P(self):
        # Проверка выйгрыша игрок
        if not any(isinstance(n, Ship) for i in self.computer._batl_zone for n in i):
            self.player_Win = True
            self.Winer = True
            return
        return

    def win_C(self):
        # Проверка выйгрыша компьютера
        if not any(isinstance(n, Ship) for i in self.player._batl_zone for n in i):
            self.computer_Win = True
            self.Winer = True
            return
        return

    def Win(self):
        # Если есть победитель цикл и игра завершается
        if self.Winer:
            a = 'Игрок' if self.player_Win else 'Компьютер'
            print(f'Победил - {a}')
            return False
        return True

    def show(self):
        # отображение игрового поля и кораблей игрока (палуба коробля = 1, поподание = Х, море = 0)
        print('игрок')
        for i in self.player._batl_zone:
            for n in i:
                if n == 2:
                    n = 'X'
                if isinstance(n, Ship):
                    n = 1
                print(n, end=' ')
            print()
        print()
        print('компьютер')
        # отображение игрового поля и кораблей компьютера(клетки закрыты = #, пока игрок не попадет тогда = Х)
        # вокруг игрового поля кординаты по горизонтали и вертикали для стрельбы
        p = 0
        for i in range(len(self.computer._batl_zone)):
            if i == 0:
                print('  0 1 2 3 4 5 6 7 8 9')
            for n in range(len(self.computer._batl_zone)):
                if n == 0:
                    print(p, end=' ')
                    p += 1
                if self.computer._batl_zone[i][n] == 2:
                    print('X', end=' ')
                    continue
                print('#', end=' ')
            print()

    def shot_player(self):
        # Управление стрельбой игрока
        if self.computer_Win:  # Проверка победител компьютер
            return
        # Игрок вводит кординаты для стрельбы
        a, b = map(int, input(
            'Нажмите две цифры от 0 до 9 , через пробел , чтобы произвести выстрел и нажмите (Ввод)').split())
        if self.computer._batl_zone[a][b] != 0:  # Проверка на попадание
            self.computer._batl_zone[a][b]._is_move = False  # Если есть попадание корабль не может двигатся
            for i in range(len(self.computer._batl_zone[a][b]._cells)):  # Цикл количества целых палуб
                if self.computer._batl_zone[a][b][i] == 1:  # Если палуба цела = 1 , то становится подбитой = 2
                    self.computer._batl_zone[a][b][i] = 2
                    break  # Меняет одну целую палубу и завершает цикл
            self.computer._batl_zone[a][b] = 2  # На игровом поле поподание = 2
            print(f'Игрок попал - ({a}, {b})')
            self.win_P()  # Проверка победы игрока
            self.show()  # Вывод на дисплей игрового поля игрока и компьютера
        else:
            print(f'Игрок промазал - ({a}, {b})')  # Если помазал

    def shot_computer(self):
        # Управление стрельбой Компьютера
        if self.player_Win:  # Проверка победил игрок
            return
        if self.aimed:  # Если предыдуший выстрел компьютера попал , то переходит в прицельную стрельбу
            self.aimed_shooting()
            return
        while True:
            # Создает рандомные координаты если их нет в списки(предыдушие координаты)
            a, b = randint(0, 9), randint(0, 9)
            if (a, b) in self.res:
                continue
            break
        if self.player._batl_zone[a][b] != 0:  # Если компьютер попал
            self.hit(a, b)  # Управление попаданием
            # Возможность продолжение коробля игрока вокруг поподания
            self.gorizont = True
            self.gorizont_L = True
            self.gorizont_R = True
            self.vertical = True
            self.vertical_Up = True
            self.vertical_Down = True
            self.aimed = True  # Следуюший выстрел будет прицельный
            return
        if self.player._batl_zone[a][b] == 0:  # Если компьютер промазал
            print(f'Компьютер промазал - ({a}, {b})')
            return

    def hit(self, a, b):
        self.player._batl_zone[a][b]._is_move = False  # Корабль игрока не может двигатся
        for i in range(len(self.player._batl_zone[a][b]._cells)):  # Цикл количества целых палуб
            if self.player._batl_zone[a][b][i] == 1:  # Если палуба цела = 1 , то становится подбитой = 2
                self.player._batl_zone[a][b][i] = 2
                break
        self.player._batl_zone[a][b] = 2  # На игровом поле поподание = 2
        # Добавление координат попадания и всех координат вокруг попадания в список
        self.res.add((a, b))
        self.res.add((a, b + 1))
        self.res.add((a, b - 1))
        self.res.add((a + 1, b))
        self.res.add((a + 1, b + 1))
        self.res.add((a + 1, b - 1))
        self.res.add((a - 1, b))
        self.res.add((a - 1, b + 1))
        self.res.add((a - 1, b - 1))
        self.aimed_res.append([a, b])  # Добавление координат попадания для прицельной стрельбы
        self.ship_4 += 1  # Прибавление 1 к счетчику подбитых палуб
        print(f'Компьютер попал - ({a}, {b})')
        self.win_C()  # Проверка победы компьютера
        self.show()  # Вывод на дисплей игрового поля игрока и компьютера
        return

    def aimed_shooting(self):
        # Прицельная стрельба
        if self.ship_4 == max(self.all_ship):  # Если счетчик подстреленых палуб равно максимальному значению из целых
            self.gorizont = False  # кораблей ,то по горизонтали и вертикали нет возможных палуб
            self.vertical = False
        if not self.gorizont and not self.vertical:  # Если нет по горизонтали и вертикали возможных палуб
            self.all_ship.remove(self.ship_4)  # Удаление значения счетчика палуб из списка живых кораблей
            self.ship_4 = 0  # Обнуление счетчика подбитых палуб
            self.aimed = False  # Прицельная стрельба не возможна
            self.aimed_res = []  # Список координат для прицельной стрельбы становится пустым
            self.shot_computer()  # Возвращение в обычную стрельбу компьютера
            return
        if self.gorizont:  # Если есть возможные палубы по горизонтали
            if self.gorizont_R:  # Если есть возможные палубы по горизонтали справа
                a, b = self.aimed_res[-1][0], self.aimed_res[-1][-1] + 1
                if not self.index_valid(a, b):  # Проверка координат на выход из игрового поля
                    self.gorizont_R = False  # По горизонтали справа нет палуб и игрового поля
                    self.aimed_shooting()  # Заново вызвать прицельную стрельбу
                    return
                if self.player._batl_zone[a][b] != 0:  # Если есть поподание
                    self.vertical = False  # По вертикали нет возможных палуб
                    self.vertical_Up = False
                    self.vertical_Down = False
                    self.hit(a, b)  # Управление попаданием
                    return
                if self.player._batl_zone[a][b] == 0:  # Если нет попадания
                    self.aimed_res.append(self.aimed_res[0])  # Добавление в конец списка начальных координат
                    self.gorizont_R = False  # Возможных палуб по горизонтали справа нет
                    print(f'Компьютер промазал - ({a}, {b})')
                    return
            if self.gorizont_L:  # Если есть возможные палубы по горизонтали слева
                a, b = self.aimed_res[-1][0], self.aimed_res[-1][-1] - 1
                if b == -1:  # Если есть выход из игрового поля
                    self.gorizont_L = False
                    self.gorizont = False  # По горизонтали справа нет палуб и игрового поля
                    if not self.vertical:  # Если нет возможных палуб по вертикали
                        self.aimed_res = []  # Список координат для прицельной стрельбы пуст
                        self.shot_computer()  # Возвращение в обычную стрельбу компьютера
                        return
                    self.aimed_shooting()  # Заново вызвать прицельную стрельбу
                    return
                if not self.index_valid(a, b):  # Проверка координат на выход из игрового поля
                    self.gorizont_L = False
                    self.gorizont = False  # По горизонтали справа нет палуб и игрового поля
                    if not self.vertical:  # Если нет возможных палуб по вертикали
                        self.aimed_res = []  # Список координат для прицельной стрельбы пуст
                        self.shot_computer()  # Возвращение в обычную стрельбу компьютера
                        return
                    self.aimed_shooting()  # Заново вызвать прицельную стрельбу
                    return
                if self.player._batl_zone[a][b] != 0:  # Если есть поподание
                    self.vertical = False  # По вертикали нет возможных палуб
                    self.vertical_Up = False
                    self.vertical_Down = False
                    self.hit(a, b)  # Управление попаданием
                    return
                if self.player._batl_zone[a][b] == 0:  # Если нет попадания
                    self.aimed_res.append(self.aimed_res[0])  # Добавление в конец списка начальных координат
                    self.gorizont_L = False  # Возможных палуб по горизонтали нет
                    self.gorizont = False
                    print(f'Компьютер промазал - ({a}, {b})')
                    return
        if self.vertical:
            # Проверка по вертикали проходит по тем же принципам что и по горизонтале описанные выше
            if self.vertical_Up:
                a, b = self.aimed_res[-1][0] + 1, self.aimed_res[-1][-1]
                if not self.index_valid(a, b):
                    self.vertical_Up = False
                    self.aimed_shooting()
                    return
                if self.player._batl_zone[a][b] != 0:
                    self.hit(a, b)
                    return
                if self.player._batl_zone[a][b] == 0:
                    self.aimed_res.append(self.aimed_res[0])
                    self.vertical_Up = False
                    print(f'Компьютер промазал - ({a}, {b})')
                    return
            if self.vertical_Down:
                a, b = self.aimed_res[-1][0] - 1, self.aimed_res[-1][-1]
                if a == -1:
                    self.vertical_Down = False
                    self.vertical = False
                    self.aimed_res = []
                    self.shot_computer()
                    return
                if not self.index_valid(a, b):
                    self.vertical_Down = False
                    self.vertical = False
                    self.aimed_res = []
                    self.shot_computer()
                    return
                if self.player._batl_zone[a][b] != 0:
                    self.hit(a, b)
                    return
                if self.player._batl_zone[a][b] == 0:
                    self.aimed_res.append(self.aimed_res[0])
                    self.vertical_Down = False
                    self.vertical = False
                    print(f'Компьютер промазал - ({a}, {b})')
                    return

    def index_valid(self, a, b):
        # Проверка на выход координат за пределы игрового поля
        try:
            self.player._batl_zone[a][b]
            return True
        except IndexError:  # Если происходит ошибка IndexError то координаты вышли за игровое поле
            return False


class Ship:
    # Класс для управления кораблем
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length  # Количество палуб на корабле
        self._tp = tp  # Расположение коробля 1 = горизонталь, 2 = вертикаль
        self._x, self._y = x, y  # Координаты начальной точки расположения
        self._is_move = True  # Возможность двигаться = True исли нет поподания иначе False
        self._cells = [1 for _ in range(self._length)]  # Список палуб коробля , палуба = 1, если подбита = 2

    def set_start_coords(self, x, y):
        # Установка начальных координат
        self._x, self._y = x, y

    def get_start_coords(self):
        # Возврашает начальные координаты
        return self._x, self._y

    def move_True(self, obj, go):
        # Проверка движения коробля по игровому полю на одну клетку вперед или назад
        if not self._is_move:  # Есть ли возможность двигаться
            return False
        if not self.is_out_pole(go):  # Если выходит за пределы игрового поля после движения на одну клетку
            return False
        if not self.is_collide_True(obj, go):  # Если есть столкновение с другим кораблем после движения
            return False
        return True

    def is_collide_True(self, obj, go):
        # Проверка на столкновение
        if self._tp == 1:  # Если расположение коробля по горизонтали
            if go == 1:  # Если движение вперед на одну клетку
                res = self._y + self._length + 1  # Координаты в которой проходит проверка для безопасного движения
            if go == -1:  # Если движение назад на одну клетку
                res = self._y - 2  # Координаты в которой проходит проверка для безопасного движения
            for i in range(-1, 2):  # Проверка в цикле трех координат для безапасного движения
                try:
                    if obj._batl_zone[self._x + i][res] != 0:
                        return False
                except IndexError:
                    continue
            return True
        if self._tp == 2:  # Проверка по вертикали проходит по такому же принципу ,что и по вертикали
            if go == 1:
                res = self._x + self._length + 1
            if go == -1:
                res = self._x - 2
            for i in range(-1, 2):
                try:
                    if obj._batl_zone[res][self._y + i] != 0:
                        return False
                except IndexError:
                    continue
            return True

    def is_out_pole(self, go, size=10):
        # Проверка выхода за пределы игрового поля
        if go == 1:  # Движение вперед
            if self._tp == 1:  # По горизонтале
                if self._y + self._length >= size:
                    return False
                return True
            if self._tp == 2:  # По вертикали
                if self._x + self._length >= size:
                    return False
                return True
        if go == -1:  # Движение назад
            if self._tp == 1:   # По горизонтале
                if self._y - 1 < 0:
                    return False
                return True
            if self._tp == 2:     
                if self._x - 1 < 0:
                    return False
                return True

    def __getitem__(self, item):
        # Возврашает количество палуб карабля
        return self._cells[item]

    def __setitem__(self, key, value):
        # Меняет значение палубы коробля
        self._cells[key] = value


class GamePole:
    # Класс для управления игровым полем
    def __init__(self, size):
        self._size = size  # Размер поля
        self._ships = []  # Список кораблей
        self._batl_zone = [[0] * size for _ in range(size)]  # Игровое поле (вложенный список)

    def init(self):
        # Создание кораблей(обьекты класса Ship), и расстановка их по игровому полю
        self._ships = [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)), Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)), Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))]
        self.enter_bz()  # Расстановка кораблей

    def enter_bz(self):
        # Расстановка кораблей
        for i in self._ships:
            while True:
                # Получение рандомных начальных координат для каждого коробля и их проверка
                # пока координаты не будут подходить для размешения коробля на игровом поле они будут рандомится заново
                # для каждого коробля
                i.set_start_coords(randint(0, self._size - 1), randint(0, self._size - 1))
                if i._tp == 1:
                    if i._y + i._length > self._size - 1:
                        continue
                if i._tp == 2:
                    if i._x + i._length > self._size - 1:
                        continue
                if self.control_ships(i):  # Размешение коробля
                    break

    def control_ships(self, obj):
        # Размешение коробля
        x, y = obj.get_start_coords()
        if obj._tp == 1:  # Коробль по горизонтали
            for i in range(-1, 2):
                # Проверка чтобы вокруг каждой палубы не было других караблей
                try:
                    self._batl_zone[x + i]
                except IndexError:
                    continue
                for n in range(y - 1, y + obj._length + 1):
                    try:
                        if self._batl_zone[x + i][n] != 0:
                            return False
                    except IndexError:
                        continue
            z = 0
            for i in range(y, y + obj._length):
                # Под проверенными координатами на игровом поле записыываются обьект класса Ship
                self._batl_zone[x][i] = obj
                z += 1
            return True
        if obj._tp == 2:  # Коробль по вертикали
            for i in range(x - 1, x + obj._length + 1):
                # Проверка чтобы вокруг каждой палубы не было других караблей
                try:
                    self._batl_zone[i]
                except IndexError:
                    continue
                for n in range(-1, 2):
                    try:
                        if self._batl_zone[i][y + n] != 0:
                            return False
                    except IndexError:
                        continue
            z = 0
            for i in range(x, x + obj._length):
                # Под проверенными координатами на игровом поле записыываются обьект класса Ship
                self._batl_zone[i][y] = obj
                z += 1
            return True

    def get_ships(self):
        return self._ships

    def move_ships(self):
        # Движение короблей вперед на одну клетку вперед если есть возможность, если нет то назад
        # если и назад нельзя то оставатся на месте
        for i in self._ships:
            if i.move_True(self, 1):  # Если возможно движение вперед
                self.move_1(i)  # Движение коробля вперед на одну клетку
                continue
            if i.move_True(self, -1):  # Если возможно движение назад
                self.move_2(i)  # Движение коробля назад на одну клетку

    def move_1(self, i):
        # Движение коробля вперед на одну клетку
        self._batl_zone[i._x][i._y] = 0
        if i._tp == 1:
            self._batl_zone[i._x][i._y + i._length] = i
            i.set_start_coords(i._x, i._y + 1)
        if i._tp == 2:
            self._batl_zone[i._x + i._length][i._y] = i
            i.set_start_coords(i._x + 1, i._y)

    def move_2(self, i):
        # Движение коробля назад на одну клетку
        if i._tp == 1:
            self._batl_zone[i._x][i._y + i._length - 1] = 0
            self._batl_zone[i._x][i._y - 1] = i
            i.set_start_coords(i._x, i._y - 1)
        if i._tp == 2:
            self._batl_zone[i._x + i._length - 1][i._y] = 0
            self._batl_zone[i._x - 1][i._y] = i
            i.set_start_coords(i._x - 1, i._y)

    def show(self):
        # Вывод на экран игрового поля
        for i in self._batl_zone:
            for n in i:
                if isinstance(n, Ship):
                    n = 1
                print(n, end=' ')
            print()

    def get_pole(self):
        return self._batl_zone


a = input('Добро пожаловать в - Морской бой: нажмите 1 , чтобы начать игру.')  # Запуск игры
if a == '1':
    game = SeaBattle()  # создается обьект класса для управления игрой
    game.show()  # Вывод на экран игрового поля игрока и компьютера
while game.Win():  # Цикл пока игрок или компьютер не победят
    game.shot_player()  # Выстрел игрока
    game.shot_computer()  # Выстрел компьютера
    game.player.move_ships()  # Движение всех не подбитых кораблей игрока на одну клетку
    game.computer.move_ships()  # Движение всех не подбитых кораблей компьютера на одну клетку
