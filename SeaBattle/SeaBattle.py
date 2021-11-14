from random import randint

# ь класс Dot - класс точек на поле
class Dot:
    def __init__(self, x, y):
        self.x = x  # Координата по оси x
        self.y = y  # Координата по оси y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за поле!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

# класс Ship - корабль на игровом поле
class Ship:
    def __init__(self, bow, lenght, direction): 
        self.bow = bow # Точка, где размещён нос корабля
        self.lenght = lenght # Длина
        self.direction = direction # Направление корабля (вертикальное/горизонтальное)
        self.lives = lenght # Количеством жизней (сколько точек корабля еще не подбито)
    
    # Метод dots , который возвращает список всех точек корабля
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.lenght):
            cur_x = self.bow.x 
            cur_y = self.bow.y
            
            if self.direction == 0:
                cur_x += i
            
            elif self.direction == 1:
                cur_y += i
            
            ship_dots.append(Dot(cur_x, cur_y))
        
        return ship_dots
    
    def shooten(self, shot):
        return shot in self.dots

#  класс Board - игровая доска
class Board:
    def __init__(self, hid = False, size = 6):
        self.size = size # Размер поля
        self.hid = hid # Параметр hid типа bool - информация о том, нужно ли скрывать корабли
       
        self.count = 0 # Количество живых кораблей на доске
        
        self.field = [ ["O"]*size for _ in range(size) ]
        
        self.busy = []  # Список свободных точек.
        self.ships = [] # Список кораблей доски.
    
    # Метод add_ship , который ставит корабль на доску (если ставить не
    # получается, выбрасываем исключения).
    def add_ship(self, ship):
        
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        
        self.ships.append(ship)
        self.contour(ship)
    
    # Метод contour , который обводит корабль по контуру
    def contour(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)
   
    
    # Метод out , который для точки (объекта класса Dot ) возвращает True , если
    # точка выходит за пределы поля, и False , если не выходит
    def out(self, d):
        return not((0<= d.x < self.size) and (0<= d.y < self.size))

    # Метод shot, который делает выстрел по доске
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        
        if d in self.busy:
            raise BoardUsedException()
        
        self.busy.append(d)
        
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "T"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("***** Корабль уничтожен! *****")
                    input("Для продолжения нажмите Enter!")
                    return False
                else:
                    print("***** Корабль подбит! *****")
                    input("Для продолжения нажмите Enter!")
                    return True
        
        self.field[d.x][d.y] = "."
        print("***** Мозила! *****")
        input("Для продолжения нажмите Enter!")
        return False
    
    # Метод, который выводит доску в консоль в зависимости от параметра hid
    def __str__(self):
        res = ""
        res += "   1  2  3  4  5  6 "
        for i, row in enumerate(self.field):
            res += f"\n{i+1}  " + "  ".join(row) + " "
        
        if self.hid:
            res = res.replace("■", "O")
        return res
    
    def begin(self):
        self.busy = []

# Класс игрока в игре (и AI, и пользователь). Этот класс будет родителем для классов с AI и с пользователем
class Player:
    def __init__(self, board, enemy):
        self.board = board # Собственная доска
        self.enemy = enemy # Доска врага
    
    # метод, который "спрашивает" игрока, в какую клетку он делает выстрел
    def ask(self):
        raise NotImplementedError()
    
    # метод, который делает ход в игре
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

# Класс игрок-компьютер, объект класса Ai
class AI(Player):
    # метод, который "делает" ход за компьютер (рандомно), в какую клетку он делает выстрел
    def ask(self):
        d = Dot(randint(0,5), randint(0, 5))
        print(f"Координаты выстрела AI: {d.x+1} {d.y+1}")
        return d

# Класс игрок-пользователь, объект класса User
class User(Player):
    def ask(self):
        while True:
            cords = input("Введите координаты выстрела x y: ").split()
            
            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue
            
            x, y = cords
            
            if not(x.isdigit()) or not(y.isdigit()):
                print(" Введите числа! ")
                continue
            
            x, y = int(x), int(y)
            
            return Dot(x-1, y-1)

class Game:
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board() # Доска пользователя
        co = self.random_board() # Доска компьютера
        co.hid = True
        
        # Игрок-компьютер, объект класса Ai
        self.ai = AI(co, pl)
        # Игрок-пользователь, объект класса User
        self.us = User(pl, co)

    # метод, который в консоли приветствует пользователя и рассказывает о формате ввода
    def greet(self):
        print("******************************")
        print("        Игра морской бой      ")
        print(" Координаты вводятся как: x y ")
        print("      x - номер строки        ")
        print("      y - номер столбца       ")
        print("******************************")    

    def print_board(self):
        print("="*20)
        print("Поле пользователя:")
        print(self.us.board)
        print("="*20)
        print("Поле компьютера:")
        print(self.ai.board)
        print("="*20)
        print("")
        
    # метод с самим игровым циклом
    def loop(self):
        num = 0
        
        while True:
            self.print_board()
            if num % 2 == 0:
                print("Ходит пользователь:")
                repeat = self.us.move()
            else:
                print("Ходит компьютер:")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.count == 7:
                print("Пользователь выиграл!")
                break
            
            if self.us.board.count == 7:
                print("Компьютер выиграл!")
                break
            num += 1
            
    # метод генерирует случайную доску
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board
    
    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

            
    def start(self):
        self.greet()
        self.loop()
            
            
g = Game()
g.start()