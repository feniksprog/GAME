
list_str = [" ", "0", "1", "2"]
list_str0 = ["0", "-", "-", "-"]
list_str1 = ["1", "-", "-", "-"]
list_str2 = ["2", "-", "-", "-"]

def print_table():
    print(*list_str, sep=' ', end='\n')
    print(*list_str0, sep=' ', end='\n')
    print(*list_str1, sep=' ', end='\n')
    print(*list_str2, sep=' ', end='\n')
    return 1

def inicialization():
    print("ИГРА КРЕСТИКИ-НОЛИКИ")
    print_table()
    # list_str = [" ", "0", "1", "2"]
    # print(*list_str, sep=' ', end='\n')
    # list_str0 = ["0", "-", "-", "-"]
    # print(*list_str0, sep=' ', end='\n')
    # list_str1 = ["1", "-", "-", "-"]
    # print(*list_str1, sep=' ', end='\n')
    # list_str2 = ["2", "-", "-", "-"]
    # print(*list_str2, sep=' ', end='\n')
    return 1

def input_player(stroka, stolbec):
    while True:
        stroka = input("Введите номер СТРОКИ: ")
        stolbec = input("Введите номер СТОЛБЦА: ")
        if not(stroka.isdigit()) or not(stolbec.isdigit()):
            print("Введите числа! ")
            continue

        stroka, stolbec = int(stroka), int(stolbec)
        if 0 > stroka or stroka > 2 or 0 > stolbec or stolbec > 2:
            print("Координаты вне диапазона! ")
            continue
        return stroka, stolbec

def what_result(a):
    player1, player2 = 0, 0
    for n in range(1, 4):
        if (list_str0[n] == "X" and list_str1[n] == "X" and list_str2[n] == "X"):
            player1=1
    if (list_str0[1] == "X" and list_str0[2] == "X" and list_str0[3] == "X") or (list_str1[1] == "X" and list_str1[2] == "X" and list_str1[3] == "X") or (list_str2[1] == "X" and list_str2[2] == "X" and list_str2[3] == "X"):
        player1 = 1
    if (list_str0[1] == "X" and list_str1[2] == "X" and list_str2[3] == "X") or (list_str0[3] == "X" and list_str1[2] == "X" and list_str2[1] == "X"):
        player1 = 1
    for n in range(1, 4):
        if (list_str0[n] == "0" and list_str1[n] == "0" and list_str2[n] == "0"):
            player2=1
    if (list_str0[1] == "0" and list_str0[2] == "0" and list_str0[3] == "0") or (list_str1[1] == "0" and list_str1[2] == "0" and list_str1[3] == "0") or (list_str2[1] == "0" and list_str2[2] == "0" and list_str2[3]) == "0":
        player2=1
    if (list_str0[1] == "0" and list_str1[2] == "0" and list_str2[3] == "0") or (list_str0[3] == "0" and list_str1[2] == "0" and list_str2[1]) == "0":
        player2=1
    if player1 == player2 == 1:
        print("НИЧЬЯ")
        return True
    if player1 == 1:
        print("Выиграл ИГРОК 1")
        return True
    if player2 == 1:
        print("Выиграл ИГРОК 2")
        return True
    return False

inicialization()

while True:

    print("Ходит ПЕРВЫЙ игрок. Ставит X")
    while True:
        i, j = input_player(None, None)

        if i == 0:
            if list_str0[j+1] == "-":
                list_str0[j+1] = "X"
                break
            else:
                print("Клетка занята! Выберите другую клетку!")
        if i == 1:
            if list_str1[j+1] == "-":
                list_str1[j+1] = "X"
                break
            else:
                print("Клетка занята! Выберите другую клетку!")
        if i == 2:
            if list_str2[j+1] == "-":
                list_str2[j+1] = "X"
                break
            else:
                print("Клетка занята! Выберите другую клетку!")

    print("Ходит ВТОРОЙ игрок. Ставит 0")
    while True:
        i, j = input_player(None, None)

        if i == 0:
            if list_str0[j+1] == "-":
                list_str0[j+1] = "0"
                break
            else:
                print("Клетка занята! Выберите другую клетку!")
        if i == 1:
            if list_str1[j+1] == "-":
                list_str1[j+1] = "0"
                break
            else:
                print("Клетка занята! Выберите другую клетку!")
        if i == 2:
            if list_str2[j+1] == "-":
                list_str2[j+1] = "0"
                break
            else:
                print("Клетка занята! Выберите другую клетку!")

    print_table()
    if what_result(None) == True:
        print("Игра окончена!")
        break

